# Load Memory Context - Quick Memory Loader for Active Sessions
# Use this to manually reload memory during a session

param(
    [string]$ProjectName = $env:PROJECT_NAME,
    [switch]$ShowDetails = $false
)

if (-not $ProjectName) {
    Write-Host "Error: ProjectName not specified and PROJECT_NAME environment variable not set" -ForegroundColor Red
    Write-Host "Usage: .\load-memory-context.ps1 -ProjectName active-genie-nginx" -ForegroundColor Yellow
    exit 1
}

$REPO_ROOT = Split-Path -Parent $PSScriptRoot
if (-not $REPO_ROOT) {
    $REPO_ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$INDEXER = Join-Path $REPO_ROOT "tools\auto-memory-indexer.py"

Write-Host ""
Write-Host "Loading memory context for $ProjectName..." -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $INDEXER)) {
    Write-Host "Warning: auto-memory-indexer.py not found at $INDEXER" -ForegroundColor Yellow
    return
}

# Run stats command
$output = python $INDEXER --project $ProjectName --stats 2>&1

Write-Host $output
Write-Host ""

if ($ShowDetails) {
    Write-Host "Getting detailed memory entries..." -ForegroundColor Yellow
    Write-Host ""

    $MEMORY_DB = Join-Path $REPO_ROOT "projects\$ProjectName\memory.db"

    if (Test-Path $MEMORY_DB) {
        # Show recent decisions
        Write-Host "Recent Decisions:" -ForegroundColor Cyan
        sqlite3 $MEMORY_DB "SELECT entity_name, content FROM project_memory WHERE entity_type = 'decision' ORDER BY created_at DESC LIMIT 5;"
        Write-Host ""

        # Show recent API endpoints
        Write-Host "API Endpoints:" -ForegroundColor Cyan
        sqlite3 $MEMORY_DB "SELECT entity_name, content FROM project_memory WHERE entity_type = 'api-endpoint' LIMIT 5;"
        Write-Host ""

        # Show recent issues
        Write-Host "Recent Issues Solved:" -ForegroundColor Cyan
        sqlite3 $MEMORY_DB "SELECT entity_name, content FROM project_memory WHERE entity_type = 'issue-solved' ORDER BY created_at DESC LIMIT 3;"
        Write-Host ""
    }
}

Write-Host "Memory context loaded successfully!" -ForegroundColor Green
Write-Host ""
