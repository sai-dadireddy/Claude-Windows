
## [2025-12-30 19:10:47]
Deployed parallel Workday enhancement agents with central SQLite tracker. Tracker at electron_tests/_data/enhancement_tracker.db. Agent instructions at _scripts/agent_instructions.txt. Commands: claim, complete_file(), status. Priority: LOW confidence files first.

## [2025-12-30 19:38:16]
Updated workday_docs/CLAUDE.md and oracle_docs/CLAUDE.md with MCP browser access instructions. general-purpose agents now read these files to get MCP instructions. Custom agents (Workday API Expert, PeopleSoft Expert) don't get MCP - only general-purpose does.
