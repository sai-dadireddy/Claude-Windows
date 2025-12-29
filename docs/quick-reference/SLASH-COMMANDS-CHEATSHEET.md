# Claude Code Slash Commands - Complete Cheat Sheet

**Quick Reference:** Type any command directly in Claude Code. Commands starting with `/` give me instructions to execute.

---

## 🚀 SESSION MANAGEMENT (Use These Every Day!)

| Command | Usage | Description |
|---------|-------|-------------|
| `/load-global` | `/load-global` or `/load-global full` | **ESSENTIAL** - Load all capabilities (CLAUDE.md + MCPs). Use `full` for complete 47-module load |
| `/save-session` | `/save-session [name] [notes]` | Save current session state for fast resume later |
| `/resume-session` | `/resume-session [name]` | Resume a previously saved session with full context |
| `/smart-resume` | `/smart-resume` | **INTELLIGENT** - Resume with automatic change detection (90%+ token savings) |

**Example Workflow:**
```
# Day 1
/load-global
[work for hours]
/save-session myproject "Implementing OAuth"

# Day 2 (after restart)
/resume-session myproject
[continue immediately with full context!]
```

---

## 🔧 SETUP & MANAGEMENT

| Command | Usage | Description |
|---------|-------|-------------|
| `/mcp` | `/mcp` | View MCP server status, manage connections |
| `/project` | `/project [name]` | Switch between projects with context loading |
| `/agents` | `/agents` | Browse directory of 90+ specialized AI agents |
| `/auto-optimize` | `/auto-optimize` | Get optimization recommendations for your setup |

---

## 📰 AI NEWS & RESEARCH

| Command | Usage | Description |
|---------|-------|-------------|
| `/ai-news` | `/ai-news` | View AI news dashboard (30+ sources aggregated) |
| `/n8n` | `/n8n` | Start n8n automation platform and open dashboard |
| `/research-video` | `/research-video [YouTube URL]` | Extract and analyze YouTube video transcripts |
| `/morning` | `/morning` | Personal AI assistant briefing (progress + AI news + inspiration) |

---

## 🔍 CODE ANALYSIS & REVIEW

| Command | Usage | Description |
|---------|-------|-------------|
| `/analyze` | `/analyze` | **COMPREHENSIVE** - Quality, performance, architecture, testing, security, refactoring analysis |
| `/analyze-files` | `/analyze-files [pattern]` | Analyze specific files or patterns |
| `/review-code` | `/review-code` | Code review with industry best practices |
| `/auto-review` | `/auto-review` | Automated code review triggered on file changes |

**Example:**
```
/analyze
# Provides 6-part comprehensive analysis
```

---

## 🧪 TESTING & AUTOMATION

| Command | Usage | Description |
|---------|-------|-------------|
| `/test` | `/test` | **Playwright Test Automation** - Overview of test agents |
| `/test-plan` | `/test-plan [URL]` | Launch Planner agent to explore website and create test scenarios |
| `/test-generate` | `/test-generate [plan-file]` | Launch Generator agent to convert plans to executable Playwright tests |
| `/test-heal` | `/test-heal [test-file]` | Launch Healer agent to automatically fix broken tests |
| `/generate-tests` | `/generate-tests [file]` | Auto-generate unit tests for code |

**Playwright Test Workflow:**
```
/test-plan https://example.com
# Creates test scenarios

/test-generate test-plan.md
# Generates executable tests

/test-heal tests/example.spec.ts
# Fixes any broken tests
```

---

## 🔒 SECURITY ANALYSIS

| Command | Usage | Description |
|---------|-------|-------------|
| `/security-analyze` | `/security-analyze` | **DEEP** - Security analysis with XML structure + ultrathink mode (Anthropic best practices) |
| `/security-audit` | `/security-audit` | Comprehensive security audit with compliance checking (OWASP, GDPR, SOC2) |
| `/security-review` | `/security-review` | Run automated security analysis with guardrails |
| `/security-scan` | `/security-scan` | Quick security scan (same as security-review) |

**Security Best Practice:**
```
/security-analyze
# Use before committing security-sensitive code
```

---

## 🛠️ DEVELOPMENT & DEBUGGING

| Command | Usage | Description |
|---------|-------|-------------|
| `/debug-issue` | `/debug-issue [description]` | Systematic debugging workflow with root cause analysis |
| `/optimize-performance` | `/optimize-performance` | Performance optimization analysis and recommendations |
| `/refactor-safe` | `/refactor-safe [file]` | Safe refactoring with automated validation |
| `/deploy-check` | `/deploy-check` | Pre-deployment validation checks (security, tests, config) |

---

## 🤖 AUTONOMOUS MODES (Use With Caution!)

| Command | Usage | Description |
|---------|-------|-------------|
| `/autonomous` | `/autonomous` | Enable autonomous mode with supervision |
| `/godmode` | `/godmode` | **MAXIMUM POWER** - Full autonomous capabilities (use carefully) |
| `/turbo` | `/turbo` | Turbo mode alias for autonomous |
| `/full-auto` | `/full-auto` | Full automation mode |
| `/stop` | `/stop` | Stop autonomous/godmode operation |

**Warning:** Autonomous modes give me more control. Always review actions before approving.

---

## 🎯 PRODUCTIVITY & UTILITIES

| Command | Usage | Description |
|---------|-------|-------------|
| `/create-presentation` | `/create-presentation [topic]` | Generate professional PowerPoint presentations (.pptx) |
| `/improve-prompt` | `/improve-prompt [your-prompt]` | Claude Smart Improver - One-click prompt optimization |
| `/rate-me` | `/rate-me` | Comprehensive AI engineering performance review |
| `/web-fetch-fix` | `/web-fetch-fix [URL]` | Smart web fetching using Playwright (better than WebFetch) |

---

## 📊 USAGE PATTERNS

### Daily Development Pattern
```bash
# Morning
/load-global
/morning
[work on features]

# Every 10-20 messages
/compact  # (built-in command to reduce token usage)

# Before lunch/end of day
/save-session today "Current work description"

# After break
/resume-session today
```

### New Feature Development
```bash
/load-global full  # Load complete capabilities
/analyze           # Understand codebase
[implement feature]
/generate-tests    # Create tests
/security-analyze  # Security check
/deploy-check      # Pre-deployment validation
```

### Bug Fixing
```bash
/load-global
/debug-issue "Description of bug"
[fix bug]
/test-heal tests/affected.spec.ts
/deploy-check
```

### Code Review Session
```bash
/load-global
/review-code
/security-review
/analyze
```

---

## 💡 PRO TIPS

### Tip 1: Always Start with `/load-global`
```bash
# First message in any session
/load-global

# For maximum capabilities
/load-global full
```

### Tip 2: Save Sessions Before Context Switching
```bash
/save-session projectA "API endpoints done"
# Switch context
/save-session projectB "Frontend updates"
# Resume anytime
/resume-session projectA
```

### Tip 3: Use `/smart-resume` for Zero Compromise
```bash
# After any restart
/smart-resume
# Automatically detects what changed and loads only that
```

### Tip 4: Combine Commands
```bash
# Deep analysis workflow
/analyze
/security-analyze
/optimize-performance
```

### Tip 5: Use `/morning` for Daily Start
```bash
/morning
# Gets you: progress summary + AI news + motivation
```

---

## 🔥 MOST USEFUL COMMANDS (Top 10)

1. **`/load-global`** - Load all capabilities (use first!)
2. **`/save-session`** - Save work before breaks
3. **`/resume-session`** - Resume saved work
4. **`/analyze`** - Comprehensive code analysis
5. **`/security-analyze`** - Deep security review
6. **`/test-plan`** - Create test scenarios
7. **`/debug-issue`** - Systematic debugging
8. **`/morning`** - Daily briefing
9. **`/deploy-check`** - Pre-deployment validation
10. **`/ai-news`** - Stay updated on AI

---

## 🎯 QUICK START GUIDE

### First Time Setup:
```bash
$ claude
/load-global full
/mcp
# Verify all 13 MCPs are loaded
```

### Daily Usage:
```bash
$ claude
/resume-session yesterday
[work]
/save-session today "What you accomplished"
```

### Before Major Work:
```bash
/load-global full
/analyze
/security-analyze
```

---

## 📁 WHERE SLASH COMMANDS LIVE

All commands are markdown files in:
```
.claude/commands/
├── load-global.md
├── save-session.md
├── resume-session.md
├── smart-resume.md
├── analyze.md
├── security-analyze.md
└── [38+ more commands...]
```

**Add Your Own:**
Create `.claude/commands/my-command.md` with instructions, then use `/my-command`!

---

## 🚀 TOKEN OPTIMIZATION STRATEGY

| Strategy | Tokens | Best For |
|----------|--------|----------|
| `/load-global` (lite) | 2-3K | Quick tasks |
| `/load-global full` | 15-20K | Complex work |
| `/resume-session` | 5K | Daily continuity |
| `/smart-resume` | 5-10K | Zero compromise |
| No resume (restart) | 82K+ | Avoid this! |

---

## 📖 EXAMPLES BY USE CASE

### Use Case: Implementing New Feature
```bash
/load-global full
/analyze
"I need to add user authentication with JWT"
[implement]
/generate-tests src/auth/
/security-analyze
/deploy-check
/save-session auth-feature "JWT auth complete"
```

### Use Case: Security Audit
```bash
/load-global
/security-audit
/security-analyze
/analyze
# Review all recommendations
```

### Use Case: Performance Optimization
```bash
/load-global
/analyze
/optimize-performance
# Implement optimizations
/test-heal tests/
```

### Use Case: Research & Planning
```bash
/ai-news
/research-video [YouTube URL]
/create-presentation "Research findings"
```

---

## 🎓 LEARNING PATH

**Beginner:**
1. `/load-global` - Understand basics
2. `/save-session` / `/resume-session` - Session management
3. `/analyze` - Code analysis
4. `/morning` - Daily routine

**Intermediate:**
5. `/test-plan` / `/test-generate` - Test automation
6. `/security-analyze` - Security awareness
7. `/debug-issue` - Systematic debugging
8. `/project` - Multi-project management

**Advanced:**
9. `/smart-resume` - Intelligent session management
10. `/autonomous` / `/godmode` - AI automation
11. `/improve-prompt` - Meta-optimization
12. Custom slash commands - Create your own!

---

## 🆘 TROUBLESHOOTING

**Problem: Command not working**
```bash
# Check if command file exists
dir .claude\commands\[command-name].md

# If missing, it may be in docs
# Or create your own!
```

**Problem: Lost session context**
```bash
/load-global full
# Reloads everything
```

**Problem: Too many tokens**
```bash
/compact
# Built-in command to compress context
```

**Problem: Need to switch projects**
```bash
/save-session current "Current state"
/project other-project
/resume-session other-state
```

---

## 📞 SUPPORT

- **Documentation:** `docs/` folder
- **Session Resume Guide:** `docs/SESSION-RESUME-STRATEGIES.md`
- **Hooks Guide:** `docs/HOOKS-GUIDE.md`
- **CLI Flags:** `docs/CLAUDE-CLI-FLAGS.md`

---

**Version:** 1.0
**Last Updated:** 2025-10-14
**Total Commands:** 38+
**Your Setup:** Windows PowerShell, 13 MCPs, 47 modules

---

## 🎯 REMEMBER

**Start every session with:**
```
/load-global
```

**Before any break:**
```
/save-session [name] "what you're working on"
```

**After any restart:**
```
/resume-session [name]
```

**That's it!** These three commands will save you 90%+ of your token budget! 🚀
