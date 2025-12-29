# Task Automation Guide

**Created**: 2025-10-01
**Location**: `tools/automation/`
**Purpose**: Automated maintenance and quality checks

---

## Features

✅ **Pre-Commit Hook** - Auto-format and lint before commits
✅ **Scheduled Tasks** - Cron-style automation
✅ **Auto-Cleanup** - Clean caches and temporary files

---

## Installation

### 1. Install Python Dependencies

```bash
pip install schedule
```

### 2. Optional Tools (for formatting/linting)

**Python**:
```bash
pip install black pylint
```

**Node.js**:
```bash
npm install -g prettier eslint
```

---

## Tool 1: Pre-Commit Hook

### What It Does

Runs before every Git commit to:
- **Format code** (Black for Python, Prettier for TypeScript/JS)
- **Lint code** (Pylint for Python, ESLint for TypeScript)
- **Check for secrets** (password, api_key, etc.)
- **Update timestamps** in markdown files

### Usage

**Manual run** (test without committing):
```bash
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
python tools/automation/pre-commit-hook.py
```

**Install as Git hook** (runs automatically on commit):
```bash
# Create hook file
echo "python tools/automation/pre-commit-hook.py" > .git/hooks/pre-commit

# Make executable (Git Bash)
chmod +x .git/hooks/pre-commit
```

### Output Example

```
============================================================
PRE-COMMIT HOOK - Claude Workspace
============================================================

[INFO] Checking 5 staged file(s)

[FORMAT] Checking 2 Python file(s)...
  [OK] Formatted: tools/automation/auto-cleanup.py
  [OK] Formatted: tools/git-automation.py

[LINT] Checking 2 Python file(s)...
  [OK] Linted: tools/automation/auto-cleanup.py
  [OK] Linted: tools/git-automation.py

[UPDATE] Checking 1 markdown file(s)...
  [OK] Updated timestamp: AUTOMATION-GUIDE.md

============================================================
[OK] All checks passed!
============================================================
```

---

## Tool 2: Scheduled Tasks

### What It Does

Runs maintenance tasks on schedule:

**Daily (9:00 AM)**:
- Check for system updates
- Run security scan

**Weekly (Friday 5:00 PM)**:
- Clean build outputs
- Archive old sessions
- Check for dependency updates

### Usage

**Run scheduler** (daemon mode):
```bash
python tools/automation/scheduled-tasks.py start
```

**Run specific task once**:
```bash
# Daily checks
python tools/automation/scheduled-tasks.py run --task daily

# Weekly cleanup
python tools/automation/scheduled-tasks.py run --task weekly

# Individual tasks
python tools/automation/scheduled-tasks.py run --task cleanup
python tools/automation/scheduled-tasks.py run --task archive
python tools/automation/scheduled-tasks.py run --task update
python tools/automation/scheduled-tasks.py run --task security
```

### Available Tasks

| Task | Description | Schedule |
|------|-------------|----------|
| `daily` | System updates + security scan | Daily 9 AM |
| `weekly` | Full cleanup + archival + updates | Friday 5 PM |
| `cleanup` | Clean build outputs | Manual/Weekly |
| `archive` | Archive old sessions (>30 days) | Manual/Weekly |
| `update` | Check dependency updates | Manual/Weekly |
| `security` | Security vulnerability scan | Manual/Daily |

### Output Example

```
============================================================
WEEKLY CLEANUP START
============================================================
[2025-10-01 17:00:00] [CLEANUP] Starting build outputs cleanup...
[2025-10-01 17:00:15]   [OK] Removed dist from active-genie-nginx (45.2 MB)
[2025-10-01 17:00:20]   [OK] Removed .angular from active-genie-nginx (12.8 MB)
[2025-10-01 17:00:21] [OK] Cleanup complete: 2 directories, 58.0 MB freed

[2025-10-01 17:00:22] [ARCHIVE] Archiving old sessions...
[2025-10-01 17:00:25] [OK] Archived 3 old session(s)

[2025-10-01 17:00:26] [UPDATE] Checking for dependency updates...
[2025-10-01 17:00:30]   [CHECK] active-genie-nginx (Node.js)
[2025-10-01 17:00:35]     Outdated packages:
                          @angular/core  19.0.0 → 20.0.0
[2025-10-01 17:00:36] [OK] Dependency check complete
============================================================
WEEKLY CLEANUP COMPLETE
============================================================
```

### Running as Background Service

**Windows** (Task Scheduler):
```bash
# Create a scheduled task to run at startup
schtasks /create /tn "ClaudeScheduledTasks" /tr "python C:\Users\...\tools\automation\scheduled-tasks.py start" /sc onstart
```

**Linux/Mac** (systemd or launchd):
```bash
# Create a service file
# See systemd/launchd documentation
```

---

## Tool 3: Auto-Cleanup

### What It Does

Cleans up temporary files and caches:
- **Node.js caches** (`node_modules/.cache`)
- **Angular cache** (`.angular/`)
- **Python cache** (`__pycache__`, `*.pyc`)
- **Old log files** (>7 days)
- **Temp files** (`*.tmp`, `.DS_Store`, `Thumbs.db`)
- **Build outputs** (`dist/`, `build/`) - with `--all` flag
- **npm cache** - with `--all` flag

### Usage

**Safe cleanup** (caches and temp files only):
```bash
python tools/automation/auto-cleanup.py
```

**Aggressive cleanup** (includes build outputs):
```bash
python tools/automation/auto-cleanup.py --all
```

**Dry run** (see what would be deleted):
```bash
python tools/automation/auto-cleanup.py --dry-run
python tools/automation/auto-cleanup.py --dry-run --all
```

### Output Example

```
============================================================
AUTO-CLEANUP ROUTINE START
============================================================
[2025-10-01 14:30:00] [CLEAN] Node.js cache directories...
[2025-10-01 14:30:05]   [OK] Removed cache from active-genie-nginx (23.5 MB)

[2025-10-01 14:30:06] [CLEAN] Angular cache directories...
[2025-10-01 14:30:10]   [OK] Removed .angular from active-genie-nginx (12.8 MB)

[2025-10-01 14:30:11] [CLEAN] Python cache files...
[2025-10-01 14:30:12]   [OK] Removed tools/__pycache__ (0.5 MB)
[2025-10-01 14:30:13]   [OK] Removed tools/automation/__pycache__ (0.3 MB)

[2025-10-01 14:30:14] [CLEAN] Old log files...
[2025-10-01 14:30:15]   [OK] Removed tools/automation/old.log (2.1 KB)

[2025-10-01 14:30:16] [CLEAN] Temporary files...
[2025-10-01 14:30:17]   [OK] Removed .DS_Store
[2025-10-01 14:30:18]   [OK] Removed temp.tmp

============================================================
[OK] Cleanup complete:
  Files removed: 5
  Directories removed: 3
  Space freed: 36.8 MB
============================================================
```

---

## Common Workflows

### Workflow 1: Daily Development

```bash
# Morning - run daily checks
python tools/automation/scheduled-tasks.py run --task daily

# Work on code...
# ... edit files ...

# Commit (pre-commit hook runs automatically if installed)
git add .
git commit -m "Implemented feature X"
# → Auto-formats, lints, checks for secrets
# → Updates timestamps

# End of day - cleanup
python tools/automation/auto-cleanup.py
```

---

### Workflow 2: Weekly Maintenance

```bash
# Friday evening - full cleanup
python tools/automation/scheduled-tasks.py run --task weekly
# → Cleans build outputs
# → Archives old sessions
# → Checks for updates
# → Runs security scan

# Review update recommendations
# Update dependencies if needed
```

---

### Workflow 3: Before Major Refactoring

```bash
# 1. Clean up workspace
python tools/automation/auto-cleanup.py --all

# 2. Create Git checkpoint
python tools/git-automation.py checkpoint --name "before-refactoring"

# 3. Refactor code
# ... make changes ...

# 4. Commit (pre-commit hook ensures quality)
git add .
git commit -m "Refactored authentication"

# 5. If something breaks - rollback
python tools/git-automation.py rollback --name "before-refactoring"
```

---

## Integration with Claude Code

### I Can Use These Tools Automatically!

When you ask me to work on projects, I can:

**Before starting**:
```python
# Clean up workspace
python tools/automation/auto-cleanup.py

# Create safety checkpoint
python tools/git-automation.py checkpoint --name "before-changes"
```

**While working**:
```python
# Pre-commit checks run automatically on git commit
# Or I can run manually:
python tools/automation/pre-commit-hook.py
```

**After completing work**:
```python
# Commit with quality checks
git add .
git commit -m "Completed feature X"
# → Pre-commit hook formats, lints, checks

# Cleanup build artifacts
python tools/automation/auto-cleanup.py
```

---

## Configuration

### Customize Pre-Commit Hook

Edit `tools/automation/pre-commit-hook.py`:

```python
# Add custom checks
def check_custom_pattern(self, files):
    """Your custom check."""
    for file in files:
        # Your logic here
        pass

# Register in run() method
checks = [
    ...existing...,
    ("Custom check", lambda: self.check_custom_pattern(staged_files)),
]
```

### Customize Scheduled Tasks

Edit `tools/automation/scheduled-tasks.py`:

```python
# Change schedule
schedule.every().day.at("08:00").do(self.daily_checks)  # 8 AM instead of 9 AM
schedule.every().monday.at("10:00").do(self.weekly_cleanup)  # Monday instead of Friday

# Add custom task
def my_custom_task(self):
    self.log("[CUSTOM] Running my task...")
    # Your logic here

# Schedule it
schedule.every().hour.do(self.my_custom_task)
```

### Customize Auto-Cleanup

Edit `tools/automation/auto-cleanup.py`:

```python
# Add custom cleanup patterns
def clean_custom_files(self):
    """Clean custom file patterns."""
    custom_patterns = ['*.custom', '*.old']
    # Your cleanup logic here

# Register in run() method
self.clean_custom_files()
```

---

## Troubleshooting

### Pre-Commit Hook Not Running

**Issue**: Git commit doesn't trigger hook

**Solution**:
```bash
# Verify hook exists
ls -la .git/hooks/pre-commit

# Make executable (Git Bash)
chmod +x .git/hooks/pre-commit

# Test manually
python tools/automation/pre-commit-hook.py
```

### Scheduled Tasks Not Running

**Issue**: Tasks don't run at scheduled times

**Solution**:
```bash
# Check if scheduler is running
ps aux | grep scheduled-tasks.py

# Run in foreground for debugging
python tools/automation/scheduled-tasks.py start

# Check logs
cat tools/automation/scheduled-tasks.log
```

### Cleanup Removes Too Much

**Issue**: Auto-cleanup deleted important files

**Solution**:
```bash
# Always dry-run first
python tools/automation/auto-cleanup.py --dry-run

# Avoid --all flag for daily cleanup
python tools/automation/auto-cleanup.py  # Safe mode

# Use --all only when needed
python tools/automation/auto-cleanup.py --all  # Aggressive
```

---

## Command Reference

### Pre-Commit Hook

```bash
# Manual run
python tools/automation/pre-commit-hook.py

# Install as Git hook
echo "python tools/automation/pre-commit-hook.py" > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Scheduled Tasks

```bash
# Start scheduler daemon
python tools/automation/scheduled-tasks.py start

# Run specific task once
python tools/automation/scheduled-tasks.py run --task <task_name>

# Available tasks: daily, weekly, cleanup, archive, update, security
```

### Auto-Cleanup

```bash
# Safe cleanup
python tools/automation/auto-cleanup.py

# Aggressive cleanup
python tools/automation/auto-cleanup.py --all

# Dry run
python tools/automation/auto-cleanup.py --dry-run
python tools/automation/auto-cleanup.py --dry-run --all

# Specify workspace path
python tools/automation/auto-cleanup.py --path "C:\path\to\workspace"
```

---

## Performance Impact

| Tool | CPU Impact | Disk I/O | Runtime | Frequency |
|------|------------|----------|---------|-----------|
| Pre-Commit Hook | Low | Low | 5-15 sec | Per commit |
| Scheduled Tasks | Very Low | Low | 2-5 min | Daily/Weekly |
| Auto-Cleanup | Low | Medium | 1-3 min | On-demand |

**Recommendation**:
- Pre-commit hook: Always enabled (minimal impact, high value)
- Scheduled tasks: Run as daemon (very low overhead)
- Auto-cleanup: Run weekly or on-demand (safe, predictable)

---

## Next Steps

**1. Install Pre-Commit Hook**:
```bash
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
echo "python tools/automation/pre-commit-hook.py" > .git/hooks/pre-commit
```

**2. Test Tools**:
```bash
# Test pre-commit
python tools/automation/pre-commit-hook.py

# Test cleanup (dry run)
python tools/automation/auto-cleanup.py --dry-run

# Test scheduled task
python tools/automation/scheduled-tasks.py run --task daily
```

**3. Enable Scheduler** (optional):
```bash
# Start in background (Windows)
start /B python tools/automation/scheduled-tasks.py start

# Or create Windows Task Scheduler entry
```

---

**Created**: 2025-10-01
**Status**: ✅ Ready to use
**Dependencies**: Python 3.7+, `schedule` package
**Optional**: black, pylint, prettier, eslint
