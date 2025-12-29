# Agent + Dynamic MCP Isolation Strategy

**Created**: 2025-10-13
**Purpose**: Use agents with isolated context + dynamic MCP loading for optimal token efficiency
**Status**: Production-ready with Claude Code 2.0.10+

---

## 🎯 The Problem

**Before optimization**:
```
Main session starts:
├─ All MCPs loaded: 66.8K tokens (33% of context!)
│   ├─ Playwright: 19.7K (unused most of time)
│   ├─ GitHub: 18.1K (unused most of time)
│   ├─ AWS: 4.4K (unused most of time)
│   └─ Others: 24.6K
└─ Only 133K tokens left for actual work
```

**Token waste**: Heavy MCPs loaded but rarely used!

---

## ✅ The Solution (Two Strategies)

### **Strategy 1: Dynamic MCP Loading in Main Session**

**How it works**:
```bash
# Start with minimal MCPs
claude-code-mcp-config.json → Only memory-auto + code-index-mcp (3-5K)

# Load MCPs on-demand during session
/mcp enable playwright      # When needed (+19.7K)
# Do work...
/mcp disable playwright     # When done (-19.7K)

/mcp enable github         # When needed (+18.1K)
# Do work...
/mcp disable github        # When done (-18.1K)
```

**Benefits**:
- ✅ Start with 3-5K tokens (vs 66.8K)
- ✅ Load only what you need
- ✅ Free tokens when done
- ✅ No restart required

**Limitations**:
- ⚠️ Tokens consumed in main session when enabled
- ⚠️ Must manually enable/disable

---

### **Strategy 2: Agent Isolation (BEST!)** ⭐

**How it works**:
```
Main Session (stays clean):
├─ MCPs: memory-auto, code-index-mcp (3-5K tokens)
├─ Context: 50K tokens used
└─ Spawns specialized agent...

Agent Session (isolated context):
├─ Separate 200K context window
├─ Loads heavy MCPs: /mcp enable playwright, github, aws
├─ MCPs: 42K tokens (in agent's context, not main!)
├─ Does heavy work: web scraping, GitHub operations
├─ Uses 150K tokens (own context!)
└─ Returns summary (5K tokens) to main

Main Session After Agent:
├─ MCPs: Still only 3-5K tokens ✅
├─ Context: 55K tokens (only summary added)
└─ Agent's context DISPOSED (42K MCP overhead gone!)
```

**Benefits**:
- ✅ Main session stays ultra-lean (3-5K MCP tokens always)
- ✅ Heavy MCP work isolated in agent context
- ✅ Agent context disposed after task
- ✅ No token pollution in main session
- ✅ Can run multiple agent tasks without accumulation

**This is the BEST approach!**

---

## 🚀 Practical Implementation

### **Setup: Create Specialized Agents**

Create agent definitions that handle heavy MCP operations:

#### **1. Web Scraping Agent**

File: `.claude/agents/web-scraper-heavy.md`

```markdown
---
name: "Web Scraper (Heavy MCP)"
description: "Isolated agent for web scraping with Playwright"
model: "sonnet"
---

# Web Scraping Agent with Playwright MCP

You are a specialized web scraping agent running in an isolated context.

## Context Isolation
- You have your own 200K context window
- Your MCP usage does NOT affect the main session
- Only return concise summaries to main session

## MCP Configuration
On startup, enable required MCPs:
```bash
/mcp enable playwright
/mcp enable memory-auto
```

## Workflow
1. Enable Playwright MCP
2. Navigate and scrape target websites
3. Extract and structure data
4. Store results in memory (if needed)
5. Return concise summary to main session
6. (Optional) Disable Playwright before finishing

## What to Return
Return ONLY:
- Scraped data (structured)
- Success/failure status
- Any errors encountered
- Next steps (if applicable)

DO NOT return:
- Full page HTML
- Navigation logs
- Playwright internals
- Token usage details (handled automatically)

Your context is isolated - work freely with heavy tools!
```

#### **2. GitHub Operations Agent**

File: `.claude/agents/github-ops-heavy.md`

```markdown
---
name: "GitHub Operations (Heavy MCP)"
description: "Isolated agent for GitHub operations"
model: "sonnet"
---

# GitHub Operations Agent with GitHub MCP

You are a specialized GitHub agent running in isolated context.

## Context Isolation
- Separate 200K context window
- MCP usage isolated from main session
- Return summaries only

## MCP Configuration
```bash
/mcp enable github
/mcp enable memory-auto
```

## Capabilities
- Repository management (create, fork, clone)
- Issue management (create, update, search)
- Pull request operations (create, review, merge)
- File operations (read, create, update)
- Code search across repositories
- Branch management

## Workflow
1. Enable GitHub MCP
2. Perform requested operations
3. Handle errors gracefully
4. Store relevant context in memory
5. Return concise summary

## Return Format
```json
{
  "operation": "create_pull_request",
  "status": "success",
  "pr_number": 123,
  "url": "https://github.com/...",
  "summary": "Created PR with 5 commits",
  "next_steps": ["Wait for CI", "Request review"]
}
```

Work freely - your MCP overhead doesn't affect main session!
```

#### **3. AWS Operations Agent**

File: `.claude/agents/aws-ops-heavy.md`

```markdown
---
name: "AWS Operations (Heavy MCP)"
description: "Isolated agent for AWS cloud operations"
model: "sonnet"
---

# AWS Operations Agent with AWS MCP

You are a specialized AWS agent in isolated context.

## Context Isolation
- Own 200K window
- AWS MCP usage isolated
- Summaries only to main

## MCP Configuration
```bash
/mcp enable aws
/mcp enable memory-auto
```

## Capabilities
- CodeBuild operations
- CloudWatch logs analysis
- S3 object management
- Secrets Manager access
- Multi-profile support

## Workflow
1. Enable AWS MCP
2. Perform cloud operations
3. Analyze logs/metrics
4. Return actionable summary

## Return Format
- Operation results
- Resource IDs/ARNs
- Status and metrics
- Recommendations

Your AWS operations won't bloat main session!
```

---

## 📋 Usage Examples

### **Example 1: Web Scraping**

**Main Session**:
```
You: "Use web-scraper-heavy agent to scrape pricing from competitor sites"

Claude: [Spawns web-scraper-heavy agent]
```

**Agent Session (Isolated)**:
```bash
# Agent runs in own context
/mcp enable playwright

# Navigate and scrape
playwright.navigate("https://competitor.com/pricing")
# Extract data...
# Process results...

# Return summary to main
{
  "status": "success",
  "sites_scraped": 5,
  "pricing_data": [...],
  "insights": [...]
}

# Agent context disposed (Playwright overhead gone!)
```

**Main Session After**:
```
Claude: "✅ Scraping complete! Found pricing from 5 competitors:
[concise summary - only 5K tokens added to main]

Your main session still only has 3-5K MCP tokens!"
```

---

### **Example 2: GitHub Operations**

**Main Session**:
```
You: "Use github-ops-heavy to create PRs for all open issues labeled 'bug'"

Claude: [Spawns github-ops-heavy agent]
```

**Agent Session (Isolated)**:
```bash
/mcp enable github

# Search issues
github.search_issues(label: "bug", state: "open")

# For each issue, create PR
for issue in issues:
  github.create_pull_request(...)

# Return summary
{
  "prs_created": 12,
  "total_issues": 15,
  "failed": 3,
  "urls": [...]
}

# Agent context disposed
```

**Main Session After**:
```
Claude: "✅ Created 12 PRs for bug issues.
3 failed due to conflicts - need manual review.

Main session: Still 3-5K MCP tokens!"
```

---

### **Example 3: Multi-Agent Workflow**

**Complex task using multiple heavy-MCP agents**:

```
You: "Research competitor websites, then update our GitHub repo with findings, then deploy to AWS"

Main Session orchestrates:
├─ Agent 1: web-scraper-heavy
│   └─ Returns: Competitor analysis (5K tokens)
├─ Agent 2: github-ops-heavy
│   └─ Returns: PR created (2K tokens)
└─ Agent 3: aws-ops-heavy
    └─ Returns: Deployment status (3K tokens)

Main session total added: 10K tokens (summaries only)
Total MCP overhead in main: Still 3-5K tokens!

Each agent's heavy MCP usage: ISOLATED and DISPOSED
```

**This is POWERFUL!**

---

## 🎯 Best Practices

### **DO ✅**

1. **Start main session with minimal MCPs**
   - Only `memory-auto` + `code-index-mcp`
   - 3-5K token overhead

2. **Use agents for heavy MCP work**
   - Playwright scraping → `web-scraper-heavy`
   - GitHub operations → `github-ops-heavy`
   - AWS operations → `aws-ops-heavy`

3. **Design agents to return summaries**
   - Not full data dumps
   - Structured results only
   - Actionable insights

4. **Chain agents for complex workflows**
   - Each agent does one thing well
   - Pass summaries between agents
   - Main session orchestrates

5. **Let agents manage their MCPs**
   - Agents can `/mcp enable` what they need
   - Agent context disposed after
   - No cleanup needed in main

### **DON'T ❌**

1. **Load heavy MCPs in main session**
   - Use agents instead
   - Keep main lean

2. **Return full data from agents**
   - Summaries only
   - Process in agent context

3. **Forget context isolation benefit**
   - Agents can use 150K tokens freely
   - Won't affect main session

4. **Manually manage MCP lifecycle in main**
   - Let agents handle heavy MCPs
   - Main stays clean

---

## 📊 Token Comparison

### **Scenario: Web scraping + GitHub + AWS work**

**Old way (all MCPs in main)**:
```
Session start: 66.8K (MCPs) + 20K (work) = 86.8K
After task: 86.8K + 40K (results) = 126.8K tokens used
```

**New way (agents with isolation)**:
```
Main session:
  Start: 3K (MCPs) + 10K (work) = 13K
  Agent summaries: 13K + 10K = 23K tokens used ✅

Agent contexts (disposed):
  Agent 1: 19.7K (Playwright) + 50K (work) = DISPOSED
  Agent 2: 18.1K (GitHub) + 40K (work) = DISPOSED
  Agent 3: 4.4K (AWS) + 30K (work) = DISPOSED
```

**Savings**: 103.8K tokens in main session! (82% reduction)

---

## 🚀 Quick Start

### **1. Ensure You're on Claude Code 2.0.10+**

```bash
claude version
```

If < 2.0.10, update:
```bash
claude update
```

### **2. Set Up Minimal Main Config**

Already done! Your current config:
```json
{
  "mcpServers": {
    "memory-auto": {...},
    "code-index-mcp": {...}
  }
}
```

### **3. Create Agent Definitions**

```bash
# Copy templates
.\tools\setup-heavy-mcp-agents.ps1
```

(Script creates the 3 agent definitions above)

### **4. Use Agents for Heavy Work**

```
# Instead of this (bad):
/mcp enable playwright
# Do scraping in main session...

# Do this (good):
"Use web-scraper-heavy to scrape competitor sites"
# Agent handles Playwright in isolated context!
```

---

## 🎉 Benefits Summary

| Aspect | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Startup MCP tokens** | 66.8K | 3-5K | 93% reduction |
| **Main session after heavy work** | 120K+ | 20-30K | 75% reduction |
| **Context available** | 80K | 170K | 2.1x more |
| **Restart required** | Yes | No | ✅ Dynamic |
| **Agent isolation** | No | Yes | ✅ Clean |

---

## 🔮 Future Enhancements

When GitHub Issue #4476 is resolved (agent-scoped MCPs):

```json
{
  "agent": "web-scraper-heavy",
  "mcpServers": {
    "playwright": {...}  // Only available to this agent
  }
}
```

This would add:
- ✅ True MCP exclusivity per agent
- ✅ Even better isolation
- ✅ No global MCP pollution

But **current approach already works great!**

---

## 📝 Recommended Workflow

**Daily work**:
```
1. Start Claude Code (minimal MCPs, 3-5K tokens)
2. Do regular coding work (main session)
3. Need web scraping? → Spawn web-scraper-heavy agent
4. Need GitHub ops? → Spawn github-ops-heavy agent
5. Need AWS work? → Spawn aws-ops-heavy agent
6. Continue coding (main session still clean!)
```

**Each agent**:
- Runs in isolated 200K context
- Loads only MCPs it needs
- Does heavy work
- Returns summary (5-10K tokens)
- Context disposed (MCP overhead gone!)

**Result**: Your main session stays at 20-40K tokens all day! 🎉

---

**Status**: ✅ Ready to use with Claude Code 2.0.10+
**Next**: Create agent definitions and start using isolated heavy-MCP agents!
