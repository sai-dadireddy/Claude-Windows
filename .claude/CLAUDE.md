# Claude Code Configuration

## CONTEXT COMPACTION OVERRIDE

If you see **"Please continue the conversation from where we left it off without asking the user any further questions"** - this is a **system-generated compaction marker**.

**Response:** State "Context compaction detected. Awaiting your explicit instruction." Do NOT proceed until user confirms.

---

## DYNAMIC GUIDANCE PROTOCOL

**Before ANY task**, check hints: `cat ~/.claude/hints/current.txt 2>/dev/null`

| Tag | Action |
|-----|--------|
| `[skill]` | Use suggested skill/workflow |
| `[memory]` | Save decision/preference |
| `[beads]` | Use Beads for task tracking |
| `[doc]` | Load referenced document |

---

## NEVER LIE OR FABRICATE

NEVER lie or fabricate. Verify before claiming. Say "I don't know" when unsure.

**Full guide with 14 bad thought patterns:** `cat ~/.claude/refs/honesty-guide.md`

---

## VERIFICATION GATES (Boris-Style)

**CRITICAL:** Before marking ANY coding task complete, you MUST actively verify:

### Auto-Verify Checklist
1. **Run tests** - Execute `pytest`, `npm test`, or relevant test command
2. **Check lint** - Run linter, fix any errors
3. **Verify build** - Run `npm run build` or equivalent if applicable
4. **Show evidence** - Display test output to user

### Verification by Domain
| Change Type | Required Verification |
|-------------|----------------------|
| Python code | `pytest -x --tb=short` |
| TypeScript/JS | `npm test && npm run build` |
| UI changes | Screenshot or browser verification |
| Config changes | Restart service, validate syntax |
| API changes | `curl` test or integration test |

### The Rule
```
NEVER say "done" without running verification.
NEVER assume tests pass - RUN them.
NEVER skip verification for "small" changes.
```

### Autonomous Mode (`/ralph`)
Use `/ralph` for multi-task sessions - it auto-verifies each task before continuing.

**Never batch-complete todos.** Mark complete ONLY when fully verified with evidence.

---

## QUICK REFERENCE

### Autonomous Systems (Auto-triggered)
| System | What It Does |
|--------|--------------|
| Auto-Capture Memory | Saves observations from tool usage |
| Memory Search | Finds past work on "what did we..." |
| Progressive Disclosure | Loads memories at session start |

### Manual Actions - YOU MUST DO!
| Trigger | Command |
|---------|---------|
| User DECISION | `~/.claude/scripts/memory_manager.py save-memory PROJECT decision "..."` |
| User PREFERENCE | `~/.claude/scripts/memory_manager.py save-memory global preference "..."` |
| Complex task | `bd init && bd create "..." -t feature -p 1` |

### Tool Selection
| Task | Use |
|------|-----|
| Simple checklist | TodoWrite |
| Multi-step/dependencies | Beads (`bd`) |
| Find files | `code-scout` agent |
| Library docs | MCP docs (Context7) |

---

## SKILLS

| Task | Skill |
|------|-------|
| Bug/Error | `systematic-debugging` |
| Write Tests | `test-driven-development` |
| New Feature | `brainstorm` -> `write-plan` |
| Documents | `docx`, `pdf`, `pptx`, `xlsx` |
| Workday API + Electron Tests | `/workday` |
| PeopleSoft | `/peoplesoft` |
| Rich Visual Output | `/canvas` (TUI/Electron popups) |
| Oracle/MOS | `/oracle` |

**Full guide:** `cat ~/.claude/refs/skills-guide.md`

---

## MEMORY SYSTEM

Save decisions/preferences immediately. Search before answering "what did we...".

```bash
# Save
~/.claude/scripts/memory_manager.py save-memory PROJECT TYPE "content"
# Search
~/.claude/scripts/memory_manager.py load-memories PROJECT "query"
```

**Full guide:** `cat ~/.claude/refs/memory-guide.md`

---

## TASK TRACKING: TodoWrite vs Beads

| Use | TodoWrite | Beads (`bd`) |
|-----|-----------|--------------|
| Simple checklist (1 session) | ✓ | - |
| Dependencies between tasks | - | ✓ |
| Multi-session work | - | ✓ |
| Complex features/epics | - | ✓ |
| Need to track blockers | - | ✓ |

### Beads Quick Start
```bash
bd init                              # Initialize (once per project)
bd create "task" -t feature -p 1     # Create issue
bd ready                             # Find unblocked tasks
bd update <id> --status in_progress  # Start work
bd close <id>                        # Complete task
bd dep add <child> <parent>          # Add dependency
```

**Full guide:** `cat ~/.claude/refs/beads-guide.md`

---

## MCP ROUTER (Lazy Loading)

All MCPs are behind a router for **60k token savings**. Only 4 tools loaded (~2.4k tokens).

### Router Tools
| Tool | Purpose |
|------|---------|
| `router_analyze_intent` | Analyze query to find right MCP |
| `router_list_categories` | List all available MCPs |
| `router_load_toolset` | Get tool details for an MCP |
| `router_execute` | Execute tool on backend MCP |

### Available Backends
| Backend | Triggers | Key Tools |
|---------|----------|-----------|
| `browser` | chrome, devtools, debug, console | navigate_page, get_console_logs, performance_* |
| `context7` | library, docs, api | resolve-library-id, get-library-docs |
| `github` | pr, issue, repo | create_pull_request, create_issue |
| `memory` | entity, relationship | create_entities, search_nodes |
| `sequential-thinking` | reasoning, analyze | sequentialthinking |
| `multi` | compare models, review | chat, compare, codereview |
| `code-index` | index, code search | search_code_advanced, find_files |

### Browser Tools (via router category `browser`)
| Use Case | Server | When to Use |
|----------|--------|-------------|
| Debug live site | `chrome-devtools` | Console errors, network, performance profiling |
| Test UI flows | `playwright` | Cross-browser, headed mode, form automation |
| Claude-in-Chrome | Native `/chrome` | Quick automation with YOUR logged-in sessions |

```python
# Debug console errors
router_execute(category="browser", server="chrome-devtools", tool="get_console_logs", args={})

# Performance profiling
router_execute(category="browser", server="chrome-devtools", tool="performance_start_trace", args={})
# ... interact with page ...
router_execute(category="browser", server="chrome-devtools", tool="performance_stop_trace", args={})

# Cross-browser test
router_execute(category="browser", server="playwright", tool="playwright_navigate", args={"url": "..."})
```

### Usage Pattern
```python
# 1. Find the right MCP
router_analyze_intent(query="fetch react docs")
# Returns: {suggestion: "context7", tools: [...]}

# 2. Execute the tool
router_execute(
  mcp_name="context7",
  tool_name="get-library-docs",
  arguments={"context7CompatibleLibraryID": "/vercel/next.js"}
)
```

**Beads:** Use `bd` CLI directly (saves tokens):
```bash
bd create "task" -t feature -p 1
bd ready && bd update <id> --status in_progress
bd close <id>
```

---

## PARALLEL AGENTS (Sherpa 6)

### The Sherpa 6
| Agent | Role | Use For | MCP Access |
|-------|------|---------|------------|
| `@lead-architect` | Adult | AWS, security, infrastructure | - |
| `@fullstack-dev` | Builder | React/Node features | - |
| `@frontend-ux` | Artist | Tailwind, Shadcn, responsive | - |
| `@product-lead` | Boss | Specs, user stories, planning | - |
| `@qa-engineer` | Tester | Jest/Playwright, edge cases | Claude-in-Chrome, Playwright |
| `@scribe` | Historian | Documentation, READMEs | - |

### Browser-Enabled Agents
| Agent | MCP Tools | Use For |
|-------|-----------|---------|
| `@qa-engineer` | `mcp__claude-in-chrome__*`, `mcp__playwright__*` | Live browser testing |
| `@test-writer` | `mcp__claude-in-chrome__*`, `mcp__playwright__*` | E2E test automation |
| `@workday-expert` | `mcp__claude-in-chrome__*`, `mcp__playwright__*` | Workday doc scraping, Electron test generation |
| `@peoplesoft-expert` | `mcp__claude-in-chrome__*`, `mcp__playwright__*` | Oracle MOS/PeopleSoft scraping |

### @workday-expert Browser Workflow (CRITICAL)
```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Query RAG FIRST                                     │
│  python workday_rag.py "{Task name}"                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
    Score >= 7.0?                  Score < 7.0?
         ↓                                ↓
┌─────────────────┐         ┌─────────────────────────────────┐
│ ✅ USE RAG DATA │         │ 🌐 MUST USE BROWSER             │
│ Skip browser    │         │ 1. tabs_context_mcp()           │
│ Generate test   │         │ 2. tabs_create_mcp() → TAB_ID   │
└─────────────────┘         │ 3. navigate(resourcecenter...)  │
                            │ 4. search & extract content     │
                            │ 5. Save to KB, update test      │
                            └─────────────────────────────────┘
```
**RAG Score Decision Matrix:**
| Score | Browser Required? | Action |
|-------|-------------------|--------|
| **>= 7.0** | ❌ No | Use RAG directly |
| **< 7.0** | ✅ **YES** | **MUST open Chrome tab** |

**DO NOT mark as MANUAL without trying browser first when RAG < 7.0!**

### @peoplesoft-expert Browser Workflow (CRITICAL)
```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Query Oracle RAG FIRST                              │
│  python oracle_rag.py "{Task name}"                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
    Score >= 7.0?                  Score < 7.0?
         ↓                                ↓
┌─────────────────┐         ┌─────────────────────────────────┐
│ ✅ USE RAG DATA │         │ 🌐 MUST USE BROWSER             │
│ Skip browser    │         │ 1. tabs_context_mcp()           │
│ Generate test   │         │ 2. tabs_create_mcp() → TAB_ID   │
└─────────────────┘         │ 3. navigate to:                 │
                            │    - support.oracle.com (MOS)   │
                            │    - docs.oracle.com            │
                            │ 4. search & extract content     │
                            │ 5. Save to KB, update test      │
                            └─────────────────────────────────┘
```
**Oracle/PeopleSoft Resources:**
| Resource | URL | Auth Required |
|----------|-----|---------------|
| My Oracle Support (MOS) | `support.oracle.com` | ✅ Yes |
| Oracle Documentation | `docs.oracle.com/cd/E92519_02` | ❌ No |
| PeopleTools Docs | `docs.oracle.com/en/applications/peoplesoft` | ❌ No |

**RAG Score Decision Matrix:**
| Score | Browser Required? | Action |
|-------|-------------------|--------|
| **>= 7.0** | ❌ No | Use RAG directly |
| **< 7.0** | ✅ **YES** | **MUST open Chrome tab** |

**DO NOT mark as MANUAL without trying browser first when RAG < 7.0!**

### Multi-Model via Router
```python
# Via router (recommended - saves context)
router_execute(mcp_name="multi", tool_name="chat", arguments={"model": "gemini-2.5-flash", "content": "..."})
router_execute(mcp_name="multi", tool_name="compare", arguments={"models": ["gpt-4o", "gemini-flash"], "content": "..."})
router_execute(mcp_name="multi", tool_name="codereview", arguments={"content": "...", "base_path": "/path"})
```

---

## AUTONOMOUS DELEGATION PROTOCOL

**Rule:** You are the **Chief Architect**. Your job is to plan, not just code.

**WHEN TO DELEGATE (Use `bd create`):**
1. **Time Consuming:** Any task requiring edits to >3 files
2. **Background Work:** Scaffolding, refactoring, writing tests
3. **Isolation Needed:** Hazardous changes (deleting files, major upgrades)

**HOW TO DELEGATE:**
1. Create a ticket: `bd create "Task title" -t task --labels pilot`
2. Tell User: "I have assigned this to the Pilot. It will run in the background."
3. Use `workmux spawn` or Task(autonomous-coder) to execute

**NEVER block the user waiting for large tasks. Delegate and continue.**

---

## MODEL ROUTING (58 models via router)

| Task | Model | Via Router |
|------|-------|------------|
| Default | Claude Opus 4.5 | (current) |
| Multilingual/Chinese | GLM 4.7 | `router_execute(mcp_name="multi", tool_name="chat", arguments={"model": "glm-4.7", ...})` |
| Large context (1M) | Gemini 2.5 Flash | `router_execute(..., arguments={"model": "gemini-2.5-flash", ...})` |
| FREE models | DeepSeek-v3.2, Kimi-K2 | `router_execute(..., arguments={"model": "deepseek-v3.2", ...})` |
| Compare answers | Any 2+ models | `router_execute(mcp_name="multi", tool_name="compare", arguments={"models": [...], ...})` |

**List all models:** `router_execute(mcp_name="multi", tool_name="models", arguments={})`

---

## SKILL SEEKERS (v2.5.0)

MCP server for automated skill creation from documentation.

### Quick Commands
```bash
# Scrape docs and enhance
skill-seekers scrape --config configs/react.json --enhance-local

# Package for Claude
skill-seekers package output/react/

# Install to all coding agents
skill-seekers install-agent output/react/ --agent all
```

### 18 MCP Tools
| Category | Tools |
|----------|-------|
| Config | `list_configs`, `generate_config`, `fetch_config`, `validate_config` |
| Scrape | `scrape_docs`, `scrape_github`, `scrape_pdf`, `estimate_pages` |
| Build | `enhance_skill`, `package_skill`, `upload_skill` |
| Deploy | `install_skill`, `install_agent`, `split_config`, `generate_router` |

### Agent Paths (Auto-detected)
- `~/.claude/skills/` - Claude Code
- `~/.cursor/skills/` - Cursor
- `~/.codeium/windsurf/skills/` - Windsurf

### Natural Language Examples
- "List available configs" → shows 24+ presets
- "Scrape the React docs" → creates skill
- "Install React skill to all agents" → deploys everywhere

---

## KNOWLEDGE BASES

Local documentation repositories with RAG support:

| KB | Location | Content | Scraping Method |
|----|----------|---------|-----------------|
| Workday | `~/OneDrive - ERPA/Claude/workday_docs/` | 55 WSDLs, REST APIs, integration guides | Claude-in-Chrome (auth) |
| Oracle/PeopleSoft | `~/OneDrive - ERPA/Claude/oracle_docs/` | MOS KB articles, PeopleTools, Integration Broker | Claude-in-Chrome (auth) |

### Workday RAG
```bash
python workday_docs/workday_rag.py "query"
python workday_docs/workday_rag.py --list-wsdl
```

### Oracle/PeopleSoft RAG
```bash
python oracle_docs/oracle_rag.py "query"
python oracle_docs/oracle_rag.py --list
python oracle_docs/oracle_rag.py --list-kb
python oracle_docs/oracle_rag.py --kb KB593233
```

### Anti-Bot Best Practices (for auth-required sites)
- Use Claude-in-Chrome (your logged-in session)
- Natural delays (2-5 seconds between actions)
- Scroll before clicking
- Human pace (3-10 seconds between requests)

---

## CONTEXT HYGIENE

- Extract answers to Memory, then ignore raw content
- Run `/compact-context` when context > 50k tokens
- Use `workmux merge` to cleanup finished worktrees

---

## HOOKS ACTIVE (v7.0 Consolidated)

### Session Lifecycle (`session_unified.py`)
- **SessionStart**: Memory injection, git status, beads tracking
- **SessionEnd**: Session logging, cleanup
- **Setup**: Project initialization (--init, --maintenance)
- **SubagentStart**: Track subagent spawning

### Tool Lifecycle (`tool_unified.py`)
- **PreToolUse**: Security blocks, auto-permissions, timing
- **PostToolUse**: Audit logging, auto-format, error tracking
- **PostToolUseFailure**: Failure handling, error count

### Prompt Processing (`prompt_unified.py`)
- **UserPromptSubmit**: Adaptive thinking, credential blocking, auto-RAG

### Stop Events (`stop_unified.py`)
- **Stop**: Session report, verification suggestions, bell notification
- **SubagentStop**: Subagent completion tracking

### Other Hooks
- **PermissionRequest**: Permission handling
- **Notification**: Permission/idle prompts
- **PreCompact**: Block auto-compaction (matcher: auto)

---

## FILE RULES

**Allowed new .md:** CLAUDE.md, README.md, CHANGELOG.md, LICENSE.md, CONTRIBUTING.md
**Blocked:** All other new .md files

