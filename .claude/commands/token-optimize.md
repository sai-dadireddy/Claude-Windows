Review and optimize **token consumption** for the current project/session.

## The Problem

Everything hitting stdout/stderr from tools counts as input tokens:
- Verbose test output (pytest, jest, etc.)
- Docker logs
- Build output
- Stack traces
- Progress bars
- Coverage reports

A single verbose `pytest` run can cost more tokens than the reasoning that follows.

## Token Optimization Strategies

### 1. Test Output Filtering

Create wrapper scripts that only report failures:

```bash
# pytest-quiet.sh
#!/bin/bash
pytest "$@" 2>&1 | grep -E "(FAILED|ERROR|::.*FAILED|^E )" || echo "All tests passed"
```

```bash
# jest-quiet.sh
#!/bin/bash
npm test -- --silent 2>&1 | grep -E "(FAIL|✕|Error:)" || echo "All tests passed"
```

### 2. Log Level Management

```python
# Set logging to ERROR only for AI sessions
import os
if os.environ.get('AI_SESSION'):
    logging.getLogger().setLevel(logging.ERROR)
```

### 3. Output Truncation

Add to CLAUDE.md:
```markdown
## Token Optimization

When running commands that produce verbose output:
- Add `| head -50` to limit output
- Use `--quiet` or `--silent` flags
- Pipe through `grep` for relevant lines only
```

### 4. Semantic Compaction (TOON format)

JSON → TOON conversion saves 30-60% tokens.
Already enabled via `user_prompt_submit.py` hook.

### 5. Test Wrappers for Common Commands

| Command | Optimized Version |
|---------|-------------------|
| `pytest` | `pytest -q --tb=no` (quiet, no traceback) |
| `npm test` | `npm test -- --silent` |
| `cargo test` | `cargo test --quiet` |
| `go test` | `go test -v 2>&1 \| grep -E "(FAIL\|PASS\|---)"` |

### 6. Docker Log Limits

```bash
# Instead of: docker logs -f container
docker logs --tail 50 container  # Last 50 lines only
```

### 7. Build Output Filtering

```bash
# Instead of: npm run build
npm run build 2>&1 | grep -E "(error|warning|Error|Warning)" || echo "Build succeeded"
```

## Project-Specific Recommendations

Analyze the current project and suggest:

1. **Identify verbose commands** commonly used
2. **Create wrapper scripts** in `scripts/` directory
3. **Update CLAUDE.md** with token-efficient alternatives
4. **Set environment flags** for quiet mode

## Output

```markdown
## Token Optimization Report

### Current Issues
- [Verbose command 1]: [Token impact]
- [Verbose command 2]: [Token impact]

### Recommended Changes

1. **Create `scripts/test-quiet.sh`**
   ```bash
   [wrapper script]
   ```

2. **Update CLAUDE.md**
   ```markdown
   [additions]
   ```

3. **Environment Variables**
   ```bash
   export AI_SESSION=1
   export LOG_LEVEL=ERROR
   ```

### Estimated Token Savings
- Test runs: ~[X]% reduction
- Build output: ~[X]% reduction
- Logs: ~[X]% reduction
```

---

**Analyze current project for token optimization opportunities:**

$ARGUMENTS
