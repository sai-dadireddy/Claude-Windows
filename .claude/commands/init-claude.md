Analyze this codebase and generate a **CLAUDE.md** file for future Claude instances working in this repository.

## What to Include

### 1. Development Commands
- Build commands (`npm run build`, `cargo build`, etc.)
- Lint/format commands
- Test commands (run all, run single test)
- Dev server commands

### 2. Architecture Overview
Focus on **cross-file patterns** that require understanding multiple files:
- How components communicate
- Data flow patterns
- Key abstractions and their purposes
- Non-obvious conventions

### 3. Important Context
Extract relevant sections from:
- Existing README.md
- .cursor/rules or .cursorrules
- .github/copilot-instructions.md
- Any CONTRIBUTING.md

## What to EXCLUDE

- **Generic best practices** (testing is good, handle errors, etc.)
- **Exhaustive file listings** (don't list every component)
- **Self-evident instructions** (obvious from code)
- **Made-up sections** (only document what exists)
- **Redundancy** (don't repeat existing docs)

## Quality Standards

- Keep it **concise and actionable**
- Focus on **big picture** architecture
- If quoting, max 125 characters with quotation marks
- Paraphrase where possible

## Required Header

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## Output Format

Generate a complete CLAUDE.md file ready to save. Structure:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Commands

[Essential dev commands in a table or code blocks]

## Architecture

[High-level architecture overview]

## Key Patterns

[Important patterns and conventions]

## Project-Specific Notes

[Any gotchas, non-obvious things]
```

---

**If a CLAUDE.md already exists**, suggest improvements rather than replacing it entirely.

Now analyze this codebase and generate the CLAUDE.md.
