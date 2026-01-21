"""
Tests for Agent Loader Lambda Function

Tests the lazy-loading agent prompt Lambda with mocked S3 responses.
"""

import json
import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

# Import the lambda function module
import lambda_function as agent_loader


# Sample test data
SAMPLE_MANIFEST = {
    "agents": [
        {
            "id": "lead-architect",
            "name": "Lead Architect",
            "description": "AWS, security, infrastructure expert",
            "tags": ["architecture", "aws", "security"]
        },
        {
            "id": "fullstack-dev",
            "name": "Fullstack Developer",
            "description": "React/Node features builder",
            "tags": ["react", "node", "typescript"]
        },
        {
            "id": "qa-engineer",
            "name": "QA Engineer",
            "description": "Jest/Playwright testing expert",
            "tags": ["testing", "playwright", "jest"]
        }
    ]
}

SAMPLE_AGENT_METADATA = {
    "id": "lead-architect",
    "name": "Lead Architect",
    "description": "AWS, security, infrastructure expert",
    "tags": ["architecture", "aws", "security"],
    "tools": ["mcp__github__*", "mcp__code-index__*"],
    "model": "claude-opus-4-5-20251101"
}

SAMPLE_PROMPT = """# Lead Architect Agent

You are a senior solutions architect with expertise in:
- AWS infrastructure design
- Security best practices
- Scalable system architecture

## Guidelines
1. Always consider security implications
2. Design for scalability
3. Follow AWS Well-Architected Framework
"""


@pytest.fixture(autouse=True)
def reset_cache():
    """Reset module-level cache before each test."""
    agent_loader._agent_cache.clear()
    agent_loader._manifest_cache = None
    agent_loader._cache_timestamp = 0
    agent_loader._s3_client = None
    yield


@pytest.fixture
def mock_s3():
    """Create a mock S3 client."""
    with patch.object(agent_loader, "get_s3_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        yield mock_client


class TestListAgents:
    """Tests for list_agents functionality."""

    def test_list_agents_from_manifest(self, mock_s3):
        """Test listing agents from manifest.json."""
        # Setup mock
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        # Execute
        result = agent_loader.list_agents()

        # Verify
        assert len(result) == 3
        assert result[0]["id"] == "lead-architect"
        assert result[1]["id"] == "fullstack-dev"
        mock_s3.get_object.assert_called_once()

    def test_list_agents_caches_result(self, mock_s3):
        """Test that manifest is cached on subsequent calls."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        # First call
        result1 = agent_loader.list_agents()
        # Second call (should use cache)
        result2 = agent_loader.list_agents()

        # Only one S3 call should be made
        assert mock_s3.get_object.call_count == 1
        assert result1 == result2

    def test_list_agents_scans_on_missing_manifest(self, mock_s3):
        """Test fallback to scanning when manifest doesn't exist."""
        # First call returns NoSuchKey error
        mock_s3.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
            "GetObject"
        )

        # Setup paginator for scan fallback
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {
                "CommonPrefixes": [
                    {"Prefix": "v4.1/agents/lead-architect/"},
                    {"Prefix": "v4.1/agents/qa-engineer/"}
                ]
            }
        ]
        mock_s3.get_paginator.return_value = mock_paginator

        # Execute
        result = agent_loader.list_agents()

        # Verify scan was triggered
        mock_s3.get_paginator.assert_called_with("list_objects_v2")


class TestGetAgent:
    """Tests for get_agent functionality."""

    def test_get_agent_success(self, mock_s3):
        """Test successfully getting an agent with prompt."""
        # Setup mock responses
        def mock_get_object(Bucket, Key):
            if Key.endswith("manifest.json"):
                return {
                    "Body": MagicMock(read=lambda: json.dumps(SAMPLE_AGENT_METADATA).encode())
                }
            elif Key.endswith("prompt.md"):
                return {
                    "Body": MagicMock(read=lambda: SAMPLE_PROMPT.encode())
                }
            raise ClientError(
                {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
                "GetObject"
            )

        mock_s3.get_object.side_effect = mock_get_object

        # Execute
        result = agent_loader.get_agent("lead-architect")

        # Verify
        assert result["id"] == "lead-architect"
        assert result["name"] == "Lead Architect"
        assert "prompt" in result
        assert "Lead Architect Agent" in result["prompt"]
        assert result["tools"] == ["mcp__github__*", "mcp__code-index__*"]

    def test_get_agent_not_found(self, mock_s3):
        """Test getting a non-existent agent."""
        mock_s3.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
            "GetObject"
        )

        # Execute
        result = agent_loader.get_agent("nonexistent-agent")

        # Verify error response
        assert result["error"] == "not_found"

    def test_get_agent_caches_result(self, mock_s3):
        """Test that agent data is cached."""
        call_count = 0

        def mock_get_object(Bucket, Key):
            nonlocal call_count
            call_count += 1
            if Key.endswith("manifest.json"):
                return {
                    "Body": MagicMock(read=lambda: json.dumps(SAMPLE_AGENT_METADATA).encode())
                }
            elif Key.endswith("prompt.md"):
                return {
                    "Body": MagicMock(read=lambda: SAMPLE_PROMPT.encode())
                }

        mock_s3.get_object.side_effect = mock_get_object

        # First call
        result1 = agent_loader.get_agent("lead-architect")
        initial_count = call_count

        # Second call (should use cache)
        result2 = agent_loader.get_agent("lead-architect")

        # No additional S3 calls
        assert call_count == initial_count
        assert result1 == result2


class TestSearchAgents:
    """Tests for search_agents functionality."""

    def test_search_by_name(self, mock_s3):
        """Test searching agents by name."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.search_agents("architect")

        assert len(result) == 1
        assert result[0]["id"] == "lead-architect"

    def test_search_by_tag(self, mock_s3):
        """Test searching agents by tag."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.search_agents("react")

        assert len(result) == 1
        assert result[0]["id"] == "fullstack-dev"

    def test_search_by_description(self, mock_s3):
        """Test searching agents by description."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.search_agents("testing")

        assert len(result) == 1
        assert result[0]["id"] == "qa-engineer"

    def test_search_no_results(self, mock_s3):
        """Test search with no matching results."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.search_agents("nonexistent")

        assert len(result) == 0

    def test_search_case_insensitive(self, mock_s3):
        """Test that search is case-insensitive."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.search_agents("ARCHITECT")

        assert len(result) == 1
        assert result[0]["id"] == "lead-architect"


class TestLambdaHandler:
    """Tests for the Lambda handler."""

    def test_handler_list_action(self, mock_s3):
        """Test handler with list action."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.lambda_handler({"action": "list"}, None)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "agents" in body
        assert len(body["agents"]) == 3

    def test_handler_get_action_success(self, mock_s3):
        """Test handler with get action."""
        def mock_get_object(Bucket, Key):
            if Key.endswith("manifest.json"):
                return {
                    "Body": MagicMock(read=lambda: json.dumps(SAMPLE_AGENT_METADATA).encode())
                }
            elif Key.endswith("prompt.md"):
                return {
                    "Body": MagicMock(read=lambda: SAMPLE_PROMPT.encode())
                }

        mock_s3.get_object.side_effect = mock_get_object

        result = agent_loader.lambda_handler(
            {"action": "get", "agent_id": "lead-architect"},
            None
        )

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "agent" in body
        assert body["agent"]["id"] == "lead-architect"

    def test_handler_get_action_not_found(self, mock_s3):
        """Test handler when agent not found."""
        mock_s3.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "Not found"}},
            "GetObject"
        )

        result = agent_loader.lambda_handler(
            {"action": "get", "agent_id": "nonexistent"},
            None
        )

        assert result["statusCode"] == 404

    def test_handler_get_action_missing_param(self, mock_s3):
        """Test handler with missing agent_id."""
        result = agent_loader.lambda_handler({"action": "get"}, None)

        assert result["statusCode"] == 400
        body = json.loads(result["body"])
        assert body["error"] == "missing_param"

    def test_handler_search_action(self, mock_s3):
        """Test handler with search action."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        result = agent_loader.lambda_handler(
            {"action": "search", "query": "aws"},
            None
        )

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "agents" in body

    def test_handler_search_action_missing_query(self, mock_s3):
        """Test handler with missing search query."""
        result = agent_loader.lambda_handler({"action": "search"}, None)

        assert result["statusCode"] == 400
        body = json.loads(result["body"])
        assert body["error"] == "missing_param"

    def test_handler_invalid_action(self, mock_s3):
        """Test handler with invalid action."""
        result = agent_loader.lambda_handler({"action": "invalid"}, None)

        assert result["statusCode"] == 400
        body = json.loads(result["body"])
        assert body["error"] == "invalid_action"

    def test_handler_function_url_format(self, mock_s3):
        """Test handler with Lambda Function URL format (body as JSON string)."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        # Lambda Function URL sends body as JSON string
        result = agent_loader.lambda_handler(
            {"body": json.dumps({"action": "list"})},
            None
        )

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "agents" in body

    def test_handler_invalid_json_body(self, mock_s3):
        """Test handler with invalid JSON in body."""
        result = agent_loader.lambda_handler(
            {"body": "not valid json"},
            None
        )

        assert result["statusCode"] == 400
        body = json.loads(result["body"])
        assert body["error"] == "invalid_json"

    def test_handler_default_action_is_list(self, mock_s3):
        """Test that default action is list."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        # No action specified
        result = agent_loader.lambda_handler({}, None)

        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "agents" in body


class TestCacheTTL:
    """Tests for cache TTL behavior."""

    def test_cache_expires_after_ttl(self, mock_s3):
        """Test that cache expires after TTL."""
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: json.dumps(SAMPLE_MANIFEST).encode())
        }

        # First call
        agent_loader.list_agents()

        # Simulate cache expiration
        agent_loader._cache_timestamp = 0

        # Second call should hit S3 again
        agent_loader.list_agents()

        # Two S3 calls
        assert mock_s3.get_object.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
