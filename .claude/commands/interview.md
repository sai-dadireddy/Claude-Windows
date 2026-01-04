# Interview-First Spec Development

Based on Tariq's (Claude Code team) workflow: Interview → Spec → Code

## Philosophy

"Slow down to speed up" - Spend time discovering requirements BEFORE coding.

## Process

### Phase 1: Discovery Interview

Use the AskUserQuestion tool to interview about:

1. **Core Purpose**
   - What are you building?
   - Who is it for?
   - What problem does it solve?

2. **Technical Decisions**
   - Framework/language preferences?
   - Database requirements?
   - Authentication approach?
   - Hosting/deployment target?

3. **UI/UX Concerns**
   - Design system or component library?
   - Responsive requirements?
   - Accessibility needs?
   - Key user flows?

4. **Trade-offs**
   - Speed vs. quality priority?
   - Build vs. buy decisions?
   - Scalability requirements?
   - Budget/resource constraints?

5. **Integration Points**
   - External APIs needed?
   - Third-party services?
   - Existing systems to connect?

6. **Non-Obvious Details**
   - Edge cases to handle?
   - Error handling approach?
   - Logging/monitoring needs?
   - Security requirements?

### Phase 2: Write Spec

After interview, write comprehensive spec to `SPEC.md`:

```markdown
# Feature Specification: [Name]

## Overview
[What we're building and why]

## Requirements
### Functional
- [List of features]

### Technical
- [Architecture decisions]
- [Technology choices]

## User Stories
- As a [user], I want [feature] so that [benefit]

## Implementation Plan
1. [Phase 1]
2. [Phase 2]
...

## Open Questions
- [Any unresolved items]
```

### Phase 3: Execute

Start new session with: "Implement SPEC.md"

## Interview Prompt

When triggered, use this approach:

```
Read any existing spec or context, then interview me using the AskUserQuestion
tool about everything needed to build this. Ask about:
- Technical implementation details
- UI/UX concerns
- Trade-offs and priorities
- Edge cases and error handling
- Integration requirements

Be very in-depth. Ask non-obvious questions. Continue interviewing until
you have enough detail for a comprehensive spec. Then write the spec to SPEC.md.
```

## Key Principles

1. **Questions over assumptions** - Ask, don't guess
2. **Cheap decisions early** - Discover issues before coding
3. **40+ questions for large features** - Be thorough
4. **Write spec before code** - Document decisions

## Usage

```
/interview                    # Start fresh interview
/interview [topic]            # Interview about specific feature
/interview --spec SPEC.md     # Update existing spec
```

## Example Session

User: `/interview add authentication`

Claude: "Let me interview you about the authentication feature..."
- Q1: What auth method? (OAuth, JWT, session-based, magic links)
- Q2: Which providers? (Google, GitHub, email/password)
- Q3: Role-based access control needed?
- Q4: MFA requirements?
- Q5: Session duration preferences?
- Q6: Account recovery flow?
...continues until comprehensive spec is ready...

Then writes detailed SPEC.md for implementation.
