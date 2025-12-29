<#
.SYNOPSIS
Switch between Claude, Codex, and Gemini AI contexts

.DESCRIPTION
Loads appropriate configuration and workspace for the selected AI,
ensuring proper MCP access, memory namespace, and change tracking.

.PARAMETER AI
The AI to switch to: claude, codex, or gemini

.EXAMPLE
.\ai-switch.ps1 claude

.EXAMPLE
.\ai-switch.ps1 codex

.NOTES
Version: 1.0
Date: 2025-10-15
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("claude", "codex", "gemini")]
    [string]$AI
)

$ErrorActionPreference = "Stop"

# Get root directory
$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🔄 Switching to $($AI.ToUpper()) Context" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

# Verify .ai-workspace exists
$WorkspacePath = Join-Path $RootDir ".ai-workspace"
if (-not (Test-Path $WorkspacePath)) {
    Write-Host "❌ Error: Multi-AI workspace not found!" -ForegroundColor Red
    Write-Host "   Run: .\tools\ai-collaboration\setup-multi-ai.ps1" -ForegroundColor Yellow
    exit 1
}

# Step 1: Set working directory
$AIWorkspace = Join-Path $RootDir $AI
if (Test-Path $AIWorkspace) {
    Set-Location $AIWorkspace
    Write-Host "[INFO] Working directory: $AIWorkspace" -ForegroundColor Green
} else {
    Write-Host "[WARN] AI directory not found, creating: $AI/" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $AIWorkspace -Force | Out-Null
    Set-Location $AIWorkspace
}

# Step 2: Load shared MCP configuration
$McpShared = Join-Path $RootDir ".ai-workspace/config/mcp-shared.json"
if (Test-Path $McpShared) {
    Write-Host "[INFO] Shared MCP configuration available" -ForegroundColor Green
} else {
    Write-Host "[WARN] Shared MCP config not found: $McpShared" -ForegroundColor Yellow
}

# Step 3: Load features configuration
$FeaturesPath = Join-Path $RootDir ".ai-workspace/config/features.json"
if (Test-Path $FeaturesPath) {
    $Features = Get-Content $FeaturesPath -Raw | ConvertFrom-Json
    $AIFeatures = $Features.enhanced_features.$AI
    Write-Host "[INFO] AI-specific features loaded:" -ForegroundColor Green
    foreach ($Feature in $AIFeatures) {
        Write-Host "  • $Feature" -ForegroundColor Gray
    }
} else {
    Write-Host "[WARN] Features config not found" -ForegroundColor Yellow
}

# Step 4: Check for pending reviews
$ReviewQueue = Join-Path $RootDir ".ai-workspace/shared/review-queue.json"
if (Test-Path $ReviewQueue) {
    $Reviews = Get-Content $ReviewQueue -Raw | ConvertFrom-Json
    $PendingCount = $Reviews.pending_reviews.Count
    if ($PendingCount -gt 0) {
        Write-Host "`n[INFO] $PendingCount pending review(s) in queue" -ForegroundColor Cyan
        Write-Host "  Run: python tools/ai-collaboration/review-helper.py show-pending" -ForegroundColor Gray
    }
}

# Step 5: Show recent changes from other AIs
$ChangeLog = Join-Path $RootDir ".ai-workspace/shared/change-log.jsonl"
if (Test-Path $ChangeLog) {
    $AllLines = Get-Content $ChangeLog
    if ($AllLines.Count -gt 1) {
        Write-Host "`n[INFO] Recent changes from other AIs:" -ForegroundColor Cyan
        $RecentChanges = $AllLines | Select-Object -Last 5 | Select-Object -Skip 1
        foreach ($Line in $RecentChanges) {
            try {
                $Change = $Line | ConvertFrom-Json
                if ($Change.ai -ne $AI) {
                    $Timestamp = [datetime]::Parse($Change.timestamp).ToString("MM/dd HH:mm")
                    Write-Host "  • [$($Change.ai)] $($Change.action) ($Timestamp)" -ForegroundColor Gray
                }
            } catch {
                # Skip malformed lines
            }
        }
    }
}

# Step 6: Set environment variables for AI-specific memory namespace
$env:AI_CONTEXT = $AI
$env:MEMORY_NAMESPACE = "${AI}_specific"
$env:AI_WORKSPACE = Join-Path $RootDir ".ai-workspace/$AI"

Write-Host "`n[INFO] Environment variables set:" -ForegroundColor Green
Write-Host "  AI_CONTEXT = $AI" -ForegroundColor Gray
Write-Host "  MEMORY_NAMESPACE = ${AI}_specific" -ForegroundColor Gray

# Step 7: AI-specific setup
switch ($AI) {
    "claude" {
        Write-Host "`n📘 Claude Code Context" -ForegroundColor Blue
        Write-Host "  • Full MCP access (10 servers)" -ForegroundColor Gray
        Write-Host "  • Sequential thinking available" -ForegroundColor Gray
        Write-Host "  • Playwright testing enabled" -ForegroundColor Gray
        Write-Host "  • Code index search ready" -ForegroundColor Gray
        Write-Host "`n  Start: claude code" -ForegroundColor Cyan
    }
    "codex" {
        Write-Host "`n🟢 Codex GPT-5 Context" -ForegroundColor Green
        Write-Host "  • Full MCP access (10 servers)" -ForegroundColor Gray
        Write-Host "  • Advanced planning mode" -ForegroundColor Gray
        Write-Host "  • High confidence implementation" -ForegroundColor Gray
        Write-Host "`n  Start: codex" -ForegroundColor Cyan
    }
    "gemini" {
        Write-Host "`n🔵 Gemini Context" -ForegroundColor Magenta
        Write-Host "  • Full MCP access (10 servers)" -ForegroundColor Gray
        Write-Host "  • Google APIs integration" -ForegroundColor Gray
        Write-Host "  • Multimodal analysis" -ForegroundColor Gray
        Write-Host "`n  Start: gemini" -ForegroundColor Cyan
    }
}

# Step 8: Show quick commands
Write-Host "`n🎯 Quick Commands:" -ForegroundColor Yellow
Write-Host "  # Log a change"
Write-Host "  python ../tools/ai-collaboration/change-tracker.py log $AI 'action' files.txt"
Write-Host ""
Write-Host "  # View recent changes"
Write-Host "  python ../tools/ai-collaboration/change-tracker.py list --recent 10"
Write-Host ""
Write-Host "  # Check pending reviews"
Write-Host "  python ../tools/ai-collaboration/review-helper.py show-pending"

Write-Host "`n✨ Context switched to $($AI.ToUpper())!`n" -ForegroundColor Green

# Return to root for convenience
Set-Location $RootDir
Write-Host "[INFO] Working directory reset to: $RootDir`n" -ForegroundColor Gray
