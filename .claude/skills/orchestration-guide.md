# AI Orchestration Guide - Models, Agents & Parallel Work

## WHEN TO USE WHAT

### Model Selection Matrix

| Task | Model | Why | Invoke |
|------|-------|-----|--------|
| **Normal coding** | Claude Opus 4.5 | DEFAULT, best overall | Just do it |
| **Multilingual code** | GLM 4.7 | 66.7% SWE-bench multilingual | `multi:chat glm` |
| **Large context >200K** | Gemini 2.5 Flash | 1M context window | `multi:chat gemini` |
| **FREE/cheap** | DeepSeek V3.2 | $0 via Ollama | `multi:chat deepseek` |
| **Reasoning/math** | DeepSeek R1 | FREE chain-of-thought | `multi:chat r1` |
| **Compare approaches** | multi:compare | 3-model consensus | `multi:compare` |
| **Images/video** | Gemini or Pixtral | Multimodal | `multi:chat gemini` |

### Parallel Agents - WHEN to Use

**USE parallel agents when:**
- Multiple INDEPENDENT tasks (different files/features)
- Large refactoring across many files
- Writing tests for multiple modules
- User says "in parallel", "simultaneously"
- Tasks have NO dependencies on each other

**DON'T USE when:**
- Tasks depend on each other's output
- Working on the same files
- Need to coordinate changes
- Single focused task

### Available Specialized Agents

| Agent | Best For | Key Strengths |
|-------|----------|---------------|
| `code-scout` | File discovery | Fast parallel search, JSON output |
| `autonomous-coder` | General coding | Full autonomy, no questions |
| `feature-builder` | New features | Complete implementation |
| `test-writer` | Test coverage | All edge cases |
| `refactorer` | Code quality | Pattern consistency |
| `lambda-builder` | AWS Lambda | Serverless patterns |
| `frontend-builder` | React/Vue/Next | Component architecture |
| `ui-ux-designer` | Design systems | Accessibility, themes |

---

## CRITICAL: How to Prompt Parallel Agents

### BAD (causes confusion):
```
"Add authentication"
```

### GOOD (specific and complete):
```
TASK: Implement JWT authentication

WORKING DIRECTORY: /home/user/project/src/auth/
(Work ONLY in this directory!)

FILES TO CREATE:
- jwt.ts - Token sign/verify functions
- middleware.ts - Express auth middleware
- types.ts - Auth type definitions

FILES TO MODIFY:
- ../app.ts - Add auth middleware (line ~15)

DO NOT TOUCH:
- Any files outside /src/auth/
- Database models
- Environment files

EXISTING PATTERNS TO FOLLOW:
- Look at /src/users/service.ts for code style
- Use existing Logger from /src/utils/logger.ts

EXPECTED OUTPUT:
- 3 new files in /src/auth/
- 1 modification to app.ts
- All TypeScript, no JS

VERIFICATION:
- Run: npm run typecheck
- Run: npm test -- --grep auth
```

### Parallel Agent Template

```
TASK: [One-line description]

WORKING DIRECTORY: [Exact path - STAY HERE]

CREATE:
- [file1] - [purpose]
- [file2] - [purpose]

MODIFY:
- [existing file] - [what to change]

DO NOT TOUCH:
- [files/directories to avoid]

PATTERNS:
- Follow [existing file] for style
- Use [existing module] for [purpose]

VERIFY:
- [command to run]
```

---

## Model-Specific Prompts

### For GLM 4.7 (Multilingual, Tool Calling)
```xml
<task>
[Clear imperative statement]
</task>

<context>
[Relevant code/info]
</context>

<constraints>
- Language: [specify]
- Must: [requirements]
- Must NOT: [restrictions]
</constraints>
```

### For Gemini (Large Context)
```
TASK: [One-line description]

CONTEXT:
[Paste large file/codebase - Gemini handles 1M tokens]

FOCUS ON:
- [Point 1]
- [Point 2]

OUTPUT FORMAT:
[Bullet points/JSON/etc]
```

### For DeepSeek R1 (Reasoning)
```
Think step by step.

[Your question/task]

Show your reasoning.
```

### For OpenAI (GPT-4o, o1)
```markdown
# Task
[Description]

# Context
[Background]

# Requirements
1. [Req 1]
2. [Req 2]

# Output Format
[Specify exactly]
```

---

## Multi-Model Commands

```bash
# Chat with specific model
multi:chat glm "Translate this Python to Go with Chinese comments"

# Compare 3 models' approaches
multi:compare "Best architecture for real-time chat?"

# Debate between models (critical decisions)
multi:debate "Should we use microservices or monolith?"

# Auto-route based on task
/route [your task description]
```

---

## Workmux (Git Worktrees + Tmux)

For truly parallel work with separate git branches:

```bash
# Source cargo env first
. /home/claude/.cargo/env

# Create worktree + Claude agent
workmux add auth-feature -a claude -p "$(cat << 'EOF'
TASK: Implement user authentication

DIRECTORY: Work only in ./src/auth/
CREATE:
- jwt.ts
- middleware.ts

VERIFY: npm test -- --grep auth
EOF
)"

# Multiple parallel with numbered tasks
workmux add refactor -n 4 -p "Refactor module #{{ num }}"

# List active
workmux list

# Merge when done
workmux merge
```

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION CHEATSHEET                 │
├─────────────────────────────────────────────────────────────┤
│ DEFAULT → Claude Opus 4.5                                   │
├─────────────────────────────────────────────────────────────┤
│ Multilingual?     → multi:chat glm                          │
│ Context > 200K?   → multi:chat gemini                       │
│ FREE needed?      → multi:chat deepseek                     │
│ Reasoning/Math?   → multi:chat r1                           │
│ Compare options?  → multi:compare                           │
├─────────────────────────────────────────────────────────────┤
│ Parallel coding?  → Task tool with specialized agent        │
│ Multiple files?   → workmux add feature -a claude           │
│ Find files first? → code-scout agent                        │
└─────────────────────────────────────────────────────────────┘
```
