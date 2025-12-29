# Test Web Access Orchestration
# Validates that Playwright is properly configured and orchestration rules are loaded

Write-Host "🧪 Testing Web Access Orchestration..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Check Playwright browsers installed
Write-Host "Test 1: Checking Playwright browser installation..." -ForegroundColor Yellow
$playwrightDir = "$env:USERPROFILE\.playwright-browsers"
if (Test-Path $playwrightDir) {
    $browsers = Get-ChildItem $playwrightDir -Directory
    Write-Host "  ✅ Found $($browsers.Count) browser installations:" -ForegroundColor Green
    foreach ($browser in $browsers) {
        Write-Host "     - $($browser.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ❌ Playwright browsers directory not found!" -ForegroundColor Red
    Write-Host "     Expected: $playwrightDir" -ForegroundColor Gray
}
Write-Host ""

# Test 2: Check orchestration file exists
Write-Host "Test 2: Checking orchestration file..." -ForegroundColor Yellow
$orchestrationFile = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\global-instructions\auto-web-fetch-orchestration.md"
if (Test-Path $orchestrationFile) {
    Write-Host "  ✅ Orchestration file exists" -ForegroundColor Green
    $fileSize = (Get-Item $orchestrationFile).Length
    Write-Host "     Size: $([math]::Round($fileSize/1KB, 2)) KB" -ForegroundColor Gray
} else {
    Write-Host "  ❌ Orchestration file not found!" -ForegroundColor Red
}
Write-Host ""

# Test 3: Check CLAUDE.md includes orchestration
Write-Host "Test 3: Checking CLAUDE.md includes orchestration..." -ForegroundColor Yellow
$claudeMd = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\CLAUDE.md"
if (Test-Path $claudeMd) {
    $content = Get-Content $claudeMd -Raw
    if ($content -match "auto-web-fetch-orchestration\.md") {
        Write-Host "  ✅ CLAUDE.md includes orchestration file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ CLAUDE.md does NOT include orchestration file!" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ CLAUDE.md not found!" -ForegroundColor Red
}
Write-Host ""

# Test 4: Check MCP config
Write-Host "Test 4: Checking Playwright MCP configuration..." -ForegroundColor Yellow
$mcpConfig = "$env:APPDATA\Claude\claude-code-mcp-config.json"
if (Test-Path $mcpConfig) {
    $config = Get-Content $mcpConfig -Raw | ConvertFrom-Json
    if ($config.mcpServers.playwright) {
        Write-Host "  ✅ Playwright MCP server configured" -ForegroundColor Green
        Write-Host "     Command: $($config.mcpServers.playwright.command)" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ Playwright MCP server NOT configured!" -ForegroundColor Red
    }
} else {
    Write-Host "  ❌ MCP config file not found!" -ForegroundColor Red
}
Write-Host ""

# Test 5: Check guide files
Write-Host "Test 5: Checking guide documentation..." -ForegroundColor Yellow
$guideFiles = @(
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\docs\guides\HOW-TO-FIX-WEB-ACCESS.md",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\global-instructions\auto-playwright-web-access.md"
)
foreach ($guide in $guideFiles) {
    if (Test-Path $guide) {
        Write-Host "  ✅ $(Split-Path $guide -Leaf)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $(Split-Path $guide -Leaf) missing!" -ForegroundColor Red
    }
}
Write-Host ""

# Summary
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "  If all tests passed, web access orchestration is properly configured!" -ForegroundColor White
Write-Host "  Claude Code will automatically use WebSearch → Playwright → WebFetch" -ForegroundColor White
Write-Host ""
Write-Host "  To verify in next session, ask Claude:" -ForegroundColor Yellow
Write-Host "    Check if Playwright is installed and show me the orchestration pattern" -ForegroundColor Gray
Write-Host ""
