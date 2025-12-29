# One-time setup for Playwright MCP
# Run this script once to install browsers for the MCP server

Write-Host "Installing Playwright MCP globally..." -ForegroundColor Cyan
npm install -g @playwright/mcp

Write-Host "`nInstalling Playwright browsers..." -ForegroundColor Cyan
npx playwright install chromium

Write-Host "`nVerifying installation..." -ForegroundColor Cyan
npx playwright --version

Write-Host "`nBrowsers installed:" -ForegroundColor Green
Get-ChildItem "$env:LOCALAPPDATA\ms-playwright" | Select-Object Name

Write-Host "`nSetup complete! Restart Claude Code for changes to take effect." -ForegroundColor Green
