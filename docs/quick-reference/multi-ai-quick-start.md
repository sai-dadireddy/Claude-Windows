# Multi-AI Collaboration Quick Start Guide

**Setup Time**: 5 minutes
**For**: Claude + Codex + Gemini working together seamlessly

---

## 🚀 One-Time Setup (5 minutes)

```bash
# 1. Run setup script
pwsh tools/ai-collaboration/setup-multi-ai.ps1

# Output: Creates .ai-workspace with shared resources
```

**What this does**:
- ✅ Creates workspace structure for all 3 AIs
- ✅ Sets up shared MCP configuration (no duplication)
- ✅ Initializes unified memory database
- ✅ Creates change tracking system
- ✅ Installs collaboration helper scripts

---

## 📝 Daily Workflow

### Example: Codex Creates, Claude Enhances, Gemini Validates

**Step 1: Codex creates initial version**
```bash
# Switch to Codex context
pwsh tools/ai-collaboration/ai-switch.ps1 codex

# Codex works and creates file
codex> "Create API documentation"
# Creates: codex/api-docs.md

# Log the change
python tools/ai-collaboration/change-tracker.py log codex "Created API documentation" codex/api-docs.md
```

**Step 2: User asks Claude to enhance**
```bash
# Switch to Claude context
pwsh tools/ai-collaboration/ai-switch.ps1 claude

# Claude reviews Codex's work
claude> "Review and enhance Codex's API docs"

# Claude reads: codex/api-docs.md
# Claude creates enhanced version
# Creates: docs/api-docs.md (enhanced)

# Log the enhancement with reference
python tools/ai-collaboration/change-tracker.py log claude "Enhanced API docs from Codex" docs/api-docs.md --references change-2025-10-15-abc123
```

**Step 3: User asks Gemini to validate**
```bash
# Switch to Gemini context
pwsh tools/ai-collaboration/ai-switch.ps1 gemini

# Gemini validates both versions
gemini> "Validate Claude's API doc enhancements"

# Gemini approves
python tools/ai-collaboration/change-tracker.py validate change-2025-10-15-def456 gemini
```

---

## 🔄 Common Commands

### Switch AI Context
```bash
# Switch to Claude
pwsh tools/ai-collaboration/ai-switch.ps1 claude

# Switch to Codex
pwsh tools/ai-collaboration/ai-switch.ps1 codex

# Switch to Gemini
pwsh tools/ai-collaboration/ai-switch.ps1 gemini
```

### Track Changes
```bash
# Log a change
python tools/ai-collaboration/change-tracker.py log <ai> "<action>" <files...>

# Example
python tools/ai-collaboration/change-tracker.py log claude "Fixed authentication bug" src/auth.ts

# View recent changes
python tools/ai-collaboration/change-tracker.py list --recent 10

# View changes by specific AI
python tools/ai-collaboration/change-tracker.py list --ai codex

# Get change details
python tools/ai-collaboration/change-tracker.py status change-2025-10-15-abc123
```

### Validate Changes
```bash
# Validate a change
python tools/ai-collaboration/change-tracker.py validate <change-id> <validator-ai>

# Example: Codex validates Claude's work
python tools/ai-collaboration/change-tracker.py validate change-2025-10-15-abc123 codex
```

---

## 🎯 Workflow Patterns

### Pattern 1: Draft → Enhance
```
Codex drafts → Claude enhances → Gemini validates
```

**Use Case**: Documentation, API specs, architectural plans

**Commands**:
```bash
# Codex
ai-switch codex
# ... work ...
change-tracker log codex "Draft architecture doc" docs/draft-arch.md

# Claude
ai-switch claude
# ... enhance ...
change-tracker log claude "Enhanced architecture doc" docs/architecture.md --references change-xxx

# Gemini
ai-switch gemini
# ... validate ...
change-tracker validate change-yyy gemini
```

### Pattern 2: Plan → Implement
```
Claude plans → Codex implements → Claude reviews
```

**Use Case**: New features, refactoring, complex implementations

### Pattern 3: Parallel Work
```
Claude optimizes DB → Codex adds caching → Gemini merges
```

**Use Case**: Independent improvements that need coordination

---

## 🧠 Memory Sharing

All AIs share the same memory database but have separate namespaces:

```
.ai-workspace/shared/memory.db
├── global_memory        (accessible to all)
├── claude_specific      (Claude only)
├── codex_specific       (Codex only)
└── gemini_specific      (Gemini only)
```

**Each AI can**:
- ✅ Read global memory
- ✅ Write to own namespace
- ✅ Reference other AI's work via change IDs

---

## 🔧 MCP Sharing

All AIs share same MCP configuration:

```
.ai-workspace/config/mcp-shared.json (master config)
├── Symlink: claude/claude-code-mcp-config.json
├── Symlink: codex/codex-mcp-config.json
└── Symlink: gemini/gemini-mcp-config.json
```

**Benefits**:
- ✅ Single configuration to maintain
- ✅ No duplication (saves 6KB per AI)
- ✅ All AIs have same tool access
- ✅ Memory efficient

---

## 📊 Check Collaboration Status

```bash
# View recent activity from all AIs
python tools/ai-collaboration/change-tracker.py list --recent 20

# Check pending reviews
python tools/ai-collaboration/review-helper.py show-pending

# See what each AI is working on
ls .ai-workspace/*/in-progress/
```

---

## 🎓 Example Session

```bash
# Morning: Setup
pwsh tools/ai-collaboration/setup-multi-ai.ps1

# 9:00 AM: Claude plans feature
pwsh tools/ai-collaboration/ai-switch.ps1 claude
claude> "Plan OAuth implementation"
python tools/ai-collaboration/change-tracker.py log claude "OAuth implementation plan" docs/oauth-plan.md

# 10:00 AM: Codex implements
pwsh tools/ai-collaboration/ai-switch.ps1 codex
codex> "Implement OAuth based on Claude's plan"
python tools/ai-collaboration/change-tracker.py log codex "OAuth implementation" src/oauth/*.ts --references change-001

# 11:00 AM: Claude reviews
pwsh tools/ai-collaboration/ai-switch.ps1 claude
claude> "Review Codex's OAuth implementation"
python tools/ai-collaboration/change-tracker.py validate change-002 claude

# 12:00 PM: Gemini validates
pwsh tools/ai-collaboration/ai-switch.ps1 gemini
gemini> "Final validation of OAuth system"
python tools/ai-collaboration/change-tracker.py validate change-002 gemini
```

---

## 🔐 Security & Best Practices

### ✅ DO:
- Log every significant change
- Reference other AI's work when building on it
- Validate changes from other AIs before merging
- Use descriptive action messages
- Check pending reviews regularly

### ❌ DON'T:
- Work on same file simultaneously (check change log first)
- Skip change tracking for "small" changes
- Merge without validation
- Overwrite another AI's work without referencing it

---

## 🐛 Troubleshooting

**Problem**: `.ai-workspace not found`
```bash
# Solution: Run setup
pwsh tools/ai-collaboration/setup-multi-ai.ps1
```

**Problem**: Changes not showing up
```bash
# Solution: Check change log manually
cat .ai-workspace/shared/change-log.jsonl
```

**Problem**: MCP not working for an AI
```bash
# Solution: Verify symlink
ls -la claude/claude-code-mcp-config.json
# Should point to .ai-workspace/config/mcp-shared.json
```

---

## 📚 Full Documentation

For comprehensive details, see:
- **Architecture**: `docs/guides/multi-ai-collaboration-system.md`
- **Setup Script**: `tools/ai-collaboration/setup-multi-ai.ps1`
- **Change Tracker**: `tools/ai-collaboration/change-tracker.py`

---

## ✨ Benefits Summary

✅ **Clear Attribution**: Know exactly who made which changes
✅ **No Conflicts**: Coordination system prevents overlap
✅ **Memory Efficient**: Shared resources, no duplication (saves 50-100MB)
✅ **Feature Parity**: All AIs have same MCP/memory access
✅ **Easy Validation**: Quick review workflow
✅ **Seamless Handoffs**: Build on each other's work smoothly

---

**Ready to collaborate!** Start with: `pwsh tools/ai-collaboration/setup-multi-ai.ps1`
