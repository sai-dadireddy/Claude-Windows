---
description: Implement plan phase-by-phase - Phase 3 of 4-phase workflow
argument-hint: @thoughts/shared/plans/[file].md Phase [N]
allowed-tools: Read, Write, Edit, Bash, Task
model: sonnet
---

# Phase 3: Implement

**Goal:** Execute ONE phase at a time with confidence

**Plan:** $ARGUMENTS

---

## Critical Rule

**IMPLEMENT ONE PHASE AT A TIME!**

Never try to implement entire plan at once = recipe for disaster!

---

## Workflow

### Step 1: Read Plan (10 seconds)
```bash
Read plan from thoughts/shared/plans/
Extract Phase N specifications
Identify all files to modify
```

### Step 2: Read Required Files (30 seconds)
```bash
Read ONLY files mentioned in Phase N

Use line ranges when possible:
  Read file.ts --offset:100 --limit:50

NOT: Read entire codebase
```

### Step 3: Implement Changes (variable)
```bash
Make changes specified in Phase N

Follow plan exactly:
- File paths from plan
- Code snippets from plan
- Patterns from plan

If plan unclear → Ask questions, don't guess!
```

### Step 4: Automated Verification (30 seconds)
```bash
Run ALL automated checks from plan:

- [ ] Tests: npm test
- [ ] Lint: npm run lint
- [ ] Type check: tsc --noEmit
- [ ] Build: npm run build

Build hook catches errors automatically!

If errors found:
  → Fix them before proceeding
  → Build hook shows them to you
```

### Step 5: Manual Testing Prompt
```
Phase N Complete - Ready for Manual Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Automated verification passed:
  ✅ Tests pass
  ✅ No lint errors
  ✅ Type checking clean
  ✅ Build successful

Please perform manual verification:
  - [ ] Feature works as expected
  - [ ] No console errors
  - [ ] UX is smooth
  - [ ] Edge cases handled

Test the feature, then respond:
  - "Looks good, continue Phase 2" (if context < 60%)
  - "Looks good, clearing context" (if context > 60%)
  - "Issue: [description]" (if something's wrong)

Waiting for your verification...
```

### Step 6: Proceed or Clear
```bash
After manual testing:

If context < 60% AND more phases:
  → Continue to next phase in same session

If context > 60%:
  → MUST clear: /clear
  → Next session: /implement @thoughts/shared/plans/[file].md Phase N+1

If all phases complete:
  → Proceed to /validate
```

---

## Context Management

**Critical Thresholds:**

- <50%: ✅ Safe, continue
- 50-60%: ⚠️ Monitor, finish phase then clear
- >60%: 🔴 STOP! Clear immediately
- >70%: 🔴🔴 Quality degrading!

**Rule:** Clear between phases, not mid-phase!

---

## Output Example

```
Phase 1 Implementation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Modified:
  ✅ src/auth/AuthContext.tsx
  ✅ src/hooks/useAuth.ts
  ✅ src/api/auth.ts

Automated Verification:
  ✅ Tests pass (12/12)
  ✅ No lint errors
  ✅ Type check clean
  ✅ Build successful

Manual Verification Required:
  - [ ] Login flow works
  - [ ] Token refresh works
  - [ ] Logout clears state

Context: 57% (safe to continue if verified)

Test the feature and let me know!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**Key Insight:** One phase at a time = continuous validation = fewer surprises!
