---
name: ralph-enhanced
description: Enhanced Ralph Wiggum loop with negative memory, plan/build phases, and LLM-as-judge backpressure
context: fork
user-invocable: true
triggers:
  - "ralph enhanced"
  - "smart ralph"
  - "ralph with memory"
---

# Ralph Enhanced - Autonomous Loop with Negative Memory

An enhanced implementation of Geoffrey Huntley's Ralph Wiggum technique that adds:
- **Negative memory** - Track failed approaches to avoid repeating mistakes
- **Plan/Build phases** - Separate planning from execution
- **LLM-as-judge backpressure** - Subjective quality checks
- **Model routing** - Cost optimization with subagents

## File Structure

```
project-root/
├── .ralph/
│   ├── state.json           # Current progress
│   ├── negative-memory.json # Failed approaches (DON'T REPEAT)
│   ├── plan.md              # Current implementation plan
│   └── log.md               # Iteration history
└── specs/                   # Requirements (one per topic)
    ├── auth.md
    ├── api.md
    └── ...
```

## State File (.ralph/state.json)

```json
{
  "phase": "build",
  "iteration": 5,
  "max_iterations": 50,
  "started": "2026-01-10T15:00:00Z",
  "completion_promise": "ALL_TASKS_VERIFIED",
  "current_task": 2,
  "tasks": [
    {"id": 1, "task": "Implement auth", "status": "complete", "verified": true},
    {"id": 2, "task": "Write tests", "status": "in_progress", "attempts": 1},
    {"id": 3, "task": "Update docs", "status": "pending"}
  ]
}
```

## Negative Memory (.ralph/negative-memory.json)

**CRITICAL: Read this BEFORE each task to avoid repeating failures**

```json
{
  "failed_approaches": [
    {
      "task": "Implement auth",
      "approach": "Used bcrypt directly without salt",
      "failure": "Security review failed - salt required",
      "lesson": "Always use bcrypt.gensalt() before hashing",
      "timestamp": "2026-01-10T15:30:00Z"
    },
    {
      "task": "Database migration",
      "approach": "Ran migration without backup",
      "failure": "Lost data in dev environment",
      "lesson": "Always pg_dump before migrations",
      "timestamp": "2026-01-10T16:00:00Z"
    }
  ],
  "blockers": [
    {
      "description": "Puppeteer won't install on Windows without admin",
      "workaround": "Use Playwright instead",
      "discovered": "2026-01-10T15:45:00Z"
    }
  ],
  "anti_patterns": [
    "Don't use any() without proper null checks in this codebase",
    "This project uses pnpm, not npm - commands will fail with npm",
    "Tests require DB to be running (docker-compose up db)"
  ]
}
```

## Phase 1: Planning

Run planning phase to analyze gaps between specs and implementation:

```
1. Study ALL files in specs/ directory
2. Study current codebase structure
3. Gap analysis: What's in specs but not in code?
4. Create/update .ralph/plan.md with prioritized tasks
5. Each task must have:
   - Clear acceptance criteria
   - Verification method
   - Estimated complexity (S/M/L)
```

**Planning triggers:**
- First run (no .ralph/state.json)
- User says "ralph plan" or "replan"
- Major blocker encountered

## Phase 2: Building

Execute tasks from plan:

```
1. READ .ralph/negative-memory.json FIRST
2. Read .ralph/state.json for current task
3. Check: Has this approach failed before?
   - YES → Use different approach
   - NO → Proceed
4. Execute task
5. Verify (tests, builds, LLM-judge if needed)
6. If PASS:
   - Mark complete
   - Update state.json
   - Continue to next task
7. If FAIL:
   - Log to negative-memory.json
   - Try alternative (max 3 attempts)
   - If still failing → mark as blocker
```

## Backpressure Mechanisms

### Hard Backpressure (Must Pass)
- `pytest -x` or `npm test` passes
- `npm run build` or equivalent succeeds
- No lint errors
- Type checks pass

### Soft Backpressure (LLM-as-Judge)

For subjective criteria (UI, docs, naming), use a judge prompt:

```bash
# Ask a subagent to review
Task(subagent_type="haiku", prompt="
Review this code change for:
1. Naming consistency with codebase
2. Documentation completeness
3. Error handling quality

Code:
<code>
$DIFF
</code>

Respond ONLY with: PASS or FAIL: <reason>
")
```

## Model Routing

| Task Type | Model | Reason |
|-----------|-------|--------|
| Main execution | opus | Complex reasoning |
| Code search | haiku | Fast, cheap |
| Test generation | sonnet | Good balance |
| LLM-as-judge | haiku | Binary decisions |
| Documentation | sonnet | Writing quality |

## Verification by Task Type

| Task Type | Verification |
|-----------|--------------|
| Code change | Tests pass + types check |
| New feature | Tests + manual verification |
| Bug fix | Regression test passes |
| Refactor | All existing tests pass |
| Config | Service starts successfully |
| Docs | Renders + LLM-judge review |
| UI | Screenshot + visual check |

## Usage

### Start Fresh Loop
```
/ralph-enhanced

Tasks:
1. [ ] Implement user authentication
2. [ ] Add login/logout endpoints
3. [ ] Write integration tests
4. [ ] Update API documentation

Work autonomously with negative memory until all tasks complete.
```

### Resume Existing Loop
```
/ralph-enhanced resume

Check .ralph/ directory and continue from where we left off.
```

### Force Replan
```
/ralph-enhanced replan

Regenerate the plan from specs/, preserving negative memory.
```

## Negative Memory Protocol

**On Task Start:**
```python
# Pseudocode
neg_mem = read(".ralph/negative-memory.json")
current_task = state["tasks"][state["current_task"]]

# Check for relevant failures
relevant_failures = [
    f for f in neg_mem["failed_approaches"]
    if f["task"] == current_task["task"]
]

if relevant_failures:
    print("WARNING: Previous failed approaches for this task:")
    for f in relevant_failures:
        print(f"  - {f['approach']}: {f['lesson']}")
    print("Choose a DIFFERENT approach.")
```

**On Task Failure:**
```python
# Log to negative memory
neg_mem["failed_approaches"].append({
    "task": current_task["task"],
    "approach": what_i_tried,
    "failure": error_message,
    "lesson": what_to_do_instead,
    "timestamp": now()
})
write(".ralph/negative-memory.json", neg_mem)
```

## Key Language (from ghuntley)

Use these phrases for better results:
- **"study"** not "read" - implies deeper understanding
- **"Ultrathink"** - requests extended reasoning
- **"capture the why"** - ensures documentation
- **"don't assume not implemented"** - prevents duplicate work
- **"using parallel subagents"** - enables Task tool usage

## Exit Conditions

Only output completion promise when:
1. ALL tasks marked complete AND verified
2. No items in blockers array (or all have workarounds applied)
3. Tests pass
4. Build succeeds

## Integration with Your Memory System

After Ralph completes, save learnings:

```bash
# Save significant decisions
~/.claude/scripts/memory_manager.py save-memory PROJECT decision "Ralph completed: implemented X using Y approach. Key learnings: ..."

# Save blockers discovered
~/.claude/scripts/memory_manager.py save-memory PROJECT learning "Blocker: Z doesn't work on Windows. Workaround: use W instead"
```

## Sources

- [Geoffrey Huntley's Ralph](https://ghuntley.com/ralph/)
- [ghuntley/how-to-ralph-wiggum](https://github.com/ghuntley/how-to-ralph-wiggum)
- Enhanced with negative memory based on Reddit discussion (Jan 2026)
