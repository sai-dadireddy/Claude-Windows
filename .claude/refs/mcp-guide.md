# MCP Router Guide - Lazy Loading Architecture

## Architecture Overview

```
  Claude Context (~2.4k tokens)           Backend MCPs (loaded on-demand)
  ┌─────────────────────────────┐         ┌────────────────────────────┐
  │  router_analyze_intent      │ ──────▶ │  context7 (docs)           │
  │  router_list_categories     │         │  github (repos, PRs)       │
  │  router_load_toolset        │         │  memory (knowledge graph)  │
  │  router_execute             │         │  multi (58 AI models)      │
  └─────────────────────────────┘         │  playwright (browser)      │
                                          │  code-index (search)       │
                                          │  sequential-thinking       │
                                          └────────────────────────────┘
```

**Benefit:** 60k token savings (31% → 1.2% of context)

## Router Tools

### 1. router_analyze_intent
Analyze a query to find the right MCP backend.

```python
mcp__router__router_analyze_intent(query="fetch react docs")
# Returns: {suggestion: "context7", tools: [...], matched: ["library", "docs"]}
```

### 2. router_list_categories
List all available MCP backends.

```python
mcp__router__router_list_categories()
# Returns: List of backends with descriptions and tools
```

### 3. router_load_toolset
Get detailed tool info for a specific MCP.

```python
mcp__router__router_load_toolset(mcp_name="github")
# Returns: {name, description, tools: [...], triggers: [...]}
```

### 4. router_execute
Execute a tool on a backend MCP.

```python
mcp__router__router_execute(
  mcp_name="context7",
  tool_name="get-library-docs",
  arguments={"context7CompatibleLibraryID": "/vercel/next.js", "topic": "hooks"}
)
```

## Available Backends

| Backend | Description | Key Tools | Triggers |
|---------|-------------|-----------|----------|
| `context7` | Library documentation | resolve-library-id, get-library-docs | library, docs, api |
| `github` | GitHub operations | create_pull_request, create_issue, push_files | pr, issue, repo |
| `memory` | Knowledge graph | create_entities, create_relations, search_nodes | entity, relationship |
| `multi` | 58 AI models | chat, compare, debate, codereview | gemini, gpt, glm |
| `playwright` | Browser automation | navigate, screenshot, click, fill | browser, screenshot |
| `code-index` | Code search | search_code_advanced, find_files | index, code search |
| `sequential-thinking` | Reasoning | sequentialthinking | step by step, analyze |

## Usage Patterns

### Get Library Docs (Context7)
```python
# 1. Get library ID
router_execute(mcp_name="context7", tool_name="resolve-library-id",
               arguments={"libraryName": "react"})

# 2. Fetch docs
router_execute(mcp_name="context7", tool_name="get-library-docs",
               arguments={"context7CompatibleLibraryID": "/facebook/react", "topic": "hooks"})
```

### Create GitHub Issue
```python
router_execute(mcp_name="github", tool_name="create_issue",
               arguments={"owner": "org", "repo": "repo", "title": "Bug", "body": "..."})
```

### Multi-Model Query
```python
# Chat with specific model
router_execute(mcp_name="multi", tool_name="chat",
               arguments={"model": "gemini-2.5-flash", "content": "..."})

# Compare models
router_execute(mcp_name="multi", tool_name="compare",
               arguments={"models": ["gpt-4o", "gemini-flash"], "content": "..."})

# Code review
router_execute(mcp_name="multi", tool_name="codereview",
               arguments={"content": "...", "base_path": "/path"})
```

### Browser Automation (Playwright)
```python
router_execute(mcp_name="playwright", tool_name="playwright_navigate",
               arguments={"url": "https://example.com"})

router_execute(mcp_name="playwright", tool_name="playwright_screenshot",
               arguments={"name": "page"})
```

## Model Routing via Multi

| Task | Model | Arguments |
|------|-------|-----------|
| Large context (1M) | gemini-2.5-flash | `{"model": "gemini-2.5-flash"}` |
| Multilingual/Chinese | glm-4.7 | `{"model": "glm-4.7"}` |
| Reasoning/Math | deepseek-r1 | `{"model": "deepseek-r1"}` |
| Code generation | qwen3-coder | `{"model": "qwen3-coder"}` |
| Vision/Images | pixtral-large | `{"model": "pixtral-large"}` |
| FREE models | deepseek-v3.2, kimi-k2 | `{"model": "deepseek-v3.2"}` |

## MCP Memory vs Semantic Memory

| Use Case | System |
|----------|--------|
| Entity relationships | MCP Memory (via router) |
| Decisions/preferences | Semantic Memory (`memory_manager.py`) |
| Knowledge graph | MCP Memory (via router) |
| Session state | Semantic Memory |

## Fallback: Direct CLI

If router fails, use CLI tools directly:

```bash
# GitHub
gh pr create --title "..." --body "..."
gh issue create --title "..."

# Beads (task tracking)
bd create "task" -t feature
bd ready
```
