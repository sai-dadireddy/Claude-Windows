---
name: ralph-loop
description: Start Ralph Wiggum autonomous loop (official Anthropic pattern)
allowed-tools:
  - Bash(python ~/.claude/scripts/ralph_loop.py *)
user-invocable: true
---

# Ralph Loop - Autonomous Development Iteration

You are now in **Ralph Loop Mode** - an iterative AI development methodology that continues until all tasks are complete.

## How Ralph Works

1. You receive a task list
2. Work through each task systematically
3. When you try to stop, the stop hook checks if work is complete
4. If not complete, you continue with the same prompt (seeing your progress via git/files)
5. Loop continues until completion promise is met OR max iterations reached

## State Management

The loop state is tracked in `.claude/ralph-loop.local.md`:
- Current iteration count
- Max iterations limit
- Completion promise text
- Progress log

## Starting the Loop

To initialize, run:
```bash
python ~/.claude/scripts/ralph_loop.py start "YOUR_TASK_DESCRIPTION" MAX_ITERATIONS "COMPLETION_PROMISE"
```

Example:
```bash
python ~/.claude/scripts/ralph_loop.py start "1. Implement auth system 2. Write tests 3. Update docs" 30 "ALL_TASKS_VERIFIED"
```

## Completion Rules

You may ONLY output the completion promise (e.g., "DONE" or "ALL_TASKS_VERIFIED") when:
- ALL specified tasks are complete
- ALL tasks have been VERIFIED (tests pass, builds work)
- You are 100% certain the work is done

**NEVER use the completion promise as an escape mechanism.**

## Loop Behavior

Each iteration:
1. Read current state: `python ~/.claude/scripts/ralph_loop.py status`
2. Check what's been done (git log, file contents)
3. Work on next incomplete task
4. Verify completion
5. If all done → output completion promise
6. If not done → the loop continues automatically

## Cancel the Loop

To stop early:
```bash
python ~/.claude/scripts/ralph_loop.py cancel
```

Or user says "stop ralph" / "cancel loop"

## Best Practices

1. **Clear tasks** - Vague tasks cause infinite loops
2. **Verification criteria** - Include how to verify each task
3. **Iteration limits** - Always set max_iterations (default: 50)
4. **Self-correct** - If something fails, fix it and continue
5. **Track progress** - Use TodoWrite to show what's done

## Begin

The user has initiated a ralph loop. Check the state file, understand the tasks, and begin working. Continue until the completion promise conditions are met.
