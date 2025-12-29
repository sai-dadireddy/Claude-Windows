# Beads - Detailed Task Tracking Guide

## CLI Commands

Location: `~/.local/bin/bd`

### Initialize
```bash
bd init  # Creates .beads/ directory
```

### Create Issues
```bash
bd create "Implement user authentication" -t feature -p 1
bd create "Fix login bug" -t bug -p 2
bd create "Add unit tests" -t task -p 3
```

### View Issues
```bash
bd list                    # All issues
bd ready                   # Issues ready to work (no blockers)
bd show <id>               # Show issue details
bd status                  # Overview
```

### Update Issues
```bash
bd update <id> --status in_progress
bd update <id> --status done
bd close <id> --reason "Implemented"
```

### Dependencies
```bash
bd dep add <child-id> <parent-id>      # Child blocks parent
bd dep add <id> <id> --discovered      # Found while working
bd dep tree <id>                       # Visualize dependencies
```

### Epics
```bash
bd epic create "User Management Feature"
bd epic add <epic-id> <issue-id>
```

## Workflow Example

```
1. START PROJECT
   bd init
   bd create "Main feature" -t epic -p 1

2. BREAK DOWN WORK
   bd create "Subtask 1" -t task -p 2
   bd create "Subtask 2" -t task -p 2
   bd dep add <subtask1-id> <epic-id>
   bd dep add <subtask2-id> <epic-id>

3. FIND READY WORK
   bd ready  # Shows tasks with no blockers

4. WORK ON TASK
   bd update <id> --status in_progress
   ... do the work ...
   bd close <id> --reason "Done"

5. DISCOVER NEW WORK
   bd create "Found bug X" -t bug -p 1
   bd dep add <new-id> <current-id> --discovered

6. REPEAT
   bd ready  # Next ready task
```

## Priority Levels

| Priority | When to Use |
|----------|-------------|
| P0 | Critical/Blocker - Must fix NOW |
| P1 | High - Important feature/bug |
| P2 | Medium - Normal priority |
| P3 | Low - Nice to have |
| P4 | Backlog - Future work |

## Issue Types

| Type | Use For |
|------|---------|
| `feature` | New functionality |
| `bug` | Something broken |
| `task` | General work item |
| `epic` | Group of related issues |
| `chore` | Maintenance, cleanup |
| `docs` | Documentation |

## Full Example: "Add authentication"

```bash
# 1. Initialize
bd init

# 2. Create epic
bd create "User Authentication System" -t epic -p 1
# Returns: bd-a1b2

# 3. Create subtasks with dependencies
bd create "Design auth schema" -t task -p 2
# Returns: bd-c3d4
bd dep add bd-c3d4 bd-a1b2

bd create "Implement JWT tokens" -t task -p 2
# Returns: bd-e5f6
bd dep add bd-e5f6 bd-a1b2
bd dep add bd-e5f6 bd-c3d4  # Must design first

bd create "Add login endpoint" -t task -p 2
# Returns: bd-g7h8
bd dep add bd-g7h8 bd-e5f6  # Need JWT first

# 4. Start working
bd ready  # Shows "Design auth schema"
bd update bd-c3d4 --status in_progress
... design ...
bd close bd-c3d4 --reason "Schema designed"

bd ready  # Now shows "Implement JWT tokens"
```
