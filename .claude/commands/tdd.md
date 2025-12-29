Implement a feature using **Test-Driven Development** (Red-Green-Refactor).

## TDD Workflow

### Phase 1: RED - Write Failing Tests First

Before writing any implementation:

1. **Define the interface** - What should this code do?
2. **Write test cases** - Cover happy path + edge cases
3. **Run tests** - Confirm they fail (RED)

```markdown
## Test Plan

**Feature:** [What we're building]
**Interface:** [Function/class signature]

### Test Cases
| Test | Input | Expected Output | Priority |
|------|-------|-----------------|----------|
| Happy path | [Input] | [Output] | P0 |
| Edge case 1 | [Input] | [Output] | P1 |
| Edge case 2 | [Input] | [Output] | P1 |
| Error case | [Input] | [Error] | P1 |

### Test File
`path/to/feature.test.ts`
```

### Phase 2: GREEN - Make Tests Pass

Write the **minimum code** to make tests pass:

1. **Implement feature** - Just enough to pass
2. **Run tests** - Confirm they pass (GREEN)
3. **No premature optimization** - "Make it work" first

```markdown
### Implementation
**File:** `path/to/feature.ts`
**Approach:** [Simplest solution that passes tests]
```

### Phase 3: REFACTOR - Improve the Code

Now that tests pass, improve code quality:

1. **Clean up** - Remove duplication, improve naming
2. **Optimize** - If needed for performance
3. **Run tests again** - Ensure still GREEN

```markdown
### Refactoring
- [ ] Remove code duplication
- [ ] Improve variable/function names
- [ ] Extract helper functions if needed
- [ ] Add inline documentation for complex logic
- [ ] Run tests: `npm test` ✓
```

## TDD Cycle Summary

```
┌─────────────────────────────────────────┐
│  1. RED: Write failing test             │
│     ↓                                   │
│  2. GREEN: Write minimal code to pass   │
│     ↓                                   │
│  3. REFACTOR: Clean up, keep tests green│
│     ↓                                   │
│  Repeat for next test case...           │
└─────────────────────────────────────────┘
```

## Test Types to Consider

| Type | When | Example |
|------|------|---------|
| **Unit** | Individual functions | `validateEmail()` returns true for valid email |
| **Integration** | Component interactions | API endpoint returns correct response |
| **Edge Cases** | Boundary conditions | Empty input, null, max values |
| **Error Handling** | Failure scenarios | Network timeout, invalid data |

## Commands

```bash
# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- path/to/file.test.ts

# Run with coverage
npm test -- --coverage
```

## Output

After TDD cycle, you'll have:
- ✅ Tests that document expected behavior
- ✅ Implementation that passes all tests
- ✅ Confidence to refactor safely

---

**Feature to implement with TDD:**

$ARGUMENTS
