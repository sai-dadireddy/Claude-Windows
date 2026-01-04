# Commit, Push and Create PR

Fast workflow command with inline bash precomputation (Boris's pattern).

## Pre-computed Context

```bash
# Git status
git status --short

# Current branch
git branch --show-current

# Recent commits on this branch
git log --oneline -5

# Diff stats
git diff --stat HEAD~1 2>/dev/null || git diff --stat --cached
```

## Workflow

Based on the context above:

1. **If uncommitted changes exist:**
   - Stage all changes: `git add -A`
   - Create commit with descriptive message following repo conventions
   - Message format: `type: description` (feat/fix/refactor/docs/test/chore)

2. **Push to remote:**
   - Push current branch: `git push -u origin $(git branch --show-current)`

3. **Create PR:**
   - Use `gh pr create` with:
     - Title matching commit message
     - Body with Summary and Test Plan sections
     - Use HEREDOC for body formatting

## PR Template

```bash
gh pr create --title "type: description" --body "$(cat <<'EOF'
## Summary
- Brief description of changes

## Test Plan
- [ ] Tests pass
- [ ] Manual verification complete

---
Generated with Claude Code
EOF
)"
```

## Options

- `--draft` - Create as draft PR
- `--reviewer @username` - Request review
- `--label bug|feature` - Add labels

## Usage

```
/commit-push-pr
/commit-push-pr --draft
/commit-push-pr --reviewer @teammate
```
