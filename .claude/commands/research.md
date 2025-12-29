---
description: Research codebase with parallel agents - Phase 1 of 4-phase workflow
argument-hint: <topic/feature>
allowed-tools: Read, Grep, Glob, Task
model: sonnet
---

# Phase 1: Research

**Goal:** Understand what exists & what needs to change. NO code written.

**Topic:** $ARGUMENTS

---

## Workflow (Parallel Agents)

### Step 1: Spawn 4 Parallel Research Agents

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

**Run in PARALLEL** - All 4 agents at once!

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
Research Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: User Authentication System

Findings:
  ✅ 4 parallel agents completed
  ✅ Found 12 relevant files
  ✅ Current implementation analyzed
  ✅ 2 related docs found in thoughts/

Research saved to:
  ~/thoughts/shared/research/2025-10-30_user-auth.md

Context: 58% (safe to continue)

Next: /plan @thoughts/shared/research/2025-10-30_user-auth.md
Or: /clear → Start fresh planning session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

**This is Phase 1 of the 4-phase workflow!**
