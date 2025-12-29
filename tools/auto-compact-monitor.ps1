# Auto-Compact Monitor (Enhanced with CLI Flags)
# Checks token usage and suggests/runs compact automatically using headless mode

param(
    [int]$CurrentTokens = 0,
    [int]$MaxTokens = 200000,
    [switch]$AutoRun = $false,
    [switch]$UseHeadless = $false,
    [switch]$Verbose = $false
)

$usagePercent = ($CurrentTokens / $MaxTokens) * 100

Write-Host "Token Usage: $CurrentTokens / $MaxTokens ($([math]::Round($usagePercent, 1))%)"

# Function to run compact via headless mode
function Invoke-Compact {
    param([string]$Level)

    if ($UseHeadless) {
        Write-Host "[HEADLESS] Running /compact via headless mode..." -ForegroundColor Cyan

        $flags = @()
        if (-not $Verbose) { $flags += "--quiet" }
        $flags += "--skip-permissions"

        & claude @flags -p "/compact"
    } else {
        Write-Host "💡 Run: /compact (or use -UseHeadless flag for automation)" -ForegroundColor Yellow
    }
}

# Threshold checks
if ($CurrentTokens -ge 50000 -and $CurrentTokens -lt 80000) {
    if ($AutoRun) {
        Write-Host "[AUTO-COMPACT] Threshold 50K reached - compacting..." -ForegroundColor Yellow
        Invoke-Compact -Level "moderate"
        exit 1  # Signal to Claude Code to run /compact
    } else {
        Write-Host "💡 Recommendation: Run /compact (50K threshold)" -ForegroundColor Yellow
    }
}
elseif ($CurrentTokens -ge 80000 -and $CurrentTokens -lt 120000) {
    if ($AutoRun) {
        Write-Host "[AUTO-COMPACT] Threshold 80K reached - force compacting..." -ForegroundColor Yellow
        exit 1  # Signal to Claude Code to run /compact
    } else {
        Write-Host "⚠️  Recommendation: Run /compact now (80K threshold)" -ForegroundColor Red
    }
}
elseif ($CurrentTokens -ge 120000 -and $CurrentTokens -lt 150000) {
    if ($AutoRun) {
        Write-Host "[AUTO-COMPACT] Threshold 120K reached - aggressive compact..." -ForegroundColor Red
        exit 1  # Signal to Claude Code to run /compact
    } else {
        Write-Host "🔴 Strong recommendation: Run /compact immediately (120K threshold)" -ForegroundColor Red
    }
}
elseif ($CurrentTokens -ge 150000 -and $CurrentTokens -lt 180000) {
    Write-Host "💡 Session at 150K tokens. Recommend /clear for fresh session?" -ForegroundColor Yellow
    exit 2  # Signal to suggest /clear
}
elseif ($CurrentTokens -ge 180000) {
    Write-Host "⚠️  Session at $CurrentTokens tokens ($(([math]::Round($usagePercent, 0)))% of limit). Strongly recommend /clear." -ForegroundColor Red
    exit 2  # Signal to strongly suggest /clear
}
else {
    Write-Host "✅ Token usage optimal" -ForegroundColor Green
    exit 0  # All good
}
