"""Tests for Context Distiller Lambda.

Run with: pytest test_distiller.py -v
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

# Import the module under test
from lambda_function import (
    estimate_tokens,
    extract_code_blocks,
    restore_code_blocks,
    build_distill_prompt,
    distill_document,
    distill_batch,
    lambda_handler,
    DistillResult,
    BatchResult,
    DEFAULT_MAX_TOKENS,
)


class TestEstimateTokens:
    """Tests for token estimation function."""

    def test_empty_string(self):
        """Empty string should return 0 tokens."""
        assert estimate_tokens("") == 0

    def test_none_input(self):
        """None input should return 0 tokens."""
        assert estimate_tokens(None) == 0

    def test_single_word(self):
        """Single word should return at least 1 token."""
        result = estimate_tokens("hello")
        assert result >= 1

    def test_sentence(self):
        """Sentence should return reasonable token count."""
        text = "This is a test sentence with multiple words."
        result = estimate_tokens(text)
        # Expect roughly 8-12 tokens for 8 words
        assert 5 <= result <= 15

    def test_longer_text(self):
        """Longer text should scale appropriately."""
        short_text = "Hello world"
        long_text = "Hello world " * 100
        short_tokens = estimate_tokens(short_text)
        long_tokens = estimate_tokens(long_text)
        # Long text should have significantly more tokens
        assert long_tokens > short_tokens * 50


class TestExtractCodeBlocks:
    """Tests for code block extraction."""

    def test_no_code_blocks(self):
        """Text without code blocks should return empty list."""
        text = "This is plain text without any code."
        result_text, blocks = extract_code_blocks(text)
        assert result_text == text
        assert blocks == []

    def test_single_code_block(self):
        """Single code block should be extracted."""
        text = """Some text
```python
def hello():
    print("hello")
```
More text"""
        result_text, blocks = extract_code_blocks(text)
        assert "[CODE_BLOCK_0]" in result_text
        assert len(blocks) == 1
        assert 'def hello()' in blocks[0]

    def test_multiple_code_blocks(self):
        """Multiple code blocks should all be extracted."""
        text = """First
```python
code1
```
Middle
```javascript
code2
```
End"""
        result_text, blocks = extract_code_blocks(text)
        assert "[CODE_BLOCK_0]" in result_text
        assert "[CODE_BLOCK_1]" in result_text
        assert len(blocks) == 2

    def test_code_block_without_language(self):
        """Code blocks without language specifier should work."""
        text = """Text
```
plain code
```
End"""
        result_text, blocks = extract_code_blocks(text)
        assert len(blocks) == 1


class TestRestoreCodeBlocks:
    """Tests for code block restoration."""

    def test_restore_single_block(self):
        """Single code block should be restored."""
        text = "Before [CODE_BLOCK_0] After"
        blocks = ["print('hello')"]
        result = restore_code_blocks(text, blocks)
        assert "```\nprint('hello')```" in result
        assert "[CODE_BLOCK_0]" not in result

    def test_restore_multiple_blocks(self):
        """Multiple code blocks should all be restored."""
        text = "[CODE_BLOCK_0] middle [CODE_BLOCK_1]"
        blocks = ["code1", "code2"]
        result = restore_code_blocks(text, blocks)
        assert "```\ncode1```" in result
        assert "```\ncode2```" in result

    def test_restore_with_no_placeholders(self):
        """Text without placeholders should remain unchanged."""
        text = "No code blocks here"
        blocks = ["unused"]
        result = restore_code_blocks(text, blocks)
        assert result == text


class TestBuildDistillPrompt:
    """Tests for prompt building."""

    def test_includes_text(self):
        """Prompt should include the input text."""
        text = "Document content here"
        prompt = build_distill_prompt(text, 500)
        assert text in prompt

    def test_includes_max_tokens(self):
        """Prompt should mention target tokens."""
        prompt = build_distill_prompt("test", 300)
        assert "300" in prompt

    def test_preserve_code_true(self):
        """Should mention code preservation when enabled."""
        prompt = build_distill_prompt("test", 500, preserve_code=True)
        assert "code" in prompt.lower()

    def test_preserve_code_false(self):
        """Should not emphasize code preservation when disabled."""
        prompt = build_distill_prompt("test", 500, preserve_code=False)
        # The instruction to keep code verbatim should not be present
        assert "keep verbatim" not in prompt.lower()


class TestDistillDocument:
    """Tests for single document distillation."""

    def test_empty_document(self):
        """Empty document should return error result."""
        result = distill_document("", max_tokens=100)
        assert result.error == "Empty document"
        assert result.original_tokens == 0

    def test_whitespace_only(self):
        """Whitespace-only document should return error."""
        result = distill_document("   \n\t  ", max_tokens=100)
        assert result.error == "Empty document"

    def test_small_document_passthrough(self):
        """Small documents should pass through without distillation."""
        text = "Short text"
        result = distill_document(text, max_tokens=1000)
        assert result.distilled_text == text
        assert result.compression_ratio == 1.0
        assert result.error is None

    def test_document_id_preserved(self):
        """Document ID should be preserved in result."""
        result = distill_document("text", max_tokens=1000, document_id="doc-123")
        assert result.document_id == "doc-123"

    @patch("lambda_function.call_nova_micro")
    def test_successful_distillation(self, mock_nova):
        """Successful distillation should return compressed result."""
        mock_nova.return_value = "Compressed summary"
        long_text = "This is a very long document. " * 100

        result = distill_document(long_text, max_tokens=50)

        assert result.distilled_text == "Compressed summary"
        assert result.compression_ratio < 1.0
        assert result.error is None
        mock_nova.assert_called_once()

    @patch("lambda_function.call_nova_micro")
    def test_distillation_error_handling(self, mock_nova):
        """Errors should be caught and original text returned."""
        mock_nova.side_effect = Exception("API Error")
        long_text = "This is a very long document. " * 100

        result = distill_document(long_text, max_tokens=50)

        assert result.distilled_text == long_text  # Original returned
        assert result.error == "API Error"

    @patch("lambda_function.call_nova_micro")
    def test_code_blocks_preserved(self, mock_nova):
        """Code blocks should be extracted and restored."""
        mock_nova.return_value = "Summary with [CODE_BLOCK_0]"
        text = """Description
```python
def test():
    pass
```
More text""" * 50  # Make it long enough to trigger distillation

        result = distill_document(text, max_tokens=50, preserve_code=True)

        # 50 repetitions means 50 code blocks
        assert result.preserved_code_blocks == 50
        assert "```" in result.distilled_text


class TestDistillBatch:
    """Tests for batch document distillation."""

    def test_empty_batch(self):
        """Empty batch should return empty results."""
        result = distill_batch([])
        assert result.results == []
        assert result.success_count == 0
        assert result.error_count == 0

    def test_single_document_batch(self):
        """Single document batch should work."""
        docs = [{"text": "Short text", "id": "doc1"}]
        result = distill_batch(docs, max_tokens=1000)
        assert len(result.results) == 1
        assert result.success_count == 1

    @patch("lambda_function.call_nova_micro")
    def test_multiple_documents(self, mock_nova):
        """Multiple documents should all be processed."""
        mock_nova.return_value = "Summary"
        docs = [
            {"text": "Long text " * 100, "id": "doc1"},
            {"text": "Another long " * 100, "id": "doc2"},
        ]

        result = distill_batch(docs, max_tokens=50)

        assert len(result.results) == 2
        assert result.success_count == 2
        assert result.total_original_tokens > result.total_compressed_tokens

    @patch("lambda_function.distill_document")
    def test_batch_size_limit(self, mock_distill):
        """Batch should be truncated if exceeds limit."""
        mock_distill.return_value = DistillResult(
            original_text="",
            distilled_text="",
            original_tokens=10,
            compressed_tokens=5,
            compression_ratio=0.5,
            preserved_code_blocks=0
        )

        # Create batch larger than MAX_BATCH_SIZE (10)
        docs = [{"text": f"doc{i}"} for i in range(15)]

        with patch("lambda_function.MAX_BATCH_SIZE", 10):
            result = distill_batch(docs)

        # Should only process up to limit
        assert mock_distill.call_count == 10

    def test_per_document_max_tokens(self):
        """Each document can have its own max_tokens."""
        docs = [
            {"text": "Short", "max_tokens": 100},
            {"text": "Another", "max_tokens": 200},
        ]
        result = distill_batch(docs)
        assert len(result.results) == 2


class TestLambdaHandler:
    """Tests for the Lambda handler function."""

    def test_single_document_request(self):
        """Single document request should work."""
        event = {
            "text": "Short document",
            "max_tokens": 500
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "distilled_text" in body
        assert "original_tokens" in body

    def test_batch_request(self):
        """Batch request should work."""
        event = {
            "documents": [
                {"text": "Doc 1", "id": "1"},
                {"text": "Doc 2", "id": "2"}
            ],
            "max_tokens": 500
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert "results" in body
        assert len(body["results"]) == 2

    def test_api_gateway_proxy_integration(self):
        """API Gateway proxy format should be handled."""
        event = {
            "body": json.dumps({"text": "Document text", "max_tokens": 100})
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

    def test_invalid_json_body(self):
        """Invalid JSON should return 400 error."""
        event = {
            "body": "not valid json{"
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "error" in body

    def test_cors_headers(self):
        """Response should include CORS headers."""
        event = {"text": "test"}
        response = lambda_handler(event, None)

        assert "Access-Control-Allow-Origin" in response["headers"]

    def test_default_max_tokens(self):
        """Request without max_tokens should use default."""
        event = {"text": "test"}
        response = lambda_handler(event, None)

        assert response["statusCode"] == 200

    @patch("lambda_function.distill_document")
    def test_exception_handling(self, mock_distill):
        """Unexpected exceptions should return 500."""
        mock_distill.side_effect = RuntimeError("Unexpected error")
        event = {"text": "Long text " * 100}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "error" in body


class TestCallNovaMicro:
    """Tests for Nova Micro API calls."""

    @patch("lambda_function.bedrock_client")
    def test_successful_call(self, mock_client):
        """Successful API call should return text."""
        from lambda_function import call_nova_micro

        mock_response = {
            "output": {
                "message": {
                    "content": [{"text": "Distilled content"}]
                }
            }
        }
        mock_body = Mock()
        mock_body.read.return_value = json.dumps(mock_response).encode()
        mock_client.invoke_model.return_value = {"body": mock_body}

        result = call_nova_micro("Test prompt", max_output_tokens=500)

        assert result == "Distilled content"
        mock_client.invoke_model.assert_called_once()

    @patch("lambda_function.bedrock_client")
    def test_empty_response(self, mock_client):
        """Empty response should return empty string."""
        from lambda_function import call_nova_micro

        mock_response = {"output": {"message": {"content": []}}}
        mock_body = Mock()
        mock_body.read.return_value = json.dumps(mock_response).encode()
        mock_client.invoke_model.return_value = {"body": mock_body}

        result = call_nova_micro("Test prompt")

        assert result == ""


class TestIntegration:
    """Integration tests (require mocking Bedrock)."""

    @patch("lambda_function.call_nova_micro")
    def test_full_distillation_workflow(self, mock_nova):
        """Test complete workflow from handler to result."""
        mock_nova.return_value = "- Key fact 1\n- Key fact 2\n- Action item"

        event = {
            "body": json.dumps({
                "text": """
                # Long Document Title

                This document contains many paragraphs of information.
                """ * 50,
                "max_tokens": 100,
                "preserve_code": True
            })
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])

        assert body["compression_ratio"] < 1.0
        assert body["original_tokens"] > body["compressed_tokens"]
        assert "Key fact" in body["distilled_text"]

    @patch("lambda_function.call_nova_micro")
    def test_batch_workflow_with_mixed_sizes(self, mock_nova):
        """Test batch with documents of varying sizes."""
        mock_nova.return_value = "Summary"

        event = {
            "documents": [
                {"text": "Short", "id": "small"},
                {"text": "Medium length text " * 20, "id": "medium"},
                {"text": "Very long document " * 100, "id": "large"},
            ],
            "max_tokens": 50
        }

        response = lambda_handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])

        assert body["success_count"] == 3
        assert body["error_count"] == 0
        # Small doc should pass through, others should be compressed
        assert body["overall_compression_ratio"] < 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
