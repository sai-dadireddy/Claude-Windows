# Save Session State
# Saves current session context for fast resume

param(
    [string]$SessionName = "default",
    [string]$Notes = ""
)

$timestamp = Get-Date -Format 'yyyy-MM-dd_HHmmss'
$stateDir = ".claude\session-states"
$stateFile = "$stateDir\$SessionName-$timestamp.json"

# Create directory
if (-not (Test-Path $stateDir)) {
    New-Item -ItemType Directory -Path $stateDir -Force | Out-Null
}

# Capture current state
$state = @{
    timestamp = $timestamp
    sessionName = $SessionName
    workingDirectory = (Get-Location).Path
    notes = $Notes

    # Capture git state
    gitBranch = if (Test-Path .git) {
        (git rev-parse --abbrev-ref HEAD 2>$null)
    } else {
        "N/A"
    }

    gitStatus = if (Test-Path .git) {
        (git status --porcelain 2>$null)
    } else {
        "N/A"
    }

    # Recent files accessed
    recentFiles = @()

    # Context hints
    contextHints = @{
        taskType = "general"
        priority = "normal"
        needsCodingContext = $false
        needsSecurityContext = $false
        needsN8nContext = $false
    }

    # Quick resume prompt
    resumePrompt = @"
Resume previous session:
- Session: $SessionName
- Time: $timestamp
- Directory: $((Get-Location).Path)
- Notes: $Notes

Continue where we left off.
"@
}

# Save to file
$state | ConvertTo-Json -Depth 10 | Out-File -FilePath $stateFile -Encoding UTF8

Write-Host ""
Write-Host "✅ Session state saved!" -ForegroundColor Green
Write-Host "Session: $SessionName" -ForegroundColor Cyan
Write-Host "File: $stateFile" -ForegroundColor Gray
Write-Host ""
Write-Host "To resume this session:" -ForegroundColor Yellow
Write-Host "  .\tools\resume-session.ps1 -SessionName $SessionName" -ForegroundColor White
Write-Host ""
Write-Host "Or in new Claude Code session, paste:" -ForegroundColor Yellow
Write-Host "  Resume session: $SessionName" -ForegroundColor White
Write-Host ""

# Store in memory for Claude
$memoryEntry = @"
Session saved: $SessionName at $timestamp
Working directory: $((Get-Location).Path)
Notes: $Notes
"@

# Save to quick access file
$quickAccessFile = ".claude\last-session.txt"
$memoryEntry | Out-File -FilePath $quickAccessFile -Encoding UTF8

exit 0
