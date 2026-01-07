# Swarm - Parallel Agent Spawner

**Description:** Spawn parallel agents with complexity tiers (Auto-Claude + Boris method)
**Argument Hint:** [simple|standard|complex] <feature-description> [--agents N]
**Allowed Tools:** Task, Read, Glob, Grep, Bash

---

## Usage

```bash
/swarm simple "Add logout button"              # 3 agents (quick tasks)
/swarm standard "Add user authentication"      # 5-6 agents (features)
/swarm complex "Build payment system"          # 8-12 agents (systems)
/swarm "Implement dashboard"                   # Auto-detect complexity
/swarm analyze                                 # Analyze task for parallelization
```

---

## Complexity Tiers (Auto-Claude Pattern)

### SIMPLE (3 agents, ~10 min)
For: Bug fixes, small features, UI tweaks

| Wave | Agents |
|------|--------|
| 1 | @fullstack-dev (implement) |
| 2 | @test-writer (tests), @qa-fixer (validate & fix) |

### STANDARD (5-6 agents, ~20 min)
For: New features, API endpoints, components

| Wave | Agents |
|------|--------|
| 1 | @lead-architect (plan) |
| 2 | @fullstack-dev (backend), @frontend-ux (frontend) |
| 3 | @test-writer (tests), @qa-fixer (validate & fix), @scribe (docs) |

### COMPLEX (8-12 agents, ~30-45 min)
For: Major features, system integrations, refactors

| Wave | Agents |
|------|--------|
| 1 | @lead-architect (architecture), @qa-engineer (test plan) |
| 2 | @fullstack-dev x2 (backend, DB), @frontend-ux x2 (UI, state) |
| 3 | @test-writer x2 (unit, E2E), @security-code-reviewer |
| 4 | @qa-fixer (validate all), @scribe (documentation) |

---

## Prompt

When user runs `/swarm`:

Feature: $ARGUMENTS

### Phase 1: DETECT COMPLEXITY

```
Analyzing task complexity...

Factors:
- Number of files likely affected
- Cross-cutting concerns (auth, DB, API, UI)
- Integration points
- Test requirements

Detected: [SIMPLE|STANDARD|COMPLEX]
Agent Count: [3-12]
```

### Phase 2: AGENT PIPELINE (Auto-Claude Pattern)

```
┌─────────────────────────────────────────────────────────────┐
│                    SWARM PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WAVE 1: PLANNING                                           │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │  Planner    │    │  QA Plan    │                        │
│  │  (Opus)     │    │  (Sonnet)   │                        │
│  └──────┬──────┘    └──────┬──────┘                        │
│         └────────┬─────────┘                                │
│                  ↓                                          │
│  WAVE 2: IMPLEMENTATION                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │ Backend │ │ Backend │ │Frontend │ │Frontend │          │
│  │   #1    │ │   #2    │ │   #1    │ │   #2    │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
│       └──────────┬┴──────────┬┴──────────┘                 │
│                  ↓                                          │
│  WAVE 3: VALIDATION                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
│  │ Test Writer │ │  Security   │ │   Scribe    │          │
│  │  (Haiku)    │ │  (Sonnet)   │ │  (Haiku)    │          │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘          │
│         └────────────────┴────────────────┘                 │
│                          ↓                                  │
│  WAVE 4: QA FIX (Auto-Claude Pattern)                      │
│  ┌─────────────────────────────────────┐                   │
│  │            @qa-fixer                 │                   │
│  │  - Run all tests                    │                   │
│  │  - Fix failing tests                │                   │
│  │  - Fix linting errors               │                   │
│  │  - Validate security findings       │                   │
│  │  - Ensure build passes              │                   │
│  └─────────────────────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: SPAWN AGENTS

```python
# WAVE 1 - Planning (parallel)
Task(subagent_type="lead-architect", prompt="...", run_in_background=True)
Task(subagent_type="qa-engineer", prompt="...", run_in_background=True)

# Wait for Wave 1...

# WAVE 2 - Implementation (parallel)
Task(subagent_type="fullstack-dev", prompt="Backend API...", run_in_background=True)
Task(subagent_type="fullstack-dev", prompt="Database...", run_in_background=True)
Task(subagent_type="frontend-ux", prompt="UI components...", run_in_background=True)
Task(subagent_type="frontend-ux", prompt="State management...", run_in_background=True)

# Wait for Wave 2...

# WAVE 3 - Validation (parallel)
Task(subagent_type="test-writer", prompt="...", run_in_background=True)
Task(subagent_type="security-code-reviewer", prompt="...", run_in_background=True)
Task(subagent_type="scribe", prompt="...", run_in_background=True)

# Wait for Wave 3...

# WAVE 4 - QA Fix (sequential, catches everything)
Task(subagent_type="qa-fixer", prompt="Run tests, fix failures, ensure build passes")
```

### Phase 4: OUTPUT

```
SWARM ACTIVATED
═══════════════════════════════════════════════════════════════

Feature: [Feature Name]
Complexity: [SIMPLE|STANDARD|COMPLEX]
Total Agents: [N]
Pipeline: Planner → Coder → QA → Fixer

WAVE 1: PLANNING - Launching NOW
─────────────────────────────────────────
🚀 @lead-architect - System design
🚀 @qa-engineer - Test strategy

WAVE 2: IMPLEMENTATION - Queued
─────────────────────────────────────────
⏳ @fullstack-dev x2 - Backend + Database
⏳ @frontend-ux x2 - UI + State

WAVE 3: VALIDATION - Queued
─────────────────────────────────────────
⏳ @test-writer - Unit + E2E tests
⏳ @security-code-reviewer - Security audit
⏳ @scribe - Documentation

WAVE 4: QA FIX - Final
─────────────────────────────────────────
⏳ @qa-fixer - Fix all issues, ensure green build

═══════════════════════════════════════════════════════════════

Commands:
  /swarm status     - Check agent progress
  /swarm results    - Collect completed work
  /swarm wave2      - Launch next wave when ready
  /swarm abort      - Cancel all agents
```

---

## Agent Assignment Matrix

| Tier | Agent | Model | Role |
|------|-------|-------|------|
| Planning | @lead-architect | opus | System design, ADRs |
| Planning | @qa-engineer | sonnet | Test strategy, fixtures |
| Coding | @fullstack-dev | sonnet | Backend, API, DB |
| Coding | @frontend-ux | sonnet | UI, components, state |
| Testing | @test-writer | haiku | Unit tests, E2E tests |
| Security | @security-code-reviewer | sonnet | Vulnerabilities, OWASP |
| Docs | @scribe | haiku | README, API docs |
| **QA Fix** | **@qa-fixer** | **sonnet** | **Fix all failures** |

---

## QA Fixer Agent (Auto-Claude Pattern)

The **@qa-fixer** agent runs LAST and ensures:

1. All tests pass (`npm test`, `pytest`, etc.)
2. Linting passes (`eslint`, `black`, etc.)
3. Type checking passes (`tsc`, `pyright`, etc.)
4. Build succeeds (`npm run build`, etc.)
5. Security issues from review are addressed
6. No TODO comments left unresolved

This is the **self-validating QA loop** from Auto-Claude.

---

## Examples

### Simple Task
```bash
/swarm simple "Add dark mode toggle to settings"

# Spawns 3 agents:
# Wave 1: @fullstack-dev (implement toggle)
# Wave 2: @test-writer (test), @qa-fixer (validate)
```

### Standard Feature
```bash
/swarm standard "Add user profile with avatar upload"

# Spawns 6 agents:
# Wave 1: @lead-architect (design)
# Wave 2: @fullstack-dev (API), @frontend-ux (UI)
# Wave 3: @test-writer, @scribe, @qa-fixer
```

### Complex System
```bash
/swarm complex "Build payment processing with Stripe integration"

# Spawns 10 agents:
# Wave 1: @lead-architect, @qa-engineer
# Wave 2: @fullstack-dev x2, @frontend-ux x2
# Wave 3: @test-writer, @security-code-reviewer, @scribe
# Wave 4: @qa-fixer (ensures everything works)
```

---

## Token Efficiency by Tier

| Tier | Agents | Tokens | Time |
|------|--------|--------|------|
| Simple | 3 | ~3,000 | ~10 min |
| Standard | 5-6 | ~8,000 | ~20 min |
| Complex | 8-12 | ~15,000 | ~30-45 min |

Sequential alternative would use 3-5x more tokens.

---

## Safety

- All agents work in feature branches
- No direct commits to main
- @qa-fixer ensures build passes before completion
- Security review catches vulnerabilities
- Conflicts flagged for manual resolution

---

**Combines Boris's parallel method + Auto-Claude's QA pipeline!**
