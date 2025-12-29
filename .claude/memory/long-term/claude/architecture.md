
## [2025-12-23 18:41:18]
Multi-MCP setup: config at ~/.multi_mcp/, skills at ~/.claude/skills/model-*.md, /route command for auto-routing. All 8 APIs tested working. FREE models via Ollama Cloud and OpenRouter (deepseek, kimi, llama-405b).

## [2025-12-28 21:34:32]
Windows Claude Code Setup (Dec 28, 2025):
- Multi-Model MCP: 44 models, 8 providers (OpenAI, Gemini, GLM, Ollama, OpenRouter, Mistral, HuggingFace), 26 FREE. Config at ~/.multi_mcp/.env, venv at %TEMP%/multi_mcp
- Beads CLI: v0.40.0 at ~/.local/bin/bd.exe. Global DB: ~/.beads/global.db. Wrapper: gbd. PowerShell aliases in profile.
- Hooks: Fixed 31+ files for Windows cp1252 emoji encoding (replaced with ASCII)
- Router: ~/.claude/mcp/router/server.py has multi backend with Windows path
- Detection hooks: intent_detector.py (model routing), parallel_agent_reminder.py (agents), beads_reminder.py (tasks), decision_reminder.py (memory saves)
