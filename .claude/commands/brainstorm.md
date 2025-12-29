Explore a problem from **multiple perspectives** before committing to an approach.

## When to Use

- You know WHAT to build but not HOW
- Multiple valid approaches exist
- Need to consider trade-offs
- Want to avoid tunnel vision

## Multi-Role Analysis

Analyze the problem from these perspectives:

### 1. Product Manager Lens
```markdown
## Product Perspective

**User Problem:** What pain point does this solve?
**Success Metrics:** How will we measure success?
**MVP Scope:** What's the minimum viable solution?
**Future Expansion:** What could this become later?
```

### 2. System Architect Lens
```markdown
## Architecture Perspective

**System Boundaries:** Where does this fit in the architecture?
**Data Flow:** How does data move through the system?
**Integration Points:** What does this connect to?
**Scalability:** Will this approach scale?
```

### 3. Security Expert Lens
```markdown
## Security Perspective

**Attack Surface:** What new vulnerabilities could this introduce?
**Auth/AuthZ:** Are permissions handled correctly?
**Data Protection:** Is sensitive data properly secured?
**Compliance:** Any regulatory considerations?
```

### 4. Developer Experience Lens
```markdown
## DX Perspective

**Complexity:** How hard is this to implement?
**Maintainability:** Will future devs understand this?
**Testing:** How testable is this approach?
**Documentation:** What needs to be documented?
```

### 5. Operations Lens
```markdown
## Ops Perspective

**Deployment:** How does this get deployed?
**Monitoring:** How do we know if it's working?
**Failure Modes:** What happens when it breaks?
**Rollback:** Can we undo this easily?
```

## Synthesis

After multi-role analysis, synthesize:

```markdown
## Brainstorm Summary

### Recommended Approach
[Primary recommendation with rationale]

### Alternative Approaches
| Approach | Pros | Cons | Effort |
|----------|------|------|--------|
| [Option A] | [+] | [-] | [Est.] |
| [Option B] | [+] | [-] | [Est.] |

### Key Decisions Needed
1. [Decision 1] - [Options]
2. [Decision 2] - [Options]

### Risks to Mitigate
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

### Next Step
[Clear action to move forward]
```

## Usage

```
/brainstorm implement real-time notifications
/brainstorm migrate from REST to GraphQL
/brainstorm add multi-tenant support
```

---

**Topic to brainstorm:**

$ARGUMENTS
