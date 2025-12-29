# MCP Servers Guide - When, Why, and How

## Architecture: Lazy Router Pattern

```
┌────────────────────────────────────────────────────────────────┐
│  Claude Context (Always Loaded)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  mcp-router (4 tools, ~2.4k tokens)                      │  │
│  │    • router_analyze_intent                               │  │
│  │    • router_list_categories                              │  │
│  │    • router_load_toolset                                 │  │
│  │    • router_execute                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼ (on-demand)
┌────────────────────────────────────────────────────────────────┐
│  Backend MCP Servers (NOT in context - called via router)      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ context7 │ │  github  │ │  memory  │ │sequential-think  │  │
│  │  (docs)  │ │  (repo)  │ │ (graph)  │ │   (reasoning)    │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │playwright│ │   aws    │ │ database │ │      time        │  │
│  │(browser) │ │ (cloud)  │ │  (sql)   │ │   (timezone)     │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

**Why Lazy Router?**
- Direct MCPs: Each loads ALL its tools into context (15-30k tokens total)
- Lazy Router: Only 2.4k tokens always loaded, tools called on-demand
- **Savings: 85-90% token reduction**

---

## MCP Server Reference

### 1. context7 (Library Documentation)

**Package:** `@upstash/context7-mcp`

**WHEN to use:**
- Looking up library API (React, Vue, Next.js, FastAPI, etc.)
- Checking current syntax (your training data may be outdated!)
- "How do I use X?" questions about any library
- Before writing code that uses a library API

**HOW to use:**
```
1. router_load_toolset category="docs"
2. resolve-library-id libraryName="react"
3. get-library-docs context7CompatibleLibraryID="..." topic="hooks"
```

**WHY use it:**
- Claude's training data has a cutoff date
- APIs change (React 19, Next.js 15, etc.)
- Get CURRENT documentation, not stale knowledge

**Trigger keywords:** "docs", "documentation", "api", "library", "react", "vue", "how to use", "current version"

---

### 2. github (Repository Operations)

**Package:** `@modelcontextprotocol/server-github`

**WHEN to use:**
- Creating/viewing pull requests
- Managing issues
- Checking commit history
- Repository operations

**HOW to use:**
```
1. router_load_toolset category="git"
2. router_execute category="git" server="github" tool="create_pull_request" args={...}
```

**WHY use it:**
- Programmatic GitHub access
- Faster than CLI for complex operations
- Integrated with Claude workflow

**Trigger keywords:** "pr", "pull request", "issue", "commit", "branch", "repo", "github"

---

### 3. memory (Entity Knowledge Graph)

**Package:** `@modelcontextprotocol/server-memory`

**WHEN to use:**
- Storing entity relationships (not decisions/preferences - use semantic memory for those)
- Building knowledge graphs
- "UserService depends on AuthService"
- Tracking component relationships

**HOW to use:**
```
1. router_load_toolset category="memory"
2. router_execute category="memory" tool="create_entity" args={"name": "UserService", "type": "service"}
3. router_execute category="memory" tool="create_relation" args={"from": "UserService", "to": "AuthService", "type": "depends_on"}
```

**WHY use it:**
- Track complex system relationships
- Persist knowledge beyond session
- Different from semantic memory (which is for decisions/preferences)

**Trigger keywords:** "remember entity", "relationship", "knowledge graph", "depends on"

---

### 4. sequential-thinking (Multi-Step Reasoning)

**Package:** `@modelcontextprotocol/server-sequential-thinking`

**WHEN to use:**
- Complex problems requiring step-by-step breakdown
- Debugging hard issues
- Architecture decisions
- Math/logic problems

**HOW to use:**
```
1. router_load_toolset category="thinking"
2. router_execute category="thinking" tool="sequential_think" args={"problem": "..."}
```

**WHY use it:**
- Forces structured thinking
- Prevents jumping to conclusions
- Documents reasoning chain

**Trigger keywords:** "step by step", "reason through", "analyze carefully", "break down", "think through"

---

### 5. playwright (Browser Automation)

**Package:** `@anthropic/mcp-server-playwright` or `@anthropic/mcp-server-puppeteer`

**WHEN to use:**
- Taking screenshots
- Scraping web pages
- Testing UI
- Automating browser actions

**HOW to use:**
```
1. router_load_toolset category="web"
2. router_execute category="web" tool="browser_navigate" args={"url": "..."}
3. router_execute category="web" tool="browser_snapshot" args={}
```

**WHY use it:**
- Visual verification
- Web scraping
- E2E testing
- Debug UI issues

**Trigger keywords:** "browser", "screenshot", "scrape", "web page", "click", "navigate to"

---

### 6. aws (Cloud Operations)

**Package:** `@aws/mcp-server-aws` (hypothetical) or custom

**WHEN to use:**
- AWS service operations
- Lambda deployments
- S3 operations
- Infrastructure management

**Trigger keywords:** "aws", "lambda", "s3", "ec2", "cloudformation"

---

### 7. database (SQL Operations)

**Package:** Custom PostgreSQL MCP

**WHEN to use:**
- Running SQL queries
- Database schema exploration
- Data analysis

**Trigger keywords:** "query", "sql", "database", "table", "select"

---

## Semantic Memory vs MCP Memory

| Aspect | Semantic Memory | MCP Memory |
|--------|----------------|------------|
| **Store** | SQLite + embeddings | Knowledge graph |
| **Use for** | Decisions, preferences, learnings | Entity relationships |
| **Query** | Semantic search | Graph traversal |
| **Example** | "User prefers TypeScript" | "UserService → AuthService" |
| **Command** | `memory_manager.py save-memory` | `mcp memory create_entity` |

---

## Router Commands Quick Reference

```bash
# List all categories
router_list_categories

# Analyze what MCP to use
router_analyze_intent query="How do I use React hooks?"

# Load a toolset (for reference only)
router_load_toolset category="docs"

# Execute a tool
router_execute category="docs" server="context7" tool="get-library-docs" args={...}
```

---

## Intent Detection Flow

```
User prompt: "How do I use React 19 hooks?"
                    │
                    ▼
┌──────────────────────────────────────┐
│  intent_detector.py hook             │
│  Detects: "react", "how to use"      │
│  Output: [mcp] Consider using        │
│          context7 (library docs)     │
└──────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│  Claude sees hint in context         │
│  Uses router to query context7       │
│  Gets current React 19 docs          │
└──────────────────────────────────────┘
                    │
                    ▼
        Accurate, up-to-date answer
```

---

## Troubleshooting

### MCP not responding
```bash
# Check if router is running
claude mcp list

# Test router directly
router_list_categories
```

### Wrong MCP being suggested
Edit `~/.claude/hooks/intent_detector.py` and adjust keywords in `MCP_ROUTING` dict.

### Too many tokens still
Ensure you're using the lazy router pattern, not direct MCP registration.
