"""Context Distiller Lambda - Compress RAG documents using Nova Micro (85% cost reduction).

This Lambda pre-processes large documents into concise summaries before RAG retrieval,
preserving key facts, code snippets, and actionable items while significantly reducing
token costs.

Environment Variables:
    AWS_REGION: AWS region for Bedrock (default: us-east-1)
    NOVA_MODEL_ID: Model ID for Nova Micro (default: amazon.nova-micro-v1:0)
    MAX_BATCH_SIZE: Maximum documents per batch (default: 10)
"""

import json
import logging
import os
import re
from dataclasses import dataclass, asdict
from typing import Any

import boto3
from botocore.config import Config

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
NOVA_MODEL_ID = os.environ.get("NOVA_MODEL_ID", "amazon.nova-micro-v1:0")
MAX_BATCH_SIZE = int(os.environ.get("MAX_BATCH_SIZE", "10"))
DEFAULT_MAX_TOKENS = 500

# Bedrock client with retry config
bedrock_config = Config(
    region_name=AWS_REGION,
    retries={"max_attempts": 3, "mode": "adaptive"}
)
bedrock_client = boto3.client("bedrock-runtime", config=bedrock_config)


@dataclass
class DistillResult:
    """Result of distilling a single document."""
    original_text: str
    distilled_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    preserved_code_blocks: int
    document_id: str | None = None
    error: str | None = None


@dataclass
class BatchResult:
    """Result of batch distillation."""
    results: list[dict]
    total_original_tokens: int
    total_compressed_tokens: int
    overall_compression_ratio: float
    success_count: int
    error_count: int


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough approximation: ~4 chars per token for English).

    Args:
        text: Input text to estimate tokens for

    Returns:
        Estimated token count
    """
    if not text:
        return 0
    # More accurate estimation considering whitespace and punctuation
    words = len(text.split())
    chars = len(text)
    # Hybrid approach: average of word-based and char-based estimates
    return max(1, int((words * 1.3 + chars / 4) / 2))


def extract_code_blocks(text: str) -> tuple[str, list[str]]:
    """Extract code blocks from text to preserve them during distillation.

    Args:
        text: Input text potentially containing code blocks

    Returns:
        Tuple of (text with placeholders, list of extracted code blocks)
    """
    # Pattern to match code blocks with optional language specifier
    code_pattern = r'```\w*\n(.*?)```'
    code_blocks = re.findall(code_pattern, text, re.DOTALL)

    # Replace code blocks with placeholders one at a time
    placeholder_text = text
    for i in range(len(code_blocks)):
        placeholder_text = re.sub(
            r'```\w*\n.*?```',
            f'[CODE_BLOCK_{i}]',
            placeholder_text,
            count=1,
            flags=re.DOTALL
        )

    return placeholder_text, code_blocks


def restore_code_blocks(text: str, code_blocks: list[str]) -> str:
    """Restore code blocks after distillation.

    Args:
        text: Text with placeholders
        code_blocks: List of original code blocks

    Returns:
        Text with code blocks restored
    """
    result = text
    for i, block in enumerate(code_blocks):
        placeholder = f'[CODE_BLOCK_{i}]'
        if placeholder in result:
            result = result.replace(placeholder, f'```\n{block}```')
    return result


def build_distill_prompt(text: str, max_tokens: int, preserve_code: bool = True) -> str:
    """Build the prompt for Nova Micro to distill the document.

    Args:
        text: Document text to distill
        max_tokens: Target maximum tokens for output
        preserve_code: Whether to preserve code blocks verbatim

    Returns:
        Formatted prompt string
    """
    instructions = f"""Distill this document into a concise summary targeting {max_tokens} tokens.

PRESERVE:
- Key facts, numbers, and dates
- Action items and requirements
- Technical specifications
- Error messages and solutions
- API endpoints and parameters
{"- Code snippets (keep verbatim)" if preserve_code else ""}

REMOVE:
- Redundant explanations
- Filler words and phrases
- Repeated information
- Unnecessary context

OUTPUT FORMAT:
- Use bullet points for facts
- Keep code blocks intact
- Preserve technical accuracy

DOCUMENT:
{text}

DISTILLED SUMMARY:"""

    return instructions


def call_nova_micro(prompt: str, max_output_tokens: int = 1000) -> str:
    """Call Nova Micro via Bedrock to distill content.

    Args:
        prompt: The distillation prompt
        max_output_tokens: Maximum tokens in response

    Returns:
        Distilled text from Nova Micro

    Raises:
        Exception: If Bedrock call fails
    """
    body = {
        "inferenceConfig": {
            "max_new_tokens": max_output_tokens,
            "temperature": 0.1,  # Low temperature for factual preservation
            "top_p": 0.9
        },
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    }

    response = bedrock_client.invoke_model(
        modelId=NOVA_MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())

    # Extract text from Nova response
    output = response_body.get("output", {})
    message = output.get("message", {})
    content = message.get("content", [])

    if content and len(content) > 0:
        return content[0].get("text", "")

    return ""


def distill_document(
    text: str,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    document_id: str | None = None,
    preserve_code: bool = True
) -> DistillResult:
    """Distill a single document using Nova Micro.

    Args:
        text: Document text to distill
        max_tokens: Target maximum tokens for distilled output
        document_id: Optional identifier for the document
        preserve_code: Whether to preserve code blocks verbatim

    Returns:
        DistillResult with original and compressed text plus metadata
    """
    if not text or not text.strip():
        return DistillResult(
            original_text="",
            distilled_text="",
            original_tokens=0,
            compressed_tokens=0,
            compression_ratio=1.0,
            preserved_code_blocks=0,
            document_id=document_id,
            error="Empty document"
        )

    original_tokens = estimate_tokens(text)

    # If document is already small enough, return as-is
    if original_tokens <= max_tokens:
        return DistillResult(
            original_text=text,
            distilled_text=text,
            original_tokens=original_tokens,
            compressed_tokens=original_tokens,
            compression_ratio=1.0,
            preserved_code_blocks=0,
            document_id=document_id
        )

    try:
        # Extract code blocks to preserve them
        code_blocks = []
        text_for_distill = text

        if preserve_code:
            text_for_distill, code_blocks = extract_code_blocks(text)

        # Build prompt and call Nova Micro
        prompt = build_distill_prompt(text_for_distill, max_tokens, preserve_code)
        distilled = call_nova_micro(prompt, max_output_tokens=max_tokens * 2)

        # Restore code blocks
        if preserve_code and code_blocks:
            distilled = restore_code_blocks(distilled, code_blocks)

        compressed_tokens = estimate_tokens(distilled)
        compression_ratio = compressed_tokens / original_tokens if original_tokens > 0 else 1.0

        return DistillResult(
            original_text=text,
            distilled_text=distilled,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compression_ratio,
            preserved_code_blocks=len(code_blocks),
            document_id=document_id
        )

    except Exception as e:
        logger.error(f"Error distilling document {document_id}: {str(e)}")
        return DistillResult(
            original_text=text,
            distilled_text=text,  # Return original on error
            original_tokens=original_tokens,
            compressed_tokens=original_tokens,
            compression_ratio=1.0,
            preserved_code_blocks=0,
            document_id=document_id,
            error=str(e)
        )


def distill_batch(
    documents: list[dict[str, Any]],
    max_tokens: int = DEFAULT_MAX_TOKENS,
    preserve_code: bool = True
) -> BatchResult:
    """Distill a batch of documents.

    Args:
        documents: List of documents with 'text' and optional 'id' keys
        max_tokens: Target maximum tokens per document
        preserve_code: Whether to preserve code blocks

    Returns:
        BatchResult with all results and aggregate statistics
    """
    if len(documents) > MAX_BATCH_SIZE:
        logger.warning(f"Batch size {len(documents)} exceeds max {MAX_BATCH_SIZE}, truncating")
        documents = documents[:MAX_BATCH_SIZE]

    results = []
    total_original = 0
    total_compressed = 0
    success_count = 0
    error_count = 0

    for doc in documents:
        text = doc.get("text", "")
        doc_id = doc.get("id")
        doc_max_tokens = doc.get("max_tokens", max_tokens)

        result = distill_document(
            text=text,
            max_tokens=doc_max_tokens,
            document_id=doc_id,
            preserve_code=preserve_code
        )

        results.append(asdict(result))
        total_original += result.original_tokens
        total_compressed += result.compressed_tokens

        if result.error:
            error_count += 1
        else:
            success_count += 1

    overall_ratio = total_compressed / total_original if total_original > 0 else 1.0

    return BatchResult(
        results=results,
        total_original_tokens=total_original,
        total_compressed_tokens=total_compressed,
        overall_compression_ratio=overall_ratio,
        success_count=success_count,
        error_count=error_count
    )


def lambda_handler(event: dict, context: Any) -> dict:
    """AWS Lambda handler for context distillation.

    Accepts either single document or batch processing requests.

    Single document request:
    {
        "text": "Document content...",
        "max_tokens": 500,
        "preserve_code": true,
        "document_id": "optional-id"
    }

    Batch request:
    {
        "documents": [
            {"text": "...", "id": "doc1", "max_tokens": 500},
            {"text": "...", "id": "doc2"}
        ],
        "max_tokens": 500,
        "preserve_code": true
    }

    Args:
        event: Lambda event payload
        context: Lambda context object

    Returns:
        Response dict with distilled content and metadata
    """
    logger.info(f"Received event: {json.dumps(event)[:500]}...")

    try:
        # Handle API Gateway proxy integration
        if "body" in event:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        else:
            body = event

        # Determine if batch or single document
        if "documents" in body:
            # Batch processing
            documents = body["documents"]
            max_tokens = body.get("max_tokens", DEFAULT_MAX_TOKENS)
            preserve_code = body.get("preserve_code", True)

            result = distill_batch(
                documents=documents,
                max_tokens=max_tokens,
                preserve_code=preserve_code
            )

            response_body = asdict(result)

        else:
            # Single document
            text = body.get("text", "")
            max_tokens = body.get("max_tokens", DEFAULT_MAX_TOKENS)
            preserve_code = body.get("preserve_code", True)
            document_id = body.get("document_id")

            result = distill_document(
                text=text,
                max_tokens=max_tokens,
                document_id=document_id,
                preserve_code=preserve_code
            )

            response_body = asdict(result)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response_body)
        }

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }


# For local testing
if __name__ == "__main__":
    # Test single document
    test_event = {
        "text": """
# Python Best Practices Guide

## Introduction
This comprehensive guide covers essential Python best practices that every developer should know.
It includes detailed explanations and examples for writing clean, maintainable code.

## Code Style
Follow PEP 8 guidelines for consistent code formatting:
- Use 4 spaces for indentation
- Limit lines to 79 characters
- Use descriptive variable names

```python
def calculate_total(items: list[float]) -> float:
    \"\"\"Calculate the sum of all items.\"\"\"
    return sum(items)
```

## Error Handling
Always handle exceptions gracefully:
- Use specific exception types
- Provide meaningful error messages
- Log errors for debugging

## Testing
Write comprehensive tests:
- Unit tests for individual functions
- Integration tests for workflows
- Use pytest for test framework
""",
        "max_tokens": 200
    }

    result = lambda_handler(test_event, None)
    print(json.dumps(json.loads(result["body"]), indent=2))
