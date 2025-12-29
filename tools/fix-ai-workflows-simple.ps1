# Fix ai-workflows MCP Configuration - Simple Version
$ErrorActionPreference = "Stop"

Write-Host "Fixing ai-workflows configuration..." -ForegroundColor Cyan

# Paths
$claudeJsonPath = "$env:USERPROFILE\.claude.json"
$backupPath = "$env:USERPROFILE\.claude.json.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Check if file exists
if (-not (Test-Path $claudeJsonPath)) {
    Write-Host "ERROR: .claude.json not found at: $claudeJsonPath" -ForegroundColor Red
    exit 1
}

# Create backup
Write-Host "Creating backup..." -ForegroundColor Yellow
Copy-Item -Path $claudeJsonPath -Destination $backupPath -Force
Write-Host "Backup created at: $backupPath" -ForegroundColor Green

# Read the JSON file
Write-Host "Reading configuration..." -ForegroundColor Yellow
$json = Get-Content -Path $claudeJsonPath -Raw | ConvertFrom-Json

# Check if mcpServers exists
if (-not $json.mcpServers) {
    Write-Host "ERROR: No mcpServers section found" -ForegroundColor Red
    exit 1
}

# Remove ai-workflows if it exists
if ($json.mcpServers.'ai-workflows') {
    Write-Host "Removing old ai-workflows..." -ForegroundColor Yellow
    $json.mcpServers.PSObject.Properties.Remove('ai-workflows')
    Write-Host "Removed ai-workflows" -ForegroundColor Green
}

# Add lm-studio configuration
Write-Host "Adding lm-studio configuration..." -ForegroundColor Yellow

$lmStudioConfig = @{
    command = "node"
    args = @("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/projects/mcp-servers/lm-studio-mcp/server.js")
    env = @{
        LM_STUDIO_URL = "http://localhost:1234"
        MODEL_NAME = "Qwen2.5-Coder-7B-Instruct"
    }
}

$json.mcpServers | Add-Member -NotePropertyName "lm-studio" -NotePropertyValue $lmStudioConfig -Force

Write-Host "Added lm-studio configuration" -ForegroundColor Green

# Save the updated JSON
Write-Host "Saving configuration..." -ForegroundColor Yellow
$json | ConvertTo-Json -Depth 100 | Set-Content -Path $claudeJsonPath -Encoding UTF8
Write-Host "Configuration saved" -ForegroundColor Green

Write-Host ""
Write-Host "SUCCESS - Configuration Updated!" -ForegroundColor Green
Write-Host ""
Write-Host "Changes made:" -ForegroundColor Cyan
Write-Host "  - Removed: ai-workflows (Ollama)" -ForegroundColor Yellow
Write-Host "  - Added: lm-studio (LM Studio)" -ForegroundColor Yellow
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Install LM Studio from https://lmstudio.ai/" -ForegroundColor White
Write-Host "2. Download Qwen2.5-Coder model in LM Studio" -ForegroundColor White
Write-Host "3. Start LM Studio server (port 1234)" -ForegroundColor White
Write-Host "4. Restart Claude Code (exit then claude)" -ForegroundColor White
Write-Host "5. Verify: claude mcp list" -ForegroundColor White
Write-Host ""
Write-Host "Full guide: INSTALLATION-GUIDE-LM-STUDIO.md" -ForegroundColor Cyan
Write-Host "Backup: $backupPath" -ForegroundColor Gray
