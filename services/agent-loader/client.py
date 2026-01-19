"""
Agent Loader Client

Calls the sherpa-agent-loader Lambda for lazy loading agent prompts from S3.
Uses SigV4 signing via boto3 for authentication.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests

logger = logging.getLogger(__name__)

# Configuration
LAMBDA_FUNCTION_URL = "https://sherpa-agent-loader.lambda-url.us-east-1.on.aws"
AWS_REGION = "us-east-1"
AWS_PROFILE = "sherpa"
S3_BUCKET = "sherpa-agent-prompts-458798750195"


class AgentLoaderError(Exception):
    """Base exception for agent loader errors."""
    pass


class AgentNotFoundError(AgentLoaderError):
    """Raised when an agent is not found."""
    pass


class AgentLoaderClient:
    """
    Client for the sherpa-agent-loader Lambda.

    Provides lazy loading of agent prompts from S3 bucket.
    Uses AWS SigV4 signing for authentication.
    """

    def __init__(
        self,
        profile: str = AWS_PROFILE,
        region: str = AWS_REGION,
        function_url: Optional[str] = None
    ):
        """
        Initialize the agent loader client.

        Args:
            profile: AWS profile name (default: sherpa)
            region: AWS region (default: us-east-1)
            function_url: Lambda function URL (optional override)
        """
        self.profile = profile
        self.region = region
        self.function_url = function_url or LAMBDA_FUNCTION_URL
        self._session = None
        self._credentials = None

    @property
    def session(self) -> boto3.Session:
        """Get or create boto3 session with configured profile."""
        if self._session is None:
            self._session = boto3.Session(
                profile_name=self.profile,
                region_name=self.region
            )
        return self._session

    @property
    def credentials(self):
        """Get AWS credentials for signing."""
        if self._credentials is None:
            self._credentials = self.session.get_credentials()
        return self._credentials

    def _sign_request(self, method: str, url: str, body: Optional[str] = None) -> Dict[str, str]:
        """
        Sign a request using SigV4.

        Args:
            method: HTTP method
            url: Request URL
            body: Request body (optional)

        Returns:
            Dictionary of signed headers
        """
        headers = {"Content-Type": "application/json"}
        request = AWSRequest(method=method, url=url, headers=headers, data=body)
        SigV4Auth(self.credentials, "lambda", self.region).add_auth(request)
        return dict(request.headers)

    def _invoke(self, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Invoke the Lambda function.

        Args:
            action: Action to perform (list, get, search)
            params: Additional parameters

        Returns:
            Response data from Lambda
        """
        payload = {"action": action}
        if params:
            payload.update(params)

        body = json.dumps(payload)
        headers = self._sign_request("POST", self.function_url, body)

        try:
            response = requests.post(
                self.function_url,
                headers=headers,
                data=body,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Lambda invocation failed: {e}")
            raise AgentLoaderError(f"Failed to invoke agent loader: {e}")

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        Get manifest of available agents.

        Returns:
            List of agent metadata dictionaries with keys:
            - id: Agent identifier
            - name: Display name
            - description: Brief description
            - tags: List of tags for categorization
        """
        result = self._invoke("list")
        return result.get("agents", [])

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Load full agent prompt from S3.

        Args:
            agent_id: Unique agent identifier (e.g., "lead-architect")

        Returns:
            Agent data including:
            - id: Agent identifier
            - name: Display name
            - prompt: Full system prompt
            - metadata: Additional agent metadata

        Raises:
            AgentNotFoundError: If agent does not exist
        """
        result = self._invoke("get", {"agent_id": agent_id})

        if result.get("error") == "not_found":
            raise AgentNotFoundError(f"Agent not found: {agent_id}")

        return result.get("agent", {})

    def search_agents(self, query: str) -> List[Dict[str, Any]]:
        """
        Search agents by keyword.

        Args:
            query: Search query string

        Returns:
            List of matching agent metadata dictionaries
        """
        result = self._invoke("search", {"query": query})
        return result.get("agents", [])

    def get_agent_prompt(self, agent_id: str) -> str:
        """
        Convenience method to get just the prompt text.

        Args:
            agent_id: Unique agent identifier

        Returns:
            Agent system prompt string
        """
        agent = self.get_agent(agent_id)
        return agent.get("prompt", "")


# Singleton instance for convenience
_default_client: Optional[AgentLoaderClient] = None


def get_client() -> AgentLoaderClient:
    """Get the default singleton client instance."""
    global _default_client
    if _default_client is None:
        _default_client = AgentLoaderClient()
    return _default_client
