# Memory Recall

Recall information from long-term memory.

## Usage
`/memory-recall [query]`

## Instructions

Load memories from the current project and global storage:

```bash
~/.claude/scripts/memory_manager.py load-memories "$(basename $PWD)" "$ARGUMENTS"
```

If $ARGUMENTS contains a search query, filter memories by that query.

Present the memories to the user in a readable format, organized by:
1. Global memories (preferences, cross-project learnings)
2. Project-specific memories (decisions, architecture, bugs)

If no memories are found, let the user know they can save memories with `/memory-save`.

## Search Query
$ARGUMENTS
