Generate **comprehensive tests** for existing code that doesn't have test coverage.

## When to Use

- Code already written, needs test coverage
- Retrofitting tests to legacy code
- Increasing coverage metrics
- Understanding existing code through tests

**Note:** For new code, use `/tdd` instead (write tests first).

## Process

### Phase 1: Code Analysis

Analyze the target code:

```markdown
## Test Generation Plan

**Target:** [File or module path]
**Type:** [Function/Class/Module/API endpoint]
**Current Coverage:** [X% or "None"]

### Code Characteristics
- Pure function / Has side effects
- Sync / Async
- Dependencies: [List external deps]
- Complexity: [Low/Medium/High]
```

### Phase 2: Test Case Identification

```markdown
### Identified Test Cases

#### Happy Path Tests
| Test | Input | Expected Output |
|------|-------|-----------------|
| [Basic usage] | [Input] | [Output] |
| [Common case] | [Input] | [Output] |

#### Edge Cases
| Test | Input | Expected Output |
|------|-------|-----------------|
| [Empty input] | [] | [Behavior] |
| [Null/undefined] | null | [Behavior] |
| [Boundary value] | [Max/Min] | [Behavior] |

#### Error Cases
| Test | Input | Expected Error |
|------|-------|----------------|
| [Invalid input] | [Bad data] | [Error type] |
| [Missing required] | [Partial] | [Error type] |

#### Integration Points
| Test | Setup | Assertion |
|------|-------|-----------|
| [External call] | [Mock setup] | [Verify behavior] |
```

### Phase 3: Test Implementation

```markdown
### Test Structure

**Test File:** `[path]/__tests__/[name].test.ts`

**Setup Required:**
- [ ] Mock [dependency 1]
- [ ] Test fixtures for [data]
- [ ] Database seeding (if needed)

**Test Organization:**
```
describe('[ModuleName]', () => {
  describe('[functionName]', () => {
    it('should [happy path]', ...)
    it('should [edge case]', ...)
    it('should throw when [error case]', ...)
  })
})
```
```

### Phase 4: Coverage Verification

```bash
# Run tests with coverage
npm test -- --coverage --collectCoverageFrom='[target]'

# Or for Python
pytest --cov=[module] --cov-report=term-missing
```

## Test Patterns by Code Type

### Pure Functions
```typescript
describe('calculateTotal', () => {
  it('should sum items correctly', () => {
    expect(calculateTotal([10, 20, 30])).toBe(60)
  })

  it('should return 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0)
  })
})
```

### Async Functions
```typescript
describe('fetchUser', () => {
  it('should return user data', async () => {
    const user = await fetchUser('123')
    expect(user).toMatchObject({ id: '123' })
  })

  it('should throw on not found', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow('Not found')
  })
})
```

### Classes
```typescript
describe('UserService', () => {
  let service: UserService

  beforeEach(() => {
    service = new UserService(mockDb)
  })

  describe('create', () => {
    it('should create user with valid data', ...)
  })
})
```

### API Endpoints
```typescript
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com' })

    expect(res.status).toBe(201)
    expect(res.body).toHaveProperty('id')
  })
})
```

## Output

After generation:
- ✅ Test file created at appropriate location
- ✅ All identified cases covered
- ✅ Mocks/fixtures set up
- ✅ Coverage report generated

---

**Code to generate tests for:**

$ARGUMENTS
