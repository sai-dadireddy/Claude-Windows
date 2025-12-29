# Parallel Agents - Detailed Guide

## Custom Subagents

Location: `~/.claude/agents/`

All agents use `model: opus` and `permissionMode: bypassPermissions` - fully autonomous:

| Agent | Use For |
|-------|---------|
| `code-scout` | Fast file discovery - use FIRST to find files |
| `autonomous-coder` | General coding tasks |
| `feature-builder` | Complete feature implementation |
| `test-writer` | Writing comprehensive tests |
| `refactorer` | Code quality improvements |
| `lambda-builder` | AWS Lambda, serverless, API Gateway |
| `frontend-builder` | React, Vue, Next.js, components |
| `ui-ux-designer` | Design systems, styling, themes |

## When to Use

**USE parallel agents when:**
- Multiple independent tasks (different files/features)
- Large refactoring across many files
- Writing tests for multiple modules
- User says "in parallel", "simultaneously"
- Tasks have no dependencies on each other

**DON'T USE when:**
- Tasks depend on each other's output
- Working on the same files
- Need to coordinate changes
- Single focused task

## How to Launch

### Method 1: Task Tool
```
Use Task tool with subagent_type="autonomous-coder"
Give VERY SPECIFIC instructions
```

### Method 2: Workmux (Git Worktrees + Tmux)
```bash
. /home/claude/.cargo/env && workmux add feature-name -a claude -p "PROMPT"
```

## Prompt Engineering for Agents

### BAD (causes confusion):
```
"Add authentication"
```

### GOOD (specific and complete):
```
"Implement JWT authentication in /src/auth/:
1. Create /src/auth/jwt.ts with sign/verify functions
2. Create /src/auth/middleware.ts with auth middleware
3. Use existing User model from /src/models/user.ts
4. Add tests in /src/auth/__tests__/
5. Use bcrypt for password hashing (already installed)
DO NOT modify any files outside /src/auth/"
```

## Prompt Template

```
TASK: [Clear one-line description]

WORKING DIRECTORY: [Exact path]

FILES TO CREATE/MODIFY:
- [file1.ts] - [what to do]
- [file2.ts] - [what to do]

DO NOT TOUCH:
- [files/dirs to avoid]

EXISTING PATTERNS TO FOLLOW:
- Look at [example file] for code style
- Use [existing module] for [purpose]

EXPECTED OUTPUT:
- [What should exist when done]

VERIFICATION:
- Run: [test command]
```

## Preventing File Scatter

Each parallel agent MUST be told:
1. **Exact working directory** - "Work ONLY in /src/feature-x/"
2. **Files to avoid** - "Do NOT modify /src/core/"
3. **Where to put new files** - "Create new files in /src/feature-x/components/"

## Workmux Commands

```bash
. /home/claude/.cargo/env

# Create worktree + tmux window
workmux add auth-feature -a claude -p "$(cat << 'EOF'
TASK: Implement user authentication
DIRECTORY: Work only in ./src/auth/
CREATE:
- jwt.ts - JWT token handling
- middleware.ts - Express auth middleware
FOLLOW: Patterns in ./src/users/
TEST: npm test -- --grep auth
EOF
)"

# Multiple parallel agents
workmux add refactor -n 4 -p "Refactor module #{{ num }} in ./src/modules/mod{{ num }}/"

# List active worktrees
workmux list

# Merge and cleanup
workmux merge

# Remove without merging
workmux rm feature-name
```

## Status Icons in Tmux
- 🤖 = agent working
- 💬 = waiting for input
- ✅ = finished
