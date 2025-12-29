---
description: Systematic validation - Phase 4 of 4-phase workflow
argument-hint: @thoughts/shared/plans/[file].md
allowed-tools: Read, Bash
model: sonnet
---

# Phase 4: Validate

**Goal:** Verify entire implementation systematically

**Plan:** $ARGUMENTS

---

## Workflow

### Step 1: Load Plan & Check Git
```bash
Read plan from thoughts/shared/plans/
Check git log: git log --oneline --since="1 day ago"
Verify all phases implemented
```

### Step 2: Run All Automated Checks
```bash
npm test
npm run lint
tsc --noEmit
npm run build
```

### Step 3: Compare Implementation vs Plan
```bash
For each phase:
  ✅ What was implemented correctly
  ⚠️ Any deviations (explain why)
  ✗ Missing implementations
```

### Step 4: Generate Report
```
Validation Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Implementation: User Authentication

✅ Correctly Implemented:
  - Phase 1: Auth context (100%)
  - Phase 2: Token management (100%)
  - Phase 3: API integration (95%)

⚠️ Beneficial Deviations:
  - Added rate limiting (not in plan - good addition!)

✗ Issues Found:
  - Logout doesn't clear all state
  - Missing error toast on 401

Automated Verification:
  ✅ Tests: 48/48 passing
  ✅ Lint: Clean
  ✅ Types: Clean
  ✅ Build: Successful
  ✅ Coverage: 89%

📋 Manual Testing:
  - [ ] Login works
  - [ ] Logout works
  - [ ] Token refresh works
  - [ ] 401 handling works

Next: Fix 2 issues, then ready for git commit!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Fix or Approve
```bash
If issues: Fix them
If clean: Ready for commit!
```

---

**Safety net:** Catches everything before shipping!
