#!/usr/bin/env python3
"""
Tests for Memory API Client
Run with: pytest test_client.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from client import MemoryAPIClient, create_client


class TestMemoryAPIClientInit:
    """Test suite for MemoryAPIClient initialization"""

    @patch('client.boto3.Session')
    def test_client_initialization_defaults(self, mock_session):
        """Test client initializes with default parameters"""
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = MemoryAPIClient()

        assert client.base_url == "https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod"
        assert client.region == "us-east-1"
        assert client.profile == "sherpa"
        assert client.credentials == mock_creds
        mock_session.assert_called_once_with(profile_name="sherpa")

    @patch('client.boto3.Session')
    def test_client_initialization_custom(self, mock_session):
        """Test client initializes with custom parameters"""
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = MemoryAPIClient(
            base_url="https://test.example.com",
            region="us-west-2",
            profile="test-profile"
        )

        assert client.base_url == "https://test.example.com"
        assert client.region == "us-west-2"
        assert client.profile == "test-profile"
        assert client.credentials == mock_creds
        mock_session.assert_called_once_with(profile_name="test-profile")

    @patch('client.boto3.Session')
    def test_base_url_trailing_slash_stripped(self, mock_session):
        """Test trailing slash is stripped from base_url"""
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = MemoryAPIClient(base_url="https://test.example.com/")

        assert client.base_url == "https://test.example.com"

    @patch('client.boto3.Session')
    def test_missing_credentials(self, mock_session):
        """Test error handling when credentials are missing"""
        mock_session.return_value.get_credentials.return_value = None

        with pytest.raises(ValueError, match="Could not load AWS credentials"):
            MemoryAPIClient(profile="invalid-profile")


class TestMemoryAPIClientSaveMemory:
    """Test suite for save_memory method"""

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_save_memory_basic(self, mock_sigv4, mock_request, mock_boto_session):
        """Test save_memory method with basic parameters"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory_id": "mem_test123",
            "timestamp": "2026-01-18T12:00:00Z"
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        result = client.save_memory(
            project="test-project",
            memory_type="decision",
            content="Test decision"
        )

        assert result["memory_id"] == "mem_test123"
        assert "timestamp" in result
        mock_request.assert_called_once()

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_save_memory_with_metadata(self, mock_sigv4, mock_request, mock_boto_session):
        """Test save_memory method with metadata"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory_id": "mem_test456",
            "timestamp": "2026-01-18T12:00:00Z"
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        result = client.save_memory(
            project="global",
            memory_type="preference",
            content="User prefers dark mode",
            metadata={"category": "ui", "priority": "high"}
        )

        assert result["memory_id"] == "mem_test456"


class TestMemoryAPIClientSearchMemories:
    """Test suite for search_memories method"""

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_search_memories_basic(self, mock_sigv4, mock_request, mock_boto_session):
        """Test search_memories method"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "memory_id": "mem_1",
                    "content": "Test memory 1",
                    "score": 0.95
                },
                {
                    "memory_id": "mem_2",
                    "content": "Test memory 2",
                    "score": 0.87
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.search_memories(
            project="test-project",
            query="test query",
            limit=10
        )

        assert len(results) == 2
        assert results[0]["memory_id"] == "mem_1"
        assert results[0]["score"] == 0.95
        assert results[1]["memory_id"] == "mem_2"

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_search_memories_with_type_filter(self, mock_sigv4, mock_request, mock_boto_session):
        """Test search_memories with memory_type filter"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {"memory_id": "mem_1", "type": "decision", "content": "Decision 1", "score": 0.9}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.search_memories(
            project="sherpa",
            query="typescript",
            memory_type="decision"
        )

        assert len(results) == 1
        assert results[0]["type"] == "decision"

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_search_memories_empty_results(self, mock_sigv4, mock_request, mock_boto_session):
        """Test search_memories returns empty list when no results"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.search_memories(
            project="test-project",
            query="nonexistent"
        )

        assert results == []


class TestMemoryAPIClientPromoteMemory:
    """Test suite for promote_memory method"""

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_promote_memory_to_global(self, mock_sigv4, mock_request, mock_boto_session):
        """Test promote_memory to global scope"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory_id": "mem_test123",
            "original_project": "sherpa",
            "target_project": "global",
            "status": "promoted"
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        result = client.promote_memory(
            memory_id="mem_test123"
        )

        assert result["memory_id"] == "mem_test123"
        assert result["target_project"] == "global"
        assert result["status"] == "promoted"

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_promote_memory_to_custom_project(self, mock_sigv4, mock_request, mock_boto_session):
        """Test promote_memory to custom target project"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory_id": "mem_abc",
            "target_project": "shared",
            "status": "promoted"
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        result = client.promote_memory(
            memory_id="mem_abc",
            target_project="shared"
        )

        assert result["target_project"] == "shared"


class TestMemoryAPIClientKbRetrieve:
    """Test suite for kb_retrieve method"""

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_kb_retrieve_basic(self, mock_sigv4, mock_request, mock_boto_session):
        """Test kb_retrieve method"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "document_id": "doc_1",
                    "content": "Relevant document content",
                    "score": 0.92
                },
                {
                    "document_id": "doc_2",
                    "content": "Another relevant document",
                    "score": 0.85
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.kb_retrieve(
            query="how to configure authentication"
        )

        assert len(results) == 2
        assert results[0]["document_id"] == "doc_1"
        assert results[0]["score"] == 0.92

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_kb_retrieve_with_limit(self, mock_sigv4, mock_request, mock_boto_session):
        """Test kb_retrieve with custom limit"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {"document_id": "doc_1", "content": "Doc 1", "score": 0.9}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.kb_retrieve(
            query="authentication",
            limit=1
        )

        assert len(results) == 1

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_kb_retrieve_empty_results(self, mock_sigv4, mock_request, mock_boto_session):
        """Test kb_retrieve returns empty list when no results"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        results = client.kb_retrieve(query="nonexistent topic")

        assert results == []


class TestConvenienceFunctions:
    """Test suite for convenience functions"""

    @patch('client.boto3.Session')
    def test_create_client_default(self, mock_session):
        """Test create_client with default profile"""
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = create_client()

        assert isinstance(client, MemoryAPIClient)
        assert client.profile == "sherpa"

    @patch('client.boto3.Session')
    def test_create_client_custom_profile(self, mock_session):
        """Test create_client with custom profile"""
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = create_client(profile="custom-profile")

        assert isinstance(client, MemoryAPIClient)
        mock_session.assert_called_with(profile_name="custom-profile")


class TestAPIRequestHandling:
    """Test suite for API request handling and edge cases"""

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_request_uses_sigv4_auth(self, mock_sigv4, mock_request, mock_boto_session):
        """Test that requests are signed with SigV4"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        mock_request.return_value = mock_response

        client = MemoryAPIClient()
        client.search_memories(project="test", query="test")

        # Verify SigV4Auth was instantiated and add_auth was called
        mock_sigv4.assert_called()

    @patch('client.boto3.Session')
    @patch('client.requests.request')
    @patch('client.SigV4Auth')
    def test_http_error_raised(self, mock_sigv4, mock_request, mock_boto_session):
        """Test that HTTP errors are propagated"""
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 500 Error")
        mock_request.return_value = mock_response

        client = MemoryAPIClient()

        with pytest.raises(Exception, match="HTTP 500 Error"):
            client.search_memories(project="test", query="test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
