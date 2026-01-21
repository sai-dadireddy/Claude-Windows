"""
Agent Loader Lambda Function

Lazy-loads agent prompts from S3 on-demand with in-memory caching
for Lambda warm starts.

S3 Structure:
    s3://sherpa-config/v4.1/agents/{agent_name}/prompt.md
    s3://sherpa-config/v4.1/agents/{agent_name}/manifest.json

Actions:
    - list: Return manifest of all available agents
    - get: Load full agent prompt by name
    - search: Search agents by keyword
"""

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration
S3_BUCKET = os.environ.get("S3_BUCKET", "sherpa-config")
S3_PREFIX = os.environ.get("S3_PREFIX", "v4.1/agents")
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "300"))

# In-memory cache for Lambda warm starts
_agent_cache: Dict[str, Dict[str, Any]] = {}
_manifest_cache: Optional[Dict[str, Any]] = None
_cache_timestamp: float = 0

# S3 client (reused across invocations)
_s3_client = None


def get_s3_client():
    """Get or create S3 client (singleton for Lambda reuse)."""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3")
    return _s3_client


def _is_cache_valid() -> bool:
    """Check if cache is still valid based on TTL."""
    import time
    global _cache_timestamp
    return (time.time() - _cache_timestamp) < CACHE_TTL_SECONDS


def _refresh_cache_timestamp():
    """Update cache timestamp."""
    import time
    global _cache_timestamp
    _cache_timestamp = time.time()


def _get_agent_path(agent_name: str) -> str:
    """Get S3 key prefix for an agent."""
    return f"{S3_PREFIX}/{agent_name}"


def load_manifest() -> Dict[str, Any]:
    """
    Load the agents manifest from S3.

    Returns:
        Dictionary containing agent metadata list.
    """
    global _manifest_cache

    if _manifest_cache is not None and _is_cache_valid():
        logger.info("Returning cached manifest")
        return _manifest_cache

    s3 = get_s3_client()
    manifest_key = f"{S3_PREFIX}/manifest.json"

    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=manifest_key)
        content = response["Body"].read().decode("utf-8")
        _manifest_cache = json.loads(content)
        _refresh_cache_timestamp()
        logger.info(f"Loaded manifest from s3://{S3_BUCKET}/{manifest_key}")
        return _manifest_cache if _manifest_cache else {}
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            logger.warning("Manifest not found, scanning for agents")
            scanned = _scan_agents()
            return scanned if scanned else {}
        logger.error(f"Failed to load manifest: {e}")
        raise


def _scan_agents() -> Dict[str, Any]:
    """
    Scan S3 bucket to discover available agents.

    Fallback when manifest.json doesn't exist.
    """
    global _manifest_cache

    s3 = get_s3_client()
    agents = []

    try:
        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=S3_BUCKET,
            Prefix=f"{S3_PREFIX}/",
            Delimiter="/"
        )

        for page in pages:
            for prefix in page.get("CommonPrefixes", []):
                # Extract agent name from prefix
                agent_path = prefix["Prefix"].rstrip("/")
                agent_name = agent_path.split("/")[-1]

                if agent_name and agent_name != "manifest.json":
                    agent_meta = _load_agent_metadata(agent_name)
                    if agent_meta:
                        agents.append(agent_meta)

        _manifest_cache = {"agents": agents}
        _refresh_cache_timestamp()
        return _manifest_cache

    except ClientError as e:
        logger.error(f"Failed to scan agents: {e}")
        return {"agents": []}


def _load_agent_metadata(agent_name: str) -> Optional[Dict[str, Any]]:
    """
    Load metadata for a single agent.

    Args:
        agent_name: Name of the agent

    Returns:
        Agent metadata dictionary or None if not found
    """
    s3 = get_s3_client()
    manifest_key = f"{_get_agent_path(agent_name)}/manifest.json"

    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=manifest_key)
        content = response["Body"].read().decode("utf-8")
        metadata = json.loads(content)
        metadata["id"] = agent_name
        return metadata
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            # Return basic metadata if manifest doesn't exist
            return {
                "id": agent_name,
                "name": agent_name.replace("-", " ").title(),
                "description": f"Agent: {agent_name}",
                "tags": []
            }
        logger.error(f"Failed to load metadata for {agent_name}: {e}")
        return None


def load_agent_prompt(agent_name: str) -> Optional[str]:
    """
    Load agent prompt from S3.

    Args:
        agent_name: Name of the agent

    Returns:
        Prompt content string or None if not found
    """
    # Check cache first
    if agent_name in _agent_cache and _is_cache_valid():
        cached = _agent_cache[agent_name]
        if "prompt" in cached:
            logger.info(f"Returning cached prompt for {agent_name}")
            return cached["prompt"]

    s3 = get_s3_client()
    prompt_key = f"{_get_agent_path(agent_name)}/prompt.md"

    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=prompt_key)
        content = response["Body"].read().decode("utf-8")

        # Cache the prompt
        if agent_name not in _agent_cache:
            _agent_cache[agent_name] = {}
        _agent_cache[agent_name]["prompt"] = content
        _refresh_cache_timestamp()

        logger.info(f"Loaded prompt from s3://{S3_BUCKET}/{prompt_key}")
        return content

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "")
        if error_code == "NoSuchKey":
            logger.warning(f"Prompt not found for agent: {agent_name}")
            return None
        logger.error(f"Failed to load prompt for {agent_name}: {e}")
        raise


def get_agent(agent_name: str) -> Dict[str, Any]:
    """
    Get full agent data including prompt.

    Args:
        agent_name: Name of the agent

    Returns:
        Agent manifest with prompt included
    """
    # Check full cache first
    if agent_name in _agent_cache and _is_cache_valid():
        cached = _agent_cache[agent_name]
        if "full" in cached:
            logger.info(f"Returning fully cached agent: {agent_name}")
            return cached["full"]

    # Load metadata
    metadata = _load_agent_metadata(agent_name)
    if metadata is None:
        return {"error": "not_found", "message": f"Agent not found: {agent_name}"}

    # Load prompt
    prompt = load_agent_prompt(agent_name)
    if prompt is None:
        return {"error": "not_found", "message": f"Agent prompt not found: {agent_name}"}

    # Build full agent response
    agent_data = {
        "id": agent_name,
        "name": metadata.get("name", agent_name),
        "description": metadata.get("description", ""),
        "tags": metadata.get("tags", []),
        "tools": metadata.get("tools", []),
        "prompt": prompt,
        "metadata": {
            k: v for k, v in metadata.items()
            if k not in ("id", "name", "description", "tags", "tools")
        }
    }

    # Cache full agent
    if agent_name not in _agent_cache:
        _agent_cache[agent_name] = {}
    _agent_cache[agent_name]["full"] = agent_data
    _refresh_cache_timestamp()

    return agent_data


def list_agents() -> List[Dict[str, Any]]:
    """
    List all available agents.

    Returns:
        List of agent metadata (without prompts)
    """
    manifest = load_manifest()
    return manifest.get("agents", [])


def search_agents(query: str) -> List[Dict[str, Any]]:
    """
    Search agents by keyword.

    Args:
        query: Search query string

    Returns:
        List of matching agent metadata
    """
    query_lower = query.lower()
    query_pattern = re.compile(re.escape(query_lower))

    agents = list_agents()
    results = []

    for agent in agents:
        # Search in name, description, and tags
        searchable = " ".join([
            agent.get("name", ""),
            agent.get("description", ""),
            " ".join(agent.get("tags", []))
        ]).lower()

        if query_pattern.search(searchable):
            results.append(agent)

    return results


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for agent loader.

    Event format:
    {
        "action": "list" | "get" | "search",
        "agent_id": "agent-name",  # for "get" action
        "query": "search term"      # for "search" action
    }

    Response format:
    {
        "statusCode": 200,
        "body": {
            "agents": [...],      # for "list" and "search"
            "agent": {...}        # for "get"
        }
    }
    """
    logger.info(f"Received event: {json.dumps(event)}")

    # Handle Lambda Function URL format
    if "body" in event:
        try:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "invalid_json", "message": "Invalid JSON in request body"})
            }
    else:
        body = event

    action = body.get("action", "list")

    try:
        if action == "list":
            agents = list_agents()
            response_body = {"agents": agents}

        elif action == "get":
            agent_id = body.get("agent_id")
            if not agent_id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "missing_param", "message": "agent_id is required"})
                }

            agent_data = get_agent(agent_id)
            if "error" in agent_data:
                return {
                    "statusCode": 404,
                    "body": json.dumps(agent_data)
                }
            response_body = {"agent": agent_data}

        elif action == "search":
            query = body.get("query", "")
            if not query:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "missing_param", "message": "query is required"})
                }

            agents = search_agents(query)
            response_body = {"agents": agents}

        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "invalid_action", "message": f"Unknown action: {action}"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response_body)
        }

    except Exception as e:
        logger.exception(f"Error processing request: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal_error", "message": str(e)})
        }


# For local testing
if __name__ == "__main__":
    # Test list action
    print("Testing list action:")
    result = lambda_handler({"action": "list"}, None)
    print(json.dumps(result, indent=2))

    # Test get action
    print("\nTesting get action:")
    result = lambda_handler({"action": "get", "agent_id": "lead-architect"}, None)
    print(json.dumps(result, indent=2))
