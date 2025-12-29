# Claude Code vs Codex: Real-World CTO Comparison

**Source**: Patrick Ellis (CTO, Seattle AI startup) - Real-world battle testing on massive web app migration
**Date**: 2025 (Post Sonnet 4.5 & Codex GPT-5 releases)

---

## 🎯 TL;DR - The Optimal Workflow

**Use Codex for**: Exploration, research, scaffolding (async cloud agents)
**Use Claude Code for**: Implementation, execution, security (tactical hands-on work)
**Cross-review**: Each AI reviews the other's code

---

## 9 Critical Differences

### 1. The Models: Sonnet 4.5 vs Codex GPT-5

**Winner**: Sonnet 4.5

**Sonnet 4.5 Strengths**:
- ✅ **Best benchmarks** - Beats all on SWE Bench Verified
- ✅ **Faster iteration** - Significantly quicker responses
- ✅ **Gritty & autonomous** - Dives deep, figures things out independently
- ✅ **Context awareness** - Only model that knows its context limits (Cognition research)
- ✅ **Superior context management** - Can run 30+ hours vs Codex's 7 hours
- ✅ **Self-validating** - Creates internal tests/scripts to validate its work
- ✅ **Better at backend/architecture** - Deeper reasoning for complex tasks
- ✅ **Excellent file operations** - Uses grep, bash tools masterfully

**Codex Strengths**:
- ✅ **Better UI/UX output** - More polished front-end designs (without guidance)
- ✅ **Better architectural reasoning** - Deeper thinking on complex backend tasks
- ✅ **More academic approach** - "Measure twice, cut once"

**Personality Comparison**:
- **Sonnet 4.5**: Startup entrepreneur - learns by doing, tactical, hands-on, not afraid to get dirty
- **Codex**: Academic - strategic, systematic, thinks deeply before acting

---

### 2. CLI Tool: Claude Code vs Codex Harness

**Winner**: Claude Code (by far)

**Claude Code Advantages**:
- ✅ `/add-dir` - Add entire directories to context (KILLER for multi-service projects)
- ✅ `/context` - View context window usage and what's filling it
- ✅ **Subagents** - Massive advantage for context management
- ✅ **Memory tools** - Built-in memory management
- ✅ **Rich ecosystem** - Security reviews, code reviews, custom workflows
- ✅ **Agent SDK** - Build custom workflows easily
- ✅ **More mature** - More features, better UX

**Codex Advantages**:
- ✅ **Open source** - Community can contribute
- ✅ **Bring your own model** - Can use any LLM

**Missing in Codex**: Subagents (critical for context management)

---

### 3. IDE Integration

**Winner**: Codex

**Codex Advantages**:
- ✅ **Robust VS Code integration** - Beyond just CLI wrapper
- ✅ **Intelligent context inheritance** - Sees open tabs, files
- ✅ **Cloud handoff** - Delegate local tasks to Codex Cloud seamlessly
- ✅ **Pull down cloud work** - Apply diffs from cloud to local

**Claude Code**: Basic VS Code wrapper around CLI

---

### 4. Codex Cloud (Agent Swarms)

**Winner**: Codex (no competition)

**Game-changing paradigm**:
- ✅ **Spin up 1-4 cloud agents** in containers
- ✅ **Connect to GitHub repos** directly
- ✅ **Run for days/weeks** exploring solutions
- ✅ **Unblock local machine** - Delegate and keep working
- ✅ **Abundance mindset** - Kick off multiple approaches in parallel

**Use cases**:
- Research & exploration
- Security updates across codebase
- Migration tasks
- Learning & understanding codebases
- Smaller front-end changes

**Anthropic**: No cloud environment (yet)

---

### 5. GitHub Integration

**Winner**: Claude Code (slight edge)

**Both have**:
- ✅ Tag AI in issues/comments (@claude, @codex)
- ✅ Automatic PR reviews
- ✅ Manual review invocation

**Claude Code edge**:
- Better extensibility with Agent SDK
- Better out-of-box slash commands
- Security review agent (succinct, powerful)

**Codex edge**:
- Better default reviewer (finds nuanced bugs)
- Less verbose (no fluff in comments)

---

### 6. Vision & Roadmap

**Winner**: Tie (different philosophies)

**OpenAI (AGI-pilled)**:
- Goal: Fully autonomous software dev agent by EOY
- Focus: End-to-end delegation, async cloud agents
- Vision: "Abundance of intelligence" - swarm approaches

**Anthropic (Tactical)**:
- Focus: Real-world feedback, practical solutions
- Approach: Simple, robust, industrious tools that work NOW
- Philosophy: Grep, markdown, CLI tools (not fancy RAG)

**Verdict**: Anthropic's approach helps more day-to-day NOW, but OpenAI's vision is more exciting long-term

---

### 7. Pro Tips

**Codex Configuration**:
```toml
# codex/.config.toml
web_search = true  # Enable if OK with security risks
agentic = true     # Enable long-running tasks
```

**Context Auditing** (CRITICAL):
- ⚠️ **Audit your context regularly** - Don't poison with conflicting info
- ⚠️ **MCP servers add 25+ tools each** - Each tool has description, bloats context
- ⚠️ **Only expose needed tools** - Use subagents to isolate context
- ✅ `/context` command in Claude Code - See what's using context

**Why subagents matter**:
- Isolate MCP tools to specific tasks
- Prevent context pollution
- Delegate without bloating main context
- Dispose of context when done

---

### 8. Deep Research Integration

**Use Gemini Deep Think for**:
- ✅ Creating PRDs
- ✅ Gathering context for tasks
- ✅ Building subagent prompts
- ✅ Learning domain expertise

**Workflow**:
1. Use Gemini Deep Research on topic (e.g., "SEO best practices for world-class strategist")
2. Summarize into actionable checklist/system prompt
3. Turn into subagent OR add to CLAUDE.md OR use as PRD
4. Model learns and executes workflow on your behalf

**Applies to**: Frontend design, architecture, data modeling, QA, testing, ANY workflow

---

### 9. Patrick's Personal Workflow (CTO-Level)

**Current Setup** (as of Sonnet 4.5 release):

**Primary Development**: Sonnet 4.5 (Claude Code)
- All implementation
- Tactical execution
- Day-to-day coding

**Research & Exploration**: Codex Cloud
- Spawn multiple agents to explore approaches
- Generate scaffolding & skeleton apps
- Collect information for PRDs
- Async investigation while working locally

**Cross-Review** (Critical):
- ✅ Claude Code reviews everything from Codex
- ✅ Codex reviews everything from Claude Code
- Different perspectives catch different issues

**Previous Journey**:
- Started with Opus 4.1 (heavy use)
- Switched to Codex Medium/High (better than Opus)
- Now: Sonnet 4.5 for 90% of work

---

## Key Insights

### Sonnet 4.5 Characteristics

**"Cut twice, measure once"** (vs Codex's "measure twice, cut once")
- Tries things, iterates fast
- Not afraid to get hands dirty
- Creates validation loops quickly
- Tests hypotheses through action

**Perfect for**:
- Rapid iteration
- Refactoring
- Data model migrations
- Complex multi-service projects
- Hands-on tactical work

### Codex Characteristics

**Academic, systematic, strategic**
- Thinks deeply before acting
- Better at pure front-end design (initially)
- Deeper architectural reasoning
- More measured approach

**Perfect for**:
- Research & exploration
- Multiple parallel approaches
- Scaffolding & planning
- Initial UI design (without context)

---

## The Optimal Multi-AI Workflow

```
┌─────────────────────────────────────────────────┐
│         CODEX CLOUD (Exploration)               │
│  • Spawn 1-4 agents for research                │
│  • Generate multiple approaches                 │
│  • Build scaffolding & skeleton apps            │
│  • Collect context for PRDs                     │
│  • Run async while working locally              │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│    SONNET 4.5 (Implementation)                  │
│  • Primary development AI                       │
│  • Tactical execution                           │
│  • Rapid iteration                              │
│  • Context-aware implementation                 │
│  • 30+ hour deep dives                          │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│         CROSS-REVIEW (Quality)                  │
│  • Codex reviews Claude's code                  │
│  • Claude reviews Codex's code                  │
│  • Different perspectives = better quality      │
└─────────────────────────────────────────────────┘
```

---

## Advanced: Orchestration Framework

**Critical for long-running agents**:
- ✅ Surround models with context
- ✅ Provide tools & examples
- ✅ Define validators for success
- ✅ Create environments where they thrive

**Models are hungry for and good at understanding context**
- Give them what they need
- Define success criteria
- Provide validation loops
- They'll exceed expectations

---

## Context Management (Critical for 2025)

**The Problem**:
- Models can run 7-30+ hours now
- Context bloat kills productivity
- MCP servers add massive tool overhead
- Conflicting info poisons outputs

**The Solution**:
1. **Audit context regularly** - Use `/context` command
2. **Use subagents** - Isolate tools to specific tasks
3. **Remove unused MCPs** - Each MCP = 25+ tools in context
4. **Keep main context lean** - Delegate to subagents
5. **Document in markdown** - Both models love simple file-based context

---

## Sources

- **Patrick Ellis** (CTO, Seattle AI startup)
- **Real-world testing**: Massive web app migration (Python Django → Postgres/Next.js/React)
- **Companies**: Google, Amazon, FIFA, Disney
- **Experience**: Battle-tested Claude Code since February, Codex since May
- **Video**: "Claude Code 2.0 vs Codex: Real-World Comparison"

---

## Bottom Line

**Use Codex for**: Async exploration, research, scaffolding (cloud agents)
**Use Claude Code for**: Synchronous implementation, execution, security (hands-on)
**Cross-review everything**: Different perspectives = higher quality

**Winner**: Depends on task
- **Day-to-day work**: Sonnet 4.5 (Claude Code)
- **Exploration**: Codex Cloud
- **Long-term vision**: Both (they complement each other perfectly)
