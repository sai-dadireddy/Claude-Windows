#!/bin/bash
# =============================================================================
# Claude Code Multi-AI & MCP Routing Setup
# =============================================================================
# Works on: macOS, Linux, Windows (Git Bash/WSL)
# Prerequisites: Node.js 18+, Claude Code CLI installed
# =============================================================================

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Claude Code Multi-AI & MCP Routing Setup                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Detect OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    CLAUDE_DIR="$USERPROFILE/.claude"
    IS_WINDOWS=true
else
    CLAUDE_DIR="$HOME/.claude"
    IS_WINDOWS=false
fi

# Create directories
echo "[1/5] Creating directories..."
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/hints"
mkdir -p "$CLAUDE_DIR/memory/long-term/global"
mkdir -p "$CLAUDE_DIR/scripts"
mkdir -p "$CLAUDE_DIR/commands"

# =============================================================================
# STEP 2: Add MCP Servers
# =============================================================================
echo ""
echo "[2/5] Adding MCP servers..."

# Context7 - Library documentation
echo "  Adding context7 (library docs)..."
claude mcp add context7 -s user -- npx -y @upstash/context7-mcp 2>/dev/null || \
    echo "  (context7 may already exist)"

# GitHub - Repository operations
echo "  Adding github (repo ops)..."
claude mcp add github -s user -- npx -y @modelcontextprotocol/server-github 2>/dev/null || \
    echo "  (github may already exist)"

# Memory - Entity knowledge graph
echo "  Adding memory (knowledge graph)..."
claude mcp add memory -s user -- npx -y @modelcontextprotocol/server-memory 2>/dev/null || \
    echo "  (memory may already exist)"

# Sequential Thinking - Reasoning
echo "  Adding sequential-thinking (reasoning)..."
claude mcp add sequential-thinking -s user -- npx -y @modelcontextprotocol/server-sequential-thinking 2>/dev/null || \
    echo "  (sequential-thinking may already exist)"

# =============================================================================
# STEP 3: Create Intent Detector Hook
# =============================================================================
echo ""
echo "[3/5] Creating intent detector hook..."

cat > "$CLAUDE_DIR/hooks/intent_detector.py" << 'HOOK_EOF'
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
HOOK_EOF

chmod +x "$CLAUDE_DIR/hooks/intent_detector.py"

# =============================================================================
# STEP 4: Create CLAUDE.md
# =============================================================================
echo ""
echo "[4/5] Creating CLAUDE.md..."

cat > "$CLAUDE_DIR/CLAUDE.md" << 'MD_EOF'
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
MD_EOF

# =============================================================================
# STEP 5: Configure Hooks
# =============================================================================
echo ""
echo "[5/5] Configuring hooks..."

# Create hooks-config.json if it doesn't exist
if [ ! -f "$CLAUDE_DIR/hooks-config.json" ]; then
    cat > "$CLAUDE_DIR/hooks-config.json" << 'HOOKS_EOF'
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
HOOKS_EOF
fi

# =============================================================================
# DONE
# =============================================================================
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE!                           ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  MCP Servers Added:                                          ║"
echo "║    - context7 (library docs)                                 ║"
echo "║    - github (repo operations)                                ║"
echo "║    - memory (entity graph)                                   ║"
echo "║    - sequential-thinking (reasoning)                         ║"
echo "║                                                              ║"
echo "║  Hooks Configured:                                           ║"
echo "║    - intent_detector.py (auto-routing)                       ║"
echo "║                                                              ║"
echo "║  Files Created:                                              ║"
echo "║    - ~/.claude/CLAUDE.md                                     ║"
echo "║    - ~/.claude/hooks/intent_detector.py                      ║"
echo "║    - ~/.claude/hooks-config.json                             ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  NEXT STEPS:                                                 ║"
echo "║  1. Restart Claude Code                                      ║"
echo "║  2. Try: 'How do I use React hooks?' (triggers context7)     ║"
echo "║  3. Try: 'Create a PR for this' (triggers github)            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
