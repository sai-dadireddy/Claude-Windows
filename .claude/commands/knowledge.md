---
description: Knowledge management & RAG (query|search|status|index|add|export)
argument-hint: <action> <query> [--tech technology]
allowed-tools: Bash, Read, Write, Grep
model: haiku
---

# Knowledge Management

Action: $ARGUMENTS

## Available Actions:

### query <question> [--tech technology]
Query RAG system for documentation
- 12+ collections available
- 15,828+ chunks indexed
- 97% token savings vs reading full docs
- Auto-selects relevant collections
- Returns top 5 relevant snippets with citations
- tech: nextjs|react|aws|tailwind|zustand|etc.

### search <term> [--limit 5]
Semantic search across codebase and docs
- Vector similarity search (using langchain MCP)
- Full-text + semantic hybrid search
- limit: number of results (default: 5)
- Returns similarity scores (0-1)
- Faster than /query for broad searches

### status
Show RAG system status
- Available collections (count)
- Index statistics (chunks, tokens, date)
- Memory usage (MB)
- Last indexed (timestamp)
- Collection health report

### index [collection]
Index new collection or re-index existing
- collection: name or path (default: auto-detect)
- Creates embeddings
- Builds vector index
- Time: 1-10 minutes per collection
- Auto-scheduled weekly

### add <path> [--collection name]
Add new documents to knowledge base
- path: file or directory
- Auto-detects file type (markdown, code, pdf)
- collection: optional target collection
- Processes and indexes documents
- Time: <1 minute per file

### export <format> [--collection name]
Export knowledge base
- format: json|csv|markdown|html
- collection: export specific or all
- Includes metadata and embeddings
- Saved to .claude/context/knowledge-export.{format}

### list [--verbose]
List all available collections
- Shows name, size, chunk count
- --verbose: detailed statistics
- Shows sync status
- Recommendations for most relevant

### memory-status
Show current memory/session knowledge state
- Context files loaded
- Session-specific knowledge
- Available in this session
- Recommended to load

### memory-query <question>
Query loaded session memory
- Searches current context only
- Faster than RAG (no index lookup)
- Good for session-specific info

## Usage Examples:
```
/knowledge query "how to use useState" --tech react
/knowledge search authentication patterns --limit 10
/knowledge status
/knowledge index nextjs
/knowledge add docs/guides/
/knowledge export json --collection react
/knowledge list --verbose
/knowledge memory-status
/knowledge memory-query "current project structure"
```

## RAG Collections (12+):
**Frontend**: nextjs, react, shadcn, tailwind, zustand
**Backend**: express, django, fastapi, agupgrade-backend
**Cloud**: aws-cognito, aws-ecs-fargate, aws-api-gateway
**Testing**: playwright, cypress
**Performance**: web-performance, lighthouse
**Custom**: Add your own with /knowledge add

## Key Features:
- Semantic understanding (not just keywords)
- Multi-collection search
- Automatic collection detection
- Citation & source tracking
- Embedding caching
- Offline-capable (after indexing)

## Performance:
- Query: <500ms (vs 2-5s reading docs)
- Token savings: 97% (50 tokens vs 1500-2000)
- Index time: 1-10 min per collection
- Memory per collection: 5-50MB

## Integration:
- RAG index in .claude/context/rag-collections/
- Query results cached for 1 hour
- Metrics tracked in token-tracker.json
- Syncs with /optimize tokens

## Smart Recommendations:
- File >10KB? → Use /knowledge instead of Read
- Multiple docs? → Use /knowledge query
- Current session only? → Use memory-query
