# ADR-002: Hybrid Storage Strategy (Local + GitHub + AWS)

## Status

**Accepted** - January 2025

## Context

Sherpa requires persistent storage for multiple data types with different access patterns, durability requirements, and sensitivity levels:

| Data Type | Access Pattern | Sensitivity | Size |
|-----------|----------------|-------------|------|
| Session memories | Frequent read/write | Low | Small |
| Knowledge bases (Workday, Oracle) | Read-heavy | Medium | Large |
| User preferences | Read-heavy | Low | Tiny |
| Project context | Session-scoped | Low | Medium |
| Scraped documentation | Write-once, read-many | Low | Large |
| Authentication tokens | Secure access | High | Tiny |

Single-storage solutions had limitations:
- **Local only**: No cross-machine sync, no backup
- **Cloud only**: Latency for frequent ops, cost for large files
- **GitHub only**: Rate limits, not suitable for binary/large files

## Decision

Implement a three-tier hybrid storage strategy:

### Tier 1: Local Storage (Hot)
**Location**: `~/.claude/` and project `.claude/` directories

**Purpose**: Fast access, session-critical data

**Contents**:
- Memory index and recent memories
- Hint files (`hints/current.txt`)
- Session state
- Cached skill definitions
- Project-specific CLAUDE.md

**Sync**: Git-tracked where appropriate

### Tier 2: GitHub (Warm)
**Location**: Repository and Gists

**Purpose**: Version control, collaboration, backup

**Contents**:
- CLAUDE.md files (repo)
- Shared skill configurations
- Architecture documentation
- ADRs (this directory)
- Public knowledge base snapshots

**Sync**: Git push/pull on explicit save

### Tier 3: AWS (Cold/Secure)
**Location**: S3 + DynamoDB + Secrets Manager

**Purpose**: Large storage, secure credentials, durable backup

**Contents**:
- S3: Large knowledge bases, scraped docs, binary assets
- DynamoDB: Memory search index, usage analytics
- Secrets Manager: API keys, OAuth tokens
- API Gateway: Secure API access with SigV4

**Sync**: Background sync, on-demand fetch

## Architecture

```
+------------------+     +------------------+     +------------------+
|  Local (~/.claude)     |     GitHub Repo      |        AWS         |
+------------------+     +------------------+     +------------------+
| - memories/      |<--->| - CLAUDE.md      |     | S3:              |
| - hints/         |     | - docs/adr/      |     |  - workday_docs/ |
| - cache/         |     | - skills/        |     |  - oracle_docs/  |
| - sessions/      |     +------------------+     |                  |
+------------------+            ^                 | DynamoDB:        |
        |                       |                 |  - memory_index  |
        v                       |                 |                  |
+------------------+            |                 | Secrets Manager: |
| OneDrive Sync    |------------+                 |  - api_keys      |
| (workday_docs/)  |                              +------------------+
+------------------+                                       ^
                                                          |
                                                   +------+------+
                                                   | API Gateway |
                                                   | (SigV4 Auth)|
                                                   +-------------+
```

## Data Flow

### Memory Write
1. Memory created locally (`~/.claude/memories/`)
2. Index updated in local SQLite
3. Background sync to DynamoDB (if connected)
4. Critical memories pushed to GitHub gist (manual)

### Knowledge Base Query
1. Check local cache first
2. If miss, query DynamoDB index
3. Fetch content from S3 if needed
4. Cache locally for session

### Credential Access
1. Request via API Gateway (SigV4 authenticated)
2. Lambda retrieves from Secrets Manager
3. Short-lived token returned
4. Never stored locally in plaintext

## Consequences

### Positive

- **Performance**: Hot data always local, sub-ms access
- **Resilience**: Multiple redundant copies
- **Cost-effective**: Large files in cheap S3 storage
- **Security**: Sensitive data in AWS Secrets Manager
- **Offline capable**: Local tier works without internet
- **Scalable**: AWS tier handles growth

### Negative

- **Complexity**: Three systems to maintain
- **Sync conflicts**: Potential for divergence
- **AWS costs**: Storage and API calls (minimal)
- **Setup overhead**: Initial AWS configuration required

### Mitigations

- Clear ownership rules (local = authoritative for session)
- Conflict resolution: last-write-wins with backup
- AWS Free Tier covers most usage
- Terraform/CDK scripts for AWS setup

## Implementation Notes

### Local Paths
```
~/.claude/
  memories/           # Memory JSON files
  hints/current.txt   # Dynamic hints
  cache/              # Cached skills, agent defs

~/OneDrive - ERPA/Claude/
  workday_docs/       # Workday knowledge base
  oracle_docs/        # Oracle/PeopleSoft KB
```

### AWS Resources
```
S3: sherpa-knowledge-bases-{account-id}
DynamoDB: sherpa-memory-index
Secrets Manager: sherpa/api-keys/*
API Gateway: sherpa-api.execute-api.{region}.amazonaws.com
```

## References

- ADR-004: SigV4 Authentication
- Knowledge base locations in CLAUDE.md
- Memory system: `~/.claude/scripts/memory_manager.py`
