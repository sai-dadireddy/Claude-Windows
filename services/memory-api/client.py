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
        endpoint: str = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/memory",
        region: str = "us-east-1",
        profile: str = "sherpa"
    ):
        """
        Initialize memory API client.

        Args:
            endpoint: API Gateway endpoint URL
            region: AWS region (default: us-east-1)
            profile: AWS credentials profile (default: sherpa)
        """
        self.endpoint = endpoint
        self.region = region
        self.profile = profile

        # Load credentials from profile
        session = boto3.Session(profile_name=profile)
        self.credentials = session.get_credentials()

        if not self.credentials:
            raise ValueError(f"Could not load AWS credentials from profile: {profile}")

    def _sign_request(self, method: str, url: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Sign request with SigV4 for IAM authentication.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            data: Request body (will be JSON encoded)

        Returns:
            Signed PreparedRequest ready to send
        """
        # Prepare request body
        body = json.dumps(data) if data else ""

        # Create AWS request
        request = AWSRequest(
            method=method,
            url=url,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        # Sign with SigV4
        SigV4Auth(self.credentials, "execute-api", self.region).add_auth(request)

        # Convert to requests PreparedRequest
        return request.prepare()

    def _make_request(self, method: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make signed API request.

        Args:
            method: HTTP method
            data: Request payload

        Returns:
            API response as dict

        Raises:
            requests.HTTPError: If request fails
        """
        signed_request = self._sign_request(method, self.endpoint, data)
        response = requests.Session().send(signed_request)
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

        return self._make_request("POST", payload)

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

        response = self._make_request("POST", payload)
        return response.get("results", [])

    def list_memories(
        self,
        project: str,
        memory_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        List all memories for a project.

        Args:
            project: Project name (or "global")
            memory_type: Optional filter by type
            limit: Max results to return (default: 50)

        Returns:
            List of memories sorted by timestamp (newest first)

        Example:
            >>> memories = client.list_memories(
            ...     project="sherpa",
            ...     memory_type="decision"
            ... )
        """
        payload = {
            "action": "list",
            "project": project,
            "limit": limit
        }

        if memory_type:
            payload["type"] = memory_type

        response = self._make_request("POST", payload)
        return response.get("memories", [])

    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific memory by ID.

        Args:
            memory_id: Unique memory identifier

        Returns:
            Memory details

        Example:
            >>> memory = client.get_memory("mem_abc123")
        """
        payload = {
            "action": "get",
            "memory_id": memory_id
        }

        response = self._make_request("POST", payload)
        return response.get("memory", {})


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
