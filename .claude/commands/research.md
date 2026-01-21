---
description: Research codebase with parallel agents - Phase 1 of 4-phase workflow
argument-hint: [--quick|--deep|--exhaustive] <topic/feature>
allowed-tools: Read, Grep, Glob, Task
model: sonnet
context: fork
---

# Phase 1: Research

**Goal:** Understand what exists & what needs to change. NO code written.

**Topic:** $ARGUMENTS

---

## Research Depth Levels

Parse arguments for depth flag (default: standard):

| Flag | Depth | Agents | Scope | Use When |
|------|-------|--------|-------|----------|
| `--quick` | Quick | 2 | Focused file search | Know where to look |
| (default) | Standard | 4 | Full codebase + thoughts | General feature work |
| `--deep` | Deep | 6 | + Dependencies + tests | Complex changes |
| `--exhaustive` | Exhaustive | 8 | + External docs + patterns | Major refactors |

### Depth: Quick (2 agents)
```
Agent 1: codebase-locator - Find files matching topic
Agent 2: codebase-analyzer - Quick analysis of found files
Skip: thoughts search, dependency analysis
Output: Brief summary with file:line references
```

### Depth: Standard (4 agents) - DEFAULT
```
Agent 1: codebase-locator - Find all relevant files
Agent 2: codebase-analyzer - Analyze implementation
Agent 3: thoughts-locator - Search ~/thoughts/
Agent 4: thoughts-analyzer - Extract prior knowledge
Output: Full research document
```

### Depth: Deep (6 agents)
```
Standard 4 agents PLUS:
Agent 5: dependency-analyzer - Check imports, packages, related modules
Agent 6: test-analyzer - Find related tests, coverage gaps
Output: Research doc + dependency map + test coverage
```

### Depth: Exhaustive (8 agents)
```
Deep 6 agents PLUS:
Agent 7: pattern-matcher - Search similar patterns in ~/refs/claude-cookbooks
Agent 8: external-researcher - WebSearch for best practices (2026)
Output: Comprehensive doc with external references
```

---

## Workflow (Parallel Agents)

### Step 1: Parse Depth & Spawn Agents

First, detect depth from arguments:
```
--quick     -> DEPTH=quick (2 agents)
--deep      -> DEPTH=deep (6 agents)
--exhaustive -> DEPTH=exhaustive (8 agents)
(no flag)   -> DEPTH=standard (4 agents)
```

Then spawn agents based on depth:

**QUICK (2 agents):**
```bash
Task 1: codebase-locator - Find files for: [topic]
Task 2: codebase-analyzer - Quick analysis
```

**STANDARD (4 agents):**
```bash
Task 1: codebase-locator agent
  - Find all relevant files for: [topic]
  - Use Glob patterns efficiently
  - Return: File paths with descriptions

Task 2: codebase-analyzer agent
  - Analyze current implementation
  - Extract patterns and architecture
  - Return: Code references with file:line numbers

Task 3: thoughts-locator agent
  - Search ~/thoughts/ for existing research
  - Find related plans/docs
  - Return: Relevant document paths

Task 4: thoughts-analyzer agent
  - Extract insights from found documents
  - Identify related decisions
  - Return: Summary of prior knowledge
```

**DEEP (add 2 more):**
```bash
Task 5: dependency-analyzer agent
  - Trace imports/exports
  - Map module dependencies
  - Return: Dependency graph

Task 6: test-analyzer agent
  - Find related test files
  - Identify coverage gaps
  - Return: Test coverage report
```

**EXHAUSTIVE (add 2 more):**
```bash
Task 7: pattern-matcher agent
  - Search ~/refs/claude-cookbooks for patterns
  - Find similar implementations
  - Return: Reference patterns

Task 8: external-researcher agent
  - WebSearch for "[topic] best practices 2026"
  - Find current documentation
  - Return: External references
```

**Run ALL agents in PARALLEL!**

### Step 2: Synthesize Results

```
Combine findings from all 4 agents:
- File locations
- Current architecture
- Existing documentation
- Open questions
```

### Step 3: Generate Research Document

```bash
Write ~/thoughts/shared/research/[YYYY-MM-DD]_[topic].md

Include:
## Summary of Findings
[Comprehensive overview]

## Code References
- file.ts:123 - Function handles X
- component.tsx:456 - Component does Y

## Architecture Insights
[How it currently works]

## Open Questions
- Question 1
- Question 2

## Next Steps
[What to do in planning phase]
```

### Step 4: Check Context & Clear

```bash
/context

If context > 60%:
  Save research doc ✅
  Clear context: /clear
  Ready for Phase 2: /plan @thoughts/shared/research/[file].md

If context < 60%:
  Can continue to planning in same session
```

---

## Token Efficiency

**Traditional:** 10,000-20,000 tokens (sequential file reads)
**This approach:** 2,000-4,000 tokens (parallel agents + Grep)
**Savings:** 75-80%!

---

## Output Example

```
Research Complete [STANDARD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: User Authentication System
Depth: standard (4 agents)

Findings:
  [1/4] codebase-locator: Found 12 relevant files
  [2/4] codebase-analyzer: Implementation analyzed
  [3/4] thoughts-locator: 2 related docs found
  [4/4] thoughts-analyzer: Prior decisions extracted

Research saved to:
  ~/thoughts/shared/research/2026-01-21_user-auth.md

Context: 58% (safe to continue)

Next: /plan @thoughts/shared/research/2026-01-21_user-auth.md
Or: /clear -> Start fresh planning session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**EXHAUSTIVE Example:**
```
Research Complete [EXHAUSTIVE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: Authentication Refactor
Depth: exhaustive (8 agents)

Findings:
  [1/8] codebase-locator: Found 23 relevant files
  [2/8] codebase-analyzer: 15 code references mapped
  [3/8] thoughts-locator: 4 related docs found
  [4/8] thoughts-analyzer: Prior decisions extracted
  [5/8] dependency-analyzer: 8 module dependencies
  [6/8] test-analyzer: 67% coverage, 3 gaps identified
  [7/8] pattern-matcher: Found 2 cookbook patterns
  [8/8] external-researcher: 5 external references

Research saved to:
  ~/thoughts/shared/research/2026-01-21_auth-refactor-exhaustive.md

Context: 72% (consider /clear before planning)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**This is Phase 1 of the 4-phase workflow!**
