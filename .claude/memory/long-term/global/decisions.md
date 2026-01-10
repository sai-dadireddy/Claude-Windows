
## [2025-12-23 18:41:14]
Implemented multi-model AI orchestration with 8 providers (Claude, GLM, Gemini, OpenAI, Ollama Cloud, OpenRouter, Mistral, HuggingFace). 265+ models available. Claude Opus 4.5 remains default. Others used only when explicitly invoked via multi:chat or /route command.

## [2025-12-23 20:00:38]
Installed Agent Deck (v0.6.0) for managing multiple Claude Code sessions. Sessions: AARP, AGUPGRADE, erpagpt, Home. Alias: claude-agent

## [2025-12-23 20:54:22]
Created claude-doctor health check script at ~/.claude/scripts/claude-doctor (symlinked to ~/.local/bin/). Validates: 27 hooks, signal file, semantic DB (25 memories), MCP router, Beads CLI, Python deps, Gemini API key, disk space, skills/RAG, workmux. Run with 'claude-doctor' for pre-flight checks.

## [2026-01-10 18:31:45]
ByteRover CLI (team context engineering tool) evaluated Jan 2026: Cannot install on Windows without admin rights (requires VS Build Tools for native compilation). Alternative: Use git-based team sharing via existing ~/.claude/ repo sync. ByteRover features: brv curate/query/pull, web hub for team collaboration, context tree with relations. For team sharing without ByteRover: Create ~/.claude/memory/team/ folder, team members clone/pull repo.

## [2026-01-10 18:54:23]
Added PRD workflow for Ralph (Jan 2026, Ryan Carson method): (1) /prd skill - generates PRD from feature description, (2) /prd-to-stories skill - converts PRD to prd.json with atomic user stories and acceptance criteria, (3) ralph_loop.sh and ralph_loop.ps1 - spawns fresh Claude instances for each iteration. Workflow: /prd -> /prd-to-stories -> ralph_loop.ps1. Key insight: acceptance criteria must be testable by agent without human input.
