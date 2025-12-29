# Monitoring & Alerts Guide

**Created**: 2025-10-01
**Location**: `tools/monitoring/`
**Purpose**: Real-time monitoring and proactive alerts

---

## Features

✅ **File Watcher** - Auto-trigger actions on file changes
✅ **Build Monitor** - Track build/test status
✅ **Alert Manager** - Email, desktop notifications, logs

---

## Installation

### 1. Install Python Dependencies

```bash
pip install watchdog
```

### 2. Configure Alerts (Optional)

```bash
# Generate config template
python tools/monitoring/alert-manager.py config --output tools/monitoring/alert-config.json

# Edit configuration
# For email: Add Gmail app password from https://myaccount.google.com/apppasswords
```

---

## Tool 1: File Watcher

### What It Does

Watches files for changes and triggers actions automatically:
- **TypeScript changes** → Run tests
- **Python changes** → Run linter
- **Markdown changes** → Update timestamps

### Usage

**Generate config template**:
```bash
python tools/monitoring/file-watcher.py config --output file-watcher-config.json
```

**Start watching** (with default config):
```bash
python tools/monitoring/file-watcher.py start
```

**Start watching** (with custom config):
```bash
python tools/monitoring/file-watcher.py start --config file-watcher-config.json
```

### Example Configuration

`file-watcher-config.json`:
```json
{
  "watches": [
    {
      "name": "TypeScript files - Run tests",
      "path": "claude/projects/active-genie-nginx/src",
      "patterns": [".ts", ".tsx"],
      "debounce_seconds": 2,
      "actions": {
        "on_modify": {
          "command": "npm test -- --watch=false",
          "timeout": 120
        }
      }
    },
    {
      "name": "Python files - Run linter",
      "path": "tools",
      "patterns": [".py"],
      "debounce_seconds": 2,
      "actions": {
        "on_modify": {
          "command": "pylint {file}",
          "timeout": 30
        }
      }
    }
  ]
}
```

**Placeholders**:
- `{file}` - Full file path
- `{dir}` - Directory path
- `{name}` - File name

### Output Example

```
============================================================
FILE WATCHER - Claude Workspace
============================================================

[WATCH] TypeScript files - Run tests
  Path: C:\...\claude\projects\active-genie-nginx\src
  Patterns: .ts, .tsx

[WATCH] Python files - Run linter
  Path: C:\...\tools
  Patterns: .py

[INFO] Press Ctrl+C to stop watching

[2025-10-01 14:30:15] [MODIFIED] src/app/app.component.ts
[2025-10-01 14:30:15] [ACTION] on_modify: npm test -- --watch=false
[2025-10-01 14:30:45]   [OK] on_modify completed
```

---

## Tool 2: Build Monitor

### What It Does

Monitors build processes and tracks status:
- **Build tracking** - npm build, python setup
- **Test tracking** - npm test, pytest
- **Status persistence** - JSON status file
- **Watch mode** - Auto-rebuild on changes

### Usage

**Monitor single build**:
```bash
python tools/monitoring/build-monitor.py build \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm run build" \
  --timeout 600
```

**Monitor tests**:
```bash
python tools/monitoring/build-monitor.py test \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm test -- --watch=false" \
  --timeout 300
```

**Monitor all projects**:
```bash
python tools/monitoring/build-monitor.py all
```

**Show status**:
```bash
python tools/monitoring/build-monitor.py status
```

**Watch and rebuild** (auto-rebuild on file changes):
```bash
python tools/monitoring/build-monitor.py watch \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm run build"
```

### Output Example

```
============================================================
BUILD MONITOR - active-genie-nginx
============================================================
Command: npm run build
Path: C:\...\claude\projects\active-genie-nginx
Timeout: 600s
============================================================

[2025-10-01 14:30:00] [BUILD] Starting build for active-genie-nginx...
[2025-10-01 14:32:15] [OK] Build succeeded (135.2s)
Output:
✓ Browser application bundle generation complete
✓ Copying assets complete
✓ Index html generation complete

============================================================
TEST MONITOR - active-genie-nginx
============================================================
Command: npm test -- --watch=false
Path: C:\...\claude\projects\active-genie-nginx
Timeout: 300s
============================================================

[2025-10-01 14:32:20] [TEST] Running tests for active-genie-nginx...
[2025-10-01 14:33:45] [OK] Tests passed (85.3s)
Output:
✓ 42 tests passed
```

**Status output**:
```
============================================================
BUILD STATUS
============================================================

Project: active-genie-nginx
  build: [OK] (135.2s) - 2025-10-01 14:32:15
  test: [OK] (85.3s) - 2025-10-01 14:33:45

Project: PeopleSoft-RAG
  test: [OK] (12.5s) - 2025-10-01 14:35:00

============================================================
```

---

## Tool 3: Alert Manager

### What It Does

Sends alerts via multiple channels:
- **Desktop notifications** - Windows/Mac/Linux
- **Email alerts** - Gmail, SMTP
- **Log file** - Persistent alert history

### Usage

**Generate config template**:
```bash
python tools/monitoring/alert-manager.py config --output tools/monitoring/alert-config.json
```

**Send alert**:
```bash
# Info alert
python tools/monitoring/alert-manager.py send --level info --title "Build Complete" --message "Build succeeded"

# Warning alert (desktop notification)
python tools/monitoring/alert-manager.py send --level warning --title "Test Failed" --message "3 tests failing"

# Error alert (desktop notification)
python tools/monitoring/alert-manager.py send --level error --title "Build Failed" --message "Check build logs"

# Critical alert (desktop + email)
python tools/monitoring/alert-manager.py send --level critical --title "Production Down" --message "Server not responding"
```

**Test all channels**:
```bash
python tools/monitoring/alert-manager.py test
```

**With custom config**:
```bash
python tools/monitoring/alert-manager.py send --config alert-config.json --level error --title "Error" --message "Something went wrong"
```

### Configuration

`alert-config.json`:
```json
{
  "email": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from_email": "your-email@gmail.com",
    "to_email": "your-email@gmail.com",
    "password": "your-app-password"
  },
  "desktop": {
    "enabled": true
  },
  "log": {
    "enabled": true,
    "file": "tools/monitoring/alerts.log"
  }
}
```

**Enable email alerts**:
1. Go to https://myaccount.google.com/apppasswords
2. Generate app-specific password
3. Update `alert-config.json` with credentials
4. Set `"enabled": true`

### Alert Levels

| Level | Desktop | Email | Use Case |
|-------|---------|-------|----------|
| `info` | ❌ | ❌ | Informational messages |
| `warning` | ✅ | ❌ | Non-critical issues |
| `error` | ✅ | ❌ | Build failures, test failures |
| `critical` | ✅ | ✅ | Production issues, system down |

---

## Common Workflows

### Workflow 1: Auto-Test on Changes

**Setup**:
```bash
# Create watcher config
cat > file-watcher-config.json << EOF
{
  "watches": [
    {
      "name": "Auto-test TypeScript",
      "path": "claude/projects/active-genie-nginx/src",
      "patterns": [".ts", ".tsx"],
      "debounce_seconds": 3,
      "actions": {
        "on_modify": {
          "command": "npm test -- --watch=false",
          "timeout": 120
        }
      }
    }
  ]
}
EOF

# Start watching
python tools/monitoring/file-watcher.py start --config file-watcher-config.json
```

**Result**: Tests run automatically when you save TypeScript files

---

### Workflow 2: Continuous Build Monitoring

**Setup**:
```bash
# Watch and rebuild on changes
python tools/monitoring/build-monitor.py watch \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm run build"
```

**Result**: Automatic rebuild on file changes, instant feedback

---

### Workflow 3: Scheduled Build Checks

**Setup** (add to scheduled-tasks.py):
```python
def check_builds(self):
    """Check all project builds."""
    import subprocess
    result = subprocess.run([
        'python', 'tools/monitoring/build-monitor.py', 'all'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        # Send alert on failure
        subprocess.run([
            'python', 'tools/monitoring/alert-manager.py', 'send',
            '--level', 'error',
            '--title', 'Build Failed',
            '--message', result.stderr
        ])

# Schedule daily at 9 AM
schedule.every().day.at("09:00").do(self.check_builds)
```

**Result**: Daily build checks with alerts on failure

---

## Integration Example

### Combined: Watch + Build + Alert

**Script**: `watch-and-alert.sh` (Git Bash)
```bash
#!/bin/bash

# Watch TypeScript files
python tools/monitoring/file-watcher.py start --config file-watcher-config.json &
WATCHER_PID=$!

# Monitor builds
python tools/monitoring/build-monitor.py watch \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm run build" &
MONITOR_PID=$!

# Cleanup on exit
trap "kill $WATCHER_PID $MONITOR_PID" EXIT

echo "Monitoring active. Press Ctrl+C to stop."
wait
```

---

## Integration with Claude Code

### I Can Use These Tools Automatically!

When working on projects, I can:

**Before making changes**:
```python
# Start file watcher
python tools/monitoring/file-watcher.py start --config file-watcher-config.json
# → Auto-tests run as I make changes
```

**While building**:
```python
# Monitor build
python tools/monitoring/build-monitor.py build \
  --project "active-genie-nginx" \
  --path "claude/projects/active-genie-nginx" \
  --command "npm run build"

# Check status
python tools/monitoring/build-monitor.py status
```

**On errors**:
```python
# Send alert
python tools/monitoring/alert-manager.py send \
  --level error \
  --title "Build Failed" \
  --message "Compilation errors detected"
```

---

## Troubleshooting

### File Watcher Not Detecting Changes

**Issue**: Files change but actions don't trigger

**Solution**:
```bash
# Check file is in watched path
# Check pattern matches file extension
# Reduce debounce_seconds in config
# Check command is valid
```

### Build Monitor Timeouts

**Issue**: Builds timeout before completion

**Solution**:
```bash
# Increase timeout
python tools/monitoring/build-monitor.py build \
  --project "..." \
  --path "..." \
  --command "..." \
  --timeout 900  # 15 minutes
```

### Desktop Notifications Not Working

**Windows**:
- Check Windows notification settings
- Allow notifications for PowerShell

**Mac**:
- Grant Terminal notification permissions in System Preferences

**Linux**:
- Install `notify-send`: `sudo apt install libnotify-bin`

### Email Alerts Not Sending

**Issue**: Email configuration fails

**Solution**:
```bash
# For Gmail:
# 1. Enable 2FA
# 2. Generate app password: https://myaccount.google.com/apppasswords
# 3. Use app password in config (not regular password)
# 4. Set "enabled": true

# Test email
python tools/monitoring/alert-manager.py test
```

---

## Command Reference

### File Watcher

```bash
# Generate config
python tools/monitoring/file-watcher.py config --output <path>

# Start watching
python tools/monitoring/file-watcher.py start [--config <path>]
```

### Build Monitor

```bash
# Monitor single build
python tools/monitoring/build-monitor.py build --project <name> --path <path> --command <cmd> [--timeout <sec>]

# Monitor tests
python tools/monitoring/build-monitor.py test --project <name> --path <path> --command <cmd> [--timeout <sec>]

# Monitor all projects
python tools/monitoring/build-monitor.py all

# Show status
python tools/monitoring/build-monitor.py status

# Watch and rebuild
python tools/monitoring/build-monitor.py watch --project <name> --path <path> --command <cmd>
```

### Alert Manager

```bash
# Generate config
python tools/monitoring/alert-manager.py config --output <path>

# Send alert
python tools/monitoring/alert-manager.py send --level <level> --title <title> --message <message> [--config <path>]

# Test alerts
python tools/monitoring/alert-manager.py test [--config <path>]
```

---

## Performance Impact

| Tool | CPU Impact | Memory | Use Case |
|------|------------|--------|----------|
| File Watcher | Very Low | ~10 MB | Continuous development |
| Build Monitor | Low-Medium | ~20 MB | On-demand or scheduled |
| Alert Manager | Minimal | ~5 MB | Event-driven |

**Recommendation**:
- File watcher: Run during active development only
- Build monitor: Use watch mode or scheduled checks
- Alert manager: Always available (minimal overhead)

---

## Requirements

```bash
# Install dependencies
pip install -r tools/monitoring/requirements.txt
```

`requirements.txt`:
```
watchdog>=3.0.0
```

---

## Next Steps

**1. Install Dependencies**:
```bash
pip install watchdog
```

**2. Test Tools**:
```bash
# Test file watcher
python tools/monitoring/file-watcher.py config
python tools/monitoring/file-watcher.py start

# Test build monitor
python tools/monitoring/build-monitor.py status

# Test alerts
python tools/monitoring/alert-manager.py test
```

**3. Configure for Your Projects**:
```bash
# Generate configs
python tools/monitoring/file-watcher.py config --output file-watcher-config.json
python tools/monitoring/alert-manager.py config --output tools/monitoring/alert-config.json

# Edit configs
# Start monitoring
```

---

**Created**: 2025-10-01
**Status**: ✅ Ready to use
**Dependencies**: Python 3.7+, watchdog
**Optional**: Email SMTP credentials
