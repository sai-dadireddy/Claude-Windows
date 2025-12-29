# Session Save

Save the current session state for later continuation.

## Instructions

Create a comprehensive session summary and save it. Include:

1. **Current Task**: What we're working on right now
2. **Progress**: What's been accomplished this session
3. **Next Steps**: What needs to be done next
4. **Open Questions**: Any unresolved issues or decisions
5. **Key Files**: Important files that were modified or referenced

After creating the summary, run:
```bash
~/.claude/scripts/memory_manager.py save-session "$SESSION_ID" "$(basename $PWD)" "YOUR_SUMMARY_HERE"
```

Replace YOUR_SUMMARY_HERE with the markdown-formatted summary.

## Additional Notes from User
$ARGUMENTS

---

**Important**: Confirm to the user that the session has been saved and can be continued later with `/session-continue`.
