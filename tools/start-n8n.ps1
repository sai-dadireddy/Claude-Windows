# Start n8n with Claude Code Integration
# Version: 2.0 - Enhanced with auto-browser launch
# Created: 2025-10-11
# Updated: 2025-10-12

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " n8n + Claude Code Automation Platform" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set environment variables for Claude Code integration
$env:N8N_USER_FOLDER = "$env:USERPROFILE\.n8n"
$env:CLAUDE_PROJECT_PATH = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"

# Check if n8n is installed
Write-Host "[1/4] Checking n8n installation..." -ForegroundColor Yellow
try {
    $n8nVersion = & n8n --version 2>&1
    Write-Host "    n8n version: $n8nVersion" -ForegroundColor Green
} catch {
    Write-Host "    ERROR: n8n is not installed!" -ForegroundColor Red
    Write-Host "    Run: npm install -g n8n" -ForegroundColor Yellow
    exit 1
}

# Check if Claude Code is authenticated
Write-Host "[2/4] Checking Claude Code authentication..." -ForegroundColor Yellow
try {
    $claudeStatus = & claude auth status 2>&1
    if ($claudeStatus -match "authenticated" -or $claudeStatus -match "logged in") {
        Write-Host "    Claude Code: Authenticated" -ForegroundColor Green
    } else {
        Write-Host "    WARNING: Claude Code may not be authenticated" -ForegroundColor Yellow
        Write-Host "    Run: claude auth login" -ForegroundColor Yellow
    }
} catch {
    Write-Host "    WARNING: Could not verify Claude Code status" -ForegroundColor Yellow
}

# Check if Claude Code node is installed
Write-Host "[3/4] Checking Claude Code community node..." -ForegroundColor Yellow
$nodePackage = "$env:USERPROFILE\.n8n\nodes\node_modules\@holtweb\n8n-nodes-claudecode"
if (Test-Path $nodePackage) {
    Write-Host "    Claude Code node: Installed" -ForegroundColor Green
} else {
    Write-Host "    WARNING: Claude Code node not found" -ForegroundColor Yellow
    Write-Host "    Install it in n8n UI: Settings -> Community Nodes" -ForegroundColor Yellow
}

# Display startup information
Write-Host "[4/4] Starting n8n..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  - n8n UI:         http://localhost:5678" -ForegroundColor White
Write-Host "  - User folder:    $env:N8N_USER_FOLDER" -ForegroundColor White
Write-Host "  - Claude project: $env:CLAUDE_PROJECT_PATH" -ForegroundColor White
Write-Host ""
Write-Host "Quick Start:" -ForegroundColor Cyan
Write-Host "  1. Open http://localhost:5678 in your browser" -ForegroundColor White
Write-Host "  2. Create a new workflow" -ForegroundColor White
Write-Host "  3. Search for 'Claude Code' node" -ForegroundColor White
Write-Host "  4. Start automating!" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop n8n" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Open browser automatically after 3 seconds
Write-Host "🌐 Opening n8n in browser in 3 seconds..." -ForegroundColor Green
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:5678"
} | Out-Null

# Start n8n
n8n
