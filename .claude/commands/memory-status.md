# Memory Status

Show current memory status and available memories.

## Instructions

Get a summary of available memories:

```bash
~/.claude/scripts/memory_manager.py summary "$(basename $PWD)"
```

Also list recent sessions:

```bash
~/.claude/scripts/memory_manager.py list-sessions "$(basename $PWD)"
```

Present this information to the user showing:
1. What long-term memories exist (global and project)
2. Recent sessions available for continuation
3. Tips on using memory commands

## Memory Commands Reference
- `/session-save [notes]` - Save current session state
- `/session-continue [id]` - Continue from saved session
- `/memory-save <type> <content>` - Save to long-term memory
- `/memory-recall [query]` - Recall memories
- `/memory-status` - This command
