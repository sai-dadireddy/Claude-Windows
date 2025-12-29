---
description: MCP server status, management, and quick reference
---

# MCP Server Management & Status

Show the status of all configured MCP servers and provide quick management commands.

## Current MCP Servers (10 Total)

### 1. **playwright** 🎭
- **Purpose**: Web browser automation
- **Command**: `npx -y @executeautomation/playwright-mcp-server`
- **Tools**: browser_navigate, browser_snapshot, browser_click, browser_type, browser_take_screenshot
- **Use**: Browse URLs, web scraping, UI interaction

### 2. **memory-auto** 🧠
- **Purpose**: Automatic memory storage & retrieval
- **Command**: `python enhanced-server.py`
- **Tools**: auto_store_memory, search_global_memory, store_project_memory
- **Databases**: global.db, projects-index.db
- **Use**: Cross-session context, user preferences

### 3. **langchain** 🔍
- **Purpose**: Vector search with semantic embeddings
- **Command**: `python langchain-server/server.py`
- **Tech**: HuggingFace + Chroma
- **Tools**: semantic_search, add_to_vector_store
- **Use**: Semantic code discovery, document search

### 4. **ai-workflows** (Llama) 🦙
- **Purpose**: Local AI delegation (qwen2.5-coder:7b)
- **Command**: `python ai-workflows/mcp-server/server.py`
- **Tools**: delegate_to_llama, generate_with_llama
- **Benefits**: FREE, FAST, local execution
- **Use**: Test generation, boilerplate, simple code

### 5. **code-indexing** 📇
- **Purpose**: Custom code indexing
- **Command**: `python code-indexing/mcp-server/server.py`
- **Use**: Project-specific code search

### 6. **testing** 🧪
- **Purpose**: Test automation & generation
- **Command**: `python testing-mcp/server.py`
- **Tools**: run_tests, analyze_failures, suggest_tests
- **Use**: Auto-generate tests, coverage analysis

### 7. **code-index-mcp** 🗂️
- **Purpose**: Industry-standard code search
- **Command**: `uvx code-index-mcp`
- **Languages**: 50+
- **Performance**: Sub-100ms queries
- **Use**: Fast file discovery, multi-language support

### 8. **sequential-thinking** 🤔
- **Purpose**: Extended reasoning for complex problems
- **Command**: `run-sequential-thinking.bat`
- **Performance**: +54% on complex tasks
- **Use**: Architecture decisions, complex debugging

### 9. **github** 🐙
- **Purpose**: GitHub API integration
- **Command**: `run-github.bat`
- **Tools**: create_pr, list_issues, search_code
- **Use**: PR/issue operations, repo analysis

### 10. **aws** ☁️
- **Purpose**: AWS operations
- **Command**: `python aws-server/server.py`
- **Profile**: agdemo
- **Region**: us-east-2
- **Use**: Resource management, cloud operations

---

## Quick Commands

### Check MCP Status
```bash
claude mcp list
```

### Get MCP Details
```bash
claude mcp get <name>
```

### Add New MCP
```bash
claude mcp add <name> <command> -- <args>
```

### Remove MCP
```bash
claude mcp remove <name>
```

---

## MCP Selection Guide

### For Web Browsing:
→ **playwright** - Any URL, screenshots, interaction

### For Memory/Context:
→ **memory-auto** - Store/recall across sessions

### For Code Search:
→ **langchain** - Semantic search (finds similar code)
→ **code-index-mcp** - Fast file discovery

### For Free AI:
→ **ai-workflows** (Llama) - Simple tasks, test gen, boilerplate

### For Complex Problems:
→ **sequential-thinking** - Architecture, debugging, analysis

### For Testing:
→ **testing** - Auto-generate tests, run tests, analyze failures

### For GitHub:
→ **github** - PRs, issues, repo operations

### For AWS:
→ **aws** - Cloud resource management

---

## Automatic MCP Usage

All MCPs are configured to be used **automatically** when appropriate:

- **URL shared** → playwright activates
- **Important info** → memory-auto stores
- **Code search needed** → langchain/code-index-mcp activate
- **Simple code task** → Llama delegates
- **Complex problem** → sequential-thinking activates
- **GitHub URL** → github MCP activates

You don't need to ask - I just use the right tool automatically!

---

## Troubleshooting

### MCP Not Connecting?
```bash
# Check specific MCP
claude mcp get <name>

# Remove and re-add
claude mcp remove <name>
claude mcp add <name> <command> -- <args>
```

### Slow Response?
- MCPs initialize on first use (may take a few seconds)
- Subsequent calls are faster
- Health checks can timeout (normal)

### Want to Reset?
```bash
# Remove all MCPs
claude mcp list | grep ":" | cut -d: -f1 | xargs -I {} claude mcp remove {}
```

---

## Performance Metrics

With all MCPs active:

| Operation | Improvement |
|-----------|-------------|
| Code search | 90% faster |
| Memory recall | 100x faster |
| Simple code gen | FREE (Llama) |
| Complex problems | +54% quality |
| Web browsing | NEW capability |

---

**Status**: ✅ All 10 MCPs Configured
**Feature Parity**: 100% (Desktop = Code)
**Ready**: Just start using - automatic activation!
