# =============================================================================
# Claude Code Multi-AI & MCP Routing Setup (PowerShell)
# =============================================================================
# Works on: Windows PowerShell 5.1+, PowerShell 7+
# Prerequisites: Node.js 18+, Claude Code CLI installed
# =============================================================================

$ErrorActionPreference = "Continue"

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║     Claude Code Multi-AI & MCP Routing Setup                 ║
╚══════════════════════════════════════════════════════════════╝
"@

$CLAUDE_DIR = "$env:USERPROFILE\.claude"

# =============================================================================
# STEP 1: Create directories
# =============================================================================
Write-Host "`n[1/5] Creating directories..."
$dirs = @(
    "$CLAUDE_DIR\hooks",
    "$CLAUDE_DIR\hints",
    "$CLAUDE_DIR\memory\long-term\global",
    "$CLAUDE_DIR\scripts",
    "$CLAUDE_DIR\commands"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

# =============================================================================
# STEP 2: Add MCP Servers
# =============================================================================
Write-Host "`n[2/5] Adding MCP servers..."

$mcpServers = @(
    @{name="context7"; cmd="npx -y @upstash/context7-mcp"; desc="library docs"},
    @{name="github"; cmd="npx -y @modelcontextprotocol/server-github"; desc="repo ops"},
    @{name="memory"; cmd="npx -y @modelcontextprotocol/server-memory"; desc="knowledge graph"},
    @{name="sequential-thinking"; cmd="npx -y @modelcontextprotocol/server-sequential-thinking"; desc="reasoning"}
)

foreach ($server in $mcpServers) {
    Write-Host "  Adding $($server.name) ($($server.desc))..."
    try {
        $cmdArgs = "mcp add $($server.name) -s user -- $($server.cmd)"
        Start-Process -FilePath "claude" -ArgumentList $cmdArgs -NoNewWindow -Wait 2>$null
    } catch {
        Write-Host "  ($($server.name) may already exist)"
    }
}

# =============================================================================
# STEP 3: Create Intent Detector Hook
# =============================================================================
Write-Host "`n[3/5] Creating intent detector hook..."

$hookContent = @'
#!/usr/bin/env python3
"""Intent Detector Hook - Auto-suggests MCP servers and models based on prompt."""

import json
import sys
import os

MCP_ROUTING = {
    "context7": ["docs", "documentation", "api", "library", "react", "vue", "how to use"],
    "github": ["pr", "pull request", "issue", "commit", "branch", "repo", "github"],
    "memory": ["remember", "recall", "entity", "relationship", "knowledge graph"],
    "sequential-thinking": ["step by step", "reason through", "analyze carefully", "break down"],
    "playwright": ["browser", "screenshot", "scrape", "web page", "click", "navigate"]
}

MODEL_ROUTING = {
    "glm-4.7": ["chinese", "mandarin", "multilingual", "translate to chinese"],
    "gemini-2.5-flash": ["large file", "long document", "huge context", ">100k"],
    "deepseek-r1": ["reasoning", "math", "logic", "proof", "algorithm"]
}

MEMORY_TRIGGERS = ["decided", "decision", "chose", "i prefer", "let's use", "going with"]
BEADS_TRIGGERS = ["complex", "multi-step", "dependencies", "multiple tasks", "epic"]

def main():
    input_data = json.loads(sys.stdin.read())
    prompt = input_data.get("message", "").lower()
    hints = []

    for mcp, keywords in MCP_ROUTING.items():
        if any(kw in prompt for kw in keywords):
            hints.append(f"[mcp] Consider using {mcp}")
            break

    for model, keywords in MODEL_ROUTING.items():
        if any(kw in prompt for kw in keywords):
            hints.append(f"[model] Consider routing to {model}")
            break

    if any(t in prompt for t in MEMORY_TRIGGERS):
        hints.append("[memory] Decision detected - save to memory")

    if any(t in prompt for t in BEADS_TRIGGERS):
        hints.append("[beads] Complex task - consider using Beads")

    # Write hints
    hint_dir = os.path.expanduser("~/.claude/hints")
    os.makedirs(hint_dir, exist_ok=True)
    with open(f"{hint_dir}/current.txt", 'w') as f:
        f.write("\n".join(hints) if hints else "")

    output = {"continue": True}
    if hints:
        output["additionalContext"] = "\n".join(hints)
    print(json.dumps(output))

if __name__ == "__main__":
    main()
'@

$hookContent | Out-File -FilePath "$CLAUDE_DIR\hooks\intent_detector.py" -Encoding UTF8

# =============================================================================
# STEP 4: Create CLAUDE.md
# =============================================================================
Write-Host "`n[4/5] Creating CLAUDE.md..."

$claudeMd = @'
# Claude Code Configuration

## Multi-Model Routing

| Task | Model | Trigger |
|------|-------|---------|
| Normal coding | Claude Opus 4.5 | (default) |
| Multilingual | GLM 4.7 | "chinese", "multilingual" |
| Large context | Gemini 2.5 | ">100k", "large file" |
| Reasoning | DeepSeek R1 | "math", "logic", "proof" |

## MCP Servers

| Server | Purpose |
|--------|---------|
| context7 | Library documentation |
| github | GitHub operations |
| memory | Entity knowledge graph |
| sequential-thinking | Multi-step reasoning |

## Memory Triggers

Save to memory when user says: "decided", "prefer", "chose", "let's use"

```bash
~/.claude/scripts/memory_manager.py save-memory PROJECT TYPE "content"
```

## Rules

1. RAG-First: Query before reading files
2. Verify: Run tests after changes
3. Save Decisions: Persist user choices to memory
'@

$claudeMd | Out-File -FilePath "$CLAUDE_DIR\CLAUDE.md" -Encoding UTF8

# =============================================================================
# STEP 5: Configure Hooks
# =============================================================================
Write-Host "`n[5/5] Configuring hooks..."

$hooksConfig = @'
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "python ~/.claude/hooks/intent_detector.py",
        "timeout": 5000
      }
    ]
  }
}
'@

if (-not (Test-Path "$CLAUDE_DIR\hooks-config.json")) {
    $hooksConfig | Out-File -FilePath "$CLAUDE_DIR\hooks-config.json" -Encoding UTF8
}

# =============================================================================
# DONE
# =============================================================================
Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                    SETUP COMPLETE!                           ║
╠══════════════════════════════════════════════════════════════╣
║  MCP Servers Added:                                          ║
║    - context7 (library docs)                                 ║
║    - github (repo operations)                                ║
║    - memory (entity graph)                                   ║
║    - sequential-thinking (reasoning)                         ║
║                                                              ║
║  Hooks Configured:                                           ║
║    - intent_detector.py (auto-routing)                       ║
║                                                              ║
║  Files Created:                                              ║
║    - ~/.claude/CLAUDE.md                                     ║
║    - ~/.claude/hooks/intent_detector.py                      ║
║    - ~/.claude/hooks-config.json                             ║
╠══════════════════════════════════════════════════════════════╣
║  NEXT STEPS:                                                 ║
║  1. Restart Claude Code                                      ║
║  2. Try: 'How do I use React hooks?' (triggers context7)     ║
║  3. Try: 'Create a PR for this' (triggers github)            ║
╚══════════════════════════════════════════════════════════════╝
"@
