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
        base_url: str = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod",
        region: str = "us-east-1",
        profile: str = "sherpa"
    ):
        """
        Initialize the Beads Sync Client

        Args:
            base_url: API Gateway base URL (without trailing slash)
            region: AWS region
            profile: AWS credentials profile name
        """
        self.base_url = base_url.rstrip('/')
        self.region = region

        # Load AWS credentials from profile
        session = boto3.Session(profile_name=profile, region_name=region)
        self.credentials = session.get_credentials()

    def _make_request(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a signed POST request to the API

        Args:
            path: API path (e.g., /beads/list)
            data: Request body data

        Returns:
            Response JSON as dict
        """
        url = f"{self.base_url}{path}"
        body = json.dumps(data) if data else ''

        # Create AWS request object
        request = AWSRequest(method='POST', url=url, data=body, headers={'Content-Type': 'application/json'})

        # Sign with SigV4
        SigV4Auth(self.credentials, 'execute-api', self.region).add_auth(request)

        # Send request
        response = requests.request(
            method=str(request.method),
            url=str(request.url),
            headers=dict(request.headers),
            data=request.body
        )
        response.raise_for_status()
        return response.json()

    def list_beads(self, project: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all beads for a project

        Args:
            project: Project identifier
            status: Optional status filter (open, in_progress, closed)

        Returns:
            List of bead dictionaries
        """
        payload: Dict[str, Any] = {'project': project}
        if status:
            payload['status'] = status

        result = self._make_request('/beads/list', payload)
        return result.get('items', [])

    def get_bead(self, project: str, bead_id: str) -> Dict[str, Any]:
        """
        Get a single bead by ID

        Args:
            project: Project identifier
            bead_id: Bead ID

        Returns:
            Bead data dictionary
        """
        payload = {'project': project, 'id': bead_id}
        return self._make_request('/beads/get', payload)

    def create_bead(self, project: str, bead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new bead

        Args:
            project: Project identifier
            bead_data: Bead data (must include 'id', 'title')

        Returns:
            Response with created bead ID
        """
        if 'id' not in bead_data:
            raise ValueError("bead_data must include 'id' field")

        payload = {'project': project, **bead_data}
        return self._make_request('/beads/create', payload)

    def update_bead(self, project: str, bead_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing bead

        Args:
            project: Project identifier
            bead_id: Bead ID to update
            updates: Fields to update (title, description, status, priority, labels)

        Returns:
            Response with updated bead ID
        """
        payload = {'project': project, 'id': bead_id, **updates}
        return self._make_request('/beads/update', payload)

    def delete_bead(self, project: str, bead_id: str) -> Dict[str, Any]:
        """
        Delete a bead

        Args:
            project: Project identifier
            bead_id: Bead ID to delete

        Returns:
            Response with deleted bead ID
        """
        payload = {'project': project, 'id': bead_id}
        return self._make_request('/beads/delete', payload)

    def sync_beads(self, project: str, beads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk sync multiple beads

        Args:
            project: Project identifier
            beads: List of bead data dictionaries

        Returns:
            Response with count of synced beads
        """
        payload = {'project': project, 'items': beads}
        return self._make_request('/beads/sync', payload)


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
