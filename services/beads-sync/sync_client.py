"""
Beads Sync Client for Sherpa v4.2
Syncs local beads to AWS Lambda backend via API Gateway.
Now supports project_id isolation via sherpa-project-membership table.
"""

import json
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
from typing import Dict, List, Optional, Any, Set
import os
import logging

logger = logging.getLogger(__name__)

# Project membership table
MEMBERSHIP_TABLE = os.environ.get("MEMBERSHIP_TABLE", "sherpa-project-membership")

# Projects that bypass access checks
BYPASS_PROJECTS = {"shared", "global", "public"}


class BeadsSyncClient:
    """Client for syncing beads to AWS Lambda backend with project isolation"""

    def __init__(
        self,
        base_url: str = "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod",
        region: str = "us-east-1",
        profile: str = "sherpa",
        user_email: Optional[str] = None
    ):
        """
        Initialize the Beads Sync Client

        Args:
            base_url: API Gateway base URL (without trailing slash)
            region: AWS region
            profile: AWS credentials profile name
            user_email: User email for project membership lookup (auto-detected if None)
        """
        self.base_url = base_url.rstrip('/')
        self.region = region
        self.profile = profile

        # Load AWS credentials from profile
        self.session = boto3.Session(profile_name=profile, region_name=region)
        self.credentials = self.session.get_credentials()

        # Get user email for membership checks
        self.user_email = user_email or self._get_user_email()

        # Cache allowed projects
        self._allowed_projects: Optional[Set[str]] = None

    def _get_user_email(self) -> str:
        """Get user email from AWS SSO identity or environment."""
        # Try environment variable first
        if os.environ.get("USER_EMAIL"):
            return os.environ["USER_EMAIL"]

        # Try to get from STS caller identity
        try:
            sts = self.session.client("sts")
            identity = sts.get_caller_identity()
            arn = identity.get("Arn", "")
            # SSO ARN format: arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_.../user@domain.com
            if "@" in arn:
                email = arn.split("/")[-1]
                if "@" in email:
                    return email
        except Exception as e:
            logger.warning(f"Could not get user email from STS: {e}")

        # Fallback to environment USER
        return os.environ.get("USER", "anonymous")

    def get_allowed_projects(self, force_refresh: bool = False) -> Set[str]:
        """
        Get list of projects the user has access to.

        Args:
            force_refresh: Force refresh from DynamoDB instead of cache

        Returns:
            Set of project IDs user can access
        """
        if self._allowed_projects is not None and not force_refresh:
            return self._allowed_projects

        # Always include bypass projects
        allowed = set(BYPASS_PROJECTS)

        if self.user_email == "anonymous":
            self._allowed_projects = allowed
            return allowed

        try:
            dynamodb = self.session.resource("dynamodb")
            table = dynamodb.Table(MEMBERSHIP_TABLE)

            response = table.query(
                KeyConditionExpression="PK = :pk",
                ExpressionAttributeValues={":pk": f"USER#{self.user_email}"}
            )

            for item in response.get("Items", []):
                # SK format: PROJ#<project_id>
                sk = item.get("SK", "")
                if sk.startswith("PROJ#"):
                    project_id = sk.replace("PROJ#", "")
                    allowed.add(project_id)

            logger.info(f"User {self.user_email} has access to {len(allowed)} projects")

        except Exception as e:
            logger.error(f"Failed to query project membership: {e}")

        self._allowed_projects = allowed
        return allowed

    def can_access_project(self, project_id: str) -> bool:
        """Check if user can access a specific project."""
        if project_id in BYPASS_PROJECTS:
            return True
        return project_id in self.get_allowed_projects()

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
        List all beads for a project (enforces project access)

        Args:
            project: Project identifier
            status: Optional status filter (open, in_progress, closed)

        Returns:
            List of bead dictionaries

        Raises:
            PermissionError: If user does not have access to the project
        """
        if not self.can_access_project(project):
            raise PermissionError(f"Access denied to project: {project}")

        payload: Dict[str, Any] = {'project': project}
        if status:
            payload['status'] = status

        result = self._make_request('/beads/list', payload)
        return result.get('items', [])

    def list_beads_all_projects(self, status: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        List beads from all projects the user has access to.

        Args:
            status: Optional status filter (open, in_progress, closed)

        Returns:
            Dict mapping project_id to list of beads
        """
        all_beads: Dict[str, List[Dict[str, Any]]] = {}

        for project_id in self.get_allowed_projects():
            try:
                beads = self.list_beads(project_id, status)
                if beads:
                    all_beads[project_id] = beads
            except Exception as e:
                logger.warning(f"Failed to list beads for project {project_id}: {e}")

        return all_beads

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
        Bulk sync multiple beads (enforces project access)

        Args:
            project: Project identifier
            beads: List of bead data dictionaries

        Returns:
            Response with count of synced beads

        Raises:
            PermissionError: If user does not have access to the project
        """
        if not self.can_access_project(project):
            raise PermissionError(f"Access denied to project: {project}")

        # Ensure all beads have project_id set
        for bead in beads:
            bead['project_id'] = project

        payload = {'project': project, 'items': beads, 'user_email': self.user_email}
        return self._make_request('/beads/sync', payload)

    def sync_beads_filtered(self, beads: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Sync beads, automatically filtering to only allowed projects.

        Args:
            beads: List of bead data dictionaries (must have 'project_id' field)

        Returns:
            Dict mapping project_id to count of synced beads
        """
        allowed = self.get_allowed_projects()
        results: Dict[str, int] = {}

        # Group beads by project
        by_project: Dict[str, List[Dict[str, Any]]] = {}
        for bead in beads:
            project_id = bead.get('project_id', 'default')
            if project_id in allowed:
                if project_id not in by_project:
                    by_project[project_id] = []
                by_project[project_id].append(bead)
            else:
                logger.warning(f"Skipping bead {bead.get('id')} - no access to project {project_id}")

        # Sync each project
        for project_id, project_beads in by_project.items():
            try:
                result = self.sync_beads(project_id, project_beads)
                results[project_id] = result.get('synced', len(project_beads))
            except Exception as e:
                logger.error(f"Failed to sync beads for project {project_id}: {e}")
                results[project_id] = 0

        return results


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
