# Codex CLI Troubleshooting Guide

**Last Updated**: 2025-10-14
**Status**: ✅ All Issues Resolved

---

## Issues Found and Fixed

### Issue 1: Codex CLI Output Format Differs in Subprocess

**Problem**: Codex CLI outputs different formats when run interactively vs. in subprocess:
- **Interactive**: Includes markers like `\ncodex\n`, `\ntokens used\n`, config blocks
- **Subprocess/Piped**: Just returns raw response without markers

**Symptoms**:
- "Empty response from Codex" errors
- Response length shows data but parsing returns empty string
- Works in terminal but fails in Python subprocess

**Root Cause**:
```python
# Codex detects if it's in interactive mode (TTY) vs piped
# Interactive: Full formatted output with sections
# Piped: Minimal output, just the response
```

**Fix Applied** (`auto-multi-ai-orchestrator.py` lines 333-373):
```python
# Handle BOTH output formats
if codex_marker in output and tokens_marker in output:
    # Format 1: Interactive with markers
    start_idx = output.find(codex_marker) + len(codex_marker)
    end_idx = output.find(tokens_marker, start_idx)
    response = output[start_idx:end_idx].strip()
else:
    # Format 2: Subprocess/piped - entire output IS the response
    response = output.strip()
```

---

### Issue 2: Windows Encoding Issues (UnicodeDecodeError)

**Problem**: Windows uses cp1252 encoding by default, causing `UnicodeDecodeError` when Codex outputs Unicode characters (smart quotes, em dashes, etc.)

**Symptoms**:
```python
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 2229
```

**Root Cause**:
```python
# subprocess.run() defaults to system encoding (cp1252 on Windows)
# Codex outputs UTF-8, causing decode errors
```

**Fix Applied** (`auto-multi-ai-orchestrator.py` lines 293-303):
```python
result = subprocess.run(
    [codex_cmd, 'exec', '--full-auto'],
    input=prompt,
    capture_output=True,
    text=True,
    encoding='utf-8',          # ← Explicitly use UTF-8
    errors='replace',           # ← Replace invalid chars instead of crashing
    timeout=60,
    shell=True
)
```

---

### Issue 3: Input Sanitization Too Aggressive

**Problem**: Input sanitization blocks legitimate parentheses `()` in task descriptions, which are common in natural language (e.g., "tools (like Vite)")

**Symptoms**:
```
Input sanitization failed: Input contains potentially dangerous pattern: [;&|`$()]
```

**Root Cause**:
```python
DANGEROUS_PATTERNS = [
    r'[;&|`$()]',  # ← Blocks () which are legitimate in tasks AND code!
]
```

**Fix Applied** (`auto-multi-ai-orchestrator.py` lines 63-70):
```python
# FIXED: Removed parentheses from dangerous patterns
# Parentheses are legitimate in task descriptions AND code
DANGEROUS_PATTERNS = [
    r'[;&|`$]',  # Shell metacharacters (parentheses removed)
    r'\\x[0-9a-fA-F]{2}',  # Hex escapes
    r'\x00',  # Null bytes
]
```

**Rationale**: Parentheses are NOT a shell injection risk in Python subprocess with proper argument passing. They're legitimate in:
- Task descriptions: "technologies (like React)"
- Code: function calls, conditionals, tuples
- Only `;`, `&`, `|`, `` ` ``, `$` are truly dangerous for command injection

---

### Issue 4: Welcome Messages in Response

**Problem**: Codex sometimes starts responses with generic welcome messages instead of actual analysis

**Symptoms**:
```
Response: "Hey! I'm ready whenever you are—what can I help you build today?"
```

**Fix Applied** (`auto-multi-ai-orchestrator.py` lines 359-373):
```python
# Remove welcome messages that sometimes appear
unwanted_prefixes = [
    "Hey! I'm ready",
    "Hey there",
    "Everything's set up",
    "I'm ready whenever"
]
for unwanted in unwanted_prefixes:
    if response.startswith(unwanted):
        # Skip welcome message, get actual content
        lines = response.split('\n')
        if len(lines) > 1:
            response = '\n'.join(lines[1:]).strip()
        break
```

---

## Quick Troubleshooting Checklist

### Codex CLI Not Found

**Check**:
```bash
codex --version
# Should output: codex-cli 0.46.0
```

**Fix**:
```bash
# Windows: Add to PATH or use full path
C:\Users\USERNAME\AppData\Roaming\npm\codex.cmd

# Set environment variable (optional)
$env:CODEX_CLI_PATH="C:\...\codex.cmd"
```

### Empty Response from Codex

1. **Check exit code**:
   - Exit code 0 = Success, check parsing logic
   - Exit code != 0 = Error, check stderr

2. **Check output length**:
   ```
   [CODEX DEBUG] stdout length: 1027, exit code: 0
   ```
   - If length > 0 but empty response → Parsing issue
   - If length = 0 → Codex didn't respond

3. **Test Codex directly**:
   ```bash
   echo "Test prompt" | codex exec --full-auto
   ```

### Unicode/Encoding Errors

**Always use UTF-8**:
```python
subprocess.run(..., encoding='utf-8', errors='replace')
```

### Input Sanitization Blocking Code

**Check if prompt contains code**:
```python
if "CODE:" in prompt or "def " in prompt or "function " in prompt:
    # Skip sanitization for code reviews
```

---

## Circuit Breaker Behavior

**When It Opens**:
- After 3 consecutive failures
- Blocks calls for 60 seconds

**How to Reset**:
1. Wait 60 seconds (automatic)
2. Or restart orchestrator

**Check Status**:
```python
CIRCUIT_BREAKER_STATE = {
    "codex": {"failures": 0, "state": "closed"},  # closed = healthy
    "gemini": {"failures": 0, "state": "closed"}
}
```

---

## Testing After Fixes

### Test 1: Simple Prompt
```bash
python auto-multi-ai-orchestrator.py \
  --task "Test Codex integration" \
  --validate
```

### Test 2: Code Review with Special Characters
```bash
python auto-multi-ai-orchestrator.py \
  --task "Review for SQL injection" \
  --code "SELECT * FROM users WHERE id = user_input" \
  --validate
```

### Test 3: Both AIs Together
```bash
python auto-multi-ai-orchestrator.py \
  --task "Review authentication security" \
  --code "def login(user, pwd): return db.query('SELECT * WHERE name=' + user)" \
  --validate \
  --research \
  --google-api-key "$GOOGLE_API_KEY"
```

**Expected Result**: Both Codex and Gemini return comprehensive feedback

---

## Summary of All Fixes

| Issue | Status | Lines Changed |
|-------|--------|---------------|
| Subprocess output format | ✅ Fixed | 333-373 |
| Windows UTF-8 encoding | ✅ Fixed | 293-303 |
| Input sanitization | ✅ Fixed | 244-260, 470-484 |
| Welcome message handling | ✅ Fixed | 359-373 |
| Exit code checking | ✅ Fixed | 305-310 |

**Total**: ~80 lines of code added/modified

---

## For Future Claude Sessions

If you encounter Codex issues:

1. **Check this file first**: `CODEX-CLI-TROUBLESHOOTING.md`
2. **Verify fixes are in place**: Check lines mentioned above
3. **Test with simple prompt**: Rule out complex issues
4. **Check circuit breaker**: May be open from previous failures
5. **Review logs**: `tools/logs/multi-ai/session_*.json`

**All issues have been resolved as of 2025-10-14.**

---

## Key Learnings

1. **Codex behaves differently in subprocess vs interactive**
   - Always handle both output formats

2. **Windows encoding requires explicit UTF-8**
   - Don't rely on system defaults

3. **Code reviews need special sanitization handling**
   - Distinguish between task descriptions and code parameters

4. **Circuit breaker is your friend**
   - Prevents cascading failures
   - Auto-resets after timeout

5. **Test with real examples**
   - SQL injection code is perfect test case
   - Contains parentheses, quotes, special chars

---

**The orchestrator is now production-ready with both AIs fully functional!** 🎉
