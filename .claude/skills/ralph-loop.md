---
name: ralph-loop
description: Autonomous development loop with state persistence (Geoffrey Huntley's Ralph technique)
context: fork
user-invocable: true
triggers:
  - "ralph loop"
  - "autonomous loop"
  - "keep working until done"
---

# Ralph Loop - Persistent Autonomous Development

Implementation of Geoffrey Huntley's Ralph Wiggum technique for Claude Code.

## The Concept

Ralph is a development methodology where the AI agent:
1. Receives a task list
2. Works through tasks iteratively
3. Persists state to disk
4. Can resume after interruption
5. Continues until ALL tasks are verified complete

## State File Pattern

Create/update `.ralph-state.json` in project root:

```json
{
  "started": "2026-01-09T09:00:00Z",
  "tasks": [
    {"id": 1, "task": "Implement feature X", "status": "complete", "verified": true},
    {"id": 2, "task": "Write tests for X", "status": "in_progress", "verified": false},
    {"id": 3, "task": "Update documentation", "status": "pending", "verified": false}
  ],
  "current_task": 2,
  "iteration": 5,
  "last_action": "Running pytest",
  "blockers": []
}
```

## Execution Loop

```
1. Read .ralph-state.json (or create if missing)
2. Find first incomplete task
3. Execute task with verification
4. Update state file
5. If tasks remain → continue (DON'T STOP)
6. If all complete → announce completion and stop
```

## Verification Requirements

Each task must be verified before marking complete:

| Task Type | Verification Method |
|-----------|---------------------|
| Code change | Tests pass, no lint errors |
| New feature | Tests + manual verification |
| Bug fix | Regression test passes |
| Refactor | All existing tests pass |
| Config | Service starts successfully |
| Docs | Renders correctly |

## Usage

```
/ralph-loop

Tasks:
1. [ ] Implement user authentication
2. [ ] Add login/logout endpoints
3. [ ] Write integration tests
4. [ ] Update API documentation

Work autonomously until all tasks are complete and verified.
```

## Best Practices (from Geoffrey Huntley)

1. **Specific tasks** - Vague tasks lead to loops
2. **Verification criteria** - Include "how to verify" per task
3. **Checkpoints** - State file allows resume after crashes
4. **Cost awareness** - Long loops burn tokens ($50-100+ possible)
5. **Exit conditions** - Always have clear completion criteria

## Blockers

If you hit an unrecoverable blocker:
1. Document it in `.ralph-state.json` blockers array
2. Try 2-3 alternative approaches
3. If still blocked, stop and report to user

## Resume Pattern

If session was interrupted, check for existing `.ralph-state.json`:
- If exists: resume from `current_task`
- If not: start fresh

## Sources

- [Geoffrey Huntley's original Ralph concept](https://ghuntley.com/ralph/)
- [Ralph Wiggum autonomous loops](https://paddo.dev/blog/ralph-wiggum-autonomous-loops/)
