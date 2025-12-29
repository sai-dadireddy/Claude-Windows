# Session Continue

Continue from a previously saved session.

## Instructions

1. First, load the last session state:
```bash
~/.claude/scripts/memory_manager.py load-session "last" "$(basename $PWD)"
```

2. Also load any relevant long-term memories:
```bash
~/.claude/scripts/memory_manager.py load-memories "$(basename $PWD)"
```

3. Review the loaded session state and memories

4. Provide a brief summary to the user:
   - What we were working on
   - What was accomplished
   - What's next

5. Ask if the user wants to continue from where we left off or start something new

## Specific Session to Load
$ARGUMENTS

---

**If $ARGUMENTS contains a session ID**, load that specific session instead of "last".
