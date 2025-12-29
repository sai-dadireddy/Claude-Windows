Create or update a **project summary** document for Plan Mode context.

Inspired by sketch2prompt - prevents AI hallucination by freezing architectural intent.

## Purpose

This document helps Claude understand your project quickly when:
- Starting a planning session
- Using Plan Mode for features
- Onboarding to a new codebase
- Preventing inconsistent conventions

## Template

Generate a `PROJECT-SUMMARY.md` in the project root:

```markdown
# Project Summary

**Project:** [Name]
**Updated:** [Date]

## Overview
[1-2 sentence description of what this project does]

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | [Framework, UI lib] |
| Backend | [Language, framework] |
| Database | [DB type] |
| Infrastructure | [Cloud, deployment] |

## Architecture
[High-level architecture description]

```
[Simple ASCII diagram if helpful]
```

## Key Directories
| Directory | Purpose |
|-----------|---------|
| `src/` | [What's here] |
| `lib/` | [What's here] |
| `tests/` | [What's here] |

## Current Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Non-Goals (Out of Scope)
- [Thing we're NOT doing]
- [Another thing to avoid]

## Architecture Constraints

### ALWAYS (Non-Negotiable)
- [Required practice 1]
- [Required practice 2]

### NEVER (Prohibited)
- [Forbidden practice 1]
- [Forbidden practice 2]

### PREFER (Guidelines)
- [Preferred approach 1]
- [Preferred approach 2]

## Constraints
- [Technical constraint]
- [Business constraint]
- [Timeline constraint]

## Key Decisions Made
| Decision | Rationale | Date |
|----------|-----------|------|
| [Choice made] | [Why] | [When] |

## Known Issues / Tech Debt
- [ ] [Issue 1]
- [ ] [Issue 2]

## Quick Commands
```bash
# Development
[dev command]

# Testing
[test command]

# Build
[build command]
```

## Team / Contacts
- [Role]: [Name/handle]
```

## How to Use

1. **Initial creation:** Run this command to generate the template
2. **Keep updated:** Update when major decisions are made
3. **Reference in Plan Mode:** Claude will use this for context

## Placement

Save as one of:
- `PROJECT-SUMMARY.md` (project root)
- `docs/PROJECT-SUMMARY.md`
- Add to existing `CLAUDE.md` as a section

## Integration with Plan Mode

When you run `/plan-feature`, Claude will:
1. Check for PROJECT-SUMMARY.md
2. Load architecture context
3. Respect constraints and non-goals
4. Align with current priorities

---

**Analyze current project and generate PROJECT-SUMMARY.md:**
