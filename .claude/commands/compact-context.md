Prepare for **context compaction** by creating a summary of important state before running `/compact`.

## Why This Matters

"AI context is like milk; it's best served fresh and condensed!"

Proactive compaction is better than automatic compaction because:
1. You control what gets preserved
2. Important decisions don't get lost
3. Fresh context = better responses

## Process

### 1. Summarize Current State

Create a mental model of:
- What task we're working on
- Key decisions made
- Important code locations found
- What's working / what's not

### 2. Save Critical Context

```bash
# Save to memory system
~/.claude/scripts/memory_manager.py save-memory PROJECT context "SUMMARY"

# Or create a handoff document
# Use /handoff command
```

### 3. Document Key Files

List the most important files for the current task:
- Files we've modified
- Files we need to reference
- Test files related to our work

### 4. Note Next Steps

What should happen after compaction:
- Immediate next action
- What to verify
- What to avoid re-doing

## Output Format

```markdown
## Pre-Compaction Summary

**Task:** [Current task]
**Progress:** [X% complete / description]

### Key Decisions Made
- [Decision 1]
- [Decision 2]

### Important Files
| File | Why It Matters |
|------|----------------|
| `path/to/file` | [Reason] |

### Current Blockers
- [Blocker 1]

### Immediate Next Step
[What to do right after compaction]

### Don't Repeat
[Things we already tried that didn't work]
```

---

**Ready to compact?** After reviewing, run `/compact` to compress the conversation.

Now analyze the current conversation and prepare for compaction.
