# Finish Branch Workflow

Complete a development branch with proper merge/PR decision flow.

## Workflow

### 1. Pre-flight Checks
```bash
git status
git log --oneline main..HEAD
git diff main --stat
```

### 2. Decision Matrix

| Condition | Action |
|-----------|--------|
| Small fix, <3 commits | Squash merge to main |
| Feature complete, reviewed | Create PR |
| WIP, needs more work | Continue development |
| Conflicts exist | Resolve first |

### 3. Execute

**Option A: Direct Merge (small fixes)**
```bash
git checkout main && git pull origin main
git merge --squash <branch>
git commit -m "feat: <description>"
git push origin main
git branch -d <branch>
```

**Option B: Create PR**
```bash
git push -u origin <branch>
gh pr create --title "<title>" --body "## Summary
<description>

## Test Plan
- [ ] Tests pass
- [ ] Manual verification"
```

### 4. Post-completion
- Update Beads: `bd close <id>`
- Remove worktree: `git worktree remove <path>`

## Usage
```
/finish-branch [branch-name]
```
