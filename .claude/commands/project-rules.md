Generate a **PROJECT_RULES.md** file that defines architecture constraints for AI coding assistants.

Inspired by sketch2prompt - this creates a "system constitution" that prevents AI hallucination of architecture.

## Template

```markdown
# Project Rules

> System constitution for AI assistants working on this codebase.

## 1. System Overview

**Project:** [Name]
**Description:** [One-line description]

### Technology Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | [Framework] | [Version]+ |
| Backend | [Language/Framework] | [Version]+ |
| Database | [DB] | [Version]+ |
| Infrastructure | [Cloud/Deploy] | - |

### System Scope

**IS:**
- [What this system does]
- [Architecture style: monolith, microservices, etc.]
- [Key integrations]

**IS NOT:**
- [What this system explicitly does not do]
- [Patterns to avoid]
- [Out of scope features]

---

## 2. Component Registry

| Component | Type | Spec File |
|-----------|------|-----------|
| [Name] | frontend/backend/storage | specs/[name].yaml |

*Load specs only when needed; avoid preloading all components.*

---

## 3. Architecture Constraints

### ALWAYS (Non-Negotiable)
- [ ] Validate inputs at all system boundaries
- [ ] Use environment variables for secrets
- [ ] Implement structured error logging
- [ ] Define explicit schemas for API contracts
- [ ] [Project-specific constraint]

### NEVER (Prohibited)
- [ ] Store secrets in code or version control
- [ ] Rely solely on client-side validation
- [ ] Add enterprise patterns without explicit request
- [ ] Install dependencies without checking stdlib first
- [ ] [Project-specific prohibition]

### PREFER (Guidelines)
- Simplicity over abstraction
- Typed contracts over ad-hoc objects
- RESTful resources over RPC
- Async I/O for network operations
- [Project-specific preference]

---

## 4. Code Standards

### Naming Conventions

**[Language 1]:**
- Files: [convention]
- Functions: [convention]
- Classes: [convention]
- Constants: [convention]

**[Language 2]:**
- Files: [convention]
- Functions: [convention]
- Classes: [convention]

### Hard Limits
| Constraint | Maximum |
|-----------|---------|
| Function length | 50 lines |
| File length | 300 lines (500 absolute) |
| Nesting depth | 3 levels |
| Function parameters | 4 parameters |

### Directory Structure
```
/project-root
  /[component-1]
    /src
  /[component-2]
    /src
  /shared
  /specs
```

---

## 5. Build Order

### Phase 1: Foundation
- [ ] [Component with no dependencies]
- [ ] [Infrastructure components]

### Phase 2: Core
- [ ] [Core business logic]
- [ ] [Main features]

### Phase 3: Integration
- [ ] [Connect components]
- [ ] [External integrations]

---

## 6. Integration Rules

### Communication Patterns
| From | To | Pattern | Purpose |
|------|----|---------|---------|
| Frontend | Backend | REST/GraphQL | API calls |
| Backend | Database | ORM/Query | Data access |

### Forbidden Integrations
- Frontend must NOT directly access database
- [Other forbidden patterns]

### Environment Variables
Document in `.env.example`:
- `API_URL` - Backend API endpoint
- `DATABASE_URL` - Database connection
- [Other required vars]

---

## Architecture Philosophy

> Build MINIMALLY — only add what's needed NOW, scale when actually necessary.

- No enterprise patterns unless explicitly requested
- Start with simplest working solution
- Avoid premature abstraction
- Use lightweight defaults
```

---

**Analyze the current project and generate PROJECT_RULES.md:**
