# Fix Playwright Browser Persistence
# Version: 1.0
# Prevents browsers from reinstalling every Claude Code session

$browsersPath = "$env:USERPROFILE\.playwright-browsers"

Write-Host "Fixing Playwright Browser Persistence" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Gray
Write-Host ""

# Step 1: Set environment variable
Write-Host "[1/3] Setting PLAYWRIGHT_BROWSERS_PATH..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable(
    "PLAYWRIGHT_BROWSERS_PATH",
    $browsersPath,
    "User"
)
Write-Host "SUCCESS: Environment variable set" -ForegroundColor Green
Write-Host "         Location: $browsersPath" -ForegroundColor Gray
Write-Host ""

# Step 2: Create directory
Write-Host "[2/3] Creating browser directory..." -ForegroundColor Yellow
if (-not (Test-Path $browsersPath)) {
    New-Item -ItemType Directory -Path $browsersPath -Force | Out-Null
    Write-Host "SUCCESS: Directory created" -ForegroundColor Green
} else {
    Write-Host "INFO: Directory already exists" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Install browsers
Write-Host "[3/3] Installing Chromium browser..." -ForegroundColor Yellow
$env:PLAYWRIGHT_BROWSERS_PATH = $browsersPath
npx playwright install chromium

Write-Host ""
Write-Host "COMPLETE: Playwright browsers will now persist!" -ForegroundColor Green
Write-Host ""
Write-Host "Browser location: $browsersPath" -ForegroundColor Gray
Write-Host "Environment variable: Set at user level" -ForegroundColor Gray
Write-Host ""
Write-Host "Restart Claude Code for changes to take effect." -ForegroundColor Yellow
Write-Host ""
