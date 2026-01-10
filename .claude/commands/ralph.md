---
name: ralph
description: Autonomous loop - keeps working until all tasks complete (Ralph Wiggum style with negative memory + screenshot verification)
user-invocable: true
---

# Ralph Loop - Autonomous Task Execution with Negative Memory

You are now in **Ralph Mode** - an autonomous execution loop that continues until all tasks are complete. This version includes **negative memory** to avoid repeating failed approaches and **screenshot verification protocol** for UI work.

## How This Works

1. Initialize state: `python ~/.claude/scripts/ralph_enhanced.py start "TASKS" MAX_ITER PROMISE MIN_ITER SCREENSHOTS_DIR`
2. **CHECK NEGATIVE MEMORY FIRST** before each task
3. Work through each task systematically
4. Log failures to negative memory when they occur
5. For UI work: Take screenshots, verify them before completing
6. After completing work, check if there are remaining tasks
7. If tasks remain, continue working (don't stop)
8. Only stop when ALL tasks are verified complete AND can-complete returns YES

## State Management

```bash
# Initialize loop (with screenshot verification)
python ~/.claude/scripts/ralph_enhanced.py start "1. Task A 2. Task B" 30 "ALL_DONE" 2 ".ralph/screenshots"

# Check status
python ~/.claude/scripts/ralph_enhanced.py status

# Check negative memory before starting a task
python ~/.claude/scripts/ralph_enhanced.py check "task name"

# Log a failure (IMPORTANT - prevents repeating mistakes)
python ~/.claude/scripts/ralph_enhanced.py fail "task" "approach" "failure" "lesson"

# Mark task complete
python ~/.claude/scripts/ralph_enhanced.py complete TASK_ID

# Add blocker
python ~/.claude/scripts/ralph_enhanced.py blocker "description" "workaround"

# Add anti-pattern to remember
python ~/.claude/scripts/ralph_enhanced.py antipattern "Never use X in this codebase"

# Check if all done
python ~/.claude/scripts/ralph_enhanced.py done

# Cancel loop
python ~/.claude/scripts/ralph_enhanced.py cancel
```

## Screenshot Verification Protocol (TDD Workflow)

For UI work, screenshots must be verified before completion promise can be output:

```bash
# Check screenshot status
python ~/.claude/scripts/ralph_enhanced.py screenshots

# After reviewing a screenshot, mark it verified
python ~/.claude/scripts/ralph_enhanced.py verify-screenshot .ralph/screenshots/button.png

# Mark all screenshots verified (after reviewing all)
python ~/.claude/scripts/ralph_enhanced.py verify-all

# Reset verification (for new iteration)
python ~/.claude/scripts/ralph_enhanced.py reset-screenshots

# Check if promise output is allowed
python ~/.claude/scripts/ralph_enhanced.py can-complete
```

**Critical Rule**: After marking screenshots as verified, DO NOT immediately output the completion promise. Let the next iteration confirm all checks pass. This prevents premature completion.

## Rules

1. **Check negative memory FIRST** - Before each task, run `check "task name"`
2. **Never repeat failed approaches** - If negative memory warns, use different approach
3. **Log failures** - When something fails, log it so future iterations avoid it
4. **Verify completion** - Run tests, check builds, validate output
5. **Track progress** - Use TodoWrite AND state file
6. **Self-correct** - If you make a mistake, fix it and continue
7. **Be thorough** - Don't mark tasks complete until verified

## Execution Pattern

```
BEFORE STARTING:
    python ralph_enhanced.py start "TASKS" MAX_ITER

WHILE tasks_remaining:
    1. python ralph_enhanced.py check "current task"  # CHECK NEGATIVE MEMORY
    2. If warned: Choose DIFFERENT approach than failed ones
    3. Plan approach
    4. Execute
    5. Verify (run tests, check output)
    6. If verified:
       - python ralph_enhanced.py complete TASK_ID
    7. If failed:
       - python ralph_enhanced.py fail "task" "what I tried" "why it failed" "what to do instead"
       - Try alternative approach (max 3 attempts)
    8. Loop
```

## Verification Methods

| Task Type | Verification | Command |
|-----------|--------------|---------|
| Code changes | Tests pass | `pytest -x` or `npm test` |
| UI changes | Screenshot + Verify | Take screenshot, `verify-screenshot FILE` |
| Build changes | Build succeeds | `npm run build` |
| Config changes | Service works | Restart, validate |

### UI Verification Workflow

```
1. Complete UI task
2. Take screenshot: mcp__claude-in-chrome__computer(action="screenshot")
3. Save to .ralph/screenshots/
4. Review screenshot visually
5. If correct: python ralph_enhanced.py verify-screenshot FILE
6. Continue to next task
7. After ALL tasks done: python ralph_enhanced.py can-complete
8. If YES: Output completion promise
9. If NO: Address the reasons shown
```

## Negative Memory Protocol

**On Task Start:**
```bash
python ~/.claude/scripts/ralph_enhanced.py check "implement auth"
# Output shows previous failed approaches - AVOID THEM
```

**On Task Failure:**
```bash
python ~/.claude/scripts/ralph_enhanced.py fail \
  "implement auth" \
  "used bcrypt without salt" \
  "security review failed" \
  "always use bcrypt.gensalt() before hashing"
```

**On Discovery of Anti-Pattern:**
```bash
python ~/.claude/scripts/ralph_enhanced.py antipattern "This project uses pnpm, not npm"
```

## When to Stop

Only stop when:
- All tasks are marked complete AND verified
- `can-complete` returns YES (min iterations met, all screenshots verified)
- User explicitly says "stop" or "pause"
- You hit an unrecoverable blocker (log it and explain)
- Max iterations reached

## CallMe Integration (Phone Notifications)

If configured, Ralph can call you when complete or blocked:

```bash
# Check CallMe status
python ~/.claude/scripts/ralph_enhanced.py callme-status

# Call on completion
python ~/.claude/scripts/ralph_enhanced.py call-complete

# Call about blocker
python ~/.claude/scripts/ralph_enhanced.py call-blocker "task name" "description"
```

Setup: `python ~/.claude/scripts/callme_integration.py setup`

## Integration with Memory System

After completing Ralph loop, save significant learnings:
```bash
~/.claude/scripts/memory_manager.py save-memory PROJECT decision "Ralph completed: ..."
~/.claude/scripts/memory_manager.py save-memory PROJECT learning "Discovered blocker: ..."
```

## Begin

1. First, initialize the loop with the tasks provided
2. Check negative memory for first task
3. Begin autonomous execution
4. Track progress with TodoWrite AND ralph state
5. Keep working until complete
