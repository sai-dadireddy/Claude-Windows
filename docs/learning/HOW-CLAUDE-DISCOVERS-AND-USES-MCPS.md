# How Claude Code Discovers and Uses MCPs

**Created**: 2025-10-13
**Purpose**: Explain the complete MCP discovery, enumeration, and usage flow
**Audience**: Understanding how Claude "knows" what MCPs are available

---

## 🎯 The Question

> "How does Claude Code know it has these MCPs and when/how to use them?"

**Short answer**: Automatic discovery during startup + tool descriptions in context window

**Long answer**: Let me explain the complete flow...

---

## 📋 The Complete Flow

### **Step 1: Configuration File Read**

When Claude Code starts:

```
1. Reads: claude-code-mcp-config.json
2. Finds: "mcpServers" section
3. Sees:
   {
     "memory-auto": { "command": "python ...", "args": [...] },
     "code-index-mcp": { "command": "uvx ...", "args": [...] }
   }
```

At this point, Claude Code **knows which servers to start**, but not what tools they offer.

---

### **Step 2: MCP Server Startup (Automatic)**

For each configured MCP server:

```bash
# Claude Code launches each MCP server process
python enhanced-server.py  # memory-auto server
uvx code-index-mcp         # code-index-mcp server
```

Each MCP server:
- Starts as a separate process
- Opens communication channel with Claude Code (stdio/HTTP)
- Waits for discovery request

---

### **Step 3: MCP Discovery Protocol (Automatic)**

Claude Code sends a **discovery request** to each MCP server:

```json
// Claude Code asks each server
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

Each MCP server responds with its **tool manifest**:

```json
// Example: memory-auto responds
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "auto_store_memory",
        "description": "AUTOMATICALLY analyze and store content if important",
        "inputSchema": {
          "type": "object",
          "properties": {
            "content": { "type": "string", "description": "Content to analyze" },
            "project_name": { "type": "string", "description": "Optional project" }
          },
          "required": ["content"]
        }
      },
      {
        "name": "search_global_memory",
        "description": "Search global memory across all projects",
        "inputSchema": { ... }
      },
      // ... more tools
    ]
  }
}
```

**This is the key**: Each tool comes with:
- ✅ **Name** - What to call it
- ✅ **Description** - What it does (used by Claude for selection)
- ✅ **Input schema** - What parameters it needs

---

### **Step 4: Tool Descriptions Added to Context (Automatic)**

Claude Code takes all discovered tools and **adds their descriptions to the context window**:

```
Your context now contains:

System Tools:
├─ Read - Reads files from filesystem
├─ Write - Writes files to filesystem
├─ Bash - Executes bash commands
└─ ... (20+ built-in tools)

MCP Tools:
├─ mcp__memory-auto__auto_store_memory
│   Description: "AUTOMATICALLY analyze and store content if important"
│   Parameters: content (string), project_name (optional string)
│
├─ mcp__memory-auto__search_global_memory
│   Description: "Search global memory across all projects"
│   Parameters: query (string), limit (integer)
│
├─ mcp__code-index-mcp__search_code_advanced
│   Description: "Search for code patterns using advanced tools"
│   Parameters: pattern (string), case_sensitive (bool), ...
│
└─ ... (all other MCP tools)
```

**These tool descriptions consume tokens** - this is why Playwright (32 tools) uses 19.7K tokens!

---

### **Step 5: Claude's Reasoning (During Conversation)**

When you make a request, Claude:

1. **Reads your request**
   ```
   User: "Search my code for authentication functions"
   ```

2. **Examines available tools in context**
   ```
   Claude thinks: "I have these tools available:
   - Read (built-in) - reads files
   - Grep (built-in) - searches file contents
   - mcp__code-index-mcp__search_code_advanced - searches code patterns

   The code-index-mcp tool is best for this task because:
   - It's designed for code search
   - It has advanced pattern matching
   - It's faster than Grep for large codebases"
   ```

3. **Selects appropriate tool**
   ```
   Claude decides: Use mcp__code-index-mcp__search_code_advanced
   ```

4. **Constructs tool call**
   ```json
   {
     "tool": "mcp__code-index-mcp__search_code_advanced",
     "parameters": {
       "pattern": "authenticate|login|signin",
       "regex": true,
       "file_pattern": "*.js"
     }
   }
   ```

5. **Sends to MCP server**
   ```
   Claude Code → code-index-mcp server → executes search → returns results
   ```

6. **Processes results and responds**
   ```
   Claude: "Found 15 authentication functions in 8 files:
   - src/auth/login.js:42 - loginUser()
   - src/auth/oauth.js:18 - authenticateOAuth()
   ..."
   ```

---

## 🔍 How Claude "Knows" Which Tool to Use

Claude uses **semantic matching** between:

1. **User intent** (what you're asking for)
2. **Tool descriptions** (what each tool says it does)

### **Example 1: Memory Storage**

```
User: "Remember that we use PostgreSQL for the database"

Claude's reasoning:
- Keywords: "remember", "database"
- Available tools:
  ✅ mcp__memory-auto__auto_store_memory
     Description: "AUTOMATICALLY analyze and store content"
  ❌ mcp__code-index-mcp__search_code
     Description: "Search code patterns"

Decision: Use memory-auto because description matches "store/remember"
```

### **Example 2: Code Search**

```
User: "Find all uses of the database connection"

Claude's reasoning:
- Keywords: "find", "code", "database connection"
- Available tools:
  ❌ mcp__memory-auto__search_global_memory
     Description: "Search memory across projects"
     (This searches stored memories, not code)
  ✅ mcp__code-index-mcp__search_code_advanced
     Description: "Search code patterns"

Decision: Use code-index-mcp because it searches actual code
```

### **Example 3: Web Scraping**

```
User: "Scrape competitor pricing"

Claude's reasoning:
- Keywords: "scrape", "web", "pricing"
- Available tools:
  ❌ Read - reads local files (not web)
  ✅ mcp__playwright__playwright_navigate
     Description: "Navigate to a URL"
  ✅ mcp__playwright__playwright_get_visible_text
     Description: "Get text content from page"

Decision: Use Playwright tools for web interaction
```

---

## 💡 How Dynamic Enable/Disable Works

With Claude Code 2.0.10+:

### **Before `/mcp enable playwright`**

```
Context window contains:
├─ memory-auto tools (6 tools, ~3K tokens)
├─ code-index-mcp tools (13 tools, ~5K tokens)
└─ Total MCP tools: 19 tools, ~8K tokens

Claude cannot see Playwright tools - they're not in context!
```

### **After `/mcp enable playwright`**

```
1. User types: /mcp enable playwright

2. Claude Code:
   - Launches playwright MCP server (npx @playwright/mcp)
   - Sends discovery request
   - Receives 32 tool definitions

3. Context window updated:
├─ memory-auto tools (6 tools, ~3K tokens)
├─ code-index-mcp tools (13 tools, ~5K tokens)
├─ playwright tools (32 tools, ~19.7K tokens) ← ADDED
└─ Total MCP tools: 51 tools, ~27.7K tokens

4. Claude now sees Playwright tools and can use them!
```

### **After `/mcp disable playwright`**

```
1. User types: /mcp disable playwright

2. Claude Code:
   - Removes Playwright tool descriptions from context
   - Shuts down Playwright MCP server

3. Context window updated:
├─ memory-auto tools (6 tools, ~3K tokens)
├─ code-index-mcp tools (13 tools, ~5K tokens)
└─ Total MCP tools: 19 tools, ~8K tokens

4. Claude can no longer see Playwright tools
5. Freed ~19.7K tokens!
```

---

## 🤖 Agent Isolation Explained

### **Main Session**

```
Main Claude (You're talking to):
├─ Context: 200K window
├─ MCPs enabled: memory-auto, code-index-mcp
├─ Tool descriptions in context: 19 tools (~8K tokens)
└─ Can see: only these 19 tools
```

### **Agent Session (Spawned)**

```
Agent Claude (Isolated):
├─ Context: SEPARATE 200K window
├─ MCPs enabled: Can enable different MCPs!
│   Example: /mcp enable playwright
├─ Tool descriptions in context: 19 + 32 = 51 tools (~27.7K tokens)
└─ Can see: 51 tools (19 base + 32 Playwright)

Agent's context is isolated - doesn't affect main!
```

### **After Agent Completes**

```
Agent returns summary:
{
  "scraped_data": [...],
  "summary": "Scraped 5 sites successfully"
}

Agent context disposed:
├─ Agent's 200K context: GONE
├─ Agent's Playwright tools: GONE
├─ Agent's 27.7K tool descriptions: GONE

Main session:
├─ Receives only summary (5K tokens)
├─ Still has only 19 tools (~8K tokens)
└─ Never knew about Playwright!
```

**This is why agent isolation is so powerful!**

---

## 📊 Token Math

### **Why Playwright Uses 19.7K Tokens**

```
Playwright MCP has 32 tools:
├─ playwright_navigate (~600 tokens description)
├─ playwright_click (~580 tokens)
├─ playwright_fill (~590 tokens)
├─ playwright_screenshot (~750 tokens)
├─ playwright_get_visible_html (~790 tokens)
├─ ... 27 more tools
└─ Total: ~19,700 tokens

Each tool description includes:
- Tool name
- Description (what it does)
- Parameter schema (what inputs it needs)
- Parameter descriptions
- Default values
- Validation rules
```

### **Why GitHub Uses 18.1K Tokens**

```
GitHub MCP has 26 tools:
├─ create_repository (~660 tokens)
├─ create_pull_request (~780 tokens)
├─ search_code (~650 tokens)
├─ ... 23 more tools
└─ Total: ~18,100 tokens
```

### **Why memory-auto Uses Only 3K Tokens**

```
memory-auto MCP has 6 tools:
├─ auto_store_memory (~600 tokens)
├─ search_global_memory (~620 tokens)
├─ store_project_memory (~620 tokens)
├─ ... 3 more tools
└─ Total: ~3,000 tokens

Fewer tools = fewer tokens!
```

---

## 🎯 Key Insights

### **1. Tool Descriptions Are Always in Context**

```
If MCP is enabled → Tool descriptions consume tokens (always!)
Even if you never use the tool, its description is in your context.

This is why:
- Playwright enabled = -19.7K tokens (even if unused)
- GitHub enabled = -18.1K tokens (even if unused)
- Keep minimal MCPs = more context for actual work!
```

### **2. Claude Doesn't "Decide" to Enable MCPs**

```
❌ Claude cannot:
   - Enable MCPs automatically
   - Know about disabled MCPs
   - See tools that aren't in context

✅ Claude can only:
   - Use tools already in context
   - Suggest which tools might help (if aware of them)
   - Ask you to enable specific MCPs (if instructed)
```

### **3. Tool Selection is Semantic**

```
Claude matches:
- Your request keywords → Tool description keywords
- Your intent → Tool purpose
- Your task type → Tool capabilities

Example:
"search my code" → code-index-mcp (has "search code" in description)
"remember this" → memory-auto (has "store" in description)
"visit website" → playwright (has "navigate" in description)
```

---

## 🚀 Practical Implications

### **For Optimization**

```
Keep only essential MCPs enabled:
├─ Fewer tool descriptions in context
├─ More tokens for actual work
├─ Faster tool selection (fewer options)
└─ Cleaner reasoning

Enable heavy MCPs only when needed:
├─ /mcp enable playwright (when scraping)
├─ /mcp disable playwright (when done)
└─ Or use agents (better approach!)
```

### **For Agents**

```
Agents can enable different MCPs:
├─ Main: memory-auto, code-index-mcp (8K tokens)
├─ Agent: + playwright (27.7K tokens in agent's context!)
└─ After agent: Main still 8K tokens (agent disposed)

This is optimal because:
- Heavy MCP descriptions isolated in agent
- Main context stays lean
- Agent context disposed after task
```

### **For Tool Selection**

```
Write clear requests:
✅ "Search my code for auth functions"
   → Claude knows: use code-index-mcp

✅ "Scrape competitor pricing from their website"
   → Claude knows: use playwright

❌ "Look for auth stuff"
   → Claude confused: search code? search memory? search web?
```

---

## 📝 Summary

### **How Claude Knows About MCPs**

1. ✅ **Config file** lists enabled MCP servers
2. ✅ **Startup** launches MCP server processes
3. ✅ **Discovery** requests tool manifest from each server
4. ✅ **Tool descriptions** added to context window (consume tokens!)
5. ✅ **Reasoning** matches user request to tool descriptions
6. ✅ **Invocation** calls selected tool via MCP protocol

### **What Claude Can/Cannot Do**

✅ **Can**:
- Use any tool whose description is in context
- Reason about which tool fits the task
- Call tools with appropriate parameters
- Process tool results

❌ **Cannot**:
- Enable MCPs automatically (you must do it)
- Know about disabled MCPs (not in context)
- Use tools that aren't enabled
- Reduce token cost of tool descriptions (fixed per MCP)

### **Best Practice**

```
Start with minimal MCPs (3-5K tokens):
├─ memory-auto
└─ code-index-mcp

For heavy MCP work:
├─ Option 1: /mcp enable <server> (loads in main context)
├─ Option 2: Use specialized agent (loads in agent context) ⭐ BEST
└─ Option 3: Toggle script + restart (swap configs)

Keep main session lean - use agents for heavy MCP work!
```

---

**The magic**: MCP is an **automatic discovery protocol**. You just configure which servers to use, and Claude Code automatically discovers what tools they offer and how to use them!

No manual configuration of each tool needed - the MCP servers tell Claude everything it needs to know! 🎉
