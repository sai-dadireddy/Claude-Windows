#!/bin/bash
# Start n8n with Claude Code Integration
# Version: 1.0
# Created: 2025-10-11

echo "========================================"
echo " n8n + Claude Code Automation Platform"
echo "========================================"
echo ""

# Set environment variables
export N8N_USER_FOLDER="$HOME/.n8n"
export CLAUDE_PROJECT_PATH="$HOME/OneDrive - ERPA/Claude"

# Check if n8n is installed
echo "[1/4] Checking n8n installation..."
if command -v n8n &> /dev/null; then
    N8N_VERSION=$(n8n --version 2>&1)
    echo "    ✓ n8n version: $N8N_VERSION"
else
    echo "    ✗ ERROR: n8n is not installed!"
    echo "    Run: npm install -g n8n"
    exit 1
fi

# Check if Claude Code is authenticated
echo "[2/4] Checking Claude Code authentication..."
if command -v claude &> /dev/null; then
    CLAUDE_STATUS=$(claude auth status 2>&1)
    if [[ $CLAUDE_STATUS == *"authenticated"* ]] || [[ $CLAUDE_STATUS == *"logged in"* ]]; then
        echo "    ✓ Claude Code: Authenticated"
    else
        echo "    ⚠ WARNING: Claude Code may not be authenticated"
        echo "    Run: claude auth login"
    fi
else
    echo "    ⚠ WARNING: Could not verify Claude Code status"
fi

# Check if Claude Code node is installed
echo "[3/4] Checking Claude Code community node..."
if [ -d "$HOME/.n8n/nodes/node_modules/@holtweb/n8n-nodes-claudecode" ]; then
    echo "    ✓ Claude Code node: Installed"
else
    echo "    ⚠ WARNING: Claude Code node not found"
    echo "    Install it in n8n UI: Settings -> Community Nodes"
fi

# Display startup information
echo "[4/4] Starting n8n..."
echo ""
echo "Configuration:"
echo "  - n8n UI:         http://localhost:5678"
echo "  - User folder:    $N8N_USER_FOLDER"
echo "  - Claude project: $CLAUDE_PROJECT_PATH"
echo ""
echo "Quick Start:"
echo "  1. Open http://localhost:5678 in your browser"
echo "  2. Create a new workflow"
echo "  3. Search for 'Claude Code' node"
echo "  4. Start automating!"
echo ""
echo "Press Ctrl+C to stop n8n"
echo ""
echo "========================================"
echo ""

# Start n8n
n8n
