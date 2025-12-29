# Hooks Guide - Complete Reference

## Hook Types and When They Fire

| Hook Type | When It Fires | Use Case |
|-----------|---------------|----------|
| `SessionStart` | Claude Code starts | Load context, inject memories |
| `SessionEnd` | Claude Code closes | Save session state |
| `UserPromptSubmit` | User sends message | Analyze intent, add hints |
| `PreToolUse` | Before any tool runs | Security checks, validation |
| `PostToolUse` | After any tool runs | Logging, auto-formatting, memory capture |
| `PermissionRequest` | Permission dialog | Auto-approve safe operations |
| `Stop` | Turn ends | Checkpoint, reminders |
| `SubagentStop` | Subagent finishes | Collect results |
| `PreCompact` | Before context compaction | Save state, block auto-compact |
| `Notification` | Claude sends notification | Desktop alerts |

---

## All Hooks Explained

### 1. session_start.py
**Type:** SessionStart
**Purpose:** Initialize session with context

**What it does:**
- Loads git context (branch, recent commits)
- Injects relevant memories based on project
- Detects project type
- Loads previous session state if resuming

**Why needed:** Fresh context every session, but you want continuity.

---

### 2. session_end.py
**Type:** SessionEnd
**Purpose:** Clean up and save state

**What it does:**
- Reminds to save session if significant work done
- Saves current work state to memory
- Logs session duration

**Why needed:** Don't lose work between sessions.

---

### 3. user_prompt_submit.py
**Type:** UserPromptSubmit
**Purpose:** Main intent detection hub

**What it does:**
- Analyzes prompt for complexity (score 0-5)
- Suggests relevant commands (/plan, /review-pr, etc.)
- Detects credential exposure
- Writes hints to `~/.claude/hints/current.txt`

**Why needed:** Smart routing and security.

---

### 4. parallel_agent_reminder.py
**Type:** UserPromptSubmit
**Purpose:** Suggest parallel execution

**What it does:**
- Detects keywords: "in parallel", "multiple tasks"
- Reminds about available specialized agents
- Suggests which agent for which task

**Why needed:** Users forget they can parallelize.

---

### 5. memory_search.py
**Type:** UserPromptSubmit
**Purpose:** Auto-search memories

**What it does:**
- Triggers on "what did we...", "how did we...", "remember when..."
- Searches semantic memory
- Injects relevant findings into context

**Why needed:** Retrieve past work automatically.

---

### 6. beads_reminder.py
**Type:** UserPromptSubmit
**Purpose:** Suggest Beads for complex tasks

**What it does:**
- Detects: "complex", "multi-step", "dependencies", "epic"
- Reminds to use `bd` CLI for task tracking
- Suggests creating issues

**Why needed:** Complex tasks need tracking.

---

### 7. skill_reminder.py
**Type:** UserPromptSubmit
**Purpose:** Suggest relevant skills

**What it does:**
- Detects task types (debugging, testing, planning)
- Suggests appropriate skills
- Example: "bug" → suggests systematic-debugging skill

**Why needed:** Skills are easy to forget.

---

### 8. decision_reminder.py
**Type:** UserPromptSubmit
**Purpose:** Catch decisions to save

**What it does:**
- Detects: "decided", "chose", "prefer", "going with"
- Hints to save decision to memory
- Prevents losing important choices

**Why needed:** Decisions get lost without saving.

---

### 9. codebase_map.py
**Type:** UserPromptSubmit
**Purpose:** Inject codebase structure

**What it does:**
- On first message, scans project structure
- Creates lightweight codebase map
- Helps Claude navigate unfamiliar projects

**Why needed:** Context about project structure.

---

### 10. pre_tool_use.py
**Type:** PreToolUse
**Purpose:** Security and validation

**What it does:**
- Blocks dangerous commands (rm -rf /, etc.)
- Auto-approves safe operations
- Prevents new .md file creation (except CLAUDE.md, README.md)
- Validates file paths

**Why needed:** Prevent accidental damage.

---

### 11. post_tool_use.py
**Type:** PostToolUse
**Purpose:** Post-action processing

**What it does:**
- Logs all tool usage
- Triggers auto-formatting on Write/Edit
- Captures observations for memory

**Why needed:** Audit trail and quality.

---

### 12. audit_logger.py
**Type:** PostToolUse
**Purpose:** Comprehensive logging

**What it does:**
- Logs every tool call with timestamp
- Records success/failure
- Writes to `~/.claude/logs/audit.log`

**Why needed:** Debugging and accountability.

---

### 13. auto_capture_memory.py
**Type:** PostToolUse
**Purpose:** Automatic memory capture

**What it does:**
- On file creation: saves purpose to memory
- On package install: saves as decision
- On git commit: saves as context
- On error: saves for bug tracking

**Why needed:** Build memory without manual effort.

---

### 14. beads_integration.py
**Type:** PostToolUse
**Purpose:** Auto-create Beads issues

**What it does:**
- On error: creates bug issue in Beads
- Links discovered issues to current work
- Tracks test failures

**Why needed:** Automatic issue tracking.

---

### 15. auto_formatter.py
**Type:** PostToolUse (matcher: Write|Edit)
**Purpose:** Format code after changes

**What it does:**
- Runs prettier/black/rustfmt based on file type
- Only on files that were just modified
- Non-blocking (doesn't fail the operation)

**Why needed:** Consistent code style.

---

### 16. code_quality.py
**Type:** PostToolUse (matcher: Write|Edit)
**Purpose:** Quality checks

**What it does:**
- Runs linter on changed files
- Checks for common issues
- Reports but doesn't block

**Why needed:** Catch issues early.

---

### 17. typecheck_changed.py
**Type:** PostToolUse (matcher: Write|Edit)
**Purpose:** TypeScript type checking

**What it does:**
- Runs `tsc --noEmit` on TypeScript files
- Reports type errors
- Only checks changed files

**Why needed:** Catch type errors immediately.

---

### 18. lint_changed.py
**Type:** PostToolUse (matcher: Write|Edit)
**Purpose:** Lint changed files

**What it does:**
- Runs ESLint/Pylint on changed files
- Reports issues
- Non-blocking

**Why needed:** Code quality.

---

### 19. test_changed.py
**Type:** PostToolUse (matcher: Bash)
**Purpose:** Run related tests

**What it does:**
- After code changes, suggests related tests
- Can auto-run tests for the changed module
- Reports failures

**Why needed:** Catch regressions.

---

### 20. permission_request.py
**Type:** PermissionRequest
**Purpose:** Auto-approve safe operations

**What it does:**
- Auto-approves: git, npm, pip, read operations
- Blocks: rm -rf, format, dd
- Custom rules per project

**Why needed:** Reduce permission fatigue.

---

### 21. stop.py
**Type:** Stop
**Purpose:** End-of-turn processing

**What it does:**
- Called when Claude stops responding
- Can add final reminders
- Trigger checkpoint save

**Why needed:** Clean turn endings.

---

### 22. end_of_turn_check.py
**Type:** Stop
**Purpose:** Verify work completed

**What it does:**
- Checks if todos were completed
- Reminds about uncommitted changes
- Suggests next steps

**Why needed:** Ensure nothing forgotten.

---

### 23. create_checkpoint.py
**Type:** Stop
**Purpose:** Auto-save checkpoints

**What it does:**
- Creates lightweight checkpoint
- Saves current file states
- For recovery if needed

**Why needed:** Backup before context compaction.

---

### 24. subagent_stop.py
**Type:** SubagentStop
**Purpose:** Handle agent completion

**What it does:**
- Collects agent results
- Logs agent performance
- Updates task tracking

**Why needed:** Coordinate parallel agents.

---

### 25. pre_compact.py
**Type:** PreCompact
**Purpose:** Prepare for compaction

**What it does:**
- Auto-compact: BLOCKED (exit 2) - forces manual
- Manual compact: Saves summary, clears caches

**Why needed:** Prevent data loss on compaction.

---

### 26. skill_activation.py
**Type:** SessionStart
**Purpose:** Load relevant skills

**What it does:**
- Detects project type
- Loads appropriate skills
- Activates skill plugins

**Why needed:** Right tools for right project.

---

### 27. notification.py
**Type:** Notification
**Purpose:** Desktop notifications

**What it does:**
- Sends OS notification when Claude needs attention
- Plays sound on completion
- Works across platforms

**Why needed:** Know when long tasks complete.

---

## Hook Output Format

All hooks must output JSON to stdout:

```json
{
  "continue": true,
  "additionalContext": "Optional text injected into Claude's context",
  "systemMessage": "Goes to context, not visible to user"
}
```

To block an operation:
```json
{
  "continue": false,
  "message": "BLOCKED: Reason for blocking"
}
```

---

## Adding Custom Hooks

1. Create Python file in `~/.claude/hooks/`
2. Add to `settings.json` under appropriate hook type
3. Ensure it reads JSON from stdin, writes JSON to stdout

```python
#!/usr/bin/env python3
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())
    # Your logic here
    print(json.dumps({"continue": True}))

if __name__ == "__main__":
    main()
```
