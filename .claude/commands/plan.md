# Sprint Planning Command

## Purpose
Interactive sprint planning with epic grooming (community-proven 817-upvote pattern).

## Instructions

### Phase 1: Sprint Setup

1. **Check Current Sprint**:
   - Read PROJECT-TRACKER.md for current sprint number
   - If not set, ask: "What sprint number should we start?"

2. **Create Sprint Directory**:
   ```bash
   mkdir -p sprints/[number]/
   ```

3. **Sprint Goal**:
   - Ask: "What's the main goal for this sprint?"
   - Document in `sprints/[number]/sprint-goal.md`

### Phase 2: Epic Identification

4. **Identify Epics**:
   - Ask: "What are the 2-4 main features/epics for this sprint?"
   - For each, create: `sprints/[number]/epic-[name].md`

### Phase 3: Epic Grooming (CRITICAL - Interactive!)

For EACH epic, ask these clarifying questions:

**Relevance Questions**:
- "How does this contribute to project/MVP goals?"
- "What specific user pain does it solve?"
- "Is this core functionality or can it wait?"

**Technical Questions**:
- "What are the primary technical challenges?"
- "What external services/APIs are needed?"
- "What are the performance implications?"

**Dependency Questions**:
- "What other epics does this depend on?"
- "Any external team or resource dependencies?"

**Edge Case Questions**:
- "What happens if [unexpected scenario occurs]?"
- "How should errors be handled?"
- "What are the failure modes?"

**Testing Questions**:
- "What types of tests are critical?"
- "Any complex scenarios that will be hard to test?"

### Phase 4: Task Breakdown

5. **Break Into Tasks**:
   - Each user story → Multiple tasks
   - Each task should have:
     - Estimate (hours)
     - Dependencies (other tasks)
     - Acceptance Criteria (how to verify complete)
     - Notes (technical considerations)

6. **Update Epic File**:
   ```markdown
   # Epic: [Title]

   **Sprint**: [number]
   **Status**: Not Started | In Progress | Done
   **Owner**: [Developer name(s)]

   ## Description
   [Detailed description of epic and its purpose]

   ## User Stories
   - [ ] **Story 1**: [As a user, I want... so that...]
       - **Tasks**:
           - [ ] [Task 1] (Est: 4h, Deps: None, AC: [criteria], Notes: [notes])
           - [ ] [Task 2] (Est: 2h, Deps: Task 1, AC: [criteria])

   - [ ] **Story 2**: [User story]
       - **Tasks**:
           - [ ] [Task]...

   ## Dependencies
   - [List any dependencies on other epics or external factors]

   ## Acceptance Criteria (Overall Epic)
   - [Criterion 1]
   - [Criterion 2]
   ```

### Phase 5: Completion

7. **When All Epics Groomed**:
   - Update PROJECT-TRACKER.md with sprint reference
   - Ask: "Sprint planning complete! Ready to start implementation or plan next sprint?"

## Output Format
```
📋 **SPRINT PLANNING**

Sprint: [number]
Goal: [goal]

Epics identified: X
  1. [Epic 1 name]
  2. [Epic 2 name]
  3. [Epic 3 name]

Grooming Epic 1/3: [name]
[Interactive Q&A session...]

✅ Epic 1 groomed! (X tasks, Xh estimated)

Grooming Epic 2/3...

---

✅ **SPRINT PLANNING COMPLETE!**

Sprint [number]: [goal]
  - [X epics created]
  - [Y total tasks]
  - [Z hours estimated]

📁 Files created:
  - sprints/[number]/epic-1-[name].md
  - sprints/[number]/epic-2-[name].md
  - sprints/[number]/sprint-goal.md

📋 Updated: PROJECT-TRACKER.md

🎯 Ready to start implementation!
```

## Why This Works (817 Reddit Upvotes)
- Encourages Claude to dive MUCH deeper into problem-solving
- Discovers key decisions BEFORE coding starts
- Prevents sweeping changes without your approval
- Easy resume: "Read epic-X.md and continue"
- Creates focused, testable milestones

## Token Cost
- Per epic grooming: 3-5K tokens (interactive Q&A)
- 3 epics: ~12-15K tokens total
- **Result**: Clear, battle-tested epics ready for implementation

## When to Use
- Starting new project phase
- Planning large feature additions
- Breaking down complex requirements
- When you want structured, testable milestones
