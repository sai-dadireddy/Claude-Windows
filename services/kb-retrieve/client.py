"""KB Retrieve Client - Calls sherpa-kb-retrieve Lambda via API Gateway with SigV4 signing."""

import json
from typing import Any
from dataclasses import dataclass

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

    def retrieve(self, query: str, limit: int = 5) -> list[KBResult]:
        """Retrieve relevant documents from knowledge base.

        Args:
            query: Search query string
            limit: Maximum number of results (default: 5)

        Returns:
            List of KBResult objects with content, score, and metadata
        """
        url = f"{self.BASE_URL}/retrieve"
        body = {"query": query, "limit": limit}
        headers = self._sign_request("POST", url, body)

        response = requests.post(url, json=body, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        return [
            KBResult(
                content=r.get("content", ""),
                score=r.get("score", 0.0),
                metadata=r.get("metadata", {})
            )
            for r in results
        ]

    def ingest(self, documents: list[dict[str, Any]]) -> dict:
        """Ingest documents into the knowledge base.

        Args:
            documents: List of documents with 'content' and optional 'metadata' keys

        Returns:
            API response with ingestion status
        """
        url = f"{self.BASE_URL}/ingest"
        body = {"documents": documents}
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
