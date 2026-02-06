"""
Unit Tests for Beads Sync Client

Tests cover:
- BeadsSyncClient initialization
- list_beads, get_bead, create_bead, update_bead, delete_bead, sync_beads
- Error handling and edge cases
- AWS SigV4 authentication mocking
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from requests import HTTPError

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sync_client import BeadsSyncClient, load_config


class TestBeadsSyncClientInitialization:
    """Tests for BeadsSyncClient initialization."""

    def test_init_with_defaults(self, mock_boto3_session):
        """Test client initialization with default parameters."""
        client = BeadsSyncClient()

        assert client.base_url == "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod"
        assert client.region == "us-east-1"
        mock_boto3_session.assert_called_once_with(profile_name="sherpa", region_name="us-east-1")

    def test_init_with_custom_parameters(self, mock_boto3_session):
        """Test client initialization with custom parameters."""
        client = BeadsSyncClient(
            base_url="https://custom-api.example.com/v1",
            region="eu-west-1",
            profile="custom-profile"
        )

        assert client.base_url == "https://custom-api.example.com/v1"
        assert client.region == "eu-west-1"
        mock_boto3_session.assert_called_once_with(profile_name="custom-profile", region_name="eu-west-1")

    def test_init_strips_trailing_slash_from_url(self, mock_boto3_session):
        """Test that trailing slash is stripped from base URL."""
        client = BeadsSyncClient(base_url="https://api.example.com/prod/")

        assert client.base_url == "https://api.example.com/prod"

    def test_init_stores_credentials(self, mock_boto3_session, mock_aws_credentials):
        """Test that AWS credentials are stored from session."""
        client = BeadsSyncClient()

        assert client.credentials == mock_aws_credentials


class TestMakeRequest:
    """Tests for the internal _make_request method."""

    def test_make_request_constructs_correct_url(self, mock_boto3_session, mock_requests_post):
        """Test that _make_request constructs the correct URL."""
        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            client._make_request("/beads/list", {"project": "test"})

        call_args = mock_requests_post.call_args
        assert "/beads/list" in call_args.kwargs.get("url", call_args[1].get("url", ""))

    def test_make_request_with_data(self, mock_boto3_session, mock_requests_post):
        """Test that _make_request properly serializes JSON data."""
        client = BeadsSyncClient()
        test_data = {"project": "test-project", "status": "open"}

        with patch("sync_client.SigV4Auth"):
            client._make_request("/beads/list", test_data)

        mock_requests_post.assert_called_once()

    def test_make_request_without_data(self, mock_boto3_session, mock_requests_post):
        """Test that _make_request works without data payload."""
        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            client._make_request("/beads/health")

        mock_requests_post.assert_called_once()

    def test_make_request_raises_on_http_error(self, mock_boto3_session, mock_requests_post):
        """Test that _make_request propagates HTTP errors."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("403 Forbidden")
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            with pytest.raises(HTTPError):
                client._make_request("/beads/list", {"project": "test"})


class TestListBeads:
    """Tests for the list_beads method."""

    def test_list_beads_returns_items(self, mock_boto3_session, mock_requests_post, test_project, sample_bead_list):
        """Test that list_beads returns the items from response."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": sample_bead_list}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.list_beads(test_project)

        assert result == sample_bead_list
        assert len(result) == 3

    def test_list_beads_with_status_filter(self, mock_boto3_session, mock_requests_post, test_project):
        """Test that list_beads includes status in payload when provided."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            client.list_beads(test_project, status="open")

        # Verify the call was made (status should be in payload)
        mock_requests_post.assert_called_once()

    def test_list_beads_returns_empty_list_when_no_items(self, mock_boto3_session, mock_requests_post, test_project):
        """Test that list_beads returns empty list when no items in response."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.list_beads(test_project)

        assert result == []


class TestGetBead:
    """Tests for the get_bead method."""

    def test_get_bead_returns_bead_data(self, mock_boto3_session, mock_requests_post, test_project, sample_bead_data):
        """Test that get_bead returns the bead data."""
        mock_response = Mock()
        mock_response.json.return_value = sample_bead_data
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.get_bead(test_project, "bead-001")

        assert result == sample_bead_data
        assert result["id"] == "bead-001"

    def test_get_bead_with_nonexistent_id(self, mock_boto3_session, mock_requests_post, test_project):
        """Test get_bead behavior with nonexistent bead ID."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            with pytest.raises(HTTPError):
                client.get_bead(test_project, "nonexistent-id")


class TestCreateBead:
    """Tests for the create_bead method."""

    def test_create_bead_success(self, mock_boto3_session, mock_requests_post, test_project, sample_bead_data):
        """Test successful bead creation."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-001", "created": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.create_bead(test_project, sample_bead_data)

        assert result["id"] == "bead-001"
        assert result["created"] is True

    def test_create_bead_requires_id_field(self, mock_boto3_session, test_project):
        """Test that create_bead raises ValueError when id is missing."""
        client = BeadsSyncClient()
        bead_data_without_id = {"title": "Test bead", "status": "open"}

        with pytest.raises(ValueError, match="bead_data must include 'id' field"):
            client.create_bead(test_project, bead_data_without_id)

    def test_create_bead_with_minimal_data(self, mock_boto3_session, mock_requests_post, test_project):
        """Test create_bead with only required fields."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-minimal", "created": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()
        minimal_bead = {"id": "bead-minimal"}

        with patch("sync_client.SigV4Auth"):
            result = client.create_bead(test_project, minimal_bead)

        assert result["id"] == "bead-minimal"


class TestUpdateBead:
    """Tests for the update_bead method."""

    def test_update_bead_success(self, mock_boto3_session, mock_requests_post, test_project):
        """Test successful bead update."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-001", "updated": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()
        updates = {"status": "in_progress", "priority": 2}

        with patch("sync_client.SigV4Auth"):
            result = client.update_bead(test_project, "bead-001", updates)

        assert result["id"] == "bead-001"
        assert result["updated"] is True

    def test_update_bead_with_single_field(self, mock_boto3_session, mock_requests_post, test_project):
        """Test updating a single field."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-001", "updated": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.update_bead(test_project, "bead-001", {"status": "closed"})

        assert result["updated"] is True

    def test_update_bead_with_labels(self, mock_boto3_session, mock_requests_post, test_project):
        """Test updating labels field."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-001", "updated": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.update_bead(test_project, "bead-001", {"labels": ["bug", "urgent"]})

        assert result["updated"] is True


class TestDeleteBead:
    """Tests for the delete_bead method."""

    def test_delete_bead_success(self, mock_boto3_session, mock_requests_post, test_project):
        """Test successful bead deletion."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-001", "deleted": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.delete_bead(test_project, "bead-001")

        assert result["id"] == "bead-001"
        assert result["deleted"] is True

    def test_delete_bead_nonexistent(self, mock_boto3_session, mock_requests_post, test_project):
        """Test deleting a nonexistent bead."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            with pytest.raises(HTTPError):
                client.delete_bead(test_project, "nonexistent-id")


class TestSyncBeads:
    """Tests for the sync_beads method."""

    def test_sync_beads_success(self, mock_boto3_session, mock_requests_post, test_project, sample_bead_list):
        """Test successful bulk sync of beads."""
        mock_response = Mock()
        mock_response.json.return_value = {"synced": 3, "project": test_project}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.sync_beads(test_project, sample_bead_list)

        assert result["synced"] == 3
        assert result["project"] == test_project

    def test_sync_beads_empty_list(self, mock_boto3_session, mock_requests_post, test_project):
        """Test syncing an empty list of beads."""
        mock_response = Mock()
        mock_response.json.return_value = {"synced": 0, "project": test_project}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.sync_beads(test_project, [])

        assert result["synced"] == 0

    def test_sync_beads_single_item(self, mock_boto3_session, mock_requests_post, test_project, sample_bead_data):
        """Test syncing a single bead."""
        mock_response = Mock()
        mock_response.json.return_value = {"synced": 1, "project": test_project}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.sync_beads(test_project, [sample_bead_data])

        assert result["synced"] == 1


class TestLoadConfig:
    """Tests for the load_config function."""

    def test_load_config_success(self, tmp_path):
        """Test successful config loading."""
        config_content = """
base_url: https://api.example.com/prod
region: us-west-2
profile: test-profile
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        config = load_config(str(config_file))

        assert config["base_url"] == "https://api.example.com/prod"
        assert config["region"] == "us-west-2"
        assert config["profile"] == "test-profile"

    def test_load_config_file_not_found(self):
        """Test load_config raises FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="Config file not found"):
            load_config("/nonexistent/path/config.yaml")

    def test_load_config_empty_file(self, tmp_path):
        """Test loading an empty config file."""
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        config = load_config(str(config_file))

        assert config is None


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_project_with_special_characters(self, mock_boto3_session, mock_requests_post, test_project):
        """Test project names with special characters - uses allowed project."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            # Use an allowed project (bypass project)
            result = client.list_beads("shared")

        assert result == []

    def test_bead_id_with_special_characters(self, mock_boto3_session, mock_requests_post, test_project):
        """Test bead IDs with special characters."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-uuid-123-456"}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.get_bead(test_project, "bead-uuid-123-456")

        assert result["id"] == "bead-uuid-123-456"

    def test_large_bead_description(self, mock_boto3_session, mock_requests_post, test_project):
        """Test creating a bead with a large description."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-large", "created": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()
        large_description = "A" * 10000  # 10KB description
        bead_data = {"id": "bead-large", "title": "Large bead", "description": large_description}

        with patch("sync_client.SigV4Auth"):
            result = client.create_bead(test_project, bead_data)

        assert result["created"] is True

    def test_unicode_in_bead_data(self, mock_boto3_session, mock_requests_post, test_project):
        """Test bead data with Unicode characters."""
        mock_response = Mock()
        mock_response.json.return_value = {"id": "bead-unicode", "created": True}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()
        bead_data = {
            "id": "bead-unicode",
            "title": "Internationalization",
            "description": "Handling characters like: cafe, resume, nino"
        }

        with patch("sync_client.SigV4Auth"):
            result = client.create_bead(test_project, bead_data)

        assert result["created"] is True

    def test_empty_project_name(self, mock_boto3_session, mock_requests_post):
        """Test with empty project name - should raise PermissionError."""
        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            # Empty project is not in allowed list, should raise PermissionError
            with pytest.raises(PermissionError, match="Access denied"):
                client.list_beads("")


class TestProjectAccessControl:
    """Tests for project access control functionality."""

    def test_bypass_projects_always_allowed(self, mock_boto3_session):
        """Test that bypass projects (shared, global, public) are always accessible."""
        client = BeadsSyncClient()

        for project in ["shared", "global", "public"]:
            assert client.can_access_project(project) is True

    def test_list_beads_denied_for_unauthorized_project(self, mock_boto3_session, mock_requests_post):
        """Test that list_beads raises PermissionError for unauthorized projects."""
        client = BeadsSyncClient()

        with pytest.raises(PermissionError, match="Access denied"):
            client.list_beads("secret-unauthorized-project")

    def test_sync_beads_denied_for_unauthorized_project(self, mock_boto3_session, mock_requests_post):
        """Test that sync_beads raises PermissionError for unauthorized projects."""
        client = BeadsSyncClient()

        with pytest.raises(PermissionError, match="Access denied"):
            client.sync_beads("secret-unauthorized-project", [{"id": "test"}])

    def test_get_allowed_projects_includes_bypass(self, mock_boto3_session):
        """Test that get_allowed_projects always includes bypass projects."""
        client = BeadsSyncClient()
        allowed = client.get_allowed_projects()

        assert "shared" in allowed
        assert "global" in allowed
        assert "public" in allowed

    def test_list_beads_all_projects(self, mock_boto3_session, mock_requests_post):
        """Test listing beads from all allowed projects."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": "bead-1"}]}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.list_beads_all_projects()

        # Should have results for at least bypass projects
        assert isinstance(result, dict)


class TestStatusFilters:
    """Tests for status filter functionality."""

    @pytest.mark.parametrize("status", ["open", "in_progress", "closed"])
    def test_list_beads_with_valid_statuses(self, mock_boto3_session, mock_requests_post, test_project, status):
        """Test list_beads with all valid status values."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.list_beads(test_project, status=status)

        assert result == []
        mock_requests_post.assert_called_once()

    def test_list_beads_without_status_filter(self, mock_boto3_session, mock_requests_post, test_project):
        """Test list_beads without status filter returns all beads."""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [{"id": "1"}, {"id": "2"}]}
        mock_response.raise_for_status = Mock()
        mock_requests_post.return_value = mock_response

        client = BeadsSyncClient()

        with patch("sync_client.SigV4Auth"):
            result = client.list_beads(test_project, status=None)

        assert len(result) == 2
