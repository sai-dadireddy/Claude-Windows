<#
.SYNOPSIS
Setup multi-AI collaboration workspace for Claude, Codex, and Gemini

.DESCRIPTION
Creates shared workspace structure, MCP configuration, memory database,
and collaboration tools for seamless multi-AI workflows.

.EXAMPLE
.\setup-multi-ai.ps1

.NOTES
Version: 1.0
Date: 2025-10-15
#>

param(
    [switch]$Force  # Force recreation of existing directories
)

$ErrorActionPreference = "Stop"

# Get root directory (2 levels up from tools/ai-collaboration/)
$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🤝 Multi-AI Collaboration System Setup" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# Step 1: Create directory structure
Write-Host "[1/6] Creating AI workspace structure..." -ForegroundColor Yellow

$Directories = @(
    ".ai-workspace/claude/in-progress",
    ".ai-workspace/claude/completed",
    ".ai-workspace/claude/proposals",
    ".ai-workspace/codex/in-progress",
    ".ai-workspace/codex/completed",
    ".ai-workspace/codex/proposals",
    ".ai-workspace/gemini/in-progress",
    ".ai-workspace/gemini/completed",
    ".ai-workspace/gemini/proposals",
    ".ai-workspace/shared",
    ".ai-workspace/config"
)

foreach ($Dir in $Directories) {
    $FullPath = Join-Path $RootDir $Dir
    if (-not (Test-Path $FullPath)) {
        New-Item -ItemType Directory -Path $FullPath -Force | Out-Null
        Write-Host "  ✅ Created: $Dir" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Exists: $Dir" -ForegroundColor Gray
    }
}

# Step 2: Initialize shared resources
Write-Host "`n[2/6] Initializing shared resources..." -ForegroundColor Yellow

# Create change log
$ChangeLogPath = Join-Path $RootDir ".ai-workspace/shared/change-log.jsonl"
if (-not (Test-Path $ChangeLogPath)) {
    @"
{"version":"1.0","created":"$(Get-Date -Format 'o')","description":"Multi-AI change tracking log"}
"@ | Out-File -FilePath $ChangeLogPath -Encoding UTF8
    Write-Host "  ✅ Created: change-log.jsonl" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Exists: change-log.jsonl" -ForegroundColor Gray
}

# Create review queue
$ReviewQueuePath = Join-Path $RootDir ".ai-workspace/shared/review-queue.json"
if (-not (Test-Path $ReviewQueuePath)) {
    @"
{
  "version": "1.0",
  "pending_reviews": [],
  "completed_reviews": []
}
"@ | Out-File -FilePath $ReviewQueuePath -Encoding UTF8
    Write-Host "  ✅ Created: review-queue.json" -ForegroundColor Green
} else {
    Write-Host "  ℹ️  Exists: review-queue.json" -ForegroundColor Gray
}

# Create README for .ai-workspace
$ReadmePath = Join-Path $RootDir ".ai-workspace/README.md"
if (-not (Test-Path $ReadmePath)) {
    @"
# Multi-AI Collaboration Workspace

This directory contains shared resources for Claude, Codex, and Gemini collaboration.

## Structure

- \`claude/\` - Claude-specific workspace
- \`codex/\` - Codex-specific workspace
- \`gemini/\` - Gemini-specific workspace
- \`shared/\` - Shared resources (memory, change log, review queue)
- \`config/\` - Shared configurations (MCP, features)

## Documentation

See: \`docs/guides/multi-ai-collaboration-system.md\`

## Commands

\`\`\`bash
# Switch AI context
.\tools\ai-collaboration\ai-switch.ps1 claude|codex|gemini

# View recent changes
python tools/ai-collaboration/change-tracker.py list --recent 10

# Show pending reviews
python tools/ai-collaboration/review-helper.py show-pending
\`\`\`
"@ | Out-File -FilePath $ReadmePath -Encoding UTF8
    Write-Host "  ✅ Created: README.md" -ForegroundColor Green
}

# Step 3: Setup MCP shared configuration
Write-Host "`n[3/6] Configuring shared MCP access..." -ForegroundColor Yellow

$McpSharedPath = Join-Path $RootDir ".ai-workspace/config/mcp-shared.json"
$SourceMcpPath = Join-Path $RootDir "claude-code-mcp-config.json"

if (Test-Path $SourceMcpPath) {
    Copy-Item $SourceMcpPath $McpSharedPath -Force
    Write-Host "  ✅ Copied MCP config to shared location" -ForegroundColor Green

    # Update shared config to use shared memory database
    $McpConfig = Get-Content $McpSharedPath -Raw | ConvertFrom-Json

    # Update memory-auto to use shared database
    if ($McpConfig.mcpServers."memory-auto") {
        $SharedMemoryDb = Join-Path $RootDir ".ai-workspace/shared/memory.db"
        $McpConfig.mcpServers."memory-auto".env.GLOBAL_DB = $SharedMemoryDb
        $McpConfig | ConvertTo-Json -Depth 10 | Out-File -FilePath $McpSharedPath -Encoding UTF8
        Write-Host "  ✅ Updated memory-auto to use shared database" -ForegroundColor Green
    }
} else {
    Write-Host "  ⚠️  Source MCP config not found: $SourceMcpPath" -ForegroundColor Yellow
    Write-Host "  ℹ️  You'll need to create mcp-shared.json manually" -ForegroundColor Gray
}

# Step 4: Create feature configuration
Write-Host "`n[4/6] Creating feature parity configuration..." -ForegroundColor Yellow

$FeaturesPath = Join-Path $RootDir ".ai-workspace/config/features.json"
if (-not (Test-Path $FeaturesPath)) {
    @"
{
  "version": "1.0",
  "mcp_access": {
    "claude": true,
    "codex": true,
    "gemini": true
  },
  "memory_system": {
    "claude": {
      "enabled": true,
      "db_path": ".ai-workspace/shared/memory.db",
      "namespace": "claude_specific"
    },
    "codex": {
      "enabled": true,
      "db_path": ".ai-workspace/shared/memory.db",
      "namespace": "codex_specific"
    },
    "gemini": {
      "enabled": true,
      "db_path": ".ai-workspace/shared/memory.db",
      "namespace": "gemini_specific"
    }
  },
  "enhanced_features": {
    "all": [
      "change_tracking",
      "cross_ai_validation",
      "memory_sharing",
      "mcp_coordination"
    ],
    "claude": [
      "playwright_testing",
      "sequential_thinking",
      "code_index_search"
    ],
    "codex": [
      "advanced_planning",
      "high_confidence_mode"
    ],
    "gemini": [
      "google_integration",
      "multimodal_analysis"
    ]
  }
}
"@ | Out-File -FilePath $FeaturesPath -Encoding UTF8
    Write-Host "  ✅ Created: features.json" -ForegroundColor Green
}

# Step 5: Create Python helper scripts stubs
Write-Host "`n[5/6] Creating collaboration helper scripts..." -ForegroundColor Yellow

$PythonScripts = @(
    @{
        Name = "change-tracker.py"
        Content = @"
#!/usr/bin/env python3
"""
Multi-AI Change Tracker
Tracks and attributes changes across Claude, Codex, and Gemini
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def main():
    print("🔍 Multi-AI Change Tracker")
    print("=" * 50)
    print("Usage: python change-tracker.py <command>")
    print()
    print("Commands:")
    print("  list [--recent N] [--ai NAME]  - List changes")
    print("  log <ai> <action> <files>      - Log new change")
    print("  status <change-id>             - Show change status")
    print()
    print("Implementation: TODO - See docs/guides/multi-ai-collaboration-system.md")

if __name__ == "__main__":
    main()
"@
    },
    @{
        Name = "review-helper.py"
        Content = @"
#!/usr/bin/env python3
"""
Multi-AI Review Helper
Helps review and validate changes from any AI
"""

import json
import sys
from pathlib import Path

def main():
    print("📋 Multi-AI Review Helper")
    print("=" * 50)
    print("Usage: python review-helper.py <command>")
    print()
    print("Commands:")
    print("  show-pending         - Show pending reviews")
    print("  compare <id1> <id2>  - Compare two changes")
    print("  approve <change-id>  - Approve a change")
    print()
    print("Implementation: TODO - See docs/guides/multi-ai-collaboration-system.md")

if __name__ == "__main__":
    main()
"@
    },
    @{
        Name = "memory-sync.py"
        Content = @"
#!/usr/bin/env python3
"""
Multi-AI Memory Synchronizer
Syncs memory database across all AIs
"""

import sys
from pathlib import Path

def main():
    print("🧠 Multi-AI Memory Sync")
    print("=" * 50)
    print("Usage: python memory-sync.py <command>")
    print()
    print("Commands:")
    print("  sync-all             - Sync all AI memories")
    print("  status               - Show sync status")
    print()
    print("Implementation: TODO - See docs/guides/multi-ai-collaboration-system.md")

if __name__ == "__main__":
    main()
"@
    }
)

foreach ($Script in $PythonScripts) {
    $ScriptPath = Join-Path $PSScriptRoot $Script.Name
    if (-not (Test-Path $ScriptPath)) {
        $Script.Content | Out-File -FilePath $ScriptPath -Encoding UTF8
        Write-Host "  ✅ Created: $($Script.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ℹ️  Exists: $($Script.Name)" -ForegroundColor Gray
    }
}

# Step 6: Summary and next steps
Write-Host "`n[6/6] Setup complete!" -ForegroundColor Green

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ Multi-AI Collaboration System Ready" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "📁 Workspace Structure:" -ForegroundColor Cyan
Write-Host "  .ai-workspace/"
Write-Host "  ├── claude/          (Claude-specific work)"
Write-Host "  ├── codex/           (Codex-specific work)"
Write-Host "  ├── gemini/          (Gemini-specific work)"
Write-Host "  ├── shared/          (Shared resources)"
Write-Host "  └── config/          (Shared configurations)"

Write-Host "`n🔧 Configuration Files Created:" -ForegroundColor Cyan
Write-Host "  ✅ change-log.jsonl      (Change tracking)"
Write-Host "  ✅ review-queue.json     (Review workflow)"
Write-Host "  ✅ mcp-shared.json       (Shared MCP config)"
Write-Host "  ✅ features.json         (Feature parity)"

Write-Host "`n🛠️ Helper Scripts Created:" -ForegroundColor Cyan
Write-Host "  ✅ change-tracker.py     (Track AI changes)"
Write-Host "  ✅ review-helper.py      (Review workflow)"
Write-Host "  ✅ memory-sync.py        (Memory sync)"

Write-Host "`n📚 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Implement Python helper scripts (see docs/guides/multi-ai-collaboration-system.md)"
Write-Host "  2. Configure each AI with collaboration instructions"
Write-Host "  3. Test workflow with: .\tools\ai-collaboration\ai-switch.ps1 claude"
Write-Host "  4. Review full documentation: docs/guides/multi-ai-collaboration-system.md"

Write-Host "`n🎯 Quick Commands:" -ForegroundColor Cyan
Write-Host "  # Switch to Claude"
Write-Host "  .\tools\ai-collaboration\ai-switch.ps1 claude"
Write-Host ""
Write-Host "  # Switch to Codex"
Write-Host "  .\tools\ai-collaboration\ai-switch.ps1 codex"
Write-Host ""
Write-Host "  # View changes"
Write-Host "  python tools/ai-collaboration/change-tracker.py list --recent 10"

Write-Host "`n✨ System ready for multi-AI collaboration!`n" -ForegroundColor Green
