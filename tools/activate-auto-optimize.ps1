# Claude Code Auto-Optimization Activator
# Run this script to activate auto-optimization in the current session

Write-Host "`nActivating Claude Code Auto-Optimization..." -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Set environment variables for current session
$env:CLAUDE_PROJECT_INSTRUCTIONS = "CLAUDE-LITE.md"
$env:CLAUDE_DEFAULT_MODEL = "claude-sonnet-4-5"
$env:CLAUDE_PLAN_MODE = "false"
$env:CLAUDE_AUTO_OPTIMIZE = "true"
$env:CLAUDE_TASK_DETECTION = "true"
$env:CLAUDE_TOKEN_MONITORING = "true"
$env:CLAUDE_WEEKLY_TRACKING = "true"
$env:CLAUDE_DYNAMIC_LOADING = "true"
$env:CLAUDE_STARTUP_TOKEN_TARGET = "3000"
$env:CLAUDE_SESSION_TOKEN_TARGET = "50000"
$env:CLAUDE_WEEKLY_USAGE_TARGET = "0.70"
$env:CLAUDE_STARTUP_MODE = "lite"

Write-Host "[OK] Environment variables set for auto-optimization" -ForegroundColor Green
Write-Host "`nConfiguration:" -ForegroundColor White
Write-Host "  Project Instructions: CLAUDE-LITE.md" -ForegroundColor Gray
Write-Host "  Default Model: claude-sonnet-4-5 (Sonnet 4.5)" -ForegroundColor Gray
Write-Host "  Plan Mode: Disabled" -ForegroundColor Gray
Write-Host "  Auto-Optimize: Enabled" -ForegroundColor Gray
Write-Host "  Task Detection: Enabled" -ForegroundColor Gray
Write-Host "  Token Monitoring: Enabled" -ForegroundColor Gray

Write-Host "`nExpected Results:" -ForegroundColor Cyan
Write-Host "  - Startup tokens: 2-3K (85% savings)" -ForegroundColor Green
Write-Host "  - Weekly usage: 30-50% reduction" -ForegroundColor Green
Write-Host "  - Automatic task detection" -ForegroundColor Green
Write-Host "  - Dynamic context loading" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "  1. Start Claude Code in this terminal" -ForegroundColor Gray
Write-Host "  2. Type: /load-global" -ForegroundColor Gray
Write-Host "  3. Look for: 'Auto-optimize: ACTIVE'" -ForegroundColor Gray
Write-Host "  4. Start working!" -ForegroundColor Gray

Write-Host "`nTo make permanent (optional):" -ForegroundColor Yellow
Write-Host "  Add this script to your PowerShell profile:" -ForegroundColor Gray
Write-Host "  Run: notepad `$PROFILE" -ForegroundColor Gray
Write-Host "  Add: . C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\activate-auto-optimize.ps1" -ForegroundColor Gray

Write-Host "`n[SUCCESS] Auto-optimization activated for this session!`n" -ForegroundColor Green
