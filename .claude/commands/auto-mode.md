# Auto Mode - Autonomous Task Execution Loop

You are now in **AUTO MODE**. Execute tasks from the Beads backlog autonomously.

## Protocol

### Step 1: Check Task Queue
```bash
PATH="$HOME/.local/bin:$PATH" bd ready --limit 1
```

### Step 2: Decision Branch

**If a task exists:**
1. Parse the task ID and description
2. Run `bd update <id> --status in_progress` to claim it
3. Read the full task: `bd show <id>`
4. Execute the task:
   - For features: Plan briefly, implement, test
   - For bugs: Use systematic-debugging skill
   - For chores: Execute directly
5. Verify completion (run tests if applicable)
6. Close the task: `bd close <id> --reason "Completed: <summary>"`
7. Save any learnings to memory
8. **RECURSE**: Run `/auto-mode` again

**If no tasks exist:**
1. Summarize all work completed this session
2. Save session state to memory
3. Report: "Auto-mode complete. No remaining tasks."
4. **STOP** - Do not recurse

### Step 3: Safety Limits

- Maximum 10 tasks per auto-mode session (prevent runaway)
- Stop immediately if:
  - 3 consecutive failures on same task
  - User interrupts with any message
  - Critical error detected
- Always ask before destructive operations (delete, force push)

### Step 4: Reporting

After each task, output:
```
[AUTO-MODE] Task <id> completed
[AUTO-MODE] Tasks remaining: <count>
[AUTO-MODE] Continuing...
```

## Error Handling

If a task fails:
1. Do NOT immediately retry the same approach
2. Read systematic-debugging.md
3. Save error context to memory
4. Either:
   - Fix with different approach, OR
   - Mark task as blocked: `bd update <id> --status blocked`
   - Move to next task

## Begin

Start by running `bd ready` now.
