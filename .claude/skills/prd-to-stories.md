---
name: prd-to-stories
description: Convert a PRD markdown file to prd.json for Ralph autonomous agent
user-invocable: true
---

# PRD to Stories Converter

Convert a Product Requirements Document (PRD) into a structured JSON file for the Ralph autonomous agent system.

## Input

A PRD markdown file (created by /prd or manually)

## Output

A `prd.json` file with this structure:

```json
{
  "feature": "Feature Name",
  "created": "2026-01-10",
  "stories": [
    {
      "id": "US-1",
      "title": "Short descriptive title",
      "description": "Full user story in As a/I want/So that format",
      "acceptance_criteria": [
        "Specific testable criterion 1",
        "Specific testable criterion 2"
      ],
      "priority": 1,
      "passes": false,
      "iteration_completed": null
    }
  ]
}
```

## Critical Rules

### 1. Story Size
**THE #1 RULE**: Each story MUST be completable in ONE Ralph iteration.
- If a story is too big, split it into smaller stories
- Target: 15-30 minutes of agent work per story
- Signs it's too big: more than 5 acceptance criteria, touches more than 3 files

### 2. Story Ordering
- Put foundational stories first (database, models, types)
- Then business logic
- Then UI/frontend
- Finally integration/polish

### 3. Acceptance Criteria
Criteria MUST be verifiable by the agent without human input.

**GOOD criteria:**
- "Status column added to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking save button shows success toast"
- "API returns 400 for invalid input"
- "Unit test for priority sorting passes"

**BAD criteria:**
- "UI looks good" (subjective)
- "Works correctly" (vague)
- "User is happy" (unmeasurable)
- "Performance is acceptable" (no threshold)

### 4. Dependencies
If story B depends on story A, put A first and note in description:
```json
{
  "id": "US-2",
  "description": "... (depends on US-1)",
  ...
}
```

## Process

1. Read the PRD markdown file
2. Extract all user stories
3. Validate each story is small enough
4. Ensure acceptance criteria are testable
5. Order by dependencies and priority
6. Output prd.json

## Example Conversion

**Input PRD:**
```markdown
### US-1: Set Task Priority
**As a** user
**I want to** set a priority level when creating a task
**So that** I can indicate importance

**Acceptance Criteria:**
- [ ] Priority dropdown with High, Medium, Low
- [ ] Default is Medium
- [ ] Priority saves to database
```

**Output prd.json:**
```json
{
  "feature": "Task Priority System",
  "created": "2026-01-10",
  "stories": [
    {
      "id": "US-1",
      "title": "Set Task Priority",
      "description": "As a user, I want to set a priority level when creating a task so that I can indicate importance",
      "acceptance_criteria": [
        "Priority dropdown exists with options: High, Medium, Low",
        "Default selected priority is Medium",
        "Priority value persists to database after save"
      ],
      "priority": 1,
      "passes": false,
      "iteration_completed": null
    }
  ]
}
```

## Output Location

Save to: `.ralph/prd.json` (default) or user-specified location

## Integration with Ralph

After creating prd.json, start Ralph:
```bash
python ~/.claude/scripts/ralph_enhanced.py start "$(cat .ralph/prd.json | jq -r '.stories[].title' | head -5 | tr '\n' ' ')" 50 "FEATURE_COMPLETE"
```

Or use the bash wrapper:
```bash
~/.claude/scripts/ralph_loop.sh .ralph/prd.json
```
