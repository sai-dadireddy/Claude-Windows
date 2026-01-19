# Agent Loader Client

A Python client for the sherpa-agent-loader Lambda that provides lazy loading of agent prompts from S3.

## Overview

This client calls the `sherpa-agent-loader` Lambda function to:
- List available agents (manifest)
- Load full agent prompts from S3
- Search agents by keyword

Agent prompts are stored in the S3 bucket: `sherpa-agent-prompts-458798750195`

## Installation

```bash
pip install -r requirements.txt
```

## Prerequisites

- AWS credentials configured with profile `sherpa`
- Access to the `sherpa-agent-loader` Lambda function
- Region: `us-east-1`

## Usage

### Basic Usage

```python
from services.agent_loader import AgentLoaderClient

# Create client (uses default profile 'sherpa')
client = AgentLoaderClient()

# List all available agents
agents = client.list_agents()
for agent in agents:
    print(f"{agent['id']}: {agent['description']}")

# Load a specific agent
agent = client.get_agent("lead-architect")
print(agent['prompt'])

# Search agents by keyword
results = client.search_agents("security")
```

### Convenience Functions

```python
# Get just the prompt text
prompt = client.get_agent_prompt("qa-engineer")

# Use singleton client
from services.agent_loader.client import get_client
client = get_client()
```

### Custom Configuration

```python
client = AgentLoaderClient(
    profile="custom-profile",
    region="us-west-2",
    function_url="https://custom-url.lambda-url.us-west-2.on.aws"
)
```

## API Reference

### `AgentLoaderClient`

#### `__init__(profile, region, function_url)`

Initialize the client.

- `profile` (str): AWS profile name. Default: `sherpa`
- `region` (str): AWS region. Default: `us-east-1`
- `function_url` (str): Lambda function URL override

#### `list_agents() -> List[Dict]`

Get manifest of available agents.

Returns list of agent metadata:
```python
[
    {
        "id": "lead-architect",
        "name": "Lead Architect",
        "description": "AWS, security, infrastructure expert",
        "tags": ["aws", "security", "infrastructure"]
    },
    ...
]
```

#### `get_agent(agent_id: str) -> Dict`

Load full agent data including prompt.

Returns:
```python
{
    "id": "lead-architect",
    "name": "Lead Architect",
    "prompt": "You are a lead architect...",
    "metadata": {...}
}
```

Raises `AgentNotFoundError` if agent does not exist.

#### `search_agents(query: str) -> List[Dict]`

Search agents by keyword in name, description, or tags.

#### `get_agent_prompt(agent_id: str) -> str`

Convenience method to get just the prompt text.

## Error Handling

```python
from services.agent_loader.client import (
    AgentLoaderClient,
    AgentLoaderError,
    AgentNotFoundError
)

client = AgentLoaderClient()

try:
    agent = client.get_agent("nonexistent")
except AgentNotFoundError:
    print("Agent not found")
except AgentLoaderError as e:
    print(f"Lambda error: {e}")
```

## Available Agents (Sherpa 6)

| Agent ID | Role | Use For |
|----------|------|---------|
| `lead-architect` | Adult | AWS, security, infrastructure |
| `fullstack-dev` | Builder | React/Node features |
| `frontend-ux` | Artist | Tailwind, Shadcn, responsive |
| `product-lead` | Boss | Specs, user stories, planning |
| `qa-engineer` | Tester | Jest/Playwright, edge cases |
| `scribe` | Historian | Documentation, READMEs |

## Architecture

```
Client (SigV4) --> Lambda --> S3 Bucket
                              sherpa-agent-prompts-458798750195/
                                agents/
                                  lead-architect.json
                                  fullstack-dev.json
                                  ...
                                manifest.json
```

## License

Internal use only - ERPA Systems.
