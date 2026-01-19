"""
Pytest Configuration and Fixtures for Beads Sync Client Tests
"""

import pytest
from unittest.mock import Mock, MagicMock, patch


@pytest.fixture
def mock_aws_credentials():
    """Mock AWS credentials for testing."""
    mock_creds = Mock()
    mock_creds.access_key = "AKIAIOSFODNN7EXAMPLE"
    mock_creds.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    mock_creds.token = None
    return mock_creds


@pytest.fixture
def mock_boto3_session(mock_aws_credentials):
    """Mock boto3.Session for testing without real AWS credentials."""
    with patch("boto3.Session") as mock_session_class:
        mock_session = Mock()
        mock_session.get_credentials.return_value = mock_aws_credentials
        mock_session_class.return_value = mock_session
        yield mock_session_class


@pytest.fixture
def mock_requests_post():
    """Mock requests.request for testing API calls."""
    with patch("requests.request") as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response
        yield mock_request


@pytest.fixture
def sample_bead_data():
    """Sample bead data for testing."""
    return {
        "id": "bead-001",
        "title": "Implement authentication",
        "description": "Add JWT-based authentication to API",
        "status": "open",
        "priority": 1,
        "labels": ["feature", "security"],
    }


@pytest.fixture
def sample_bead_list():
    """Sample list of beads for testing."""
    return [
        {
            "id": "bead-001",
            "title": "Implement authentication",
            "status": "open",
            "priority": 1,
        },
        {
            "id": "bead-002",
            "title": "Add unit tests",
            "status": "in_progress",
            "priority": 2,
        },
        {
            "id": "bead-003",
            "title": "Update documentation",
            "status": "closed",
            "priority": 3,
        },
    ]


@pytest.fixture
def api_base_url():
    """API Gateway base URL for testing."""
    return "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod"


@pytest.fixture
def test_project():
    """Test project identifier."""
    return "test-project"
