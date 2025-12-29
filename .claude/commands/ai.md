---
description: Multi-AI coordination (orchestrate|review|consult|analyze|delegate)
argument-hint: <action> [task/target]
allowed-tools: Task, Bash, Read, Write, Grep
model: sonnet
---

# Multi-AI Operations

Execute action: $ARGUMENTS

## Available Actions:

### orchestrate <task>
Coordinate multiple AI models for complex task
- Claude (architecture, planning)
- GPT-4 (code generation via n8n)
- Gemini (verification, testing via API)
- Parallel execution where possible
- Auto-synthesizes results

### review <target>
Multi-AI code review with consensus
- Multiple perspectives on same code
- Consensus-based recommendations
- Security, performance, architecture angles
- Delegates to: @security-auditor, @code-reviewer, @performance-engineer
- Format: `/ai review @src/auth/` or `/ai review path/file.ts`

### consult <question>
AI panel consultation on architecture/strategy
- Get diverse AI perspectives
- Synthesize best approach
- Decision support for architectural choices
- Returns ranked recommendations

### analyze <scope>
Deep analysis using specialized models
- scope: code|architecture|performance|security (default: code)
- Claude analyzes structure
- GPT-4 analyzes efficiency
- Gemini verifies correctness

### delegate <agent> <task>
Delegate task to specialized agent with context
- Agents: @security-auditor, @performance-engineer, @test-automator, @docs-architect
- Auto-loads context (files, ROADMAP, dependencies)
- Tracks in ROADMAP.md
- Example: `/ai delegate @security-auditor "scan API endpoints"`

## Usage Examples:
```
/ai orchestrate "implement OAuth2 flow with PKCE"
/ai review @src/auth/
/ai consult "best caching strategy for API"
/ai analyze performance src/components/
/ai delegate @security-auditor "audit database access"
```

## Smart Model Selection:
- Simple tasks: Claude (fast, efficient)
- Code generation: Multi-AI (accuracy)
- Security: Delegates to @security-auditor
- Performance: Delegates to @performance-engineer
- Testing: Delegates to @test-automator

## Integration:
- n8n orchestration for GPT-4 calls
- Gemini API for verification
- Task tool for parallel execution
- Results saved to .claude/context/
