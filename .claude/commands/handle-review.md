# Handle Code Review Feedback

Process and respond to code review comments systematically.

## Workflow

### 1. Gather Feedback
```bash
gh pr view <pr-number> --comments
```

### 2. Categorize Comments

| Type | Priority | Response |
|------|----------|----------|
| **Bug/Error** | P0 | Fix immediately |
| **Security** | P0 | Fix immediately |
| **Logic issue** | P1 | Fix before merge |
| **Style/Convention** | P2 | Fix if quick |
| **Suggestion** | P3 | Consider, respond |
| **Question** | - | Answer in comment |

### 3. Batch Fixes
```bash
# Fixup commits for easy review
git commit --fixup <original-commit>

# Or single commit for all feedback
git add -A && git commit -m "fix: address PR feedback

- Fixed X per reviewer comment
- Updated Y as suggested"
```

### 4. Update PR
```bash
git push origin <branch>
gh pr comment <pr-number> --body "Addressed feedback. Ready for re-review."
```

### 5. Disagreement Protocol
1. Never dismiss without explanation
2. Provide technical rationale
3. Offer compromise if possible
4. Escalate to team if stalemate

## Usage
```
/handle-review <pr-number>
```
