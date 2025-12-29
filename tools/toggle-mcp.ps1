# Quick MCP Profile Switcher
# Usage: .\toggle-mcp.ps1 <profile-name>
# Profiles: minimal, coding, web, github, aws, full

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('minimal', 'coding', 'web', 'github', 'aws', 'full')]
    [string]$Profile
)

$configDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
$currentConfig = "$configDir\claude-code-mcp-config.json"
$backupConfig = "$configDir\claude-code-mcp-config.json.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Backup current config
Copy-Item $currentConfig $backupConfig
Write-Host "✓ Backed up current config to: $backupConfig" -ForegroundColor Green

# Define MCP profiles
$profiles = @{
    'minimal' = @('memory-auto', 'code-index-mcp')
    'coding' = @('memory-auto', 'code-index-mcp', 'testing', 'ai-workflows')
    'web' = @('memory-auto', 'code-index-mcp', 'playwright')
    'github' = @('memory-auto', 'code-index-mcp', 'github')
    'aws' = @('memory-auto', 'code-index-mcp', 'aws')
    'full' = @('memory-auto', 'code-index-mcp', 'testing', 'ai-workflows', 'playwright', 'github', 'aws', 'langchain', 'sequential-thinking')
}

$enabledMCPs = $profiles[$Profile]

Write-Host "`n🔄 Switching to profile: $Profile" -ForegroundColor Cyan
Write-Host "Enabled MCPs: $($enabledMCPs -join ', ')" -ForegroundColor Yellow

# Read the lite template (has all MCPs documented)
$templatePath = "$configDir\claude-code-mcp-config-optimized-lite.json"
if (-not (Test-Path $templatePath)) {
    Write-Error "Template not found: $templatePath"
    exit 1
}

$config = Get-Content $templatePath -Raw | ConvertFrom-Json

# Create new config with selected MCPs
$newConfig = @{
    "_comment" = "MCP Profile: $Profile"
    "_profile" = $Profile
    "_enabled_mcps" = $enabledMCPs
    "mcpServers" = @{}
    "_disabled_mcps" = @{}
}

# Move selected MCPs to active section
foreach ($mcpName in $enabledMCPs) {
    if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
        $newConfig.mcpServers[$mcpName] = $config.mcpServers.$mcpName
    }
    elseif ($config._disabled_mcps.PSObject.Properties.Name -contains $mcpName) {
        $newConfig.mcpServers[$mcpName] = $config._disabled_mcps.$mcpName
    }
}

# Move all other MCPs to disabled section
$allMCPNames = @($config.mcpServers.PSObject.Properties.Name) + @($config._disabled_mcps.PSObject.Properties.Name | Where-Object { $_ -notlike '_*' })
foreach ($mcpName in $allMCPNames) {
    if ($enabledMCPs -notcontains $mcpName) {
        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $newConfig._disabled_mcps[$mcpName] = $config.mcpServers.$mcpName
        }
        elseif ($config._disabled_mcps.PSObject.Properties.Name -contains $mcpName) {
            $newConfig._disabled_mcps[$mcpName] = $config._disabled_mcps.$mcpName
        }
    }
}

# Copy metadata from template
if ($config._disabled_mcps.PSObject.Properties.Name -contains '_comment') {
    $newConfig._disabled_mcps['_comment'] = $config._disabled_mcps._comment
}

# Save new config
$newConfig | ConvertTo-Json -Depth 10 | Set-Content $currentConfig

Write-Host "`n✅ Config updated successfully!" -ForegroundColor Green
Write-Host "`n⚠️  IMPORTANT: You must restart Claude Code for changes to take effect!" -ForegroundColor Yellow

# Show token estimate
$tokenEstimates = @{
    'minimal' = '3-5K'
    'coding' = '10-12K'
    'web' = '23-25K'
    'github' = '21-23K'
    'aws' = '7-9K'
    'full' = '80-90K'
}

Write-Host "`n📊 Estimated token usage: $($tokenEstimates[$Profile]) tokens" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
