
## [2025-12-10 01:31:40]
System test completed on 2025-12-10. Results: Semantic Memory OK, MCP Router OK (10 categories), Context7 OK, Skills OK (4 dirs). Issues: PreToolUse security hook did NOT block .env file access (API key exposed), some operations auto-denied in dontAsk mode.

## [2025-12-10 02:51:24]
Session 2025-12-10: Comprehensive Claude Code setup complete. Added: 8 custom agents (code-scout, autonomous-coder, feature-builder, test-writer, refactorer, lambda-builder, frontend-builder, ui-ux-designer), local-faiss RAG (275 docs indexed), Task Master MCP, workmux for parallel dev, reminder hooks for agents/RAG/TaskMaster. All agents use Opus with bypassPermissions. Git repo initialized at ~/.claude with 46 files committed.

## [2025-12-23 20:00:40]
Hooks systemMessage goes to Claude context, not user terminal. For user-visible output through SSM: write to log file and use tail -f. stderr from hooks doesn't reach user through SSM.

## [2025-12-26 17:51:56]
SSM pseudo-terminals fail isTTY check so Claude Code hook systemMessage output is not visible. Fix: Use SSH-over-SSM tunnel (scl -ssh) which allocates proper PTY. Plain SSM sessions need tail -f ~/.claude/logs/hooks.log as workaround.
