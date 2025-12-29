Investigate a **GitHub Actions workflow failure** and suggest fixes.

## Input

Provide either:
- A GitHub Actions run URL (e.g., `https://github.com/owner/repo/actions/runs/12345`)
- A PR URL with failing checks
- Just say "check CI" to investigate the current branch

## Investigation Process

### 1. Get Failure Details

```bash
# If URL provided, extract run ID
gh run view <run-id> --log-failed

# Or list recent failed runs
gh run list --status failure --limit 5

# Get detailed logs
gh run view <run-id> --log
```

### 2. Analyze the Failure

Check for:
- **Test failures** - Which tests failed and why?
- **Build errors** - Compilation/bundling issues?
- **Lint/type errors** - Code quality failures?
- **Timeout** - Did it exceed time limits?
- **Flaky tests** - Has this test failed intermittently before?

### 3. Check for Flakiness

```bash
# Look at recent history of this workflow
gh run list --workflow <workflow-name> --limit 20

# Check if same test failed before
gh api repos/{owner}/{repo}/actions/runs --jq '.workflow_runs[] | select(.conclusion == "failure")'
```

### 4. Identify Root Cause

- **Code issue** - Bug introduced in this PR/commit
- **Environment issue** - CI environment problem
- **Flaky test** - Intermittent failure, may pass on retry
- **Dependency issue** - Package version conflict
- **Configuration issue** - Workflow YAML problem

## Output Format

```markdown
## GitHub Actions Failure Analysis

**Run:** [URL or ID]
**Workflow:** [Workflow name]
**Status:** [Failed/Cancelled/etc.]
**Duration:** [How long it ran]

### Failure Summary
[One-line description of what failed]

### Error Details
```
[Relevant error output]
```

### Root Cause
[What caused the failure]

### Is it Flaky?
[Yes/No - with evidence]

### Recommended Fix

**Option 1:** [Primary fix]
```bash
# Commands or code to fix
```

**Option 2:** [Alternative if Option 1 doesn't work]

### Prevention
[How to prevent this in the future]
```

---

**GitHub Actions URL or context:**

$ARGUMENTS
