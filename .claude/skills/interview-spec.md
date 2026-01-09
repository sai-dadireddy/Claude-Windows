---
name: interview-spec
description: Interview user to create detailed specs before implementation
context: fork
user-invocable: true
triggers:
  - "interview me"
  - "spec first"
  - "plan this feature"
---

# Interview-Spec Skill

Trigger: User mentions "interview me", "spec first", "plan this feature", or starts a large/ambiguous request.

## Behavior

When this skill is activated:

1. **Acknowledge**: "I'll interview you first to create a detailed spec."

2. **Interview Loop**: Use AskUserQuestion tool repeatedly with questions covering:
   - Core purpose and users
   - Technical architecture choices
   - UI/UX requirements
   - Trade-offs and priorities
   - Edge cases and error handling
   - Integration points
   - Security and performance needs

3. **Question Style**:
   - Ask 2-4 questions at a time
   - Use multiSelect for non-exclusive options
   - Provide clear option descriptions
   - Include "Other" for custom input
   - Ask non-obvious, deep questions

4. **Continue Until Complete**: Keep interviewing until you have enough detail.
   For large features, this may be 20-40+ questions.

5. **Write Spec**: Output comprehensive SPEC.md with:
   - Overview
   - Requirements (functional + technical)
   - User stories
   - Implementation plan
   - Decisions made during interview

6. **Offer Next Steps**:
   - "Start a new session with: implement SPEC.md"
   - Or continue in current session if small enough

## Example Questions

```
AskUserQuestion:
  questions:
    - question: "What authentication approach should we use?"
      header: "Auth"
      options:
        - label: "OAuth (Google, GitHub)"
          description: "Managed auth, users sign in with existing accounts"
        - label: "Email/Password"
          description: "Traditional auth, you manage credentials"
        - label: "Magic Links"
          description: "Passwordless via email links"
        - label: "Session-based"
          description: "Server-side sessions with cookies"
      multiSelect: false
```

## When to Trigger

- User says "interview me about..."
- User gives vague large feature request
- User says "let's plan..." or "spec out..."
- User starts new project without clear requirements
