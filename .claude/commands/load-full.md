---
description: Load complete CLAUDE.md with all 48 modules (use when needed)
---

# Load Full Context - Complete Capabilities

**Purpose**: Load all 48 global instruction modules when you need advanced capabilities.

**Cost**: ~15-20K tokens (one-time per session)

**When to use**: Only when you need capabilities not in CLAUDE-LITE.md

---

## What This Loads

### Advanced Features (Not in CLAUDE-LITE)
1. Multi-AI orchestration (Claude + GPT-5 + Gemini)
2. Advanced agent directory (90+ specialized agents)
3. Security frameworks (comprehensive)
4. AWS-specific workflows
5. n8n knowledge base (100+ workflows)
6. Playwright test agents
7. Advanced automation patterns
8. Specialized coding workflows

### What's ALREADY Available (in CLAUDE-LITE)
1. ✅ RAG enforcement (12 collections)
2. ✅ Context management automation
3. ✅ Memory persistence
4. ✅ TodoWrite tracking
5. ✅ Token monitoring
6. ✅ Careful mode (mistake prevention)
7. ✅ Smart doc intelligence

---

## Decision Tree: Do You Need Full Context?

### ❌ DON'T Load Full If:
- Working on normal coding tasks ✅ Lite sufficient
- Using RAG for documentation ✅ Lite sufficient
- Implementing features ✅ Lite sufficient
- Debugging issues ✅ Lite sufficient
- Writing tests ✅ Lite sufficient

### ✅ DO Load Full If:
- Need multi-AI orchestration (GPT-5, Gemini)
- Complex security audit required
- AWS-specific architecture work
- n8n workflow automation
- Need specialized agent (from 90+ available)
- Complex system design requiring multiple perspectives

---

## How to Load

### Method 1: Use This Command
```
Just type: /load-full
```

### Method 2: Explicit Request
```
"Load complete CLAUDE.md with all modules"
```

### Method 3: Automatic Detection
Claude will suggest loading if task requires it:
```
🟡 CAPABILITY NEEDED:

You asked about multi-AI orchestration.
This requires full CLAUDE.md modules.

Load now? [Y/n]
- Cost: 15-20K tokens
- Benefit: Full multi-AI capabilities
```

---

## Token Impact

### Current Session (CLAUDE-LITE)
```
Session start: 2-3K tokens
Available features: 85-90% of full
Token budget remaining: ~197K tokens
```

### After Loading Full
```
Loading cost: 15-20K tokens
Available features: 100% of full
Token budget remaining: ~177K tokens
Cost: 15-20K tokens (one-time this session)
```

---

## What Happens When You Load

```python
# Step 1: Read CLAUDE.md
Read(file_path="CLAUDE.md")

# Step 2: Load all 48 modules
- Auto-context initialization
- Agent frameworks
- Multi-AI orchestration
- Security frameworks
- AWS workflows
- n8n knowledge base
- Playwright agents
- Advanced automation
- ... (all 48 modules)

# Step 3: Confirm loaded
"✅ Full CLAUDE.md loaded (48 modules active)"

# Step 4: Ready for advanced work
"All capabilities available. What would you like to do?"
```

---

## Example Usage

### Example 1: Multi-AI Review Needed
```
You: "I need feedback from GPT-5 and Gemini on this architecture"

Claude (detects need):
🟡 MULTI-AI ORCHESTRATION REQUESTED

This requires full CLAUDE.md modules.
Currently in LITE mode (missing multi-AI orchestration).

Load full context? [Y/n]
- Cost: 15-20K tokens
- Benefit: Multi-AI orchestration, agent routing

You: "Y"

Claude: [Loads CLAUDE.md]
✅ Full context loaded!
✅ Multi-AI orchestration active
✅ Can now route to GPT-5/Gemini

Proceeding with multi-AI review...
```

### Example 2: Security Audit
```
You: "Run comprehensive security audit with compliance checking"

Claude (detects need):
🟡 SECURITY FRAMEWORK NEEDED

Comprehensive audit requires full security modules.
Currently in LITE mode (basic security only).

Load full context? [Y/n]
- Cost: 15-20K tokens
- Benefit: Complete security frameworks, compliance checking

You: "Y"

Claude: [Loads CLAUDE.md]
✅ Full security frameworks loaded
✅ Compliance checking active

Proceeding with comprehensive security audit...
```

### Example 3: Normal Work (No Load Needed)
```
You: "Implement OAuth with Cognito"

Claude (LITE mode sufficient):
✅ Using LITE mode (sufficient for this task)

Capabilities available:
- RAG for Cognito docs (aws-cognito collection)
- Memory for context persistence
- Careful mode for mistake prevention
- Token monitoring active

No need to load full context.

Proceeding with implementation...
```

---

## Best Practices

### 1. Start with LITE (Default)
```
✅ Use CLAUDE-LITE.md by default
✅ Covers 85-90% of use cases
✅ Saves 12-17K tokens per session
✅ Load full only when specifically needed
```

### 2. Load Full On-Demand
```
✅ Load when Claude suggests it
✅ Load when you know you need advanced features
✅ One-time cost per session (doesn't reload after /clear)
```

### 3. Track When You Load
```
Keep note of what triggered full load:
- "Needed multi-AI" → Valid reason
- "Needed security audit" → Valid reason
- "Just in case" → ❌ Wasteful, use LITE
```

### 4. Evaluate After Session
```
Did you actually use the full features?
- Yes → Loading was justified
- No → Could have stayed with LITE (wasted 15K tokens)
```

---

## Token Optimization Strategy

### Scenario A: Normal Development Day
```
Morning:
- Start with LITE (2-3K)
- Code implementation (40K)
- /clear → LITE loads (2-3K)
- More coding (40K)
- /clear → LITE loads (2-3K)
- Final work (40K)

Total: 130K tokens
Full CLAUDE.md cost: Would be 190K (60K wasted!)
Savings: 60K tokens (31% reduction)
```

### Scenario B: Advanced Work Needed
```
Morning:
- Start with LITE (2-3K)
- Need multi-AI review
- Load full (15-20K)
- Multi-AI work (40K)
- /clear → LITE loads (2-3K)
- Normal coding (40K)

Total: 110K tokens
Worth it: Used advanced features
Optimized: Still used LITE after /clear
```

---

## FAQ

### Q: If I load full, does it stay loaded after /clear?
**A: NO.** After /clear, you restart with LITE mode.

This is GOOD because:
- Next session may not need full features
- Saves 15K tokens per /clear
- Can load full again if needed (on-demand)

### Q: How do I know if I need full context?
**A: Claude will tell you!**

If you request something not in LITE:
```
🟡 ADVANCED FEATURE REQUESTED
This requires full CLAUDE.md.
Load now? [Y/n]
```

### Q: Can I make full context the default?
**A: Yes, but not recommended.**

Rename files:
```bash
# Make full the default (NOT RECOMMENDED)
mv CLAUDE.md CLAUDE-FULL.md
mv CLAUDE-LITE.md CLAUDE.md

# Result: Load 15-20K every session
# Waste: 60-85K tokens/day
```

Better approach: Keep LITE as default, load on-demand

### Q: What if I forget what's in LITE vs FULL?
**A: Ask Claude!**

```
"What capabilities are in LITE mode vs FULL mode?"

Claude will list:
- LITE: RAG, context management, automation, memory
- FULL: Multi-AI, advanced agents, security frameworks, AWS workflows
```

---

## Token Savings Summary

| Scenario | LITE Mode | FULL Mode | Savings |
|----------|-----------|-----------|---------|
| **Per session start** | 2-3K | 15-20K | 12-17K |
| **5 /clear cycles/day** | 10-15K | 75-100K | 60-85K |
| **Per month (150 sessions)** | 300-450K | 2,250-3,000K | 1,950-2,550K |

**Annual savings: 23,400-30,600K tokens** (nearly 4-5 months of budget!)

---

## Bottom Line

**Default workflow:**
1. Start with CLAUDE-LITE.md (automatic)
2. Work normally (covers 90% of needs)
3. Load full only when specifically needed
4. After /clear, restart with LITE

**Token savings:**
- Per session: 12-17K tokens
- Per day: 60-85K tokens
- Per month: 1,950-2,550K tokens

**Result: 30-42% reduction in loading costs!**

---

**Use LITE by default. Load full on-demand. Save massive tokens.** 🚀
