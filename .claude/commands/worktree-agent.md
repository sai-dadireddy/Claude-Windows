# Worktree Agent

Spawn a background agent that works in an isolated git worktree. The agent will:
1. Create a new git worktree and branch
2. Work on the task in complete isolation
3. Commit changes to its own branch
4. Report back when done

## Usage

```
/worktree-agent <branch-name> <task-description>
```

## Examples

```
/worktree-agent feat-dark-theme Implement a dark theme for the application
/worktree-agent fix-auth-bug Fix the authentication timeout issue
/worktree-agent refactor-api Refactor the API layer to use async/await
```

## Instructions for Claude

When the user invokes this command with arguments `$ARGUMENTS`:

1. **Parse the arguments**: Extract `<branch-name>` (first word) and `<task-description>` (rest)

2. **Validate git repo**: Check we're in a git repository
   ```bash
   git rev-parse --git-dir
   ```

3. **Create the worktree**:
   ```bash
   git worktree add -b <branch-name> ../worktrees/<branch-name> HEAD
   ```

4. **Launch background agent** using the Task tool with `run_in_background: true`:

   ```
   Task(
     subagent_type: "autonomous-coder",
     run_in_background: true,
     description: "Worktree: <branch-name>",
     prompt: """
     You are working in an ISOLATED git worktree.

     WORKING DIRECTORY: ../worktrees/<branch-name>
     BRANCH: <branch-name>

     TASK: <task-description>

     WORKFLOW:
     1. cd to the worktree directory
     2. Understand the codebase structure
     3. Implement the requested changes
     4. Run any relevant tests
     5. Commit your changes with a descriptive message
     6. Report what you accomplished

     RULES:
     - Stay ONLY in your worktree directory
     - Do NOT modify the main branch
     - Commit frequently with clear messages
     - If you encounter blockers, document them and continue with what you can do

     When done, summarize:
     - What was implemented
     - Files changed
     - How to merge: git checkout main && git merge <branch-name>
     """
   )
   ```

5. **Inform the user**:
   ```
   Background agent started in worktree.

   Branch: <branch-name>
   Location: ../worktrees/<branch-name>

   Commands:
   - Check status: /tasks
   - View output: TaskOutput task_id="<id>"
   - Merge when done: git checkout main && git merge <branch-name>
   - Cleanup: git worktree remove ../worktrees/<branch-name>
   ```

## Managing Multiple Worktree Agents

```bash
# List all worktrees
git worktree list

# List running agents
/tasks

# Remove a worktree after merging
git worktree remove ../worktrees/<branch-name>
git branch -d <branch-name>  # optional: delete branch
```

## Best Practices

- Use descriptive branch names: `feat-`, `fix-`, `refactor-`, `experiment-`
- Keep tasks isolated - no dependencies between parallel agents
- Don't background tasks that need your input mid-execution
- Check `/tasks` periodically to monitor progress
- Merge or discard worktrees promptly to avoid stale branches
