---
description: Token lifecycle management (monitor|alert|profile|optimize|report|archive)
argument-hint: <action> [options]
allowed-tools: Read, Write, Bash, Grep
model: haiku
---

# Token Management

Action: $ARGUMENTS

## Available Actions:

### monitor [interval]
Real-time token usage tracking
- interval: 5s|30s|60s (default: 30s)
- Live dashboard display
- Current vs. allocated
- Burn rate (tokens/min)
- Estimated remaining time
- Status: Green (<50%), Yellow (50-80%), Red (80%+)

### alert [threshold]
Set/check token usage alerts
- threshold: 50|70|80|90 (default: 80)
- Sets alert when threshold reached
- Auto-triggers recommended actions
- Options: --email, --slack, --discord
- Persistent alerts across sessions

### profile
Analyze token usage patterns
- Session token breakdown
- Tool usage distribution (Read: 20%, Bash: 15%, etc.)
- Top consumers (files, operations)
- Weekly trends
- Efficiency metrics
- Saves to .claude/context/token-profile.json

### optimize
Get optimization recommendations
- Identifies token drains
- Suggests alternative approaches
- Context management tips
- Tool usage optimization
- Smart command consolidation
- Saves to OPTIMIZATION-RECOMMENDATIONS.md

### report [format]
Generate comprehensive report
- format: text|json|html|pdf (default: text)
- Token timeline
- Cost analysis
- Usage patterns
- Session history
- Efficiency scoring
- Saves to .claude/context/token-report.{format}

### archive [days]
Archive old session data
- days: 7|14|30|90 (default: 30)
- Archives sessions older than N days
- Compresses to .claude/sessions/archive/
- Removes from active context
- Maintains metrics summary
- Can recover archived sessions

### compact
Emergency context cleanup
- Removes stale context files
- Archives old sessions
- Cleans backup files
- Optimizes .claudeignore
- Frees 10-50K tokens
- Run when at 80%+ usage

### export [format]
Export token data
- format: csv|json|sql (default: csv)
- Export to external tools
- Integrates with analytics
- Exports to .claude/context/token-export.{format}

## Usage Examples:
```
/tokens monitor 60s
/tokens alert 80
/tokens profile
/tokens optimize
/tokens report html
/tokens archive 30
/tokens compact
/tokens export csv
```

## Key Features:
- Persistent tracking across sessions
- Multi-level alerts
- Auto-recommendations at thresholds
- Session-by-session breakdown
- Tool performance metrics
- Archival & recovery

## Integration:
- Tracks in .claude/context/token-tracker.json
- Updates ROADMAP.md with metrics
- Monitors in settings.json
- Syncs with statusline display
- Reports saved to .claude/context/

## Alert Actions:
- 50%: Informational only
- 70%: Suggests /knowledge over file reads
- 80%: Recommends agent delegation
- 90%: Requires /compact or new session
