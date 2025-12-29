Analyze the current project state and suggest the most valuable next action.

## Analysis Steps

### 1. Check Current Context
- Read any existing CLAUDE.md or README
- Check git status for uncommitted work
- Look for TODO comments or FIXME markers
- Check for failing tests or lint errors

### 2. Identify Project State
- Is this a new project (minimal files)?
- Is there work in progress (dirty git state)?
- Are there open issues or PRs?
- Are there obvious gaps (no tests, no types, etc.)?

### 3. Check for Blockers
```bash
# Uncommitted changes?
git status

# Failing tests?
npm test 2>&1 | head -50  # or equivalent

# Lint errors?
npm run lint 2>&1 | head -50  # or equivalent
```

## Output Format

```markdown
## Project State Assessment

**Current Branch:** [branch name]
**Git Status:** [clean/dirty with summary]
**Last Commit:** [commit message]

### Immediate Blockers
[Any failing tests, lint errors, uncommitted changes]

### Suggested Next Actions

#### Option 1: [Most Valuable Action] ⭐ RECOMMENDED
**Why:** [Reasoning]
**Command:** `[command to run]` or [steps to take]
**Effort:** [Low/Medium/High]

#### Option 2: [Alternative Action]
**Why:** [Reasoning]
**Effort:** [Low/Medium/High]

#### Option 3: [Another Option]
**Why:** [Reasoning]
**Effort:** [Low/Medium/High]

### Technical Debt Spotted
- [Item 1]
- [Item 2]

### Questions to Consider
- [Question that might unblock or clarify direction]
```

---

Analyze the current project and suggest what to do next.
