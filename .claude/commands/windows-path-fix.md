# Windows Path Bug Fix (Auto-Enforcement)

**Bug**: Claude Code Edit tool fails with "File has been unexpectedly modified"
**Cause**: Windows path handling bug in Claude Code
**Solution**: Always use absolute Windows paths with backslashes

---

## 🚨 MANDATORY PATH FORMAT (All File Operations!)

### ✅ CORRECT Format
```
C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\file.py
```

**Rules:**
- ✅ Absolute path (starts with drive letter)
- ✅ Backslashes (`\`)
- ✅ Full path from root

### ❌ WRONG Formats
```
# Relative paths
projects/erpa/file.py

# Forward slashes
C:/Users/.../file.py

# Mixed slashes
C:\Users/.../file.py

# Partial paths
erpa\file.py
```

---

## 🎯 Apply To ALL File Tools

**Affected Tools:**
- `Read` - Use absolute Windows paths
- `Edit` - Use absolute Windows paths
- `Write` - Use absolute Windows paths
- `Glob` - Use absolute Windows paths (for path parameter)
- `NotebookEdit` - Use absolute Windows paths

**Not Affected:**
- `Bash` commands (use as-is)
- `Grep` (optional, but recommended)

---

## 📝 Implementation Rules

1. **Before ANY file operation**, convert to absolute Windows path
2. **Start with**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\`
3. **Use backslashes**: NOT forward slashes
4. **Full path always**: From drive letter to file

---

## 🔄 Path Conversion Examples

### Example 1: Project File
**User says**: "Edit lambda_function.py"
**You use**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\infrastructure\terraform\lambda\chat-handler\lambda_function.py`

### Example 2: Root Config
**User says**: "Update CLAUDE.md"
**You use**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\CLAUDE.md`

### Example 3: Project Tracker
**User says**: "Read PROJECT-TRACKER"
**You use**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\PROJECT-TRACKER.md`

---

## 🛠️ Quick Reference

**Base Path**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\`

**Common Paths:**
```
Root:     C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\
ERPAGPT:  C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\
Phases:   C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\phases\
Docs:     C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\docs\
Lambda:   C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\projects\erpa\erpagpt\infrastructure\terraform\lambda\chat-handler\
```

---

## 🔗 Reference

**Bug Source**: [Reddit - Claude Code Windows Bug](https://www.reddit.com/r/ClaudeCode/comments/)
**Status**: Known issue, workaround required
**Auto-loaded**: Via CLAUDE.md enforcement

---

**Auto-loaded**: This command runs automatically via CLAUDE.md enforcement
**Override**: Not allowed - path format is MANDATORY on Windows
