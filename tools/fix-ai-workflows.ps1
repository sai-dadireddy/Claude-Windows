# Fix ai-workflows MCP Configuration
# This script updates .claude.json to replace ai-workflows with lm-studio

$ErrorActionPreference = "Stop"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Fix ai-workflows → Replace with lm-studio" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Paths
$claudeJsonPath = "$env:USERPROFILE\.claude.json"
$backupPath = "$env:USERPROFILE\.claude.json.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Check if file exists
if (-not (Test-Path $claudeJsonPath)) {
    Write-Host "❌ ERROR: .claude.json not found at: $claudeJsonPath" -ForegroundColor Red
    Write-Host "Please ensure Claude Code is installed." -ForegroundColor Yellow
    exit 1
}

Write-Host "📄 Found .claude.json at: $claudeJsonPath" -ForegroundColor Green

# Create backup
Write-Host "📦 Creating backup..." -ForegroundColor Yellow
Copy-Item -Path $claudeJsonPath -Destination $backupPath -Force
Write-Host "✅ Backup created at: $backupPath" -ForegroundColor Green
Write-Host ""

# Read the JSON file
Write-Host "📖 Reading configuration..." -ForegroundColor Yellow
$json = Get-Content -Path $claudeJsonPath -Raw | ConvertFrom-Json

# Check if mcpServers exists
if (-not $json.mcpServers) {
    Write-Host "❌ ERROR: No mcpServers section found in .claude.json" -ForegroundColor Red
    exit 1
}

# Remove ai-workflows if it exists
if ($json.mcpServers.'ai-workflows') {
    Write-Host "🗑️  Removing old ai-workflows configuration..." -ForegroundColor Yellow
    $json.mcpServers.PSObject.Properties.Remove('ai-workflows')
    Write-Host "✅ Removed ai-workflows" -ForegroundColor Green
} else {
    Write-Host "ℹ️  ai-workflows not found (may have been removed already)" -ForegroundColor Cyan
}

# Add lm-studio configuration
Write-Host "➕ Adding lm-studio configuration..." -ForegroundColor Yellow

$lmStudioConfig = @{
    command = "node"
    args = @(
        "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/projects/mcp-servers/lm-studio-mcp/server.js"
    )
    env = @{
        LM_STUDIO_URL = "http://localhost:1234"
        MODEL_NAME = "Qwen2.5-Coder-7B-Instruct"
    }
}

# Add lm-studio to mcpServers
$json.mcpServers | Add-Member -NotePropertyName "lm-studio" -NotePropertyValue $lmStudioConfig -Force

Write-Host "✅ Added lm-studio configuration" -ForegroundColor Green
Write-Host ""

# Save the updated JSON
Write-Host "💾 Saving updated configuration..." -ForegroundColor Yellow
$json | ConvertTo-Json -Depth 100 | Set-Content -Path $claudeJsonPath -Encoding UTF8
Write-Host "✅ Configuration saved" -ForegroundColor Green
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ✅ SUCCESS - Configuration Updated!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Changes made:" -ForegroundColor Cyan
Write-Host "  ❌ Removed: ai-workflows (Ollama configuration)" -ForegroundColor Red
Write-Host "  ✅ Added: lm-studio (LM Studio configuration)" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Install LM Studio:" -ForegroundColor White
Write-Host "   - Download from: https://lmstudio.ai/" -ForegroundColor Gray
Write-Host "   - Install the application" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Download Qwen2.5-Coder model in LM Studio:" -ForegroundColor White
Write-Host "   - Open LM Studio → Search tab" -ForegroundColor Gray
Write-Host "   - Search: 'Qwen2.5-Coder'" -ForegroundColor Gray
Write-Host "   - Download 7B model (recommended for 16GB RAM)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start LM Studio server:" -ForegroundColor White
Write-Host "   - Load model in Chat tab" -ForegroundColor Gray
Write-Host "   - Go to Local Server tab" -ForegroundColor Gray
Write-Host "   - Click 'Start Server' (port 1234)" -ForegroundColor Gray
Write-Host "   - Keep LM Studio running" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Restart Claude Code:" -ForegroundColor White
Write-Host "   - Type: exit" -ForegroundColor Gray
Write-Host "   - Then: claude" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Verify installation:" -ForegroundColor White
Write-Host "   - Run: claude mcp list" -ForegroundColor Gray
Write-Host "   - Check: lm-studio should show ✓ Connected" -ForegroundColor Gray
Write-Host ""
Write-Host "Full installation guide:" -ForegroundColor Cyan
Write-Host "   C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/INSTALLATION-GUIDE-LM-STUDIO.md" -ForegroundColor Gray
Write-Host ""
Write-Host "Backup location: $backupPath" -ForegroundColor Gray
Write-Host ""
