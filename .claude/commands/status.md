# Session Status Report

Display comprehensive session status including tokens, git, project info, and real-time recommendations.

## Instructions

Execute these checks in PARALLEL for speed:

### Step 1: Gather Data (Parallel Tool Calls)

**Read operations:**
- @.claude/context/token-tracker.json (token usage)
- @.claude/settings.json (project profile, agents, MCPs)
- @.claude/last-session.json (session info) - if exists
- @ROADMAP.md (project progress) - if exists

**Bash operations:**
- `git branch --show-current` (current branch)
- `git status --short` (changes count)
- `pwsh -Command "Get-Date -Format 'HH:mm'"` (current time)

### Step 2: Display Formatted Status

```
╔═══════════════════════════════════════════════════════════════╗
║            Claude Code Session Status Report                  ║
╚═══════════════════════════════════════════════════════════════╝

📊 TOKEN USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Current:   [X,XXX] / [1,000,000] tokens ([X.X]%) [🟢|🟡|🔴]
  Session:   +[X,XXX] tokens used
  Available: [XXX,XXX] tokens ([XX.X]%)
  Baseline:  [XX,XXX] tokens (startup overhead)
  Status:    [Healthy | Warning | Critical]

💰 COST ESTIMATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Input:     $[X.XX] ([XXK] tokens × $3.00/1M)
  Model:     Claude Sonnet 4.5 (1M context)
  Session:   +$[X.XX] this session

⎇ GIT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Branch:    [branch-name]
  Modified:  [X] files
  Untracked: [X] files
  Status:    [Clean | Uncommitted changes]

🔧 PROJECT CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Profile:   [profile-name]
  Agents:    [X] enabled ([agent-list-compact])
  Skills:    [X] active ([skill-list])
  MCPs:      [X] active ([mcp-list])

⏱ SESSION INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Session:   ${CLAUDE_SESSION_ID}
  Duration:  [X hours X minutes] OR [X minutes]
  Started:   [YYYY-MM-DD HH:MM] OR [N/A - new session]
  Project:   [project-name] OR [workspace root]
  Time:      [HH:MM]

🔄 BACKGROUND PROCESSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Active:    [X] processes
  [If > 0: List each process with duration]
  [If 0: No background tasks running]

📋 NEXT ACTIONS (from ROADMAP.md if exists)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Current:   [Last [-] in-progress task] OR [N/A]
  Pending:   [X] tasks remaining
  Completed: [X] tasks this session

💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [Dynamic recommendations based on data:]

  Token Management:
  - If <80%: ✅ Token usage healthy - continue working
  - If 80-89%: 🟡 Consider /session save soon
  - If 90%+: 🔴 Run /session save NOW

  Git Management:
  - If changes > 0: 💡 [X] uncommitted changes - consider commit
  - If changes = 0: ✅ Working directory clean

  Workflow Optimization:
  - 💡 Use /knowledge query for docs instead of reading files
  - 💡 Use RAG: python tools/query-docs-rag.py "query"
  - 💡 Delegate to agents: @[agent-name] for specialized tasks

  Session Management:
  - ⏱ Session duration: [X] - optimal for [X] more hours
  - 💾 Last save: [time ago] OR [Never - consider /session save]

╔═══════════════════════════════════════════════════════════════╗
║   Ready! Type /help for commands | /session save to persist  ║
╚═══════════════════════════════════════════════════════════════╝
```

## Display Rules

**Token Status Colors:**
- 🟢 Green: 0-79% (healthy)
- 🟡 Yellow: 80-89% (warning)
- 🔴 Red: 90%+ (critical)

**Number Formatting:**
- Format with commas: 52,000 not 52000
- Use K for thousands: 52K not 52000
- Use M for millions: 1M not 1000000
- Cost format: $0.16 not $0.156

**Error Handling:**
- If file doesn't exist: Show "N/A" or skip section
- If git not available: Show "Not a git repository"
- If no background processes: Show "No background tasks running"
- Suppress all errors gracefully

**Compact Display:**
- Agent list: First 3 names + "..."
- Keep total output under 50 lines
- Use box drawing for visual clarity

## Execution Notes

- Use PARALLEL tool calls (Read + Bash together) for speed
- Calculate duration from session_start in token-tracker.json
- Extract last [-] task from ROADMAP.md if exists
- Show realistic recommendations based on actual data
- Always provide actionable next steps

## Success Criteria

✅ Displays in <2 seconds (parallel execution)
✅ Shows all critical metrics in one view
✅ Clear visual hierarchy with box drawing
✅ Actionable recommendations
✅ Graceful error handling
✅ Total output <3K tokens
