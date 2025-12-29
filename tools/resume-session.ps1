# Resume Session State
# Loads a saved session for quick resume

param(
    [string]$SessionName = ""
)

$stateDir = ".claude\session-states"

# If no session name provided, load the most recent session
if ([string]::IsNullOrEmpty($SessionName)) {
    Write-Host "📂 No session name provided - loading most recent session..." -ForegroundColor Cyan
    $stateFiles = Get-ChildItem -Path $stateDir -Filter "*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

    if (-not $stateFiles) {
        Write-Host "❌ No saved sessions found" -ForegroundColor Red
        Write-Host ""
        Write-Host "💡 Save a session first using:" -ForegroundColor Yellow
        Write-Host "   /save-session [name] 'notes'" -ForegroundColor White
        exit 1
    }

    $latestState = $stateFiles[0]
} else {
    # Find latest session state for specific name
    $stateFiles = Get-ChildItem -Path $stateDir -Filter "$SessionName-*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

    if (-not $stateFiles) {
        Write-Host "❌ No saved session found for: $SessionName" -ForegroundColor Red
        Write-Host ""
        Write-Host "Available sessions:" -ForegroundColor Yellow
        Get-ChildItem -Path $stateDir -Filter "*.json" -ErrorAction SilentlyContinue | ForEach-Object {
            $name = $_.Name -replace '-\d{4}-\d{2}-\d{2}_\d{6}\.json$', ''
            Write-Host "  - $name" -ForegroundColor White
        }
        exit 1
    }

    $latestState = $stateFiles[0]
}

$state = Get-Content $latestState.FullName | ConvertFrom-Json

Write-Host ""
Write-Host "📂 Loading session state..." -ForegroundColor Cyan
Write-Host "Session: $($state.sessionName)" -ForegroundColor White
Write-Host "Saved: $($state.timestamp)" -ForegroundColor Gray
Write-Host "Directory: $($state.workingDirectory)" -ForegroundColor Gray
Write-Host "Notes: $($state.notes)" -ForegroundColor Gray
Write-Host ""

# Change to working directory
if ($state.workingDirectory -and (Test-Path $state.workingDirectory)) {
    Set-Location $state.workingDirectory
    Write-Host "✅ Changed to: $($state.workingDirectory)" -ForegroundColor Green
}

# Show git status if available
if ($state.gitBranch -and $state.gitBranch -ne "N/A") {
    Write-Host "📌 Git branch: $($state.gitBranch)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🚀 Session context restored!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick resume prompt (copy/paste into Claude Code):" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host $state.resumePrompt -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

# Copy to clipboard if available
try {
    $state.resumePrompt | Set-Clipboard
    Write-Host "✅ Resume prompt copied to clipboard!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not copy to clipboard" -ForegroundColor Yellow
}

exit 0
