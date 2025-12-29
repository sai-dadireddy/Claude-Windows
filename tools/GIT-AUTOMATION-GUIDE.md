# Git Automation Tool - User Guide

**Created**: 2025-10-01
**Location**: `tools/git-automation.py`
**Purpose**: Safe, automated Git operations with checkpoints and rollback

---

## Features

✅ **Auto-commit** - Commit changes with smart messages
✅ **Checkpoints** - Create named save points
✅ **Rollback** - Safely undo changes
✅ **Auto-init** - Initialize Git repos automatically
✅ **Smart .gitignore** - Exclude build outputs, caches

---

## Installation

**Requirements**: Git 2.0+ (already installed ✓)

**No Python packages needed** - uses built-in libraries only

---

## Usage

### 1. Initialize Git Repository

```bash
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
python tools/git-automation.py init
```

**What it does**:
- Initializes Git repository
- Creates .gitignore (node_modules, dist, .claude, etc.)
- Ready for version control

---

### 2. Auto-Commit Changes

**Simple commit**:
```bash
python tools/git-automation.py commit
```

**With custom message**:
```bash
python tools/git-automation.py commit --message "Added feature X"
```

**What it does**:
- Stages all changes (`git add .`)
- Commits with descriptive message
- Adds Claude Code attribution

---

### 3. Create Checkpoints (Save Points)

**Auto-named checkpoint**:
```bash
python tools/git-automation.py checkpoint
```
Creates: `checkpoint_20251001_143022`

**Named checkpoint**:
```bash
python tools/git-automation.py checkpoint --name "before-refactoring"
```

**What it does**:
- Commits current changes
- Creates Git tag
- Safe point to rollback to

---

### 4. List Checkpoints

```bash
python tools/git-automation.py list
```

**Output**:
```
Checkpoints (3):
  checkpoint_20251001_143022: a1b2c3d 2025-10-01 14:30:22 Checkpoint: auto
  before-refactoring: d4e5f6g 2025-10-01 15:45:10 Checkpoint: before-refactoring
  pre_rollback_safety: h7i8j9k 2025-10-01 16:20:05 Checkpoint: pre_rollback_safety
```

---

### 5. Rollback to Checkpoint

```bash
python tools/git-automation.py rollback --name "before-refactoring"
```

**What it does**:
- Creates safety checkpoint (if you have uncommitted changes)
- Resets to selected checkpoint
- **WARNING**: Discards changes after checkpoint

---

### 6. Undo Last Commit

**Keep changes in working directory**:
```bash
python tools/git-automation.py undo
```

**What it does**:
- Rolls back last commit
- Keeps changes staged
- Safe undo (can re-commit)

---

### 7. Check Status

```bash
python tools/git-automation.py status
```

**Output**:
```
Changes:
 M CLAUDE.md
 M tools/git-automation.py
?? NEW-FILE.md
```

---

### 8. Show Recent Log

```bash
python tools/git-automation.py log
```

**Output**:
```
Recent commits (last 10):
a1b2c3d (HEAD -> main, tag: checkpoint_20251001_143022) Auto-commit: 2025-10-01 14:30:22
d4e5f6g Added Git automation tool
h7i8j9k Initial commit
```

---

## Common Workflows

### Safe Experimentation

```bash
# 1. Create checkpoint before risky change
python tools/git-automation.py checkpoint --name "before-experiment"

# 2. Make experimental changes
# ... edit files ...

# 3a. If experiment works - commit it
python tools/git-automation.py commit --message "Successful experiment"

# 3b. If experiment fails - rollback
python tools/git-automation.py rollback --name "before-experiment"
```

---

### Regular Development

```bash
# Work on features
# ... edit files ...

# Commit regularly
python tools/git-automation.py commit --message "Implemented feature X"

# Create checkpoints at milestones
python tools/git-automation.py checkpoint --name "feature-x-complete"
```

---

### Fix Mistakes

**Undo last commit (keep changes)**:
```bash
python tools/git-automation.py undo
# Edit files
python tools/git-automation.py commit --message "Fixed commit"
```

**Rollback to earlier checkpoint**:
```bash
python tools/git-automation.py list
python tools/git-automation.py rollback --name "checkpoint_name"
```

---

## Integration with Claude Code

### I Can Use It Automatically!

When you ask me to make changes, I can:

**Before changes**:
```python
# I run this before risky refactoring
python tools/git-automation.py checkpoint --name "before-refactoring"
```

**After changes**:
```python
# I commit completed work
python tools/git-automation.py commit --message "Refactored authentication logic"
```

**If something breaks**:
```python
# I can rollback
python tools/git-automation.py rollback --name "before-refactoring"
```

---

## Safety Features

### 1. Auto-Safety Checkpoint

When rolling back with uncommitted changes:
```
⚠️  WARNING: You have uncommitted changes!
Creating safety checkpoint before rollback...
✓ Created checkpoint: pre_rollback_safety
✓ Rolled back to checkpoint: before-refactoring
```

### 2. Protected Files

`.gitignore` automatically excludes:
- `node_modules/` - Dependencies (regenerable)
- `dist/` - Build outputs
- `.angular/` - Build cache
- `.claude/` - Claude cache
- `*.log` - Log files
- `*.env` - Sensitive environment files

### 3. Non-Destructive Undo

`undo` command keeps changes:
```bash
python tools/git-automation.py undo
# Changes still in staging area
# Can re-commit with different message
```

---

## Examples

### Example 1: Daily Work

```bash
# Morning - check status
python tools/git-automation.py status

# Work on features
# ... code ...

# Commit at lunch
python tools/git-automation.py commit --message "WIP: Feature X progress"

# Afternoon - more work
# ... code ...

# End of day - checkpoint
python tools/git-automation.py checkpoint --name "end-of-day-2025-10-01"
python tools/git-automation.py commit --message "Completed feature X"
```

### Example 2: Risky Refactoring

```bash
# Create safety checkpoint
python tools/git-automation.py checkpoint --name "before-big-refactor"

# Refactor code
# ... make changes ...

# Test if it works
npm run build
npm test

# If tests pass - commit
python tools/git-automation.py commit --message "Refactored for performance"

# If tests fail - rollback
python tools/git-automation.py rollback --name "before-big-refactor"
```

### Example 3: Experiment with Different Approaches

```bash
# Try approach A
python tools/git-automation.py checkpoint --name "try-approach-a"
# ... implement approach A ...
python tools/git-automation.py commit --message "Approach A implementation"

# Doesn't work well, try approach B
python tools/git-automation.py checkpoint --name "try-approach-b"
python tools/git-automation.py rollback --name "try-approach-a"
# ... implement approach B ...
python tools/git-automation.py commit --message "Approach B implementation"

# Approach B is better - continue with it
```

---

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize Git repo | `python tools/git-automation.py init` |
| `commit` | Auto-commit changes | `python tools/git-automation.py commit -m "Message"` |
| `checkpoint` | Create save point | `python tools/git-automation.py checkpoint -n "name"` |
| `list` | List checkpoints | `python tools/git-automation.py list` |
| `rollback` | Rollback to checkpoint | `python tools/git-automation.py rollback -n "name"` |
| `undo` | Undo last commit | `python tools/git-automation.py undo` |
| `status` | Show Git status | `python tools/git-automation.py status` |
| `log` | Show commit history | `python tools/git-automation.py log` |

---

## Troubleshooting

### "Not a git repository"

**Solution**: Run `init` first:
```bash
python tools/git-automation.py init
```

### "Checkpoint 'name' not found"

**Solution**: List available checkpoints:
```bash
python tools/git-automation.py list
```

### Want to work on specific project

**Use `--path` flag**:
```bash
python tools/git-automation.py commit --path "claude/projects/active-genie-nginx" --message "Updated Angular app"
```

---

## Next Steps

**1. Initialize Claude Root**:
```bash
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
python tools/git-automation.py init
python tools/git-automation.py commit --message "Initial commit - Claude workspace"
```

**2. Create First Checkpoint**:
```bash
python tools/git-automation.py checkpoint --name "baseline-2025-10-01"
```

**3. Use in Daily Workflow**:
- Commit after completing tasks
- Checkpoint before risky changes
- Rollback if something breaks

---

**Created**: 2025-10-01
**Status**: ✅ Ready to use
**Time to implement**: 2 hours
**Time saved**: 30+ min/week (safe experimentation, easy rollback)
