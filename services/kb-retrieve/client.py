"""KB Retrieve Client - Calls sherpa-kb-retrieve Lambda via API Gateway with SigV4 signing.

Supports project-based S3 prefix isolation (Ticket: claudecodeshared-g3ac):
- Documents are stored with project prefix: s3://sherpa-kb-docs/{project_id}/documents/...
- Results are filtered to only include documents from user's allowed projects
- Pre-signed URLs are only generated for allowed project prefixes
"""

import json
from typing import Any, Optional
from dataclasses import dataclass, field

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests


@dataclass
class KBResult:
    """Single knowledge base result."""
    content: str
    score: float
    metadata: dict
    project_id: Optional[str] = None  # Project prefix from S3 key
    source: Optional[str] = None  # S3 key or source identifier


class KBRetrieveClient:
    """Client for sherpa-kb-retrieve Lambda API Gateway endpoint."""

    BASE_URL = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/kb"
    REGION = "us-east-1"
    SERVICE = "execute-api"

    def __init__(self, profile: str = "sherpa"):
        """Initialize client with AWS profile for SigV4 signing.

        Args:
            profile: AWS profile name (default: sherpa)
        """
        self.session = boto3.Session(profile_name=profile)
        self.credentials = self.session.get_credentials()

    def _sign_request(self, method: str, url: str, body: dict | None = None) -> dict:
        """Sign request with SigV4 and return headers."""
        headers = {"Content-Type": "application/json"}
        data = json.dumps(body) if body else ""

        request = AWSRequest(method=method, url=url, data=data, headers=headers)
        SigV4Auth(self.credentials, self.SERVICE, self.REGION).add_auth(request)

        return dict(request.headers)

    def retrieve(
        self,
        query: str,
        limit: int = 5,
        project_id: Optional[str] = None,
        search_type: str = "hybrid"
    ) -> list[KBResult]:
        """Retrieve relevant documents from knowledge base.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 5)
            project_id: Optional project ID for scoped queries (claudecodeshared-g3ac)
            search_type: Search type - 'hybrid', 'dense', or 'bm25' (default: hybrid)

        Returns:
            List of KBResult objects with content, score, metadata, and project_id
        """
        url = f"{self.BASE_URL}/retrieve"
        body = {
            "query": query,
            "numResults": limit,
            "searchType": search_type
        }

        # Add project_id for project-scoped queries
        if project_id:
            body["project_id"] = project_id

        headers = self._sign_request("POST", url, body)

        response = requests.post(url, json=body, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        return [
            KBResult(
                content=r.get("content", ""),
                score=r.get("score", 0.0),
                metadata=r.get("metadata", {}),
                project_id=r.get("project_id"),
                source=r.get("location", {}).get("key") or r.get("source")
            )
            for r in results
        ]

    def get_presigned_url(self, s3_key: str) -> Optional[str]:
        """Get a pre-signed URL for an S3 document with project access validation.

        Args:
            s3_key: S3 object key (must include project prefix)

        Returns:
            Pre-signed URL if access allowed, None otherwise

        Raises:
            requests.HTTPError: If access denied (403) or other error
        """
        url = f"{self.BASE_URL}/retrieve"
        body = {
            "action": "get_presigned_url",
            "s3_key": s3_key
        }
        headers = self._sign_request("POST", url, body)

        response = requests.post(url, json=body, headers=headers, timeout=30)

        if response.status_code == 403:
            return None

        response.raise_for_status()

        data = response.json()
        return data.get("url")

    def ingest(
        self,
        documents: list[dict[str, Any]],
        project_id: str = "shared"
    ) -> dict:
        """Ingest documents into the knowledge base.

        Documents are stored with project prefix for isolation (claudecodeshared-g3ac):
        s3://sherpa-kb-docs/{project_id}/documents/{filename}

        Args:
            documents: List of documents with 'content' and optional 'metadata' keys
            project_id: Project ID for S3 prefix (default: 'shared' for public docs)

        Returns:
            API response with ingestion status
        """
        url = f"{self.BASE_URL}/ingest"
        body = {
            "documents": documents,
            "project_id": project_id
        }
        headers = self._sign_request("POST", url, body)

        response = requests.post(url, json=body, headers=headers, timeout=60)
        response.raise_for_status()

        return response.json()


if __name__ == "__main__":
    # Quick test
    client = KBRetrieveClient()
    results = client.retrieve("test query", limit=3)
    for r in results:
        print(f"Score: {r.score:.3f} - {r.content[:100]}...")
