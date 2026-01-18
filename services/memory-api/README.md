# Memory API Client

Python client for Sherpa v4.1 memory service (AWS Lambda + DynamoDB).

## Overview

- **Endpoint**: `https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/memory`
- **Lambda**: `sherpa-memory-kb`
- **Database**: DynamoDB table `sherpa-memory-store`
- **Auth**: IAM (SigV4 signing)
- **Region**: `us-east-1`
- **Profile**: `sherpa`

## Installation

```bash
pip install boto3 requests
```

## Quick Start

```python
from services.memory_api.client import create_client

# Create client (uses 'sherpa' profile by default)
client = create_client()

# Save a memory
client.save_memory(
    project="sherpa",
    memory_type="decision",
    content="Use TypeScript for all new frontend code"
)

# Search memories
results = client.search_memories(
    project="sherpa",
    query="typescript decisions"
)

for memory in results:
    print(f"{memory['content']} (score: {memory['score']})")

# List all memories
memories = client.list_memories(project="sherpa")
```

## API Reference

### MemoryAPIClient

```python
from services.memory_api.client import MemoryAPIClient

client = MemoryAPIClient(
    endpoint="https://hl98rmqgd6.execute-api.us-east-1.amazonaws.com/prod/memory",
    region="us-east-1",
    profile="sherpa"
)
```

### Methods

#### save_memory()

Save a memory to the knowledge base.

```python
client.save_memory(
    project="sherpa",           # Project name or "global"
    memory_type="decision",     # decision, preference, observation, etc.
    content="Memory content",   # Description/details
    metadata={"key": "value"}   # Optional metadata
)
```

**Returns**: `{"memory_id": "mem_xxx", "timestamp": "2026-01-18T12:00:00Z"}`

#### search_memories()

Search memories by semantic similarity.

```python
results = client.search_memories(
    project="sherpa",
    query="search terms",
    limit=10,                   # Max results (default: 10)
    memory_type="decision"      # Optional filter
)
```

**Returns**: List of memories with similarity scores

```python
[
    {
        "memory_id": "mem_xxx",
        "project": "sherpa",
        "type": "decision",
        "content": "...",
        "timestamp": "2026-01-18T12:00:00Z",
        "score": 0.85
    },
    ...
]
```

#### list_memories()

List all memories for a project.

```python
memories = client.list_memories(
    project="sherpa",
    memory_type="decision",     # Optional filter
    limit=50                    # Max results (default: 50)
)
```

**Returns**: List of memories sorted by timestamp (newest first)

#### get_memory()

Retrieve a specific memory by ID.

```python
memory = client.get_memory("mem_abc123")
```

**Returns**: Memory details as dict

## Examples

### Save Different Memory Types

```python
# Decision
client.save_memory(
    project="sherpa",
    memory_type="decision",
    content="All API calls must include retry logic with exponential backoff"
)

# Preference
client.save_memory(
    project="global",
    memory_type="preference",
    content="User prefers concise code comments over verbose documentation"
)

# Observation
client.save_memory(
    project="sherpa",
    memory_type="observation",
    content="Lambda cold starts average 2.3s for this function",
    metadata={"function": "sherpa-memory-kb", "metric": "cold_start"}
)
```

### Search with Context

```python
# Find architecture decisions
arch_decisions = client.search_memories(
    project="sherpa",
    query="microservices architecture patterns",
    memory_type="decision",
    limit=5
)

# Find user preferences
preferences = client.search_memories(
    project="global",
    query="code style formatting",
    memory_type="preference"
)
```

### List Recent Memories

```python
# Get last 20 decisions
recent_decisions = client.list_memories(
    project="sherpa",
    memory_type="decision",
    limit=20
)

for memory in recent_decisions:
    print(f"[{memory['timestamp']}] {memory['content']}")
```

### Error Handling

```python
import requests

try:
    client.save_memory(
        project="sherpa",
        memory_type="decision",
        content="New memory"
    )
except requests.HTTPError as e:
    print(f"API error: {e.response.status_code}")
    print(e.response.text)
except ValueError as e:
    print(f"Config error: {e}")
```

## AWS Credentials

Client uses boto3 to load credentials from the `sherpa` profile (default).

### Setup Credentials

```bash
# Configure AWS profile
aws configure --profile sherpa
# AWS Access Key ID: YOUR_KEY
# AWS Secret Access Key: YOUR_SECRET
# Default region: us-east-1
```

### Using Different Profile

```python
client = MemoryAPIClient(profile="my-profile")
```

## Memory Types

Common memory types:

- **decision**: Architecture/design decisions
- **preference**: User preferences and settings
- **observation**: Performance metrics, patterns
- **bug**: Bug reports and fixes
- **pattern**: Code patterns and conventions
- **integration**: Third-party integration notes

## Integration with Sherpa

### CLI Integration

```python
#!/usr/bin/env python3
from services.memory_api.client import create_client
import sys

client = create_client()

if sys.argv[1] == "save":
    client.save_memory(
        project=sys.argv[2],
        memory_type=sys.argv[3],
        content=sys.argv[4]
    )
elif sys.argv[1] == "search":
    results = client.search_memories(
        project=sys.argv[2],
        query=sys.argv[3]
    )
    for r in results:
        print(f"{r['content']} ({r['score']:.2f})")
```

### Agent Integration

```python
from services.memory_api.client import create_client

class AgentWithMemory:
    def __init__(self):
        self.memory = create_client()

    def remember_decision(self, decision: str):
        self.memory.save_memory(
            project="sherpa",
            memory_type="decision",
            content=decision
        )

    def recall_context(self, query: str):
        return self.memory.search_memories(
            project="sherpa",
            query=query,
            limit=5
        )
```

## Troubleshooting

### Authentication Errors

```
Error: Could not load AWS credentials from profile: sherpa
```

**Solution**: Configure AWS credentials

```bash
aws configure --profile sherpa
```

### HTTP 403 Forbidden

**Solution**: Check IAM permissions for API Gateway invoke

```json
{
  "Effect": "Allow",
  "Action": "execute-api:Invoke",
  "Resource": "arn:aws:execute-api:us-east-1:*:hl98rmqgd6/prod/*"
}
```

### Connection Timeout

**Solution**: Check VPN/network access to AWS region

## Development

### Run Tests

```bash
pytest tests/test_memory_client.py
```

### Debug Requests

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Boto3 will now log SigV4 signing details
client = create_client()
```

## Architecture

```
┌─────────────┐
│   Client    │ (this library)
└──────┬──────┘
       │ HTTPS (SigV4 signed)
       ↓
┌─────────────┐
│ API Gateway │ https://hl98rmqgd6.execute-api...
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Lambda    │ sherpa-memory-kb
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  DynamoDB   │ sherpa-memory-store
└─────────────┘
```

## License

MIT
