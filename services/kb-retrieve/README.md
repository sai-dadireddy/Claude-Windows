# KB Retrieve Client

Python client for the sherpa-kb-retrieve Lambda API Gateway endpoint with AWS SigV4 authentication.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

The client uses AWS profile `sherpa` by default. Ensure your AWS credentials are configured:

```bash
aws configure --profile sherpa
```

## Usage

### Basic Retrieval

```python
from services.kb_retrieve import KBRetrieveClient

client = KBRetrieveClient()

# Retrieve documents
results = client.retrieve("How do I configure Workday integrations?", limit=5)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")
    print("---")
```

### Document Ingestion

```python
documents = [
    {
        "content": "This is document content about Workday APIs.",
        "metadata": {"source": "workday_docs", "type": "api"}
    },
    {
        "content": "Another document about PeopleSoft integration.",
        "metadata": {"source": "oracle_docs", "type": "integration"}
    }
]

response = client.ingest(documents)
print(response)
```

### Custom Profile

```python
client = KBRetrieveClient(profile="my-custom-profile")
```

## API Reference

### KBRetrieveClient

| Method | Description |
|--------|-------------|
| `retrieve(query, limit=5)` | Search knowledge base, returns list of KBResult |
| `ingest(documents)` | Add documents to knowledge base |

### KBResult

| Field | Type | Description |
|-------|------|-------------|
| `content` | str | Document content |
| `score` | float | Relevance score |
| `metadata` | dict | Document metadata |

## API Endpoints

- **Base URL**: `https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/kb`
- **Retrieve**: `POST /kb/retrieve`
- **Ingest**: `POST /kb/ingest`

## Authentication

All requests are signed using AWS SigV4. The client automatically handles signing using boto3 credentials.
