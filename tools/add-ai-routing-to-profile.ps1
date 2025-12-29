# Add AI Routing Functions to PowerShell Profile
# Clean version without Unicode characters

param(
    [switch]$Force = $false
)

Write-Host "`nAdding AI Routing to PowerShell Profile" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Gray

$profilePath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

# Backup current profile
$backupPath = "$profilePath.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $profilePath $backupPath -Force
Write-Host "[OK] Backup created: $backupPath" -ForegroundColor Green

# Clean AI Tools section (no Unicode)
$aiToolsSection = @'


# ============================================================================
# AI CODING ASSISTANTS - Intelligent Routing System
# ============================================================================

# AI Router - Automatically selects best AI for the task
function Invoke-AIRouter {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Task,
        [ValidateSet("auto", "claude", "codex", "gemini")]
        [string]$ForceAI = "auto",
        [switch]$Explain = $false
    )

    # Task classification patterns
    $patterns = @{
        claude = @(
            "refactor", "architecture", "security", "review", "debug complex",
            "multi-file", "large project", "comprehensive", "analyze",
            "best practices", "production code", "maintainability"
        )
        codex = @(
            "quick", "prototype", "algorithm", "math", "calculate",
            "one function", "simple", "fast", "convert", "translate",
            "implement", "reasoning", "logic problem"
        )
        gemini = @(
            "research", "documentation", "explain", "tutorial",
            "what is", "how to", "compare", "find", "search",
            "latest", "current", "recent", "UI", "design"
        )
    }

    # Determine best AI
    $selectedAI = "claude"  # Default

    if ($ForceAI -ne "auto") {
        $selectedAI = $ForceAI
    } else {
        $taskLower = $Task.ToLower()
        $scores = @{
            claude = 0
            codex = 0
            gemini = 0
        }

        foreach ($ai in $patterns.Keys) {
            foreach ($pattern in $patterns[$ai]) {
                if ($taskLower -like "*$pattern*") {
                    $scores[$ai]++
                }
            }
        }

        # Select AI with highest score
        $maxScore = ($scores.Values | Measure-Object -Maximum).Maximum
        if ($maxScore -gt 0) {
            $selectedAI = ($scores.GetEnumerator() | Where-Object {$_.Value -eq $maxScore} | Select-Object -First 1).Key
        }
    }

    if ($Explain) {
        Write-Host "`nAI ROUTING DECISION" -ForegroundColor Cyan
        Write-Host "==============================" -ForegroundColor Gray
        Write-Host "Task: $Task" -ForegroundColor White
        Write-Host "Selected AI: " -NoNewline -ForegroundColor Yellow
        Write-Host $selectedAI.ToUpper() -ForegroundColor Green
        Write-Host "`nWhy $($selectedAI)?" -ForegroundColor Yellow

        $reasons = @{
            claude = "Best for complex, multi-file work requiring deep understanding"
            codex = "Best for quick implementations and algorithmic tasks"
            gemini = "Best for research, documentation, and explanations"
        }
        Write-Host "  -> $($reasons[$selectedAI])" -ForegroundColor White
        Write-Host "==============================`n" -ForegroundColor Gray
    }

    # Generate command hint
    $commands = @{
        claude = "claude"
        codex = "codex"
        gemini = "gemini"
    }

    Write-Host "`nRecommended: " -NoNewline -ForegroundColor Cyan
    Write-Host $commands[$selectedAI] -ForegroundColor Green
    Write-Host "`nPaste this prompt:`n" -ForegroundColor Yellow
    Write-Host $Task -ForegroundColor White
    Write-Host ""

    return $selectedAI
}

# Quick AI launcher
function Start-AI {
    param(
        [ValidateSet("claude", "codex", "gemini", "all")]
        [string]$Which = "claude"
    )

    switch ($Which) {
        "claude" {
            Write-Host "Launching Claude Code..." -ForegroundColor Cyan
            claude
        }
        "codex" {
            Write-Host "Launching Codex (GPT-5)..." -ForegroundColor Green
            codex
        }
        "gemini" {
            Write-Host "Launching Gemini..." -ForegroundColor Magenta
            gemini
        }
        "all" {
            Write-Host "Multi-AI mode - Opening 3 terminals..." -ForegroundColor Cyan
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "claude"
            Start-Sleep -Milliseconds 500
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "codex"
            Start-Sleep -Milliseconds 500
            Start-Process powershell -ArgumentList "-NoExit", "-Command", "gemini"
        }
    }
}

# AI status checker
function Get-AIStatus {
    Write-Host "`nAI TOOLS STATUS" -ForegroundColor Cyan
    Write-Host "==============================`n" -ForegroundColor Gray

    $tools = @("claude", "codex", "gemini")

    foreach ($tool in $tools) {
        $exists = Get-Command $tool -ErrorAction SilentlyContinue
        if ($exists) {
            Write-Host "[OK] $($tool.ToUpper())" -NoNewline -ForegroundColor Green
            try {
                $version = & $tool --version 2>&1
                Write-Host " - $version" -ForegroundColor Gray
            } catch {
                Write-Host " - Installed" -ForegroundColor Gray
            }
        } else {
            Write-Host "[X] $($tool.ToUpper()) - Not installed" -ForegroundColor Red
        }
    }

    Write-Host "`n==============================" -ForegroundColor Gray
    Write-Host "Use: ai-route 'your task' for intelligent routing`n" -ForegroundColor Yellow
}

# Quick examples
function Show-AIExamples {
    Write-Host "`nAI ROUTING EXAMPLES" -ForegroundColor Cyan
    Write-Host "==============================`n" -ForegroundColor Gray

    Write-Host "CLAUDE (Complex/Multi-file):" -ForegroundColor Blue
    Write-Host "  ai-route 'Refactor authentication system across 5 files'" -ForegroundColor Gray
    Write-Host "  ai-route 'Review this code for security vulnerabilities'" -ForegroundColor Gray

    Write-Host "`nCODEX (Quick/Algorithmic):" -ForegroundColor Green
    Write-Host "  ai-route 'Write a quick sort algorithm in Python'" -ForegroundColor Gray
    Write-Host "  ai-route 'Convert this SQL query to MongoDB'" -ForegroundColor Gray

    Write-Host "`nGEMINI (Research/Docs):" -ForegroundColor Magenta
    Write-Host "  ai-route 'Explain React Server Components'" -ForegroundColor Gray
    Write-Host "  ai-route 'Find the latest Next.js 15 changes'" -ForegroundColor Gray

    Write-Host "`n==============================`n" -ForegroundColor Gray
}

# Shortcuts
Set-Alias -Name ai-route -Value Invoke-AIRouter
Set-Alias -Name ai -Value Invoke-AIRouter
Set-Alias -Name ai-status -Value Get-AIStatus
Set-Alias -Name ai-examples -Value Show-AIExamples
Set-Alias -Name start-ai -Value Start-AI

Write-Host "AI Tools loaded! Type 'ai-status' to check installation." -ForegroundColor Green

'@

# Check if already added
$currentContent = Get-Content $profilePath -Raw
if ($currentContent -like "*AI CODING ASSISTANTS*" -and -not $Force) {
    Write-Host "[WARN] AI Tools section already exists in profile" -ForegroundColor Yellow
    Write-Host "       Use -Force to overwrite`n" -ForegroundColor Gray
    exit 0
}

# Add to profile
Add-Content -Path $profilePath -Value $aiToolsSection -Encoding UTF8
Write-Host "[OK] AI Tools added to PowerShell profile!`n" -ForegroundColor Green

Write-Host "==============================" -ForegroundColor Gray
Write-Host "AVAILABLE COMMANDS" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Gray

Write-Host "ai-route 'task'                 - Intelligent AI selection" -ForegroundColor Yellow
Write-Host "ai-status                       - Check AI installations" -ForegroundColor Yellow
Write-Host "ai-examples                     - Show example use cases" -ForegroundColor Yellow
Write-Host "start-ai [claude|codex|gemini|all] - Quick launch AIs`n" -ForegroundColor Yellow

Write-Host "==============================" -ForegroundColor Gray
Write-Host "NEXT STEPS" -ForegroundColor Cyan
Write-Host "==============================`n" -ForegroundColor Gray

Write-Host "1. Restart PowerShell or run:" -ForegroundColor White
Write-Host "   . `$PROFILE`n" -ForegroundColor Gray

Write-Host "2. Test the routing system:" -ForegroundColor White
Write-Host "   ai-route 'Refactor my authentication code'`n" -ForegroundColor Gray

Write-Host "3. Check AI status:" -ForegroundColor White
Write-Host "   ai-status`n" -ForegroundColor Gray

Write-Host "==============================`n" -ForegroundColor Gray
Write-Host "Setup complete!`n" -ForegroundColor Green
