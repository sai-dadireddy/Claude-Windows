# Agent-MCP Architecture Strategy

## The Problem We're Solving

**Current situation**: Loading all MCPs in settings.json loads 66.8K tokens into EVERY session.

**Goal**: Load MCPs only when specific agents need them.

## ❌ What DOESN'T Work

```bash
# This command doesn't exist in Claude Code!
/mcp enable playwright
```

## ✅ Correct Architecture

### Option 1: Task Tool Agent Pattern (RECOMMENDED)

**Main session** stays completely clean - no MCP tools loaded at all.

**Agent file** specifies which MCPs it needs:

```markdown
---
name: "Web Scraper"
description: "Web scraping with Playwright"
model: "sonnet"
---

You have access to Playwright MCP tools for web scraping.
Use them directly - no need to enable anything.

Available tools:
- playwright_navigate
- playwright_screenshot
- playwright_get_visible_text
... (all 32 Playwright tools)
```

**How it works**:
1. Main session: 0 MCP tools loaded
2. User: "Scrape this website"
3. Claude invokes Task tool with "Web Scraper" agent
4. Agent context: Playwright MCP automatically loaded (20K tokens in isolated context)
5. Agent does work, returns summary
6. Agent context disposed → Playwright MCP unloaded
7. Main session: Still 0 MCP tools

### Option 2: MCP Config Profiles (ALTERNATIVE)

Create multiple MCP config files:

**claude-code-mcp-config-minimal.json** (default):
```json
{
  "mcpServers": {
    "memory-auto": { ... },
    "code-index-mcp": { ... }
  }
}
```

**claude-code-mcp-config-web.json** (for web tasks):
```json
{
  "mcpServers": {
    "memory-auto": { ... },
    "code-index-mcp": { ... },
    "playwright": { ... }
  }
}
```

**Usage**:
```bash
# Start with minimal config (default)
claude

# Or start with specific config
claude --mcp-config claude-code-mcp-config-web.json
```

## 🎯 Recommended Solution

### Step 1: Remove ALL MCPs from settings.json

```json
"mcp": {
  "enabled": false,
  "comment": "MCPs configured per-project in claude-code-mcp-config.json"
}
```

### Step 2: Keep minimal MCP config as default

**claude-code-mcp-config.json**:
```json
{
  "mcpServers": {
    "memory-auto": { ... },
    "code-index-mcp": { ... }
  }
}
```

### Step 3: Agents inherit MCPs automatically

When you invoke an agent with Task tool:
- Agent gets its OWN 200K context
- Agent inherits MCPs from config file
- MCP tools only load in agent context, not main
- Agent completes → context disposed → MCPs gone

### Step 4: Update agent files to NOT mention `/mcp enable`

```markdown
---
name: "Web Scraper"
description: "Web scraping with Playwright"
model: "sonnet"
---

# Web Scraper Agent

You are running in an ISOLATED context with Playwright MCP available.

## How Playwright is Available

Playwright MCP is automatically available in your context via the MCP configuration.
The 32 Playwright tools are loaded in YOUR context only - not the main session.

Just use the tools directly:
- playwright_navigate(url=...)
- playwright_screenshot(...)
- etc.

No need to "enable" anything - tools are already available!
```

## 📊 Token Impact

### Before (Current - Wrong):
```
Main session startup: 155K tokens
- System: 4.5K
- Tools: 21K
- MCP tools: 66.8K ← ALL MCPs loaded!
- Messages: 9K
- Free space: 45K (22%)
```

### After (Correct - Agent-Based):
```
Main session startup: 40K tokens
- System: 4.5K
- Tools: 21K
- MCP tools: 5K ← Only memory-auto + code-index
- Messages: 9K
- Free space: 160K (80%)

Agent context (when invoked):
- Agent inherits Playwright MCP: 20K
- Agent does work
- Agent context disposed → Playwright gone
- Main session: Still 40K tokens!
```

## 🚀 Implementation Steps

1. **Fix settings.json**: Set `mcp.enabled = false`
2. **Keep minimal MCP config**: Only memory-auto + code-index
3. **Update agent files**: Remove `/mcp enable` instructions
4. **Add auto-inheritance note**: Agents automatically get MCPs
5. **Test with Task tool**: Verify agents work correctly

## ✅ Success Criteria

- Main session: < 50K tokens at startup
- Agent invocation: Transparent MCP loading
- Agent completion: MCP tools disposed
- Main session after agent: Still < 50K tokens
- No manual MCP enabling needed

## 💡 Pro Tips

1. **Lazy agent loading**: Agents only load when invoked
2. **Context isolation**: Each agent gets fresh 200K context
3. **Automatic cleanup**: No manual MCP disabling needed
4. **Parallel agents**: Multiple agents can run with different MCPs
5. **Main stays clean**: MCP overhead never touches main session

---

**This is the architecture we should have been using all along!**
