# Worktree List

List all git worktrees and their status, including any running background agents.

## Usage

```
/worktree-list
```

## Instructions for Claude

When the user invokes this command:

1. **List git worktrees**:
   ```bash
   git worktree list
   ```

2. **Check for running agents**:
   Use `/tasks` to see background agents

3. **Show status** in a table format:
   ```
   | Worktree | Branch | Status | Agent |
   |----------|--------|--------|-------|
   | ../worktrees/feat-dark-theme | feat-dark-theme | clean | running |
   | ../worktrees/fix-auth | fix-auth | 3 uncommitted | done |
   ```

4. **Provide actions**:
   ```
   Actions:
   - Merge: git merge <branch-name>
   - Remove: git worktree remove <path> && git branch -d <branch>
   - Check agent: TaskOutput task_id="<id>"
   ```
