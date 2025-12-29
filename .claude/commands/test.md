---
description: Comprehensive testing (generate|heal|plan|run|coverage|e2e)
argument-hint: <action> [target]
allowed-tools: Read, Write, Bash, Grep, Task
model: sonnet
---

# Testing Operations

Action: $ARGUMENTS

## Available Actions:

### generate [file]
Generate comprehensive tests for file or component
- Unit tests, integration tests
- Edge cases, error scenarios
- Coverage analysis (80%+ target)
- Test fixtures and mocks
- Delegates to: @test-automator

### heal [test-file]
Fix failing tests automatically
- Analyzes failure reasons (logs, diffs)
- Updates test logic
- Maintains test intent
- Regenerates fixtures if needed
- Updates snapshots when safe
- Delegates to: @test-healer

### plan [feature]
Create test plan for feature/module
- Test strategy (unit/integration/e2e)
- Test cases breakdown (scenarios, inputs)
- Coverage goals
- Risk analysis
- Generates TEST-PLAN.md

### run [pattern]
Run tests with pattern matching
- Executes test suite
- Reports results (passed/failed/skipped)
- Suggests fixes for failures
- Pattern: path/name/regex

### coverage [threshold]
Generate coverage report
- threshold: 80|90|100 (default: 80)
- Identifies uncovered code
- Coverage report saved
- Suggests tests for gaps
- Delegates to: @coverage-analyzer

### e2e [test-file]
End-to-end/integration testing
- Browser automation (Playwright, Cypress)
- User flow testing
- Multi-step scenarios
- Performance monitoring
- Visual regression
- Delegates to: @playwright-test-engineer

### audit
Security testing audit
- Test coverage for security paths
- Injection testing
- Authentication testing
- Authorization testing
- Delegates to: @security-auditor

### performance [component]
Performance/load testing
- Load testing
- Stress testing
- Memory profiling
- Response time analysis
- Delegates to: @performance-engineer

## Usage Examples:
```
/test generate @src/auth.ts
/test heal tests/auth.test.ts
/test plan user-authentication
/test run auth
/test coverage 90
/test e2e tests/checkout.spec.ts
/test audit
/test performance api-endpoints
```

## Frameworks Supported:
- Unit: Jest, Vitest, Pytest, unittest
- Integration: Cucumber, Test Café
- E2E: Playwright, Cypress, Selenium
- Load: k6, Apache JMeter
- API: REST Assured, SuperTest

## Key Features:
- Auto-detects test framework
- Generates skeleton tests
- Maintains test organization
- Updates test configs
- Parallel test execution
- CI/CD integration ready

## Integration:
- Task tool for parallel test runs
- Results tracked in ROADMAP.md
- Coverage reports saved to .claude/context/
- Test metrics in token-tracker.json
