# Project: {{PROJECT_NAME}}

## Quick Start

```bash
# Development
{{DEV_COMMAND}}

# Tests
{{TEST_COMMAND}}

# Build
{{BUILD_COMMAND}}
```

## Tech Stack

- **Language:** {{LANGUAGE}}
- **Framework:** {{FRAMEWORK}}
- **Database:** {{DATABASE}}
- **Other:** {{OTHER_TECH}}

## Project Structure

```
{{PROJECT_STRUCTURE}}
```

## Key Files

| File | Purpose |
|------|---------|
| `{{MAIN_FILE}}` | Entry point |
| `{{CONFIG_FILE}}` | Configuration |

## Coding Conventions

- {{CONVENTION_1}}
- {{CONVENTION_2}}
- {{CONVENTION_3}}

## DO NOT

- Do not modify files in `{{PROTECTED_DIR}}`
- Do not commit directly to `main` branch
- Do not expose secrets in code

---

## For Claude (Auto-injected)

### Task Management

**Use Beads for this project if:**
- Implementing multi-step features
- Tasks have dependencies
- Work spans multiple sessions

```bash
# Initialize beads (if not done)
PATH=$HOME/.local/bin:$PATH bd init

# Create issue
PATH=$HOME/.local/bin:$PATH bd create "Task description" -t feature -p 1

# Find ready work
PATH=$HOME/.local/bin:$PATH bd ready
```

### Memory

Save important decisions:
```bash
~/.claude/scripts/memory_manager.py save-memory "{{PROJECT_NAME}}" decision "Decision details"
```

### Testing Changes

Before marking work complete:
```bash
{{TEST_COMMAND}}
{{LINT_COMMAND}}
```
