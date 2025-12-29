# Claude Code Complete Setup Guide

A production-ready Claude Code configuration with:
- **Lazy MCP Router** (2.4k tokens vs 15-20k for direct MCPs)
- **27 Hooks** for automation, security, and intelligence
- **Multi-model routing** (GLM, Gemini, DeepSeek, Claude)
- **Memory system** (semantic + entity graph)
- **Intent detection** (auto-suggest MCPs and models)

## Quick Start

### Option 1: Automated Setup

**macOS/Linux:**
```bash
cd ~/.claude
git clone https://github.com/YOUR_REPO/claude-setup.git setup-temp
cp -r setup-temp/hooks setup-temp/scripts setup-temp/settings.json .
rm -rf setup-temp
```

**Windows (PowerShell):**
```powershell
cd $env:USERPROFILE\.claude
# Copy hooks, scripts, settings.json to this directory
```

### Option 2: Manual Setup

1. Copy `hooks/` to `~/.claude/hooks/`
2. Copy `scripts/` to `~/.claude/scripts/`
3. Copy `settings.json` to `~/.claude/settings.json`
4. Install MCP router (see below)

---

## What's Included

### Directory Structure

```
~/.claude/
├── settings.json          # Main configuration
├── CLAUDE.md              # Instructions for Claude
├── hooks/                 # 27 automation hooks
│   ├── session_start.py
│   ├── session_end.py
│   ├── user_prompt_submit.py
│   ├── pre_tool_use.py
│   ├── post_tool_use.py
│   ├── audit_logger.py
│   ├── auto_capture_memory.py
│   ├── memory_search.py
│   ├── skill_reminder.py
│   ├── decision_reminder.py
│   ├── beads_reminder.py
│   ├── parallel_agent_reminder.py
│   └── ... (see docs/HOOKS-GUIDE.md)
├── scripts/               # Utility scripts
│   ├── memory_manager.py
│   ├── semantic_memory.py
│   └── hint_writer.py
├── hints/                 # Dynamic hints (auto-generated)
│   └── current.txt
└── memory/                # Persistent memory
    ├── semantic.db
    ├── short-term/
    └── long-term/
```

---

## MCP Router Setup

The lazy router pattern keeps ALL MCP tools behind a single router, saving ~85% tokens.

### Install mcp-router

```bash
# Option 1: npm global
npm install -g mcp-router

# Option 2: Run via npx
npx mcp-router

# Option 3: Custom server (see mcp-router repo)
```

### Configure in settings.json

The provided `settings.json` expects `mcp-router` with these backends:
- context7 (library docs)
- github (repo operations)
- memory (knowledge graph)
- sequential-thinking (reasoning)
- playwright (browser)
- aws (cloud)
- database (SQL)

### Router Usage

```
# List available MCP categories
router_list_categories

# Get suggestion for what MCP to use
router_analyze_intent query="How do I use React hooks?"

# Execute a tool
router_execute category="docs" server="context7" tool="get-library-docs" args={...}
```

---

## Hooks Reference

| Hook | Type | Purpose |
|------|------|---------|
| `session_start.py` | SessionStart | Load context, inject memories |
| `session_end.py` | SessionEnd | Save state, remind to commit |
| `user_prompt_submit.py` | UserPromptSubmit | Intent detection, complexity scoring |
| `pre_tool_use.py` | PreToolUse | Security checks, block dangerous ops |
| `post_tool_use.py` | PostToolUse | Logging, auto-formatting |
| `audit_logger.py` | PostToolUse | Comprehensive audit trail |
| `auto_capture_memory.py` | PostToolUse | Auto-save observations |
| `memory_search.py` | UserPromptSubmit | Search memories on "what did we..." |
| `skill_reminder.py` | UserPromptSubmit | Suggest skills for task type |
| `decision_reminder.py` | UserPromptSubmit | Catch decisions to save |
| `beads_reminder.py` | UserPromptSubmit | Suggest Beads for complex tasks |
| `parallel_agent_reminder.py` | UserPromptSubmit | Suggest parallel execution |

**Full documentation:** See `docs/HOOKS-GUIDE.md`

---

## Multi-Model Routing

| Task | Model | Trigger Keywords |
|------|-------|------------------|
| Normal coding | Claude Opus 4.5 | (default) |
| Multilingual/Chinese | GLM 4.7 | "chinese", "multilingual", "translate" |
| Large context (>200K) | Gemini 2.5 Flash | "large file", "huge context", ">100k" |
| Reasoning/Math | DeepSeek R1 | "math", "logic", "proof", "algorithm" |
| Compare models | Multi | "compare", "ask multiple models" |

The `user_prompt_submit.py` hook detects these keywords and suggests routing.

---

## Memory System

### Two Memory Systems

1. **Semantic Memory** (decisions, preferences, learnings)
   - SQLite with embeddings
   - Query by meaning
   - Use for: "User prefers TypeScript"

2. **MCP Memory** (entity relationships)
   - Knowledge graph
   - Query by traversal
   - Use for: "UserService → AuthService"

### Save to Memory

```bash
# Semantic memory (decisions, preferences)
~/.claude/scripts/memory_manager.py save-memory PROJECT decision "Chose PostgreSQL for ACID"
~/.claude/scripts/memory_manager.py save-memory global preference "User prefers explicit types"

# Search memory
~/.claude/scripts/memory_manager.py load-memories PROJECT "database choice"
```

### Auto-Capture

The `auto_capture_memory.py` hook automatically captures:
- New files created (with purpose)
- Package installations
- Git commits
- Errors encountered

---

## Permissions

The `settings.json` includes safe auto-approve rules:

**Auto-approved:**
- `mcp__mcp-router__*` - All router operations
- `Bash(git:*)` - All git commands
- `Bash(npm:*)`, `Bash(pip:*)` - Package managers
- `WebSearch` - Web searches
- `WebFetch(domain:github.com)` - GitHub fetches

**Blocked:**
- `rm -rf /` - Dangerous deletions
- Credential files (*.env, *.key, *.pem)
- SSH/AWS credentials

---

## Customization

### Add New MCP Keywords

Edit `hooks/user_prompt_submit.py`:
```python
MCP_KEYWORDS = {
    "your-mcp": ["keyword1", "keyword2"],
    ...
}
```

### Add New Hook

1. Create `hooks/my_hook.py`
2. Add to `settings.json`:
```json
"UserPromptSubmit": [
  {
    "hooks": [
      {"type": "command", "command": "~/.claude/hooks/my_hook.py"}
    ]
  }
]
```

### Disable a Hook

Remove it from `settings.json` or set `"timeout": 0`.

---

## Troubleshooting

### Hooks not running
```bash
# Test hook manually
echo '{"message":"test"}' | python ~/.claude/hooks/user_prompt_submit.py
```

### MCP router not responding
```bash
# Check if router is registered
claude mcp list

# Check router process
ps aux | grep mcp-router
```

### Memory not saving
```bash
# Check if memory directory exists
ls ~/.claude/memory/

# Test memory script
python ~/.claude/scripts/memory_manager.py save-memory test decision "test"
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `settings.json` | Main config (hooks, permissions, plugins) |
| `CLAUDE.md` | Instructions Claude reads each session |
| `docs/MCP-GUIDE.md` | When/why/how for each MCP |
| `docs/HOOKS-GUIDE.md` | All 27 hooks explained |

---

## Token Budget

| Component | Tokens | Notes |
|-----------|--------|-------|
| System prompt | ~8k | Claude Code base |
| MCP Router | ~2.4k | Lazy loading |
| Custom agents | ~1k | After cleanup |
| CLAUDE.md | ~300 | Minimal mode |
| Hooks overhead | ~0 | Hooks run externally |
| **Total** | ~12k | 73% context free |

Compare to: Direct MCPs (15-20k) + bloated agents (5k) = 35k+ tokens
