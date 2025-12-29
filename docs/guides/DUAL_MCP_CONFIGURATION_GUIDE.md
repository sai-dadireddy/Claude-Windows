# Dual MCP Configuration: Claude Desktop vs Claude Code

## Overview

Your system has **TWO separate MCP configurations** optimized for different use cases:

1. **Claude Desktop** - Conversational AI, planning, research
2. **Claude Code** - Implementation, coding, agent orchestration

---

## Configuration Files

### Claude Desktop MCP Config

**Location:** `C:\Users\SainathreddyDadiredd\AppData\Roaming\Claude\claude_desktop_config.json`

**Purpose:** All MCPs loaded immediately for interactive conversations

**Characteristics:**
- ✅ All MCPs available instantly
- ✅ Tools appear in conversation immediately
- ✅ No agent invocation needed
- ⚠️ Higher token overhead (~66K MCP tools)
- ⚠️ Less context space for conversations

**When to Use:**
- Quick questions requiring MCP tools
- Interactive exploration with GitHub, AWS, etc.
- Web browsing with Playwright
- Memory searches
- One-off tasks

### Claude Code MCP Config

**Location:** `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude-code-mcp-config.json`

**Purpose:** Agent-ready architecture - MCPs loaded only when agents need them

**Characteristics:**
- ✅ Zero token overhead in main session
- ✅ 80-85% more context space (160-170K free)
- ✅ MCPs auto-load in agent contexts
- ✅ Clean context disposal after agents
- ✅ Optimal for coding work
- ⏳ Requires agent invocation via Task tool

**When to Use:**
- Long coding sessions
- Complex implementation work
- Multi-step projects
- Architecture design
- When you need maximum context space

---

## Draw.io MCP - Dual Installation Complete ✅

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "drawio": {
      "command": "npx",
      "args": ["-y", "drawio-mcp-server"]
    }
  }
}
```

**Access Method:** Direct - tools available immediately after restart

**Usage:**
```
User: "Create an AWS architecture diagram with API Gateway, Lambda, DynamoDB"
Claude: *Uses draw.io tools directly*
```

### Claude Code Configuration

```json
{
  "mcpServers": {
    "drawio": {
      "_tokens": "~5-8K (8 tools)",
      "_agent_usage": "Live diagram creation and modification",
      "command": "npx",
      "args": ["-y", "drawio-mcp-server"]
    }
  }
}
```

**Access Method:** Via agents (Task tool)

**Usage:**
```
User: "Create an AWS architecture diagram"
Claude: *Launches diagram-creation agent with draw.io MCP loaded*
Agent: *Creates diagram in isolated context*
Claude: *Returns diagram summary to main session*
```

---

## Complete MCP Inventory

### Shared Across Both Configs

| MCP Server | Tools | Claude Desktop | Claude Code | Primary Use |
|------------|-------|----------------|-------------|-------------|
| **memory-auto** | 6 | ✅ Instant | ✅ Agent-ready | Knowledge storage/retrieval |
| **code-index-mcp** | 13 | ✅ Instant | ✅ Always available | Code search, file indexing |
| **playwright** | 32 | ✅ Instant | ✅ Agent-ready | Web automation, scraping |
| **github** | 26 | ✅ Instant | ✅ Agent-ready | GitHub operations |
| **aws** | 7 | ✅ Instant | ✅ Agent-ready | AWS operations |
| **sequential-thinking** | 1 | ✅ Instant | ✅ Agent-ready | Complex reasoning |
| **langchain** | 5 | ✅ Instant | ✅ Agent-ready | Vector search, embeddings |
| **ai-workflows** | 6 | ✅ Instant | ✅ Agent-ready | Local AI code generation |
| **testing** | 4 | ✅ Instant | ✅ Agent-ready | Test automation |
| **drawio** | 8 | ✅ Instant (new) | ✅ Agent-ready (new) | Diagram creation |

**Total Tools:**
- Claude Desktop: ~128 tools (~66K tokens)
- Claude Code Main Session: 0 tools (0K tokens)
- Claude Code Agent Session: Only tools agent needs

---

## Token Impact Analysis

### Claude Desktop

```
Startup Tokens: ~100K
├── System + Context: ~34K
├── MCP Tools: ~66K
└── Free Space: ~100K (50%)

After adding draw.io:
├── System + Context: ~34K
├── MCP Tools: ~74K (+8K)
└── Free Space: ~92K (46%)
```

**Impact:** -4% free space (acceptable for conversational use)

### Claude Code (Agent Architecture)

```
Main Session: ~40K
├── System + Tools: ~30-40K
├── MCP Tools: 0K
└── Free Space: ~160K (80%)

Agent Session (with draw.io):
├── Agent Context: ~20K
├── draw.io MCP: ~8K
├── memory-auto: ~3K
└── Free Space: ~169K (84.5%)

After agent completes:
├── Context Disposed: -31K
├── Main Session: ~40K
└── Free Space: ~160K (80%)
```

**Impact:** Zero impact on main session (perfect)

---

## How Agent Architecture Works (Claude Code)

### Traditional Approach (Claude Desktop)
```
Main Session:
  ├── All 128 MCP tools loaded (~66K tokens)
  ├── Free space: ~100K
  └── All conversations share same context
```

### Agent Architecture (Claude Code)
```
Main Session:
  ├── Zero MCP tools (0K tokens)
  ├── Free space: ~160K
  └── Use Task tool to invoke agents

Agent Invocation:
  ├── New isolated 200K context
  ├── Only MCPs agent needs loaded
  ├── Agent works independently
  └── Returns summary to main

Agent Completion:
  ├── Agent context disposed
  ├── MCP tools unloaded
  ├── Main session unchanged
  └── 5-10K summary added
```

**Benefits:**
- 85% more context in main session
- MCPs only loaded when needed
- Clean context isolation
- Optimal token efficiency

---

## Usage Patterns

### Creating Diagrams in Claude Desktop

**After Restart:**

1. Open draw.io desktop application
2. Create new blank diagram
3. Ask Claude directly:

```
"Create an AWS architecture diagram showing:
- API Gateway at the top
- Lambda function in the middle
- DynamoDB at the bottom
- Connect them with arrows"
```

**Claude Response:**
```
*Uses draw.io MCP tools directly*
- Creates rectangles with create-rectangle
- Adds connections with create-connection
- Inserts AWS icons with insert-shape
- Returns: "Diagram created!"
```

### Creating Diagrams in Claude Code

**Approach A: Direct Request (Agent Auto-Launch)**

```
User: "Create an AWS architecture diagram with API Gateway, Lambda, DynamoDB"

Claude Code:
  ├── Detects diagram creation task
  ├── Launches diagram-creation agent
  └── Agent uses draw.io MCP in isolated context

Agent:
  ├── Opens draw.io (if not open)
  ├── Creates diagram elements
  ├── Adds connections and labels
  └── Returns: "Diagram complete with 3 services and 2 connections"

Main Session: Free space still 160K
```

**Approach B: Explicit Agent Request**

```
User: "Use the diagram agent to create an AWS architecture"

Claude Code:
  ├── Invokes Task tool with diagram-creation agent
  └── Passes detailed requirements

Agent:
  ├── draw.io MCP loaded (~8K tokens in agent context)
  ├── memory-auto loaded (~3K tokens in agent context)
  ├── Creates diagram live
  └── Stores diagram metadata in memory

Result: Main session unaffected, 160K space preserved
```

---

## Activation Steps

### Claude Desktop

1. **Already Configured:** Draw.io MCP added to config
2. **Restart Required:** Close and reopen Claude Desktop
3. **Verification:** Run `claude mcp list` in Claude Desktop
4. **Test:** Open draw.io desktop → Ask Claude to create diagram

### Claude Code

1. **Already Configured:** Draw.io MCP added to config
2. **No Restart Needed:** Agent architecture auto-inherits config
3. **Verification:** Check `claude-code-mcp-config.json` exists
4. **Test:** Ask to create diagram → Agent launches with draw.io MCP

---

## Best Practices

### When to Use Claude Desktop

✅ Quick interactive tasks
✅ Browsing documentation with Playwright
✅ GitHub repository exploration
✅ AWS service queries
✅ Memory searches
✅ Simple diagram creation

### When to Use Claude Code

✅ Long implementation sessions
✅ Complex multi-file refactoring
✅ Architecture design work
✅ Large codebase analysis
✅ When you need maximum context
✅ Agent-based workflows

---

## Agent-to-MCP Mapping (Claude Code)

When agents are invoked, they automatically get these MCPs:

| Agent Type | MCPs Loaded | Token Cost |
|------------|-------------|------------|
| **diagram-creation** | drawio, memory-auto | ~11K |
| **architecture-designer** | drawio, memory-auto | ~11K |
| **web-scraper-heavy** | playwright, memory-auto | ~23K |
| **github-ops-heavy** | github, memory-auto | ~21K |
| **aws-ops-heavy** | aws, memory-auto | ~7K |
| **youtube-research-heavy** | playwright, memory-auto | ~23K |
| **visual-analysis-heavy** | playwright, memory-auto | ~23K |
| **any-agent** | memory-auto, code-index-mcp | ~11K |

**Note:** Token costs only apply to agent context, NOT main session!

---

## Troubleshooting

### Draw.io Tools Not Available in Claude Desktop

**Check:**
1. Config file has `"drawio"` section
2. Package name is `drawio-mcp-server` (NOT `@lgazo/drawio-mcp-server`)
3. Claude Desktop was restarted after config change
4. Run `claude mcp list` to verify connection

**Fix:**
```bash
# Verify config
cat "C:\Users\SainathreddyDadiredd\AppData\Roaming\Claude\claude_desktop_config.json"

# Test package
npx -y drawio-mcp-server --help

# Restart Claude Desktop
```

### Draw.io Agent Not Loading in Claude Code

**Check:**
1. `claude-code-mcp-config.json` exists in project root
2. File has `"drawio"` section
3. Node.js and npx are installed

**Fix:**
```bash
# Verify config
cat claude-code-mcp-config.json

# Test package directly
npx -y drawio-mcp-server --help

# Explicitly request agent
"Use the diagram-creation agent to make an AWS diagram"
```

### MCP Connection Failed

**Common Issues:**

1. **Node.js not installed**
   - Download: https://nodejs.org/
   - Verify: `node --version`

2. **npx not in PATH**
   - Fix: Restart terminal/application after Node.js install

3. **draw.io desktop not running**
   - The MCP server needs draw.io desktop application open
   - Launch draw.io first, then ask Claude

4. **Firewall blocking npx**
   - Allow npx in Windows Defender
   - Check antivirus settings

---

## Memory Storage

This dual configuration setup has been stored in memory:

**Stored Knowledge:**
- Two separate MCP configs (Desktop vs Code)
- Agent architecture token benefits
- Draw.io MCP installation in both configs
- Usage patterns for each environment
- Agent-to-MCP mapping
- Troubleshooting steps

**Future Sessions:**
- Claude will know about dual configuration
- Claude will choose appropriate environment
- Claude will recommend agents when beneficial
- Claude will reference token efficiency

---

## Summary

### Configuration Status

✅ **Claude Desktop:** draw.io MCP added - restart required
✅ **Claude Code:** draw.io MCP added - ready now (agent-based)
✅ **Memory:** Dual configuration knowledge stored
✅ **Documentation:** Complete reference created

### Token Efficiency

| Metric | Claude Desktop | Claude Code |
|--------|----------------|-------------|
| **Startup Tokens** | ~100K | ~40K |
| **MCP Tools** | 128 tools | 0 tools |
| **Free Space** | ~100K (50%) | ~160K (80%) |
| **Draw.io Impact** | -8K (-4%) | 0K (0%) |
| **Optimal For** | Quick tasks | Long sessions |

### Next Steps

**Claude Desktop:**
1. Restart application
2. Verify: `claude mcp list`
3. Test: Create simple diagram

**Claude Code:**
1. No restart needed
2. Test: Ask for diagram → agent launches
3. Observe: Main session context preserved

---

## Related Documentation

- `projects/aws-chatbot/docs/DRAWIO_MCP_SETUP_COMPLETE.md` - Draw.io MCP details
- `projects/aws-chatbot/docs/AWS_ICONS_GUIDE.md` - AWS architecture icons
- `claude-code-mcp-config.json` - Agent-ready configuration
- `CLAUDE.md` - Global instructions referencing both configs

**The dual MCP configuration gives you the best of both worlds: instant access in Claude Desktop and token-efficient agents in Claude Code!** 🚀
