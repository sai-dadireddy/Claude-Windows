---
description: CAREFUL MODE - Prevents mistakes that waste tokens
---

# CAREFUL MODE - Think First, Act Once

**CRITICAL**: This mode prevents the costly mistake-redo cycle that burns tokens.

## Step 1: STOP and Read Requirements

Before ANY implementation:

1. **Read the request 3 times**
   - What is the EXACT goal?
   - What are the constraints?
   - What should NOT be changed?

2. **Check existing implementations**
   ```bash
   # Search for similar patterns FIRST
   grep -r "similar_function_name" --include="*.py" --include="*.ts" .
   ```

3. **Verify file paths exist**
   ```bash
   # Don't assume files exist - CHECK
   ls -la path/to/file
   ```

## Step 2: Plan with Verification

**ULTRATHINK before coding:**

```
1. What files need to change?
   - [ ] File 1: path/to/file1.py
   - [ ] File 2: path/to/file2.ts

2. What existing code can I reuse?
   - Function X in utils.py
   - Component Y in components/

3. What are the dependencies?
   - Imports needed
   - APIs to call
   - Database models to reference

4. What could go wrong?
   - Edge case 1
   - Edge case 2
   - Potential conflicts
```

## Step 3: Verify BEFORE Implementation

**Check these BEFORE writing code:**

1. **Does this function already exist?**
   ```bash
   # Search entire codebase
   grep -r "function_name" --include="*.py" .
   ```

2. **Does this pattern already exist?**
   ```bash
   # Search for similar implementations
   grep -r "similar_pattern" -A 5 -B 5 .
   ```

3. **Are there existing utilities?**
   - Check utils/ directory
   - Check helpers/ directory
   - Check lib/ directory

## Step 4: Implement Once, Correctly

**Rules:**
- ✅ Write code ONLY after verification complete
- ✅ Test assumptions before coding
- ✅ Use existing patterns and utilities
- ❌ Never assume file paths
- ❌ Never duplicate existing functions
- ❌ Never implement without verification

## Step 5: Self-Review Before Submitting

**Before showing user the code, check:**

1. Did I follow existing patterns?
2. Did I reuse existing utilities?
3. Did I handle edge cases?
4. Did I verify all file paths?
5. Is this the SIMPLEST solution?

## Token Impact

**Without Careful Mode:**
- Implementation: 20K tokens
- Find mistake: 5K tokens
- Fix attempt 1: 15K tokens
- Fix attempt 2: 15K tokens
- **Total: 55K tokens**

**With Careful Mode:**
- Verification: 5K tokens
- Implementation: 20K tokens
- **Total: 25K tokens**

**Savings: 30K tokens per task** (54% reduction)

---

**Use this mode for EVERY task to prevent costly mistakes!**
