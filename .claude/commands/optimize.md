---
description: Comprehensive optimization (code|performance|refactor|tokens|all)
argument-hint: <type> [target]
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
model: sonnet
---

# Optimization Operations

Type: $ARGUMENTS

## Available Actions:

### code [file|dir]
General code optimization
- Clean code principles (SOLID, DRY, KISS)
- Design patterns (Factory, Strategy, Observer)
- Best practices (error handling, logging)
- Readability improvements
- Dead code removal
- Complexity analysis

### performance [component]
Performance optimization
- Algorithm efficiency (Big O analysis)
- Memory usage (profiling, leaks)
- Database queries (indexing, caching)
- Caching strategies (Redis, in-memory)
- Bundle size (tree-shaking, compression)
- Delegates to: @performance-engineer

### refactor [scope]
Safe refactoring operations
- Scope: safe (default), large, aggressive
- Maintains functionality (tests required)
- Improves structure (modularization)
- Updates tests automatically
- Generates refactoring report
- Delegates to: @code-reviewer

### tokens
Token usage optimization
- Reduce context consumption
- Optimize configs (.claudeignore, settings)
- Consolidate duplicate commands
- Profile token usage patterns
- Archive old context files
- Archive old sessions

### database [component]
Database optimization
- Query analysis and tuning
- Index optimization
- Connection pooling
- Query caching strategies
- Delegates to: @database-optimizer

### security [scope]
Security-focused optimization
- scope: dependencies|code|infrastructure (default: code)
- Vulnerability scanning
- Dependency updates
- Security hardening
- Delegates to: @security-auditor

### all [dir]
Run all optimizations on directory
- Code quality
- Performance
- Token usage
- Security
- Generates comprehensive report
- Time: 5-10 minutes for medium projects

## Usage Examples:
```
/optimize code @src/utils.ts
/optimize performance api-endpoints
/optimize refactor safe
/optimize tokens
/optimize database users-table
/optimize security
/optimize all src/
```

## Pre-execution Checks:
```bash
!git status
```
Ensures clean working directory before major optimizations.

## Key Features:
- Auto-detects problem areas
- Generates before/after metrics
- Maintains test coverage
- Updates documentation
- Creates git-friendly diffs
- Supports parallel execution

## Integration:
- Specialized agents for each type
- Task tool for parallel optimizations
- Results tracked in ROADMAP.md
- Metrics saved to token-tracker.json
