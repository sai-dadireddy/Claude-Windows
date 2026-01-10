
## [2025-12-28 21:06:48]
decision_reminder.py hook was crashing on Windows due to emoji encoding (cp1252). Fixed by replacing Unicode emojis with ASCII text. Line 121 print statement was the culprit.

## [2025-12-28 21:16:11]
Fixed Windows cp1252 encoding issue in 31+ hooks. Python print() statements with emojis crash on Windows. Solution: Replace all emojis with ASCII equivalents like [FAST], [OK], [WARN], etc. Used Python script to batch-replace since sed failed with multi-byte chars.

## [2025-12-28 21:21:47]
Pilot + Beads workflow: Beads (bd) is dependency-aware task tracker. Pilot is autonomous agent that picks up tickets with --labels pilot. Delegate to Pilot when task touches >3 files, is scaffolding, or hazardous. Creates via bd create + workmux spawn. Use for multi-session, complex features.

## [2025-12-28 21:30:43]
Beads (bd) is project-specific by default - creates .beads/beads.db per project. For global db: use --db flag (bd --db ~/.beads/global.db) or create wrapper script 'gbd'. Hybrid approach recommended: global for cross-cutting tasks, project-specific for feature work.

## [2025-12-29 13:02:55]
PowerShell toolkit: cct (claude-code-transcripts with timestamped folders), ccstatusline, startup banner showing all aliases. Profiles updated: OneDrive-ERPA/Documents/PowerShell/ for PS7.

## [2025-12-30 10:52:57]
Workday RAG KB at ~/OneDrive - ERPA/Claude/workday_docs/. Query: python workday_rag.py 'question'. Has Projects API (OpenAPI) + Payments API (text). Capture snippet at capture_snippet.js for DevTools scraping.

## [2025-12-30 10:53:30]
Workday scraping: WAF blocks curl/fetch (403). Use Cyborg approach - human navigates, tool extracts. DevTools snippet (capture_snippet.js) for zero-detection scraping. REST API docs at apidocs.workdayspend.com have OpenAPI JSON downloads (click Download button in browser). robots.txt allows /sites/default/files/file-hosting/restapi/ only.

## [2025-12-30 11:11:38]
Workday KB complete at ~/OneDrive - ERPA/Claude/workday_docs/. Contains: 55 SOAP WSDLs (wsdl/), REST API docs (public/), integration guides (private/). Query: python workday_rag.py 'question'. Semantic search with Gemini embeddings. WSDL index at wsdl_index.json.

## [2026-01-04 11:31:27]
Fixed multi-AI MCP not working: Added 'multi' server to Node.js router at mcp-router/dist/categories.js. Moved multi_mcp from temp to ~/.claude/mcp/multi_mcp/. Available tools: chat (any model), compare (multi-model), models (list all). Restart Claude Code to apply.

## [2026-01-08 12:32:32]
Electron DSL Script Best Practices: 1) Use {{VARIABLE}} format for all tenant-specific data, 2) Group variables by purpose (Tenant Config, Employee Data, Expected Values), 3) wait commands must be 'wait for N seconds' not 'wait for page load', 4) select command works for dropdowns AND text fields, 5) Always end with 'click cancel button' for safe exit, 6) Version scripts (v4.0) and include UPDATED date, 7) Create EMAIL_SUMMARY.txt explaining variables for client customization

## [2026-01-10 15:02:08]
Updated to Claude Code 2.1.3: (1) AskUserQuestion adds metadata.source for analytics, (2) Bash descriptions must avoid 'complex'/'risk' terms, (3) git status -uall banned in commit/PR flows, (4) _simulatedSedEdit internal schema added, (5) Hook timeout increased 60s->10min, (6) Sub-agent model fix during compaction, (7) Slash commands and skills merged

## [2026-01-10 15:35:00]
Built claude-canvas: Windows-native TUI toolkit at ~/OneDrive - ERPA/Claude/claude-canvas. Uses ink/React for terminal UI. Canvas types: email, calendar, table, todo, json. Skill at ~/.claude/skills/canvas.md. Run with: npm run canvas -- spawn <type> --data '{...}'. Phase 2 pending: Electron popup for rich UI.

## [2026-01-10 15:48:01]
Claude Canvas Phase 2 complete: Added Electron popup mode at electron/. Features: always-on-top windows, dark theme, React components, WebSocket on port 3848. Commands: npm run popup -- --type email --data '{...}'. Both TUI and Popup modes working.

## [2026-01-10 17:07:16]
Claude Canvas toolkit built at ~/OneDrive - ERPA/Claude/claude-canvas. Two modes: (1) TUI via 'npm run canvas -- spawn <type> --data <json>' - requires interactive terminal split pane, (2) Electron popup via 'npm run popup' - needs path fix for OneDrive spaces. Canvas types: email, calendar, table, todo, json. Skill at ~/.claude/skills/canvas.md. WebSocket ports: TUI=3847, Popup=3848. Use for rich visual output instead of Claude-in-Chrome screenshots.

## [2026-01-10 17:35:31]
Claude Canvas workflow for Workday testing: (1) Query RAG first, (2) If score < 7.0 use Claude-in-Chrome to research fields, (3) Open Canvas todo for step tracking, (4) Open Canvas table for field docs, (5) Write test script checking off todos, (6) Run with DSL executor. Canvas = display workspace, Chrome = browser hands.
