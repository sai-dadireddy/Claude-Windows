# Memory Usage Patterns & Examples
**Complete guide to using Claude Code's memory systems effectively**

---

## Quick Reference

**Memory Tiers:**
1. **Short-term:** Session context (auto-cleared)
2. **Long-term:** Permanent knowledge (manually curated)
3. **SQLite:** Structured data (databases)
4. **ChromaDB:** Semantic search (vectors)

**Access Methods:**
- Main session: `mcp__memory_short__*`, `mcp__memory_long__*`
- Agents: Full MCP access + auto-classification
- Direct: SQLite queries, file operations

---

## Pattern 1: Storing Project Decisions

### When to Use
- Major architectural decisions
- Technology choices
- Design pattern selections
- Deployment strategies

### Example: Recording an Architecture Decision

```javascript
// Store decision in long-term memory
mcp__memory_long__create_entities({
  entities: [{
    name: "AGUPGRADE Dynamic UI Architecture",
    entityType: "architecture-decision",
    observations: [
      "Database: Aurora PostgreSQL with ui_configurations table (JSONB)",
      "Storage: S3 bucket agupgrade-assets for logos/images/themes",
      "Backend: 5 Python Lambda functions for /ui/* endpoints",
      "Frontend: Next.js 15 Server Components fetch config on every request",
      "Zero frontend deployments after initial setup",
      "Decided October 21, 2025 after stakeholder review",
      "Benefits: 83-92% time savings for UI changes",
      "Trade-off: Slightly slower first load (acceptable for admin UIs)"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Captures WHY decision was made
- ✅ Includes trade-offs considered
- ✅ Records date for historical context
- ✅ Measurable benefits documented
- ✅ Available across all sessions

---

## Pattern 2: Tracking Session Progress

### When to Use
- Complex multi-day tasks
- Incremental implementations
- Troubleshooting sessions
- Learning new technologies

### Example: Tracking Implementation Progress

```javascript
// Create entity for project
mcp__memory_short__create_entities({
  entities: [{
    name: "PowerShell Auto-Load Implementation",
    entityType: "implementation-task",
    observations: [
      "Goal: Auto-run /load-global when starting Claude Code with scl",
      "User requirement: As we use PS7 to start scl, auto-load global instructions",
      "Started: October 22, 2025 6:00 PM"
    ]
  }]
})

// Add observations as you progress
mcp__memory_short__add_observations({
  observations: [{
    entityName: "PowerShell Auto-Load Implementation",
    contents: [
      "✅ Researched 3 solutions: Enhanced wrapper, startup hook, clipboard",
      "✅ Recommended solution: Enhanced SCL wrapper (95% automatic)",
      "✅ Created scl-auto function in PowerShell 7 profile",
      "✅ Supports 3 modes: full, lite, manual (-NoAutoLoad)",
      "✅ Time savings: 10 sec/session, 6 hours/year",
      "✅ Backward compatible with all existing commands",
      "✅ Documentation created: 2 comprehensive guides",
      "Status: COMPLETE - Ready to use"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Shows progress over time
- ✅ Easy to resume after breaks
- ✅ Documents decision trail
- ✅ Captures solutions for similar future tasks

---

## Pattern 3: Building Knowledge Graphs

### When to Use
- Understanding system relationships
- Mapping dependencies
- Tracking interconnected concepts
- Building mental models

### Example: Mapping Multi-AI System

```javascript
// Create entities for each AI
mcp__memory_short__create_entities({
  entities: [
    {
      name: "Claude Code",
      entityType: "ai-system",
      observations: [
        "Best for: Implementation, file operations, direct tool use",
        "Context: 200K tokens",
        "Cost: $220/month (Max 20x plan)",
        "Strengths: Fastest execution, full file system access"
      ]
    },
    {
      name: "ChatGPT-5",
      entityType: "ai-system",
      observations: [
        "Best for: Architecture, deep reasoning, complex planning",
        "Model: o3-mini (deep thinking mode)",
        "Cost: $0 (included in Premium subscription)",
        "Strengths: Superior reasoning, architectural design"
      ]
    },
    {
      name: "Gemini Pro",
      entityType: "ai-system",
      observations: [
        "Best for: Large codebase analysis, security audits",
        "Context: 1-2M tokens (5-10x Claude!)",
        "Cost: $0.30/M (10x cheaper than Claude)",
        "Strengths: Massive context, cost-effective scanning"
      ]
    }
  ]
})

// Create relationships
mcp__memory_short__create_relations({
  relations: [
    {
      from: "Claude Code",
      to: "ChatGPT-5",
      relationType: "routes_planning_to"
    },
    {
      from: "Claude Code",
      to: "Gemini Pro",
      relationType: "routes_large_scans_to"
    },
    {
      from: "Multi-AI Orchestration System",
      to: "Claude Code",
      relationType: "orchestrated_by"
    }
  ]
})
```

### Why This Pattern Works
- ✅ Visual knowledge structure
- ✅ Easy to query relationships
- ✅ Expandable as system grows
- ✅ Helps AI understand connections

---

## Pattern 4: Capturing Solutions to Problems

### When to Use
- Debugging complex issues
- Finding workarounds
- Discovering undocumented behavior
- Learning from failures

### Example: Recording a Fix

```javascript
mcp__memory_long__create_entities({
  entities: [{
    name: "Auto-Compact Continuation Fix",
    entityType: "solution",
    observations: [
      "Problem: Auto-compact works but continuation to next chat fails",
      "Symptom: 40-60% context loss during session transitions",
      "Root Cause: Handoff prompt pattern is MANUAL, not automatic",
      "User feedback: Feels 'like a stroke' when auto-compact hits",
      "Solution: Automatic checkpoint at 30% context, emergency at 10%",
      "Implementation: Create NEXT_SESSION_CONTINUATION.txt with full context",
      "Result: Context loss reduced from 40-60% to 0-5%",
      "Recovery time: 10-20 min reduced to <2 min",
      "Files created: AUTO-COMPACT-CONTINUATION-FIX.md (267 lines)",
      "Discovered: October 22, 2025 during user troubleshooting session"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Problem-solution pair for future reference
- ✅ Root cause analysis preserved
- ✅ Measurable results documented
- ✅ Helps avoid repeating same debugging

---

## Pattern 5: Learning Technology Patterns

### When to Use
- Mastering new frameworks
- Best practice discovery
- Performance optimization
- Security patterns

### Example: Storing Best Practices

```javascript
mcp__memory_long__create_entities({
  entities: [{
    name: "Next.js 15 Server Components Pattern",
    entityType: "best-practice",
    observations: [
      "Pattern: Fetch data in Server Components, not Client Components",
      "Benefits: Better SEO, faster initial load, reduced client JavaScript",
      "Use case: Perfect for dynamic UI configs fetched from database",
      "Anti-pattern: Don't use useState with server-fetched data",
      "Performance: ~40% faster Time to Interactive vs client-side fetching",
      "Example: agupgrade-dashboard fetches UI config in layout.tsx",
      "Learned from: AGUPGRADE Dynamic UI implementation, Oct 21 2025"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Reusable knowledge
- ✅ Real example provided
- ✅ Performance metrics included
- ✅ Anti-patterns noted

---

## Pattern 6: Storing Tool Configurations

### When to Use
- Complex tool setups
- Multi-step configurations
- Credential management
- Environment-specific settings

### Example: Recording Configuration

```javascript
mcp__memory_long__create_entities({
  entities: [{
    name: "Gemini CLI Configuration",
    entityType: "tool-config",
    observations: [
      "Version: 0.8.2",
      "Installation: npm install -g @google/gemini-cli",
      "Location: /c/Users/.../npm/gemini",
      "Authentication: GOOGLE_API_KEY in environment",
      "File inclusion: @path/to/file or @path/to/dir/",
      "All files: --all_files flag",
      "Context window: 1-2M tokens (5-10x Claude)",
      "Cost: $0.30/M input tokens (10x cheaper than Claude)",
      "Integration: Multi-AI orchestration system",
      "Auto-routing: >50 files, security audits, pattern detection",
      "Verified working: October 22, 2025"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Quick reference for setup
- ✅ Integration notes included
- ✅ Cost comparison provided
- ✅ Verification date recorded

---

## Pattern 7: Session Handoff for Continuity

### When to Use
- Long-running tasks spanning multiple sessions
- Context window approaching limit
- Team handoffs
- Resuming after breaks

### Example: Creating Handoff Summary

```javascript
// Before context fills up
mcp__memory_short__create_entities({
  entities: [{
    name: "Session Handoff - October 22 2025",
    entityType: "session-summary",
    observations: [
      "Session duration: 4 hours",
      "Main tasks completed: 4/5",
      "✅ PowerShell auto-load implemented",
      "✅ Gemini CLI verified and integrated",
      "✅ Memory systems diagnostic complete",
      "✅ Auto-compact continuation fix designed",
      "⏳ Pending: Testing memory operations",
      "Files created: 5 (POWERSHELL-AUTO-LOAD-*.md, GEMINI-*.md, MEMORY-*.md, AUTO-COMPACT-*.md)",
      "Git commits: 2 (bf43842, 7481c38)",
      "Context at end: 72% used",
      "Next session: Test all memory systems, commit final documentation"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Clear status snapshot
- ✅ Easy to resume
- ✅ Nothing forgotten
- ✅ Context preserved

---

## Pattern 8: Multi-Agent Coordination

### When to Use
- Delegating to specialized agents
- Parallel work streams
- Complex research tasks
- Isolated operations

### Example: Agent Task Coordination

```javascript
// Before launching agents
mcp__memory_short__create_entities({
  entities: [{
    name: "Web Scraper Agent Task - AI News",
    entityType: "agent-task",
    observations: [
      "Agent: web-scraper-heavy",
      "Task: Scrape latest AI news from 30+ sources",
      "MCPs used: playwright, memory_short",
      "Expected duration: 15-20 minutes",
      "Output format: Markdown summary + JSON data",
      "Storage: docs/ai-news/daily-digest-YYYY-MM-DD.md",
      "Launched: October 22, 2025 7:15 PM",
      "Status: Running in background (isolated 200K context)"
    ]
  }]
})

// After agent completes
mcp__memory_short__add_observations({
  observations: [{
    entityName: "Web Scraper Agent Task - AI News",
    contents: [
      "✅ Completed: October 22, 2025 7:32 PM (17 minutes)",
      "Sources scraped: 28/30 (2 timeouts)",
      "Articles found: 247",
      "Filtered to: 45 high-quality articles",
      "Categories: 12 (LLMs, Tools, Research, Business, etc.)",
      "File created: docs/ai-news/daily-digest-2025-10-22.md (128KB)",
      "Context used by agent: 147K/200K (73%)",
      "Main session impact: 2K tokens (summary only)",
      "Result: SUCCESS"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Tracks agent activity
- ✅ Measures performance
- ✅ Records context efficiency
- ✅ Helps optimize future tasks

---

## Pattern 9: Error Documentation

### When to Use
- Recurring errors
- Non-obvious fixes
- System quirks
- Workarounds needed

### Example: Recording Error Solution

```javascript
mcp__memory_long__create_entities({
  entities: [{
    name: "Lambda Permission Case Sensitivity Issue",
    entityType: "error-solution",
    observations: [
      "Error: S3 triggers not working despite correct configuration",
      "Investigation: Lambda permissions had 'AWS:SourceArn' (uppercase)",
      "AWS Requirement: Condition keys should be 'aws:SourceArn' (lowercase)",
      "Surprising: AWS CLI accepts both cases (misleading!)",
      "Actual Cause: Internal validation accepts uppercase but S3 service doesn't",
      "Solution: Use lowercase 'aws:SourceArn' always",
      "Command: aws lambda add-permission with lowercase condition",
      "Verification: Tested with 6 S3 uploads - all successful",
      "Project: ERPAGPT chatbot (rag pipeline)",
      "Date: October 20, 2025",
      "Impact: Critical - blocked entire RAG document processing pipeline"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Prevents repeating same debugging
- ✅ Documents non-obvious issues
- ✅ Helps team members
- ✅ Shows AWS quirks

---

## Pattern 10: Performance Metrics Tracking

### When to Use
- Optimization efforts
- Benchmarking
- Capacity planning
- Cost analysis

### Example: Recording Performance Data

```javascript
mcp__memory_short__create_entities({
  entities: [{
    name: "Memory Architecture Performance Metrics",
    entityType: "performance-data",
    observations: [
      "Test: Main session token usage comparison",
      "Agent-only mode: 30-40K tokens startup (baseline)",
      "Hybrid mode: 42-48K tokens startup (+6-8K memory MCPs)",
      "All-MCPs mode: 155K tokens startup (not recommended)",
      "Free context - Agent-only: 160-170K (80-85%)",
      "Free context - Hybrid: 152-158K (73-76%)",
      "Free context - All-MCPs: 45K (22.5%)",
      "Memory update speed: <100ms (short-term), <200ms (long-term)",
      "ChromaDB query: <500ms average",
      "SQLite query: <50ms average",
      "Recommendation: Agent-only for max tokens, hybrid for convenience",
      "Measured: October 22, 2025"
    ]
  }]
})
```

### Why This Pattern Works
- ✅ Data-driven decisions
- ✅ Baseline established
- ✅ Trade-offs quantified
- ✅ Future comparisons possible

---

## Advanced Patterns

### Cross-Session Knowledge Transfer

```javascript
// Session A stores knowledge
mcp__memory_long__create_entities({
  entities: [{
    name: "AGUPGRADE Tech Stack Decisions",
    entityType: "tech-stack",
    observations: ["Next.js 15", "PostgreSQL", "AWS ECS Fargate", "..."]
  }]
})

// Session B (days later) can query
mcp__memory_long__search_nodes({query: "AGUPGRADE tech stack"})
// Returns: Instant recall of all stack decisions!
```

### Semantic Memory for Code Patterns

```
1. Code something once
2. ChromaDB automatically indexes
3. Later: "Find similar authentication code"
4. ChromaDB returns relevant snippets
5. No manual memory management!
```

### Multi-Tier Strategy

```javascript
// Ephemeral → Short-term
"Currently debugging CORS issue in dev environment"

// Important → Long-term
"CORS fix requires APIGW_DOMAIN placeholder (architecture decision)"

// Structured → SQLite
Store in memory.db with tags, timestamps, relationships

// Semantic → ChromaDB
Actual CORS configuration code indexed automatically
```

---

## Best Practices Summary

1. **Short-Term = Sessions** - Current work, temporary context
2. **Long-Term = Knowledge** - Permanent decisions, patterns, solutions
3. **SQLite = Structure** - Queryable data, relationships, timestamps
4. **ChromaDB = Search** - Find similar code, semantic lookup

5. **Be Specific** - Clear entity names, detailed observations
6. **Add Context** - WHY, not just WHAT
7. **Include Dates** - Temporal context matters
8. **Measure Results** - Quantify benefits/trade-offs
9. **Link Related** - Use relations to build knowledge graphs
10. **Review Regularly** - Move short → long when patterns emerge

---

## Quick Commands Reference

```javascript
// CREATE
mcp__memory_short__create_entities({entities: [...]})
mcp__memory_long__create_entities({entities: [...]})

// UPDATE
mcp__memory_short__add_observations({observations: [...]})
mcp__memory_long__add_observations({observations: [...]})

// RELATE
mcp__memory_short__create_relations({relations: [...]})
mcp__memory_long__create_relations({relations: [...]})

// SEARCH
mcp__memory_short__search_nodes({query: "..."})
mcp__memory_long__search_nodes({query: "..."})

// READ ALL
mcp__memory_short__read_graph()
mcp__memory_long__read_graph()

// DELETE
mcp__memory_short__delete_entities({entityNames: [...]})
mcp__memory_short__delete_observations({deletions: [...]})
```

---

**Memory is your AI's long-term knowledge - use these patterns to make it powerful!** 🧠
