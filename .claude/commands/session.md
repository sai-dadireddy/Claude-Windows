---
description: Universal session management (continue|save|resume|status|kill)
argument-hint: <action> [session-id]
allowed-tools: Read, Write, Bash, KillShell
---

# Session Management

Execute session action: $ARGUMENTS

## Available Actions:

### save
**Smooth Session Save** (~500 tokens, 15 seconds)

**Purpose:** Save session state for seamless continuation

**⚠️ CONTEXT WARNING:**
- Recommended at 600K tokens (60% of 1M)
- CRITICAL at 700K+ tokens (70%+)
- Quality degrades beyond 60%!

**Workflow:**

#### Step 1: Kill Background Processes (5 seconds)
```bash
!claude /bashes
KillShell for each process
Log killed process IDs
```

#### Step 2: Update PROJECT-TRACKER.md (3 seconds)
```bash
# Update ONLY if it exists, from conversation memory
Read PROJECT-TRACKER.md (if exists)
Update:
  - Current phase status
  - Last completed task → [x]
  - Current task status
Write back (minimal edit)
```

#### Step 3: Cache File Tree (2 seconds)
```bash
# Save current file structure for next session
Bash: dir /s /b > .claude/session-files.txt
# Next session can diff instead of full scan
```

#### Step 4: Save Session State (5 seconds)
```bash
Write ~/.claude/last-session.json:
{
  "saved": "[timestamp]",
  "model": "[sonnet-4-5|opus|haiku]",
  "context_limit": "[1M|200K]",
  "tokens": "[from system warnings]",
  "working_directory": "[CURRENT directory - from $PWD or cwd]",
  "project_name": "[extract from directory path]",
  "phase": "[current phase from conversation]",
  "next": "[1 sentence]",
  "done": ["[last 2 tasks]"],
  "blocker": "[if any]",
  "killed_processes": ["[IDs]"],
  "uncommitted_changes": "[from git status if available]",
  "lessons": ["[workflow tips collected this session]"],
  "project_context": {
    "active_files": ["[files being worked on]"],
    "has_dev_docs": "[check if dev/active/ exists]",
    "has_project_tracker": "[check if PROJECT-TRACKER.md exists]"
  }
}
```

#### Step 5: Recommendations
```bash
Git Status Check:
  - If uncommitted changes → "Run: git add . && git commit -m 'Session save'"
  - If commits not pushed → "Run: git push"
  - Otherwise → "✅ Git clean"

Token Status:
  - Model: [current]
  - Usage: [X]K/[1M|200K] ([%]%)
  - Next session: Will continue where you left off

Tips Collected:
  - "Use Bash tool, not PowerShell in bash context"
  - "Avoid emojis in PowerShell output"
  - "[any other lessons from this session]"
```

**Result:** 500 tokens, 15 seconds

Agent 2 (@code-reviewer): All project code files
  - Scan 17 projects
  - Archive: 23 old versions
  - Delete: 8 unused files

Agent 3 (@devops-troubleshooter): Config optimization
  - Consolidate duplicate configs
  - Update .claudeignore files
  - Clean old backups

Agent 4 (@ui-ux-designer): Media/asset cleanup
  - Compress large images
  - Delete unused screenshots
  - Archive old presentations

Agent 5 (@full-stack-developer): Archive management
  - Delete safe archives (>6 months old)
  - Compress important backups
  - Free up disk space

Agent 6 (@ai-engineer): RAG integration
  - Index 45 docs to RAG
  - Update search collections
  - Archive indexed originals
  - Update .claude/context/rag-collections.md

Time: 2 minutes (6 agents in parallel)
Cleaned: 187 files (89 MB)
Token savings: 340,000 tokens
```

#### Step 4: Update Tracking (30 seconds)
```bash
# Update all state files
1. Update ROADMAP.md with session progress
2. Update token-tracker.json with final metrics
3. Save session state to .claude/last-session.json
4. Generate optimization report
```

#### Step 5: Git Operations (2 minutes - 6 PARALLEL AGENTS)
```bash
# Parallel git commits across workspace + projects

Agent 1: Root workspace commit
  cd C:\Users\...\Claude
  git add .claude/ ROADMAP.md *.md
  git commit -m "Session save: Optimizations + cleanup (340K tokens saved)"

Agent 2: Critical projects (ERPAGPT, Strivacity, AGUPGRADE)
  For each project:
    cd project/
    git add .claudeignore ROADMAP.md .claude/
    git commit -m "Optimization: Token protection deployed"

Agent 3: Active projects (AARP, AWS-Chatbot, MCP, PeopleSoft)
  For each project:
    git add .claudeignore ROADMAP.md
    git commit -m "Session save: File cleanup + tracking"

Agent 4: Development projects (N8N, Playwright, AI-Workflows, etc.)
  For each project:
    git add optimizations
    git commit -m "Token optimization applied"

Agent 5: Research projects (Langchain, Memory, RAG, etc.)
  For each project:
    git add ROADMAP.md token-tracker.json
    git commit -m "Session tracking deployed"

Agent 6: Git push coordination
  - Waits for Agents 1-5 to complete
  - Pushes root workspace
  - Pushes all projects (in parallel)
  - Verifies all pushes successful

Time: 2 minutes (parallel commits + push)
Commits: 18 (root + 17 projects)
```

#### Step 6: Final Summary
```
Session Save Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Duration: 6 minutes total

Cleanup:
  ✅ Killed 2 unnecessary background processes
  ✅ Kept 2 active processes

File Optimization (6 agents):
  ✅ Analyzed 1,247 files
  ✅ RAG indexed: 45 docs
  ✅ Archived: 67 files
  ✅ Deleted: 187 files (89 MB freed)
  ✅ Token savings: 340,000 tokens (90%)

State Saved:
  ✅ ROADMAP.md updated
  ✅ Token tracker updated (final: 45K tokens)
  ✅ Session state saved

Git Operations (6 agents):
  ✅ Root workspace committed & pushed
  ✅ 17 projects committed & pushed
  ✅ All changes synchronized

Recommendations for Next Session:
  💡 Resume with: /session continue
  🚀 3 tasks ready for parallel agents:
     - Frontend tests (@test-automator)
     - Security scan (@security-auditor)
     - API docs (@docs-architect)
  ✅ Token usage: Excellent (4.5%)

Next: /session continue (loads in 550-1K tokens)
```

---

**Complete Automation**: One command does everything!
- Process cleanup ✓
- File optimization (6 agents) ✓
- Git commit + push (6 agents) ✓
- State persistence ✓
- Smart recommendations ✓

**Time**: 6 minutes automated (vs 45+ manual)
**Speedup**: 7-8x faster

---

### continue
**Seamless Session Resume** (~600 tokens, 12 seconds)

**Purpose:** Resume work feeling like you never left

**Workflow:**

#### Step 1: Load Session Context & Restore Project (5 seconds)
```bash
Read @~/.claude/last-session.json

Extract:
  - Model & context limit (1M/200K)
  - Tokens when saved
  - Working directory (CRITICAL!)
  - Project name
  - Current phase
  - Next action
  - Active files
  - Workflow lessons learned

RESTORE PROJECT CONTEXT:
  - Bash: cd "[saved working_directory]"
  - Show: "📂 Restored to: [project-name]"
  - Show: "📍 Directory: [working_directory]"
  - If project CLAUDE.md exists → Read it (project-specific context)
  - If dev/active/ exists → List active tasks
  - If PROJECT-TRACKER.md exists → Read current phase

Example Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Session Resumed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 Project: strivacity
📍 Directory: C:\Users\...\projects\strivacity
🕐 Saved: 2h ago

Project Context Loaded:
  ✅ Read CLAUDE.md (project-specific guidelines)
  ✅ Active task: oidc-implementation (in dev/active/)
  ✅ PROJECT-TRACKER.md: Phase 3 - Testing

Model: Sonnet 4.5 (1M) ← was Sonnet 4.5 (1M)
Context: 45K/1M (4.5%) 🟢

Next: Test OIDC redirect flow

You're back in the strivacity project exactly where you left off!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Step 2: Restore Environment Awareness (2 seconds)
```bash
# Use cached file tree (no expensive scanning!)
Read @.claude/session-files.txt (if exists)
  - Shows file structure from last session
  - Use for quick reference (no Glob needed)
  - If file changed, just Read it directly
```

#### Step 3: Smart Recommendations (7 seconds)
```bash
Model Context Analysis:
  - Saved model: [Opus/Sonnet/Haiku]
  - Current model: [check if switched]
  - Context change: "Was 180K/200K (90%) → Now 45K/1M (4.5%)"
  - Headroom: +955K tokens available!

Agent Recommendations:
  - Parse "next" action for keywords
  - "test" → @test-automator
  - "security" → @security-auditor
  - "performance/optimize" → @performance-engineer
  - "debug/error" → @debugger
  - "frontend/UI" → @frontend-developer
  - "backend/API" → @backend-architect

Parallel Work Detection:
  - Check PROJECT-TRACKER for multiple tasks
  - If 3+ tasks → "Run in parallel with Task tool"
  - Suggest agent per task

RAG First Reminder:
  - "RAG available: AWS, React, NextJS, TypeScript, etc."
  - "Use /knowledge query before reading docs"
  - "Saves ~5K tokens per doc query"

Git Recommendations:
  - If uncommitted: "git add . && git commit"
  - If unpushed: "git push"
  - Otherwise: "✅ Clean"

Workflow Lessons Applied:
  - Display lessons from last session
  - "Remember: Use Bash tool (not bash in PowerShell)"
  - "Remember: Avoid emojis in PowerShell scripts"
  - "Remember: Use absolute paths in Windows"
```

#### Step 4: Seamless Continuation
```
Session Resumed - Continuing from where you left off
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Saved: 2h ago | Phase: [current phase]
Model: Sonnet 4.5 (1M) ← was Opus (200K)
Context: 45K/1M (4.5%) 🟢 (+955K headroom!)

Next: [next action from last session]

Recommendations:
  🎯 Agent: @performance-engineer (matches your task)
  🚀 RAG: Use /knowledge query for docs
  💡 Parallel: 3 tasks ready (use Task tool)
  📂 Files: Cached tree available (.claude/session-files.txt)

Git:
  ⚠️ Uncommitted changes: Run git commit

Lessons from last session:
  • Use Bash tool for commands (not PowerShell in bash)
  • Avoid Unicode emojis in Windows scripts
  • File tree cached - no need to scan again

Ready to continue!
```

**Result:** 600 tokens, 12 seconds (seamless experience!)

---

### resume [session-id]
Resume specific session by ID

**Same token-optimized loading as continue**
- Reads session-specific state
- Restores background processes
- Shows what was in progress

---

### status
Show current session metrics and recommendations

**Displays**:
```
Session Status Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens: 45,000/1,000,000 (4.5%) 🟢 Healthy
Active Tasks: 2 in progress (see ROADMAP.md)
Background Processes: 3 running
Context Files Loaded: 3/12 (25%)
Session Duration: 2h 30m

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Token Optimization:
  ✅ Context healthy (<80%) - continue working
  💡 Consider using @rag-query skill vs reading docs
  💡 Use /knowledge query instead of loading full docs

Agent Optimization:
  💡 Current task "performance optimization" → Use @performance-engineer
  💡 Security review pending → Use @security-auditor

Parallel Work Available:
  🚀 3 independent tasks ready:
     - Frontend tests (Task tool + @test-automator)
     - API documentation (Task tool + @docs-architect)
     - Security scan (Task tool + @security-auditor)
  💡 Run in parallel: 3x faster completion

Background Processes:
  ✓ dev-server (2h 15m) - Healthy
  ✓ webpack-watch (2h 15m) - Healthy
  ⚠️ jest --watch (45m) - Check if still needed
```

---

### kill
**NEW**: Properly terminate session and cleanup

**Pre-requisites (Auto-executed)**:
```bash
# 1. List all background processes
!claude /bashes

# 2. Show what will be killed
echo "Background processes:"
- process-1 (ID: abc123)
- process-2 (ID: def456)
```

**What Gets Cleaned**:
1. Kill all background bash processes
2. Update ROADMAP.md (move [-] → [ ] for unfinished tasks)
3. Save final session state to .claude/last-session.json
4. Update token-tracker.json with final metrics
5. Archive session logs to .claude/sessions/archive/
6. Clear temporary session files

**Execution**:
```bash
# Kill each background process
KillShell(abc123)
KillShell(def456)
KillShell(xyz789)

# Update ROADMAP.md
[ ] Task 1 (was [-], returned to pending)
[x] Task 2 (completed)

# Save state
.claude/last-session.json:
{
  "killed_at": "2025-10-28T23:30:00Z",
  "tokens_used": 45000,
  "incomplete_tasks": ["Task 1"],
  "completed_tasks": ["Task 2"],
  "background_processes_killed": 3
}

# Update token tracker
{
  "session_end": "2025-10-28T23:30:00Z",
  "final_tokens": 45000,
  "session_duration": "2h 30m"
}
```

**Output**:
```
Session Kill Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Killed 3 background processes
✅ Updated ROADMAP.md (1 task returned to pending)
✅ Saved session state to .claude/last-session.json
✅ Updated token-tracker.json
✅ Session cleanly terminated

Summary:
  Tokens used: 45,000/1,000,000 (4.5%)
  Duration: 2h 30m
  Completed: 1 task
  Pending: 1 task (available for next session)

Next session will resume from clean state.
```

---

## Usage Examples

### Optimized Save Workflow
```bash
/session save

# Auto-executes:
# 1. Read token-tracker.json
# 2. Update ROADMAP.md progress
# 3. List background processes
# 4. Calculate metrics
# 5. Generate recommendations

Output:
Session saved successfully
Tokens: 45K/1M (4.5%) 🟢
Tasks: 2 active, 3 pending
Recommendations:
  💡 Use parallel agents for 3 pending tasks
  💡 Task "security review" → @security-auditor
```

### Optimized Continue Workflow
```bash
/session continue

# Auto-executes (token-optimized):
# 1. Read token-tracker.json (~50 tokens)
# 2. Read ROADMAP.md (~200 tokens)
# 3. Read last-session.json (~100 tokens)
# 4. Skip loading full epics (save 5,000+ tokens)
# 5. Show recommendations

Output:
Resuming session from 2h ago
Tokens: 45K → 46K (+1K optimized load)
Current task: "API optimization" (in progress)

Recommendations:
  🎯 Delegate to @performance-engineer (specialized)
  🚀 3 parallel tasks ready - use Task tool
  💡 Use /knowledge query vs reading AWS docs

Ready to continue!
```

### Kill Session Properly
```bash
/session kill

# Auto-executes cleanup:
# 1. List background processes (3 found)
# 2. Kill all processes
# 3. Update ROADMAP.md
# 4. Save final state
# 5. Update token tracker

Output:
Killed 3 background processes
Updated ROADMAP.md
Session cleanly terminated

Next session starts fresh (no orphaned processes)
```

---

## Smart Recommendations System

### Triggers for Recommendations

**Token Optimization**:
- If tokens > 80% → "Use /compact or start fresh session"
- If loading docs → "Use /knowledge query or @rag-query skill instead"
- If context > 500K → "Consider parallel agents to distribute work"

**Agent Suggestions**:
- Keyword "security" → "Use @security-auditor"
- Keyword "performance" → "Use @performance-engineer"
- Keyword "test" → "Use @test-automator"
- Complex architecture → "Use @backend-architect"

**Parallel Work Detection**:
- Multiple independent tasks in ROADMAP → "Use Task tool with parallel agents"
- Different domains (frontend/backend/test) → "Suggest specific agents per domain"
- >3 tasks pending → "Run 3-6 in parallel for 3x speedup"

**Context Optimization**:
- Many files read → "Move to .claude/context/ and load on demand"
- Repeated doc reads → "Add to RAG collection"
- Large files → "Use Grep instead of Read"

---

## Auto-Detection:
If no action specified, defaults to "continue" for backward compatibility.

## Session State Files

- `.claude/last-session.json` - Last session metadata
- `.claude/session-state.json` - Current session state
- `.claude/context/token-tracker.json` - Persistent token metrics
- `.claude/sessions/archive/` - Historical sessions
