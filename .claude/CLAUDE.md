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

## VERIFICATION GATES

Before claiming "done":
- [ ] Code compiles, linting passes
- [ ] Tests run and pass (show output)
- [ ] Feature works as specified
- [ ] Evidence provided to user

**Never batch-complete todos.** Mark complete ONLY when fully verified.

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
| `context7` | library, docs, api | resolve-library-id, get-library-docs |
| `github` | pr, issue, repo | create_pull_request, create_issue |
| `memory` | entity, relationship | create_entities, search_nodes |
| `sequential-thinking` | reasoning, analyze | sequentialthinking |
| `multi` | compare models, review | chat, compare, codereview |
| `playwright` | browser, screenshot | playwright_navigate, playwright_click |
| `code-index` | index, code search | search_code_advanced, find_files |

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

> **NOTE:** Task spawning requires restart with fixed env var. MCP multi-model works now.

### The Sherpa 6
| Agent | Role | Use For |
|-------|------|---------|
| `@lead-architect` | Adult | AWS, security, infrastructure |
| `@fullstack-dev` | Builder | React/Node features |
| `@frontend-ux` | Artist | Tailwind, Shadcn, responsive |
| `@product-lead` | Boss | Specs, user stories, planning |
| `@qa-engineer` | Tester | Jest/Playwright, edge cases |
| `@scribe` | Historian | Documentation, READMEs |

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

## CONTEXT HYGIENE

- Extract answers to Memory, then ignore raw content
- Run `/compact-context` when context > 50k tokens
- Use `workmux merge` to cleanup finished worktrees

---

## HOOKS ACTIVE

- **PreToolUse**: Security, auto-permissions
- **PostToolUse**: Audit, Error-Correction RAG
- **UserPromptSubmit**: Intent detection, Auto-RAG
- **SessionStart**: Memory injection

---

## FILE RULES

**Allowed new .md:** CLAUDE.md, README.md, CHANGELOG.md, LICENSE.md, CONTRIBUTING.md
**Blocked:** All other new .md files

