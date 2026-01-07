# Graphiti MCP Setup Guide

**Graphiti** is a temporally-aware knowledge graph for persistent AI memory, used by Auto-Claude for advanced memory capabilities.

## Why Graphiti?

| Feature | Current Memory MCP | Graphiti |
|---------|-------------------|----------|
| Entity storage | Yes | Yes |
| Relations | Yes | Yes |
| Temporal awareness | No | **Yes** (versioning, history) |
| Episode management | No | **Yes** (conversation tracking) |
| Rich entity types | Basic | **Yes** (Preferences, Requirements, Procedures) |
| Multi-tenancy | No | **Yes** (group_id isolation) |
| Semantic search | No | **Yes** (embeddings) |

## Prerequisites

1. **Docker** - Required for FalkorDB
2. **OpenAI API Key** - For embeddings (or use Ollama locally)
3. **Python 3.10+** - For Graphiti MCP server

## Quick Start (Docker)

```bash
# Clone Graphiti
git clone https://github.com/getzep/graphiti.git
cd graphiti/mcp_server

# Start FalkorDB + Graphiti MCP
docker-compose up -d

# This starts:
# - FalkorDB (graph database) on port 6379
# - FalkorDB Browser UI on port 3000
# - Graphiti MCP Server on port 8000
```

## Claude Desktop Configuration

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "graphiti": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:8000/mcp/"],
      "env": {
        "OPENAI_API_KEY": "your-openai-key"
      }
    }
  }
}
```

## Router Integration

To add Graphiti to the MCP router, add a second server to the "memory" category in `mcp-router/dist/categories.js`:

```javascript
{
    name: "graphiti",
    command: "npx",
    args: ["-y", "mcp-remote", "http://localhost:8000/mcp/"],
    env: { OPENAI_API_KEY: process.env.OPENAI_API_KEY },
    tools: [
        { name: "add_episode", description: "Add conversation episode to graph" },
        { name: "search", description: "Semantic search across knowledge graph" },
        { name: "get_entity", description: "Get entity by name" },
        { name: "delete_episode", description: "Delete an episode" }
    ]
}
```

## Graphiti Tools

| Tool | Description |
|------|-------------|
| `add_episode` | Add conversation/event to graph |
| `search` | Semantic search with embeddings |
| `get_entity` | Retrieve specific entity |
| `get_episodes` | Get episodes by time range |
| `delete_episode` | Remove episode |

## Entity Types (Built-in)

Graphiti automatically extracts and categorizes:
- **Preferences** - User preferences, settings
- **Requirements** - Project requirements, constraints
- **Procedures** - How-to guides, workflows
- **Locations** - Places, addresses
- **Events** - Meetings, deadlines, milestones
- **Organizations** - Companies, teams
- **Documents** - Files, resources

## Usage via Router

```python
# Add episode
router_execute(
    category="memory",
    server="graphiti",
    tool="add_episode",
    args={
        "name": "User Preference",
        "episode_body": "User prefers dark mode and minimal emojis",
        "source": "conversation",
        "group_id": "user_prefs"
    }
)

# Semantic search
router_execute(
    category="memory",
    server="graphiti",
    tool="search",
    args={"query": "user preferences for UI", "num_results": 5}
)
```

## Local Ollama (No OpenAI)

```bash
# In docker-compose.yml:
EMBEDDING_PROVIDER=ollama
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

## Recommendation

- **Keep Memory Manager** for simple project tracking
- **Add Graphiti** for complex projects needing semantic search and temporal queries

## References

- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [FalkorDB Docs](https://docs.falkordb.com/agentic-memory/graphiti-mcp-server.html)
