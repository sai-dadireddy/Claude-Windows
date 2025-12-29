Diagnose and fix a **bug** using a structured severity-adaptive workflow.

## Input

Describe the bug:
- What's the symptom? (error message, unexpected behavior)
- When does it happen? (always, sometimes, specific conditions)
- Any error logs or stack traces?

## Diagnostic Process

### Phase 1: Symptom Analysis

```markdown
## Bug Diagnosis

**Reported Symptom:** [User's description]
**Severity Assessment:** [Critical/High/Medium/Low]

### Reproduction Steps
1. [Step to reproduce]
2. [Step to reproduce]
3. [Expected vs Actual behavior]

### Error Evidence
```
[Error logs, stack traces, screenshots mentioned]
```
```

### Phase 2: Impact Assessment

```markdown
### Impact Analysis

| Dimension | Impact | Notes |
|-----------|--------|-------|
| Users Affected | [All/Some/Few] | [Details] |
| Data Risk | [High/Med/Low] | [Potential data loss?] |
| System Stability | [High/Med/Low] | [Cascading failures?] |
| Business Impact | [High/Med/Low] | [Revenue, reputation?] |

**Overall Severity:** [CRITICAL/HIGH/MEDIUM/LOW]
```

### Phase 3: Root Cause Analysis

```markdown
### Root Cause Investigation

**Hypothesis 1:** [Most likely cause]
- Evidence: [What supports this]
- Files: `path/to/suspect/file.ts`

**Hypothesis 2:** [Alternative cause]
- Evidence: [What supports this]
- Files: `path/to/other/file.ts`

**Confirmed Root Cause:** [After investigation]
```

### Phase 4: Fix Plan

```markdown
### Fix Strategy

**Approach:** [Description of the fix]

**Files to Modify:**
| File | Change | Risk |
|------|--------|------|
| `path/to/file` | [What to change] | [Low/Med/High] |

**Regression Risks:**
- [Potential side effect 1]
- [Potential side effect 2]

**Verification Steps:**
1. [How to verify the fix works]
2. [How to check for regressions]
```

### Phase 5: Execution

**For CRITICAL/HIGH severity:**
- Apply fix immediately
- Add regression test
- Verify in isolation before broader testing

**For MEDIUM/LOW severity:**
- Review fix plan with user
- Apply fix
- Run existing tests

## Hotfix Mode

Add `--hotfix` for production emergencies:
- Skip detailed analysis
- Focus on immediate mitigation
- Document for follow-up

## Output Artifacts

Save findings to project:
- `BUGFIX-[date]-diagnosis.md` (optional, for complex bugs)

---

**Bug to fix:**

$ARGUMENTS
