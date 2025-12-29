# Test All Systems

Run a comprehensive test of all Claude Code customizations: hooks, memory systems, MCP tools, and skills.

## Instructions

Perform the following tests IN ORDER and report results:

---

### 1. HOOKS TEST

**SessionStart Hook** - Check if you received:
- Git context (branch, changes)
- Skills available notification
- Memory status (if any memories exist)
- Session available notification

Report what you see in your context.

**Test PostToolUse Hook** - Create a small test file:
```bash
echo "test" > /tmp/hook_test.py
```
Check if auto-formatter or code-quality messages appeared.

**Test PreToolUse Security** - Try to read a sensitive file:
```bash
cat ~/.claude/memory/.env
```
Report if it was blocked or allowed.

---

### 2. MEMORY SYSTEMS TEST

**A. Semantic Memory (Hooks-based)**

1. Save a test memory:
```bash
~/.claude/scripts/memory_manager.py save-memory "test-project" "decision" "Test decision: Using pytest for testing framework"
```

2. Search semantically:
```bash
~/.claude/scripts/memory_manager.py search "test-project" "testing framework"
```

3. Check stats:
```bash
~/.claude/scripts/memory_manager.py stats
```

**B. MCP Memory (Knowledge Graph)**

1. Load memory toolset:
```
mcp__mcp-router__router_load_toolset category="memory"
```

2. Try to create an entity (report if it works):
```
mcp__mcp-router__router_execute category="memory" server="memory" tool="create_entities" args={"entities": [{"name": "TestEntity", "entityType": "test", "observations": ["Created for testing"]}]}
```

---

### 3. MCP TOOLS TEST

**List all categories:**
```
mcp__mcp-router__router_list_categories
```

**Test Context7 (docs):**
```
mcp__mcp-router__router_load_toolset category="docs"
```
Then try to resolve a library:
```
mcp__mcp-router__router_execute category="docs" server="context7" tool="resolve-library-id" args={"libraryName": "react"}
```

**Test other categories exist:**
- Report which of these categories are available: memory, filesystem, git, github, aws, database, thinking, web, time, docs

---

### 4. SLASH COMMANDS TEST

Test that these commands are recognized (just list them, don't execute):
- /session-save
- /session-continue
- /memory-save
- /memory-recall
- /memory-status

---

### 5. SKILLS TEST

Check if skills directory exists and list available skills:
```bash
ls ~/.config/claude-code/skills/ 2>/dev/null || echo "No skills directory"
```

---

### 6. SUMMARY REPORT

Create a summary table:

| System | Status | Notes |
|--------|--------|-------|
| SessionStart Hook | ✅/❌ | What was injected |
| PostToolUse Hook | ✅/❌ | Auto-format worked? |
| PreToolUse Security | ✅/❌ | Blocks sensitive files? |
| Semantic Memory | ✅/❌ | Save/search works? |
| MCP Memory | ✅/❌ | Knowledge graph works? |
| MCP Router | ✅/❌ | Categories available? |
| Context7 (docs) | ✅/❌ | Library lookup works? |
| Slash Commands | ✅/❌ | All 5 recognized? |
| Skills | ✅/❌ | Directory exists? |

---

## At the End

Save this test as a memory:
```bash
~/.claude/scripts/memory_manager.py save-memory "global" "learning" "System test completed on $(date). All systems operational."
```

$ARGUMENTS
