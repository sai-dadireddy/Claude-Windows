---
description: Dev docs workflow for large tasks (create|update|list)
argument-hint: <action> [task-name]
allowed-tools: Read, Write, Edit, Bash
model: sonnet
---

# Dev Docs Workflow

**Purpose:** Prevent Claude from "losing the plot" on large tasks

Action: $ARGUMENTS

---

## Available Actions:

### create [task-name]
**Create dev docs for a new task/feature** (~500 tokens, 30 seconds)

**Workflow:**

#### Step 1: Create Task Directory
```bash
mkdir -p dev/active/[task-name]/
```

#### Step 2: Create 3 Core Files

**File 1: `[task-name]-plan.md`**
```markdown
# [Task Name] - Implementation Plan

## Overview
[1-2 sentence summary]

## Phases
1. Phase 1: [Name]
   - Task 1
   - Task 2
2. Phase 2: [Name]
   - Task 3

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**File 2: `[task-name]-context.md`**
```markdown
# [Task Name] - Context

Last Updated: [timestamp]

## Key Files
- src/file1.ts - Description
- src/file2.ts - Description

## Key Decisions
- Decision 1: Rationale
- Decision 2: Rationale

## Dependencies
- Package 1: Why needed
- Package 2: Why needed

## Notes
- Important note 1
- Important note 2
```

**File 3: `[task-name]-tasks.md`**
```markdown
# [Task Name] - Tasks

## Phase 1: [Name]
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Phase 2: [Name]
- [ ] Task 4
- [ ] Task 5

## Completed
- [x] Initial setup
```

#### Step 3: Confirmation
```
Dev Docs Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Directory: dev/active/[task-name]/
📄 Files created:
   ✅ [task-name]-plan.md
   ✅ [task-name]-context.md
   ✅ [task-name]-tasks.md

Next Steps:
1. Review plan in dev/active/[task-name]/[task-name]-plan.md
2. Start implementing Phase 1
3. Update tasks.md as you complete items
4. Update context.md with new decisions

Remember: Update docs regularly to prevent losing the plot!
```

---

### update [task-name]
**Update dev docs with progress** (~300 tokens, 15 seconds)

**Workflow:**

#### Step 1: Read Current State
```bash
Read dev/active/[task-name]/[task-name]-tasks.md
Read dev/active/[task-name]/[task-name]-context.md
```

#### Step 2: Extract from Conversation
```
From conversation memory:
- What tasks were just completed?
- What's the next task?
- Any new decisions made?
- Any new key files?
- Any blockers?
```

#### Step 3: Update Files
```bash
Edit [task-name]-tasks.md:
  - Mark completed tasks as [x]
  - Add new tasks discovered

Edit [task-name]-context.md:
  - Update "Last Updated" timestamp
  - Add new key files
  - Add new decisions
  - Add blockers if any
```

#### Step 4: Summary
```
Dev Docs Updated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Marked 3 tasks complete
✅ Added 2 new tasks
✅ Updated context with new decisions
✅ Last Updated: [timestamp]

Progress: 12/20 tasks complete (60%)
Next: [next task from tasks.md]

Ready to continue or /session save
```

---

### list
**List all active dev docs** (50 tokens, 2 seconds)

```bash
Bash: ls -la dev/active/

Shows:
- task-1/ (updated 2h ago)
- task-2/ (updated 1d ago)
- task-3/ (updated 3d ago)
```

---

## When to Use

**Start of large task:**
```bash
/dev-docs create user-authentication
# Creates all 3 files
# Start implementing
```

**During implementation:**
```bash
# Periodically update
/dev-docs update user-authentication
# Marks progress, adds context
```

**Before session save:**
```bash
/dev-docs update user-authentication
/session save
# Next session: Read dev docs to continue
```

**Next session:**
```bash
/session continue
# Shows: "Read dev/active/user-authentication/ to continue"

Read dev/active/user-authentication/[task]-tasks.md
# Pick up exactly where you left off!
```

---

## Benefits

✅ **Prevents losing the plot** - Always know what you're doing
✅ **Survives compaction** - State persisted in files
✅ **Context-efficient** - Only 500 tokens to set up
✅ **Seamless continuation** - Pick up where you left off
✅ **Progress tracking** - Visual checklist

---

## Integration with /session

When `/session save` runs:
- Automatically runs `/dev-docs update` if active task exists
- Saves task name in session state
- Next session reminds: "Continue task: [name]"

When `/session continue` runs:
- Checks for active dev docs
- Shows: "Active task: [name] (60% complete)"
- Reminds: "Read dev/active/[name]/ files"

---

**This system prevents Claude amnesia!** 🎯
