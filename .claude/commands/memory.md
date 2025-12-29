# Memory Update Command

## Purpose
Manually update short-term AND long-term memory with session insights.

## Instructions

### Step 1: Analyze Current Session
Ask yourself:
- What tasks were completed?
- What decisions were made?
- What patterns were discovered?
- What gotchas were encountered?

### Step 2: Categorize

**Short-term** (session-specific, temporary):
- Current task context
- Temporary decisions
- Work-in-progress notes
- Blockers to address next session
- Session-specific learnings

**Long-term** (project-wide, permanent):
- Architectural decisions
- Reusable patterns
- Critical gotchas
- Best practices discovered
- Performance insights
- Security considerations

### Step 3: Update Memory MCP

```javascript
// Short-term (current session context)
mcp__memory_short__add_observations([{
  "entityName": "CurrentSession",
  "contents": [
    "[Task completed]",
    "[Decision made]",
    "[Blocker encountered]"
  ]
}])

// Long-term (project knowledge)
mcp__memory_long__create_entities([{
  "name": "[Entity Name]",
  "entityType": "pattern|gotcha|decision|best-practice",
  "observations": [
    "[Key insight 1]",
    "[Key insight 2]"
  ]
}])

// OR update existing entity
mcp__memory_long__add_observations([{
  "entityName": "[Existing Entity]",
  "contents": [
    "[New insight to add]"
  ]
}])
```

### Step 4: Show Summary

```
💾 **MEMORY UPDATED**

📝 **Short-Term** (Session Context):
Added X observations:
  → [Observation 1]
  → [Observation 2]
  → [Observation 3]

📚 **Long-Term** (Project Knowledge):
Created/Updated: [Entity name]
  → [Key insight 1]
  → [Key insight 2]

📊 **Memory Stats**:
- Short-term: XX observations (this project)
- Long-term: XX entities (cross-project)
- Total size: ~X MB

🔍 **Query Example**:
Try: /memory-query "how did we handle authentication?"
→ Returns: JWT pattern + gotchas from long-term memory
```

## When to Use
- After completing major tasks
- Before /session-save (to capture learnings)
- When discovering important patterns/gotchas
- Manual alternative to auto-memory
- When you want explicit control over what's saved

## Token Cost
- Session analysis: ~500
- MCP updates: 1-2K
- Summary output: ~500
- **TOTAL: 2-3K tokens**

## Follow-Up
After /memory, you can:
- /memory-query "search term" - Search what was saved
- /session-save - Save everything (includes memory reference)
