Perform **non-destructive verification** of the current implementation plan.

## What This Verifies

Run consistency checks WITHOUT making changes:

### 1. Requirements Coverage
```markdown
## Requirements Verification

| Requirement | Covered By | Status |
|-------------|------------|--------|
| [Req 1] | [Task/File] | ✅/❌ |
| [Req 2] | [Task/File] | ✅/❌ |

**Coverage:** X/Y requirements addressed
```

### 2. Task Dependencies
```markdown
## Dependency Analysis

### Dependency Chain
```
Task A (no deps)
  └── Task B (depends on A)
      └── Task C (depends on B)
Task D (parallel to A)
```

### Issues Found
- [ ] Circular dependency: [Task X ↔ Task Y]
- [ ] Missing dependency: [Task Z needs Task W first]
- [ ] Orphan task: [Task Q has no connection]
```

### 3. File Consistency
```markdown
## File Analysis

### Files to Create
| File | Created By | Depends On |
|------|------------|------------|
| `path/to/new.ts` | Task 1 | - |

### Files to Modify
| File | Modified By | Conflicts? |
|------|-------------|------------|
| `path/to/existing.ts` | Task 2, Task 3 | ⚠️ Check |

### Potential Conflicts
- [ ] `file.ts` modified by multiple tasks - need ordering
```

### 4. Specification Quality
```markdown
## Specification Check

### Ambiguous Items
- [ ] [Unclear requirement 1]
- [ ] [Vague acceptance criteria]

### Missing Details
- [ ] Error handling not specified for [X]
- [ ] Edge cases not covered for [Y]

### Assumptions Made
- [Assumption 1] - needs confirmation
- [Assumption 2] - needs confirmation
```

### 5. Risk Assessment
```markdown
## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

### High-Risk Areas
- [ ] [Area 1]: [Why it's risky]
- [ ] [Area 2]: [Why it's risky]
```

## Verification Summary

```markdown
## Plan Verification Results

**Overall Status:** ✅ Ready / ⚠️ Issues Found / ❌ Not Ready

### Summary
- Requirements: X/Y covered
- Dependencies: [OK/Issues]
- Conflicts: [None/X potential]
- Risks: [Low/Medium/High]

### Action Items Before Execution
1. [ ] [Fix issue 1]
2. [ ] [Clarify requirement 2]
3. [ ] [Add missing task 3]

### Recommendation
[Proceed / Fix issues first / Needs replanning]
```

---

**Verify the plan for:**

$ARGUMENTS
