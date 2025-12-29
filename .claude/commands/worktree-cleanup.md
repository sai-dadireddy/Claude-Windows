# Worktree Cleanup

Remove a git worktree and optionally delete its branch.

## Usage

```
/worktree-cleanup <branch-name> [--delete-branch]
```

## Examples

```
/worktree-cleanup feat-dark-theme
/worktree-cleanup fix-auth-bug --delete-branch
```

## Instructions for Claude

When the user invokes this command with arguments `$ARGUMENTS`:

1. **Parse arguments**: Extract branch name and flags

2. **Check if worktree exists**:
   ```bash
   git worktree list | grep <branch-name>
   ```

3. **Check for uncommitted changes**:
   ```bash
   cd ../worktrees/<branch-name> && git status --short
   ```

4. **If uncommitted changes exist**, warn the user:
   ```
   Warning: Worktree has uncommitted changes:
   - file1.ts
   - file2.ts

   Options:
   1. Commit first: cd ../worktrees/<branch-name> && git add . && git commit -m "WIP"
   2. Force remove: git worktree remove --force ../worktrees/<branch-name>
   3. Cancel cleanup
   ```

5. **Remove the worktree**:
   ```bash
   git worktree remove ../worktrees/<branch-name>
   ```

6. **If --delete-branch flag**, also delete the branch:
   ```bash
   git branch -d <branch-name>
   # or -D if unmerged and user confirms
   ```

7. **Confirm cleanup**:
   ```
   Cleaned up:
   - Removed worktree: ../worktrees/<branch-name>
   - Deleted branch: <branch-name> (if requested)
   ```
