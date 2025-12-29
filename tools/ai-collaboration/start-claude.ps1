<#
.SYNOPSIS
Automatic startup for Claude - No manual steps needed

.DESCRIPTION
Automatically loads all context, rules, and configuration for Claude.
Run this script to start a Claude session with full collaboration setup.

.EXAMPLE
.\tools\ai-collaboration\start-claude.ps1
#>

$ErrorActionPreference = "Stop"

# Get root directory
$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting Claude Session (Automatic)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Set working directory
Set-Location $RootDir
Write-Host "[1/6] Working Directory: $RootDir" -ForegroundColor Green

# Step 2: Set environment variables
$env:AI_CONTEXT = "claude"
$env:MEMORY_NAMESPACE = "claude_specific"
$env:AI_WORKSPACE = Join-Path $RootDir ".ai-workspace/claude"
$env:AI_SESSION = "claude"
Write-Host "[2/6] Environment Variables Set" -ForegroundColor Green
Write-Host "      AI_CONTEXT: claude" -ForegroundColor Gray
Write-Host "      AI_WORKSPACE: .ai-workspace/claude" -ForegroundColor Gray

# Step 3: Configure Git identity
git config user.name "Claude Sonnet 4.5" 2>$null
git config user.email "claude@anthropic.com" 2>$null
Write-Host "[3/6] Git Identity Configured" -ForegroundColor Green
Write-Host "      Name: Claude Sonnet 4.5" -ForegroundColor Gray

# Step 4: Check for pending reviews
$ReviewQueuePath = Join-Path $RootDir ".ai-workspace/shared/review-queue.json"
if (Test-Path $ReviewQueuePath) {
    $ReviewQueue = Get-Content $ReviewQueuePath -Raw | ConvertFrom-Json
    $PendingCount = $ReviewQueue.pending_reviews.Count
    if ($PendingCount -gt 0) {
        Write-Host "[4/6] Pending Reviews: $PendingCount" -ForegroundColor Yellow
        Write-Host "      Run: python tools/ai-collaboration/change-tracker.py list --recent 10" -ForegroundColor Gray
    } else {
        Write-Host "[4/6] No Pending Reviews" -ForegroundColor Green
    }
} else {
    Write-Host "[4/6] Review Queue: Not initialized yet" -ForegroundColor Gray
}

# Step 5: Show recent Codex activity
$ChangeLogPath = Join-Path $RootDir ".ai-workspace/shared/change-log.jsonl"
if (Test-Path $ChangeLogPath) {
    Write-Host "[5/6] Recent Activity from Codex:" -ForegroundColor Cyan
    $AllLines = Get-Content $ChangeLogPath
    if ($AllLines.Count -gt 1) {
        $RecentChanges = $AllLines | Select-Object -Last 5 | Select-Object -Skip 1
        $CodexChanges = 0
        foreach ($Line in $RecentChanges) {
            try {
                $Change = $Line | ConvertFrom-Json
                if ($Change.ai -eq "codex") {
                    $Timestamp = [datetime]::Parse($Change.timestamp).ToString("MM/dd HH:mm")
                    Write-Host "      - [$($Change.ai)] $($Change.action) ($Timestamp)" -ForegroundColor Gray
                    $CodexChanges++
                }
            } catch {
                # Skip malformed lines
            }
        }
        if ($CodexChanges -eq 0) {
            Write-Host "      No recent Codex activity" -ForegroundColor Gray
        }
    } else {
        Write-Host "      No changes logged yet" -ForegroundColor Gray
    }
} else {
    Write-Host "[5/6] Change Log: Not initialized yet" -ForegroundColor Gray
}

# Step 6: Display session rules
Write-Host ""
Write-Host "[6/6] Session Rules Loaded" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Claude Session Ready" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Working Rules:" -ForegroundColor Yellow
Write-Host "  1. Work on drafts in: .ai-workspace/claude/in-progress/" -ForegroundColor White
Write-Host "  2. Log all changes: python tools/ai-collaboration/change-tracker.py log claude ""action"" files" -ForegroundColor White
Write-Host "  3. Check Codex activity: python tools/ai-collaboration/change-tracker.py list --ai codex" -ForegroundColor White
Write-Host "  4. Move to root when done" -ForegroundColor White
Write-Host "  5. Commit with: git commit -m ""claude: type(scope) description""" -ForegroundColor White

Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Cyan
Write-Host "  python tools/ai-collaboration/change-tracker.py list --recent 10" -ForegroundColor White
Write-Host "  python tools/ai-collaboration/change-tracker.py list --ai codex" -ForegroundColor White
Write-Host "  python tools/ai-collaboration/change-tracker.py log claude ""action"" files" -ForegroundColor White

Write-Host ""
Write-Host "You're all set! Start working." -ForegroundColor Green
Write-Host ""
