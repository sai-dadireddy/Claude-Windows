"""
Memory API Client for Sherpa v4.1

Interfaces with AWS Lambda-backed memory service.
Uses SigV4 signing for IAM authentication.
"""

import json
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class MemoryAPIClient:
    """Client for Sherpa memory API (AWS Lambda + DynamoDB)"""

    def __init__(
        self,
        base_url: str = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod",
        region: str = "us-east-1",
        profile: str = "sherpa"
    ):
        """
        Initialize memory API client.

        Args:
            base_url: API Gateway base URL (without trailing slash)
            region: AWS region (default: us-east-1)
            profile: AWS credentials profile (default: sherpa)
        """
        self.base_url = base_url.rstrip('/')
        self.region = region
        self.profile = profile

        # Load credentials from profile
        session = boto3.Session(profile_name=profile)
        self.credentials = session.get_credentials()

        if not self.credentials:
            raise ValueError(f"Could not load AWS credentials from profile: {profile}")

    def _make_request(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make signed API request.

        Args:
            path: API path (e.g., /memory/save)
            data: Request payload

        Returns:
            API response as dict

        Raises:
            requests.HTTPError: If request fails
        """
        url = f"{self.base_url}{path}"
        body = json.dumps(data) if data else ""

        # Create AWS request
        request = AWSRequest(
            method="POST",
            url=url,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        # Sign with SigV4
        SigV4Auth(self.credentials, "execute-api", self.region).add_auth(request)

        # Send using requests library
        response = requests.request(
            method=str(request.method),
            url=str(request.url),
            headers=dict(request.headers),
            data=request.body
        )
        response.raise_for_status()
        return response.json()

    def save_memory(
        self,
        project: str,
        memory_type: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Save a memory to the knowledge base.

        Args:
            project: Project name (or "global")
            memory_type: Memory type (decision, preference, observation, etc.)
            content: Memory content/description
            metadata: Optional additional metadata

        Returns:
            API response with memory_id and timestamp

        Example:
            >>> client.save_memory(
            ...     project="sherpa",
            ...     memory_type="decision",
            ...     content="Use TypeScript for all new frontend code"
            ... )
        """
        payload: Dict[str, Any] = {
            "action": "save",
            "project": project,
            "type": memory_type,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

        if metadata:
            payload["metadata"] = metadata

        return self._make_request("/memory/save", payload)

    def search_memories(
        self,
        project: str,
        query: str,
        limit: int = 10,
        memory_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search memories by semantic similarity.

        Args:
            project: Project name (or "global")
            query: Search query
            limit: Max results to return (default: 10)
            memory_type: Optional filter by type

        Returns:
            List of matching memories with similarity scores

        Example:
            >>> results = client.search_memories(
            ...     project="sherpa",
            ...     query="typescript decisions"
            ... )
        """
        payload = {
            "action": "search",
            "project": project,
            "query": query,
            "limit": limit
        }

        if memory_type:
            payload["type"] = memory_type

        response = self._make_request("/memory/search", payload)
        return response.get("results", [])

    def promote_memory(
        self,
        memory_id: str,
        target_project: str = "global"
    ) -> Dict[str, Any]:
        """
        Promote a memory to a higher scope (e.g., project -> global).

        Args:
            memory_id: Memory ID to promote
            target_project: Target project (default: global)

        Returns:
            API response with promoted memory details
        """
        payload = {
            "memory_id": memory_id,
            "target_project": target_project
        }

        return self._make_request("/memory/promote", payload)

    def kb_retrieve(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve from Bedrock Knowledge Base.

        Args:
            query: Search query
            limit: Max results to return (default: 5)

        Returns:
            List of matching documents with scores
        """
        payload = {
            "query": query,
            "limit": limit
        }

        response = self._make_request("/kb/retrieve", payload)
        return response.get("results", [])


# Convenience function for quick usage
def create_client(profile: str = "sherpa") -> MemoryAPIClient:
    """
    Create a memory API client with default settings.

    Args:
        profile: AWS credentials profile (default: sherpa)

    Returns:
        Configured MemoryAPIClient instance
    """
    return MemoryAPIClient(profile=profile)
