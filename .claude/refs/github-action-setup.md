# GitHub Action: @.claude on PRs

Enable @.claude mentions on PRs for code review, CLAUDE.md updates, and more.

## Quick Setup

```bash
/install-github-app
```

This guides you through installing the Claude GitHub App and workflow.

**Alternative:** Install directly from https://github.com/apps/claude

## Manual Setup

### 1. Create Workflow File

`.github/workflows/claude.yml`:

```yaml
name: Claude Code

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Claude Code
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Add API Key

1. Go to repo Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` secret with your API key

### 3. Usage Examples

**Code review:**
```
@claude please review this PR
```

**Update CLAUDE.md:**
```
@claude add to CLAUDE.md: always use async/await instead of .then()
```

**Fix issue:**
```
@claude fix the linting errors
```

**Explain code:**
```
@claude explain what this function does
```

## Team Workflow (Boris's Pattern)

During code review, tag @.claude to:
1. Add lessons learned to CLAUDE.md
2. Fix simple issues directly
3. Request additional tests
4. Suggest refactors

This creates "Compounding Engineering" - Claude learns from each PR.

## Advanced: Custom Instructions

Create `.github/claude-instructions.md`:

```markdown
# Claude PR Instructions

When reviewing PRs:
1. Check for security issues first
2. Verify tests exist for new code
3. Suggest CLAUDE.md updates for patterns
4. Be concise in comments
```

## Rate Limits

- Uses your API quota
- Consider caching for repeated requests
- Set up alerts for high usage

## References

- [Official Plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review)
- [Claude Code Docs](https://code.claude.com/docs/en/github-actions)
