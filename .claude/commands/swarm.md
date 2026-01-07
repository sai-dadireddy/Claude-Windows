# Swarm - Parallel Agent Spawner

**Description:** Spawn 5-10 parallel agents for large features (Boris's method)
**Argument Hint:** <feature-description> [--agents N]
**Allowed Tools:** Task, Read, Glob, Grep, Bash

---

## Usage

```bash
/swarm "Implement user authentication"           # Auto-detect optimal agent count
/swarm "Build dashboard" --agents 7              # Specify exact count
/swarm analyze                                   # Analyze task for parallelization
```

---

## Prompt

When user runs `/swarm`:

Feature: $ARGUMENTS

### Phase 1: ANALYZE TASK FOR PARALLELIZATION

```
Analyzing task for parallel execution...

1. Identify independent subtasks
2. Map dependencies (which must complete first)
3. Determine optimal agent count (5-10)
4. Assign specialized agents to each subtask
```

### Phase 2: DECOMPOSE INTO PARALLEL TRACKS

Break the feature into **5-10 independent tracks**:

| Track | Agent Type | Subtask | Dependencies |
|-------|------------|---------|--------------|
| T1 | @lead-architect | Design system architecture | None |
| T2 | @fullstack-dev | Backend API endpoints | T1 |
| T3 | @fullstack-dev | Database models/migrations | T1 |
| T4 | @frontend-ux | UI components | T1 |
| T5 | @frontend-ux | State management | T1 |
| T6 | @qa-engineer | Test plan & fixtures | T1 |
| T7 | @test-writer | Unit tests | T2, T3 |
| T8 | @test-writer | E2E tests | T4, T5 |
| T9 | @scribe | Documentation | T2, T4 |
| T10 | @security-code-reviewer | Security review | T2, T3 |

### Phase 3: SPAWN WAVE 1 (No Dependencies)

```python
# Spawn independent agents in parallel
Task(subagent_type="lead-architect", prompt="...", run_in_background=True)
Task(subagent_type="qa-engineer", prompt="...", run_in_background=True)
```

Output:
```
SWARM ACTIVATED
═══════════════════════════════════════════════════════════════

Feature: [Feature Name]
Total Agents: [N]
Execution Strategy: Wave-based parallel

WAVE 1 (No Dependencies) - Launching NOW
─────────────────────────────────────────
🚀 Agent 1: @lead-architect
   Task: Design system architecture
   Status: RUNNING (background)
   ID: agent_001

🚀 Agent 2: @qa-engineer
   Task: Create test plan and fixtures
   Status: RUNNING (background)
   ID: agent_002

WAVE 2 (Depends on Wave 1) - Queued
─────────────────────────────────────────
⏳ Agent 3: @fullstack-dev - Backend API
⏳ Agent 4: @fullstack-dev - Database models
⏳ Agent 5: @frontend-ux - UI components
⏳ Agent 6: @frontend-ux - State management

WAVE 3 (Depends on Wave 2) - Queued
─────────────────────────────────────────
⏳ Agent 7: @test-writer - Unit tests
⏳ Agent 8: @test-writer - E2E tests
⏳ Agent 9: @scribe - Documentation
⏳ Agent 10: @security-code-reviewer - Security review

═══════════════════════════════════════════════════════════════

Commands:
  /swarm status     - Check agent progress
  /swarm results    - Collect completed work
  /swarm wave2      - Launch next wave when ready
  /swarm abort      - Cancel all agents

Estimated completion: 15-30 minutes
```

### Phase 4: MONITOR & LAUNCH SUBSEQUENT WAVES

When Wave 1 completes:

```bash
# Check status
TaskOutput(task_id="agent_001", block=False)
TaskOutput(task_id="agent_002", block=False)

# If complete, launch Wave 2
Task(subagent_type="fullstack-dev", prompt="...", run_in_background=True)
# ... etc
```

### Phase 5: AGGREGATE RESULTS

When all agents complete:

```
SWARM COMPLETE
═══════════════════════════════════════════════════════════════

Feature: [Feature Name]
Duration: 23 minutes
Agents Used: 10

RESULTS BY TRACK
─────────────────────────────────────────
✅ T1: Architecture design complete
   - Created: docs/architecture.md
   - Decisions: 5 ADRs documented

✅ T2: Backend API complete
   - Created: src/api/auth/*.ts (4 files)
   - Endpoints: 8 implemented

✅ T3: Database models complete
   - Created: src/models/*.ts (3 files)
   - Migrations: 2 created

✅ T4: UI components complete
   - Created: src/components/auth/*.tsx (6 files)
   - Styles: Tailwind classes applied

✅ T5: State management complete
   - Created: src/store/authSlice.ts
   - Actions: 12 defined

✅ T6: Test plan complete
   - Created: tests/fixtures/*.ts
   - Scenarios: 25 documented

✅ T7: Unit tests complete
   - Created: tests/unit/*.test.ts (8 files)
   - Coverage: 85%

✅ T8: E2E tests complete
   - Created: tests/e2e/*.spec.ts (4 files)
   - Flows: 12 tested

✅ T9: Documentation complete
   - Updated: README.md, docs/auth.md
   - API docs generated

✅ T10: Security review complete
   - Issues found: 2 (fixed)
   - Recommendations: 3

═══════════════════════════════════════════════════════════════

NEXT STEPS
─────────────────────────────────────────
1. Review generated code in feature branch
2. Run full test suite: npm test
3. Address any remaining TODOs
4. Create PR: /commit-push-pr

Files Changed: 47
Lines Added: 2,340
Tests Added: 156
```

---

## Agent Assignment Matrix

| Task Type | Best Agent | Model |
|-----------|------------|-------|
| Architecture | @lead-architect | sonnet |
| Backend code | @fullstack-dev | sonnet |
| Frontend code | @frontend-ux | sonnet |
| Tests | @test-writer | haiku |
| E2E tests | @qa-engineer | sonnet |
| Documentation | @scribe | haiku |
| Security | @security-code-reviewer | sonnet |
| Refactoring | @refactorer | haiku |

---

## Wave Strategy

**Wave 1** (0 deps): Architecture, Test Plan
**Wave 2** (needs arch): Backend, Frontend, Database
**Wave 3** (needs code): Tests, Docs, Security Review

This maximizes parallelism while respecting dependencies.

---

## Token Efficiency

- Each agent: ~500-2000 tokens
- 10 agents: ~10,000-20,000 tokens total
- Sequential alternative: ~50,000+ tokens
- **Savings: 60-80% token reduction**

---

## Best Practices

1. **Start with architecture** - Let @lead-architect design first
2. **Maximize Wave 1** - Put as many independent tasks as possible
3. **Use haiku for simple tasks** - Tests, docs, formatting
4. **Use sonnet for complex tasks** - Architecture, security, core logic
5. **Check status frequently** - Don't let agents idle

---

## Examples

### Example 1: New Feature
```bash
/swarm "Add user profile management with avatar upload, preferences, and notification settings"

# Spawns:
# - @lead-architect: Design profile system
# - @fullstack-dev: Profile API endpoints
# - @fullstack-dev: Avatar upload/storage
# - @frontend-ux: Profile UI components
# - @frontend-ux: Settings page
# - @test-writer: Profile tests
# - @scribe: Profile documentation
```

### Example 2: Major Refactor
```bash
/swarm "Migrate from REST to GraphQL" --agents 8

# Spawns:
# - @lead-architect: GraphQL schema design
# - @fullstack-dev: Resolver implementations (x2)
# - @fullstack-dev: Migration utilities
# - @test-writer: GraphQL tests
# - @refactorer: Client-side updates
# - @scribe: GraphQL documentation
# - @security-code-reviewer: Auth/permissions review
```

### Example 3: Full-Stack Feature
```bash
/swarm "Build real-time chat with WebSockets, message history, and file sharing"

# Spawns 10 agents covering:
# - WebSocket server
# - Message persistence
# - File upload handling
# - React chat components
# - Real-time state management
# - Unit tests
# - E2E tests
# - Documentation
# - Security review
# - Performance optimization
```

---

## Safety

- All agents work in feature branches
- No direct commits to main
- Code review required before merge
- Each agent's work is isolated
- Conflicts flagged for manual resolution

---

**This is Boris's 5-10 parallel agent method implemented for Claude Code!**
