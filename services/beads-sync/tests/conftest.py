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
def mock_dynamodb_table():
    """Mock DynamoDB table for project membership queries."""
    mock_table = Mock()
    # Default: return test-project as allowed
    mock_table.query.return_value = {
        "Items": [
            {"PK": "USER#test@example.com", "SK": "PROJ#test-project", "role": "member"},
            {"PK": "USER#test@example.com", "SK": "PROJ#sherpa", "role": "admin"}
        ]
    }
    return mock_table


@pytest.fixture
def mock_sts_client():
    """Mock STS client for caller identity."""
    mock_sts = Mock()
    mock_sts.get_caller_identity.return_value = {
        "Arn": "arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_Developer/test@example.com",
        "Account": "123456789012"
    }
    return mock_sts


@pytest.fixture
def mock_boto3_session(mock_aws_credentials, mock_dynamodb_table, mock_sts_client):
    """Mock boto3.Session for testing without real AWS credentials."""
    with patch("boto3.Session") as mock_session_class:
        mock_session = Mock()
        mock_session.get_credentials.return_value = mock_aws_credentials

        # Mock resource for DynamoDB
        mock_dynamodb = Mock()
        mock_dynamodb.Table.return_value = mock_dynamodb_table
        mock_session.resource.return_value = mock_dynamodb

        # Mock client for STS
        mock_session.client.return_value = mock_sts_client

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


@pytest.fixture
def test_user_email():
    """Test user email."""
    return "test@example.com"


@pytest.fixture
def allowed_projects():
    """List of projects the test user has access to."""
    return {"shared", "global", "public", "test-project", "sherpa"}


@pytest.fixture
def denied_project():
    """A project the test user does NOT have access to."""
    return "secret-project"
