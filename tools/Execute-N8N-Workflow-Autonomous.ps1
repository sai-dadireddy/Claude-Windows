# Autonomous n8n Workflow Executor
# Uses Windows UI Automation to click Execute button
# Version: 1.0

param(
    [string]$WorkflowUrl = "http://localhost:5678/workflow/ogFmtEo7KXE8mhZ5"
)

Write-Host "🤖 Autonomous Workflow Executor" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Gray
Write-Host ""

# Step 1: Open workflow in browser
Write-Host "[1/3] Opening workflow in browser..." -ForegroundColor Yellow
Start-Process $WorkflowUrl
Start-Sleep -Seconds 3

Write-Host "SUCCESS: Browser opened" -ForegroundColor Green
Write-Host ""

# Step 2: Use SendKeys to execute workflow
Write-Host "[2/3] Sending keyboard command to execute workflow..." -ForegroundColor Yellow
Write-Host "       Using Ctrl+Enter shortcut..." -ForegroundColor Gray

# Add .NET assembly for SendKeys
Add-Type -AssemblyName System.Windows.Forms

# Wait for page to load
Start-Sleep -Seconds 2

# Send Ctrl+Enter (n8n shortcut for Execute Workflow)
[System.Windows.Forms.SendKeys]::SendWait("^{ENTER}")

Write-Host "SUCCESS: Execute command sent" -ForegroundColor Green
Write-Host ""

# Step 3: Monitor execution
Write-Host "[3/3] Workflow executing..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Expected duration: 5-10 minutes" -ForegroundColor Gray
Write-Host "  - RSS feeds: ~30 seconds" -ForegroundColor Gray
Write-Host "  - Ollama scoring: ~18 seconds per article" -ForegroundColor Gray
Write-Host "  - For 30 articles: ~9 minutes" -ForegroundColor Gray
Write-Host ""
Write-Host "Monitor progress in browser window!" -ForegroundColor Yellow
Write-Host ""
Write-Host "When complete:" -ForegroundColor Cyan
Write-Host "  1. All nodes will show green checkmarks" -ForegroundColor Gray
Write-Host "  2. Final node shows article count" -ForegroundColor Gray
Write-Host "  3. Type '/ai-news' in Claude Code to view dashboard" -ForegroundColor Gray
Write-Host ""
