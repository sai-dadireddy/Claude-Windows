"""
Beads Sync Client for Sherpa v4.1
Syncs local beads to AWS Lambda backend via API Gateway
"""

import json
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
from typing import Dict, List, Optional, Any
import os


class BeadsSyncClient:
    """Client for syncing beads to AWS Lambda backend"""

    def __init__(
        self,
        api_endpoint: str = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/beads",
        region: str = "us-east-1",
        profile: str = "sherpa"
    ):
        """
        Initialize the Beads Sync Client

        Args:
            api_endpoint: API Gateway endpoint URL
            region: AWS region
            profile: AWS credentials profile name
        """
        self.api_endpoint = api_endpoint.rstrip('/')
        self.region = region

        # Load AWS credentials from profile
        session = boto3.Session(profile_name=profile, region_name=region)
        self.credentials = session.get_credentials()

    def _sign_request(self, method: str, url: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Sign and send an AWS API Gateway request using SigV4

        Args:
            method: HTTP method (GET, POST, DELETE)
            url: Full URL to request
            data: Optional request body data

        Returns:
            Response object
        """
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data) if data else ''

        # Create AWS request object
        request = AWSRequest(method=method, url=url, data=body, headers=headers)

        # Sign with SigV4
        SigV4Auth(self.credentials, 'execute-api', self.region).add_auth(request)

        # Send request
        return requests.request(
            method=str(request.method),
            url=str(request.url),
            headers=dict(request.headers),
            data=request.body
        )

    def sync_bead(self, project: str, bead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync a single bead to the backend

        Args:
            project: Project identifier
            bead_data: Bead data dictionary (must include 'id' field)

        Returns:
            Response from API

        Raises:
            ValueError: If bead_data missing required fields
            requests.HTTPError: If API request fails
        """
        if 'id' not in bead_data:
            raise ValueError("bead_data must include 'id' field")

        payload = {
            'project': project,
            'bead': bead_data
        }

        response = self._sign_request('POST', self.api_endpoint, payload)
        response.raise_for_status()

        return response.json()

    def get_beads(self, project: str) -> List[Dict[str, Any]]:
        """
        Retrieve all beads for a project

        Args:
            project: Project identifier

        Returns:
            List of bead dictionaries

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.api_endpoint}?project={project}"
        response = self._sign_request('GET', url)
        response.raise_for_status()

        result = response.json()
        return result.get('beads', [])

    def delete_bead(self, project: str, bead_id: str) -> Dict[str, Any]:
        """
        Delete a bead from the backend

        Args:
            project: Project identifier
            bead_id: Bead ID to delete

        Returns:
            Response from API

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.api_endpoint}?project={project}&id={bead_id}"
        response = self._sign_request('DELETE', url)
        response.raise_for_status()

        return response.json()


def load_config(config_path: str = "config.yaml") -> Dict[str, str]:
    """
    Load configuration from YAML file

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary
    """
    import yaml

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
