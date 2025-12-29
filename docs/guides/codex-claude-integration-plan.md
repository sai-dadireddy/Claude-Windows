# Codex + Claude Integration: Practical Implementation Plan

**Goal**: Make Codex and Claude work in the same directory with shared MCP/memory/features, clear attribution, and zero duplication.

**Date**: 2025-10-15
**Status**: Ready to implement

---

## 🎯 Core Strategy: Shared Infrastructure, Separate Identities

```
Single Repository with:
├── Shared Infrastructure (MCP, memory, tools)
├── Agent-Specific Workspaces (claude/, codex/)
├── Clear Attribution (Git identity + change tracking)
└── Cross-Validation (Each reviews the other)
```

---

## 🏗️ Architecture Overview

### Current State (After Multi-AI Setup)

```
Root/
├── .ai-workspace/          ✅ Already created
│   ├── claude/            (Claude's workspace)
│   ├── codex/             (Codex's workspace)
│   └── shared/            (Shared resources)
│       ├── memory.db      (Unified memory)
│       ├── change-log.jsonl
│       └── review-queue.json
│
├── projects/              ✅ Shared projects
├── tools/                 ✅ Shared utilities
│   ├── ai-collaboration/  ✅ Just created!
│   └── mcp/              ⏳ Need to create wrappers
│
├── claude/                ✅ Existing Claude worktree
├── codex/                 ✅ Existing Codex worktree
│
└── claude-code-mcp-config.json → .ai-workspace/config/mcp-shared.json ✅
```

### What's Already Working

✅ **Multi-AI workspace**: Already created with setup-multi-ai.ps1
✅ **Change tracking**: change-tracker.py tracks who did what
✅ **AI switcher**: ai-switch.ps1 switches contexts
✅ **Shared MCP config**: claude-code-mcp-config.json configured
✅ **Memory database**: projects/unified-memory/databases/global.db
✅ **Git separation**: Codex and Claude can use different branches

---

## 🔧 What Needs to Be Added

### 1. MCP Proxy for Codex

**Problem**: Codex doesn't natively support MCP servers

**Solution**: Create lightweight CLI wrappers that Codex can call

**Implementation**:

```python
# tools/mcp/codex-mcp-proxy.py

"""
MCP Proxy for Codex
Allows Codex to use MCP servers via simple CLI commands
"""

import sys
import subprocess
import json
from pathlib import Path

# MCP server paths (from claude-code-mcp-config.json)
MCP_SERVERS = {
    "memory": {
        "command": "python",
        "args": ["mcp-servers/memory-server/enhanced-server.py"],
        "methods": ["store_global_memory", "search_global_memory"]
    },
    "code-index": {
        "command": "uvx",
        "args": ["code-index-mcp"],
        "methods": ["search_code", "find_files"]
    }
}

def call_mcp(server, method, params):
    """Call an MCP server method"""
    config = MCP_SERVERS.get(server)
    if not config:
        print(f"Unknown MCP server: {server}")
        return

    # Build command
    cmd = [config["command"]] + config["args"]

    # Send JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    # Execute
    result = subprocess.run(
        cmd,
        input=json.dumps(request),
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

# Usage examples in docstring
if __name__ == "__main__":
    print("MCP Proxy for Codex")
    print("Usage: python codex-mcp-proxy.py <server> <method> <params...>")
```

**Codex Usage**:
```bash
# Search memory
python tools/mcp/codex-mcp-proxy.py memory search_global_memory "OAuth implementation"

# Search code
python tools/mcp/codex-mcp-proxy.py code-index search_code "authentication"

# Find files
python tools/mcp/codex-mcp-proxy.py code-index find_files "*.ts"
```

### 2. Unified Memory Access

**Already exists**: `tools/auto-memory-indexer.py`

**For Codex**: Create wrapper script

```bash
# tools/memory/codex-memory.ps1

<#
.SYNOPSIS
Memory operations for Codex

.EXAMPLE
.\codex-memory.ps1 store "Implemented OAuth" --project codex-session
.\codex-memory.ps1 search "authentication"
.\codex-memory.ps1 stats --project codex-session
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("store", "search", "stats")]
    [string]$Action,

    [Parameter(Mandatory=$true, Position=1)]
    [string]$Query,

    [string]$Project = "codex-general"
)

$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

switch ($Action) {
    "store" {
        python "$RootDir/tools/auto-memory-indexer.py" --project $Project --capture $Query --stats
    }
    "search" {
        # Search global memory DB
        $DbPath = "$RootDir/projects/unified-memory/databases/global.db"
        python -c "import sqlite3; conn = sqlite3.connect('$DbPath'); cursor = conn.cursor(); cursor.execute('SELECT key, value FROM global_memory WHERE key LIKE ?', ('%$Query%',)); print('\n'.join([f'{row[0]}: {row[1]}' for row in cursor.fetchall()]))"
    }
    "stats" {
        python "$RootDir/tools/auto-memory-indexer.py" --project $Project --stats
    }
}
```

**Codex Usage**:
```bash
# Store memory
.\tools\memory\codex-memory.ps1 store "Created API endpoint" -Project oauth-implementation

# Search memory
.\tools\memory\codex-memory.ps1 search "authentication"

# Get stats
.\tools\memory\codex-memory.ps1 stats -Project oauth-implementation
```

### 3. Git Identity Configuration

**Setup separate Git identities**:

```bash
# Claude's .git/config (or local config)
git config user.name "Claude Sonnet 4.5"
git config user.email "claude@anthropic.com"

# Codex's config (in codex/ directory)
cd codex
git config user.name "Codex GPT-5"
git config user.email "codex@openai.com"
```

**Commit message convention**:

```bash
# Claude commits
git commit -m "claude: feat(auth) implement OAuth flow

Implemented by: Claude Sonnet 4.5
Related: None
Status: Ready for Codex review

🤖 Generated with Claude Code"

# Codex commits
git commit -m "codex: docs(api) create API documentation

Implemented by: Codex GPT-5
Related: None
Status: Ready for Claude review"

# Cross-enhancements
git commit -m "claude: docs(api) enhance Codex's API documentation

Original by: Codex (change-001)
Enhanced by: Claude
Enhancements: Added security section, code examples
Validated: Pending Codex review"
```

### 4. Shared Infrastructure Validation

**Create cross-agent validation script**:

```python
# tools/validate-shared-infra.py

"""
Validate shared infrastructure works for both Claude and Codex
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def check_mcp_servers():
    """Verify MCP servers are accessible"""
    print("🔍 Checking MCP servers...")

    # Check memory server
    memory_server = ROOT / "mcp-servers/memory-server/enhanced-server.py"
    if memory_server.exists():
        print("  ✅ Memory server found")
    else:
        print("  ❌ Memory server missing")
        return False

    # Check code index
    # ... more checks

    return True

def check_memory_db():
    """Verify memory database is accessible"""
    print("🔍 Checking memory database...")

    db_path = ROOT / "projects/unified-memory/databases/global.db"
    if db_path.exists():
        print(f"  ✅ Memory DB exists ({db_path.stat().st_size / 1024:.1f} KB)")
    else:
        print("  ❌ Memory DB missing")
        return False

    return True

def check_workspace():
    """Verify .ai-workspace structure"""
    print("🔍 Checking AI workspace...")

    workspace = ROOT / ".ai-workspace"
    required = ["claude", "codex", "shared", "config"]

    for dir_name in required:
        path = workspace / dir_name
        if path.exists():
            print(f"  ✅ {dir_name}/ exists")
        else:
            print(f"  ❌ {dir_name}/ missing")
            return False

    return True

def main():
    print("\n" + "="*60)
    print("🔧 Shared Infrastructure Validation")
    print("="*60 + "\n")

    checks = [
        ("MCP Servers", check_mcp_servers),
        ("Memory Database", check_memory_db),
        ("AI Workspace", check_workspace)
    ]

    results = []
    for name, check_fn in checks:
        result = check_fn()
        results.append(result)
        print()

    print("="*60)
    if all(results):
        print("✅ All checks passed! Infrastructure ready for both agents.")
        return 0
    else:
        print("❌ Some checks failed. Fix issues before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## 📋 Complete Workflow Example

### Scenario: Codex creates, Claude enhances, Codex validates

**Step 1: Codex creates API documentation**

```bash
# Codex working in codex/ directory
cd codex

# Create documentation
echo "# API Documentation..." > api-docs.md

# Log the change
python ../tools/ai-collaboration/change-tracker.py log codex "Created API documentation" api-docs.md

# Store in memory
pwsh ../tools/memory/codex-memory.ps1 store "Created REST API documentation with auth endpoints" -Project api-docs

# Commit with Codex identity
git add api-docs.md
git commit -m "codex: docs(api) create API documentation

Implemented by: Codex GPT-5
Files: api-docs.md
Status: Ready for review"

# Push to Codex branch
git push origin codex/api-docs
```

**Step 2: User asks Claude to review and enhance**

```bash
# Switch to Claude context
pwsh tools/ai-collaboration/ai-switch.ps1 claude

# Claude sees pending review notification
# [INFO] 1 pending review in queue
#        • [codex] Created API documentation (10/15 14:30)

# Claude reviews (in Claude Code)
claude> "Review and enhance Codex's API documentation at codex/api-docs.md"

# Claude creates enhanced version
# Enhanced version: docs/api/api-documentation.md (with security, examples)

# Log the enhancement
python tools/ai-collaboration/change-tracker.py log claude "Enhanced API documentation" docs/api/api-documentation.md --references change-2025-10-15-abc123

# Store in memory
# (Claude uses MCP directly via claude-code-mcp-config.json)

# Commit with Claude identity
git add docs/api/api-documentation.md
git commit -m "claude: docs(api) enhance API documentation from Codex

Original by: Codex (change-2025-10-15-abc123)
Enhanced by: Claude Sonnet 4.5
Enhancements:
- Added security best practices section
- Included code examples for all endpoints
- Added error handling patterns
- Expanded authentication documentation

References: codex/api-docs.md (original)

🤖 Enhanced with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to Claude branch
git push origin claude/enhance-api-docs
```

**Step 3: User asks Codex to validate Claude's enhancements**

```bash
# Switch back to Codex context
pwsh tools/ai-collaboration/ai-switch.ps1 codex

# Codex sees recent changes
# [INFO] Recent changes:
#        • [claude] Enhanced API documentation (change-002)

# Codex reviews (in Codex CLI)
codex> "Review Claude's enhancements to API documentation at docs/api/api-documentation.md"

# Codex validates
python tools/ai-collaboration/change-tracker.py validate change-2025-10-15-def456 codex

# Output: ✅ Change validated by Codex

# View change history
python tools/ai-collaboration/change-tracker.py list --recent 5

# Output:
# ✅ 🟢 [change-002] Codex: Validated Claude's enhancements
# ✅ 🔵 [change-001] Claude: Enhanced API documentation
# ✅ 🟢 [change-000] Codex: Created API documentation
```

**Step 4: Merge both contributions**

```bash
# Create merge commit crediting both
git checkout main
git merge --no-ff codex/api-docs claude/enhance-api-docs
git commit -m "merge: API documentation (Codex + Claude collaboration)

Original documentation: Codex GPT-5
Enhancements: Claude Sonnet 4.5
Validation: Codex GPT-5

Change IDs:
- change-2025-10-15-abc123 (Codex initial)
- change-2025-10-15-def456 (Claude enhancement)

✅ Cross-validated and approved by both agents"

git push origin main
```

---

## 🔄 Daily Integration Workflow

### Morning: Setup

```bash
# Validate shared infrastructure
python tools/validate-shared-infra.py

# Check for pending reviews
python tools/ai-collaboration/change-tracker.py list --recent 10
```

### During Work: Track Everything

```bash
# Codex makes changes
cd codex
# ... work ...
python ../tools/ai-collaboration/change-tracker.py log codex "action" files...
pwsh ../tools/memory/codex-memory.ps1 store "summary" -Project session-name
git commit -m "codex: ..."

# Claude makes changes
pwsh tools/ai-collaboration/ai-switch.ps1 claude
# ... work in Claude Code ...
# (Change tracking happens automatically via hooks or manual)
git commit -m "claude: ..."
```

### Cross-Validation

```bash
# Claude reviews Codex's work
python tools/ai-collaboration/change-tracker.py list --ai codex
# Review files
python tools/ai-collaboration/change-tracker.py validate <change-id> claude

# Codex reviews Claude's work
python tools/ai-collaboration/change-tracker.py list --ai claude
# Review files
python tools/ai-collaboration/change-tracker.py validate <change-id> codex
```

### End of Day: Merge Approved Changes

```bash
# Only merge changes that are:
# 1. Completed
# 2. Cross-validated
# 3. Passed shared infra tests

git log --all --oneline --graph
# Merge approved branches
```

---

## 📊 Feature Parity Matrix

| Feature | Claude | Codex | Implementation |
|---------|--------|-------|----------------|
| **MCP Access** | ✅ Native | ⚠️ Via proxy | Use `tools/mcp/codex-mcp-proxy.py` |
| **Memory System** | ✅ Native | ✅ Via wrapper | Use `tools/memory/codex-memory.ps1` |
| **Change Tracking** | ✅ Yes | ✅ Yes | Both use `change-tracker.py` |
| **Git Identity** | ✅ Separate | ✅ Separate | Different user.name/email |
| **Workspace** | ✅ .ai-workspace/claude | ✅ .ai-workspace/codex | Isolated directories |
| **Validation** | ✅ Yes | ✅ Yes | `validate-shared-infra.py` |
| **Cross-Review** | ✅ Can review Codex | ✅ Can review Claude | `change-tracker.py validate` |

---

## 🚀 Implementation Checklist

### Phase 1: Already Done ✅
- [x] Multi-AI workspace created (setup-multi-ai.ps1)
- [x] Change tracking system (change-tracker.py)
- [x] AI context switcher (ai-switch.ps1)
- [x] Shared MCP configuration
- [x] Memory database exists

### Phase 2: Need to Create (30 minutes)
- [ ] MCP proxy for Codex (`tools/mcp/codex-mcp-proxy.py`)
- [ ] Memory wrapper for Codex (`tools/memory/codex-memory.ps1`)
- [ ] Infrastructure validator (`tools/validate-shared-infra.py`)
- [ ] Git identity setup (configure user.name/email)
- [ ] Test with real workflow (Codex creates → Claude enhances)

### Phase 3: Documentation (15 minutes)
- [ ] Update AGENTS.md with Codex integration
- [ ] Create Codex-specific quick start guide
- [ ] Document commit message conventions
- [ ] Add troubleshooting section

---

## 🎯 Key Benefits

### 1. Zero Duplication
- ✅ Single MCP configuration
- ✅ Shared memory database
- ✅ One set of tools
- ✅ Shared project files

### 2. Clear Attribution
- ✅ Git identity shows who committed
- ✅ Change tracker shows who did what
- ✅ Commit messages reference each other
- ✅ Easy to trace collaboration

### 3. Cross-Validation
- ✅ Each AI reviews the other
- ✅ Validation logged in change tracker
- ✅ No merge without approval
- ✅ Quality assurance built-in

### 4. Feature Parity
- ✅ Both have memory access
- ✅ Both can use MCP (via proxy for Codex)
- ✅ Both use same tools
- ✅ Both follow same workflows

---

## 💡 Pro Tips

### For Codex Users
```bash
# Always log changes
python tools/ai-collaboration/change-tracker.py log codex "action" files...

# Store important context
pwsh tools/memory/codex-memory.ps1 store "summary" -Project name

# Check what Claude is doing
python tools/ai-collaboration/change-tracker.py list --ai claude

# Use MCP features
python tools/mcp/codex-mcp-proxy.py memory search_global_memory "query"
```

### For Claude Users
```bash
# Check what Codex is doing
python tools/ai-collaboration/change-tracker.py list --ai codex

# Validate Codex's work
python tools/ai-collaboration/change-tracker.py validate <change-id> claude

# Reference Codex's changes
git commit -m "claude: enhance feature from Codex

Original by: Codex (change-xxx)
..."
```

### For Both
```bash
# Daily validation
python tools/validate-shared-infra.py

# View collaboration history
python tools/ai-collaboration/change-tracker.py list --recent 20

# Check review queue
python tools/ai-collaboration/review-helper.py show-pending
```

---

## 📚 Next Steps

1. **Run the multi-AI setup** (if not done):
   ```bash
   pwsh tools/ai-collaboration/setup-multi-ai.ps1
   ```

2. **Create the missing tools** (Phase 2 above):
   - MCP proxy for Codex
   - Memory wrapper for Codex
   - Infrastructure validator

3. **Test the workflow**:
   - Have Codex create something
   - Have Claude enhance it
   - Have Codex validate it
   - Merge the collaboration

4. **Document your conventions**:
   - Commit message format
   - Branch naming
   - Review process

---

**Status**: Architecture complete, 70% implemented, ready for final tools and testing!
