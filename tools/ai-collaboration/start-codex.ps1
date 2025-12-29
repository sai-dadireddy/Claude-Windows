<#
.SYNOPSIS
Automatic startup for Codex - No manual steps needed

.DESCRIPTION
Automatically loads all context, rules, and configuration for Codex.
Run this script to start a Codex session with full collaboration setup.

.EXAMPLE
.\tools\ai-collaboration\start-codex.ps1

.NOTES
Version: 1.0
Date: 2025-10-15
#>

$ErrorActionPreference = "Stop"

# Get root directory
$RootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Starting Codex Session (Automatic)" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Step 1: Set working directory
Set-Location $RootDir
Write-Host "[1/7] Working Directory: $RootDir" -ForegroundColor Green

# Step 2: Set environment variables
$env:AI_CONTEXT = "codex"
$env:MEMORY_NAMESPACE = "codex_specific"
$env:AI_WORKSPACE = Join-Path $RootDir ".ai-workspace/codex"
$env:AI_SESSION = "codex"
Write-Host "[2/7] Environment Variables Set" -ForegroundColor Green
Write-Host "      AI_CONTEXT: codex" -ForegroundColor Gray
Write-Host "      AI_WORKSPACE: .ai-workspace/codex" -ForegroundColor Gray

# Step 3: Configure Git identity
git config user.name "Codex GPT-5"
git config user.email "codex@openai.com"
Write-Host "[3/7] Git Identity Configured" -ForegroundColor Green
Write-Host "      Name: Codex GPT-5" -ForegroundColor Gray

# Step 4: Check for pending reviews
$ReviewQueuePath = Join-Path $RootDir ".ai-workspace/shared/review-queue.json"
if (Test-Path $ReviewQueuePath) {
    $ReviewQueue = Get-Content $ReviewQueuePath -Raw | ConvertFrom-Json
    $PendingCount = $ReviewQueue.pending_reviews.Count
    if ($PendingCount -gt 0) {
        Write-Host "[4/7] PENDING REVIEWS: $PendingCount" -ForegroundColor Yellow
        Write-Host "      These changes from Claude need your review:" -ForegroundColor Yellow
        foreach ($Review in $ReviewQueue.pending_reviews) {
            Write-Host "      - [$($Review.ai)] $($Review.action)" -ForegroundColor White
            Write-Host "        ID: $($Review.id)" -ForegroundColor Gray
            Write-Host "        Files: $($Review.files -join ', ')" -ForegroundColor Gray
        }
        Write-Host "`n      Review with: python tools/ai-collaboration/change-tracker.py status <change-id>" -ForegroundColor Cyan
    } else {
        Write-Host "[4/7] No Pending Reviews" -ForegroundColor Green
    }
} else {
    Write-Host "[4/7] Review Queue: Not initialized yet" -ForegroundColor Gray
}

# Step 5: Show recent Claude activity
$ChangeLogPath = Join-Path $RootDir ".ai-workspace/shared/change-log.jsonl"
if (Test-Path $ChangeLogPath) {
    Write-Host "[5/7] Recent Activity from Claude:" -ForegroundColor Cyan
    $AllLines = Get-Content $ChangeLogPath
    if ($AllLines.Count -gt 1) {
        $RecentChanges = $AllLines | Select-Object -Last 5 | Select-Object -Skip 1
        $ClaudeChanges = 0
        foreach ($Line in $RecentChanges) {
            try {
                $Change = $Line | ConvertFrom-Json
                if ($Change.ai -eq "claude") {
                    $Timestamp = [datetime]::Parse($Change.timestamp).ToString("MM/dd HH:mm")
                    $Status = if ($Change.validated_by -eq "codex") { "Validated" } else { "Pending" }
                    Write-Host "      - [$($Change.ai)] $($Change.action) ($Timestamp) - $Status" -ForegroundColor Gray
                    $ClaudeChanges++
                }
            } catch {
                # Skip malformed lines
            }
        }
        if ($ClaudeChanges -eq 0) {
            Write-Host "      No recent Claude activity" -ForegroundColor Gray
        }
    } else {
        Write-Host "      No changes logged yet" -ForegroundColor Gray
    }
} else {
    Write-Host "[5/7] Change Log: Not initialized yet" -ForegroundColor Gray
}

# Step 6: Load Codex instructions
Write-Host "[6/7] Loading Codex Instructions..." -ForegroundColor Green
$InstructionsPath = Join-Path $RootDir "codex/QUICK-START.md"
if (Test-Path $InstructionsPath) {
    Write-Host "      Instructions available at: codex/QUICK-START.md" -ForegroundColor Gray
} else {
    Write-Host "      Creating quick start guide..." -ForegroundColor Gray
}

# Step 7: Display session rules
Write-Host ""
Write-Host "[7/7] Session Rules Loaded" -ForegroundColor Green

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "Codex Session Ready" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Your Role:" -ForegroundColor Yellow
Write-Host "  1. Review Claude's changes (see pending reviews above)" -ForegroundColor White
Write-Host "  2. Validate good work: python tools/ai-collaboration/change-tracker.py validate <change-id> codex" -ForegroundColor White
Write-Host "  3. Work on your drafts in: .ai-workspace/codex/in-progress/" -ForegroundColor White
Write-Host "  4. Log all changes: python tools/ai-collaboration/change-tracker.py log codex ""action"" files" -ForegroundColor White
Write-Host "  5. Commit with: git commit -m ""codex: type(scope) description""" -ForegroundColor White

Write-Host ""
Write-Host "Quick Commands:" -ForegroundColor Cyan
Write-Host "  # View what Claude did" -ForegroundColor Gray
Write-Host "  python tools/ai-collaboration/change-tracker.py list --ai claude --recent 10" -ForegroundColor White
Write-Host ""
Write-Host "  # Review specific change" -ForegroundColor Gray
Write-Host "  python tools/ai-collaboration/change-tracker.py status <change-id>" -ForegroundColor White
Write-Host ""
Write-Host "  # Validate change" -ForegroundColor Gray
Write-Host "  python tools/ai-collaboration/change-tracker.py validate <change-id> codex" -ForegroundColor White
Write-Host ""
Write-Host "  # Log your change" -ForegroundColor Gray
Write-Host "  python tools/ai-collaboration/change-tracker.py log codex ""action"" files" -ForegroundColor White

Write-Host ""
Write-Host "Start reviewing! All context loaded automatically." -ForegroundColor Green
Write-Host ""

# Optional: Start Codex if installed
if (Get-Command codex -ErrorAction SilentlyContinue) {
    $StartCodex = Read-Host "Start Codex CLI now? (y/n)"
    if ($StartCodex -eq "y") {
        codex
    }
}
