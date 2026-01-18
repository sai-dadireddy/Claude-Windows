#!/usr/bin/env python3
"""
Basic tests for Memory API Client
Run with: pytest test_client.py
"""

import pytest
from unittest.mock import Mock, patch
from client import MemoryAPIClient, create_client


class TestMemoryAPIClient:
    """Test suite for MemoryAPIClient"""

    @patch('client.boto3.Session')
    def test_client_initialization(self, mock_session):
        """Test client initializes with correct parameters"""
        # Mock credentials
        mock_creds = Mock()
        mock_session.return_value.get_credentials.return_value = mock_creds

        client = MemoryAPIClient(
            endpoint="https://test.example.com",
            region="us-west-2",
            profile="test-profile"
        )

        assert client.endpoint == "https://test.example.com"
        assert client.region == "us-west-2"
        assert client.profile == "test-profile"
        assert client.credentials == mock_creds
        mock_session.assert_called_once_with(profile_name="test-profile")

    @patch('client.boto3.Session')
    def test_missing_credentials(self, mock_session):
        """Test error handling when credentials are missing"""
        mock_session.return_value.get_credentials.return_value = None

        with pytest.raises(ValueError, match="Could not load AWS credentials"):
            MemoryAPIClient(profile="invalid-profile")

    @patch('client.boto3.Session')
    @patch('client.requests.Session')
    def test_save_memory(self, mock_requests_session, mock_boto_session):
        """Test save_memory method"""
        # Mock credentials and response
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory_id": "mem_test123",
            "timestamp": "2026-01-18T12:00:00Z"
        }
        mock_response.raise_for_status = Mock()
        mock_requests_session.return_value.send.return_value = mock_response

        client = MemoryAPIClient()
        result = client.save_memory(
            project="test-project",
            memory_type="decision",
            content="Test decision"
        )

        assert result["memory_id"] == "mem_test123"
        assert "timestamp" in result

    @patch('client.boto3.Session')
    @patch('client.requests.Session')
    def test_search_memories(self, mock_requests_session, mock_boto_session):
        """Test search_memories method"""
        # Mock credentials and response
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
        mock_requests_session.return_value.send.return_value = mock_response

        client = MemoryAPIClient()
        results = client.search_memories(
            project="test-project",
            query="test query",
            limit=10
        )

        assert len(results) == 2
        assert results[0]["memory_id"] == "mem_1"
        assert results[0]["score"] == 0.95

    @patch('client.boto3.Session')
    @patch('client.requests.Session')
    def test_list_memories(self, mock_requests_session, mock_boto_session):
        """Test list_memories method"""
        # Mock credentials and response
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memories": [
                {
                    "memory_id": "mem_1",
                    "content": "Memory 1",
                    "timestamp": "2026-01-18T12:00:00Z"
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_requests_session.return_value.send.return_value = mock_response

        client = MemoryAPIClient()
        memories = client.list_memories(
            project="test-project",
            memory_type="decision"
        )

        assert len(memories) == 1
        assert memories[0]["memory_id"] == "mem_1"

    @patch('client.boto3.Session')
    @patch('client.requests.Session')
    def test_get_memory(self, mock_requests_session, mock_boto_session):
        """Test get_memory method"""
        # Mock credentials and response
        mock_creds = Mock()
        mock_boto_session.return_value.get_credentials.return_value = mock_creds

        mock_response = Mock()
        mock_response.json.return_value = {
            "memory": {
                "memory_id": "mem_test123",
                "content": "Test memory",
                "type": "decision"
            }
        }
        mock_response.raise_for_status = Mock()
        mock_requests_session.return_value.send.return_value = mock_response

        client = MemoryAPIClient()
        memory = client.get_memory("mem_test123")

        assert memory["memory_id"] == "mem_test123"
        assert memory["type"] == "decision"

    @patch('client.MemoryAPIClient')
    def test_create_client_convenience(self, mock_client_class):
        """Test create_client convenience function"""
        _ = create_client(profile="test-profile")
        mock_client_class.assert_called_once_with(profile="test-profile")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
