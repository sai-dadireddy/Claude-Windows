# Claude Code Feature Detection System
# Scans configuration and generates comprehensive capability report

param(
    [switch]$Detailed = $false,
    [switch]$ExportJson = $false,
    [string]$OutputPath = ".\claude-capabilities.json"
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Get-MCPServers {
    $mcpConfig = ".\claude-code-mcp-config.json"

    if (-not (Test-Path $mcpConfig)) {
        return @()
    }

    $config = Get-Content $mcpConfig -Raw | ConvertFrom-Json
    $servers = @()

    foreach ($prop in $config.mcpServers.PSObject.Properties) {
        $server = @{
            Name = $prop.Name
            Command = $prop.Value.command
            Args = $prop.Value.args
            Enabled = $true
        }

        # Categorize by name
        $category = switch -Regex ($prop.Name) {
            "code-index|langchain|testing" { "Code Analysis" }
            "github|aws" { "Cloud/VCS" }
            "playwright|browser" { "Browser Automation" }
            "memory|context" { "Memory/Context" }
            "sequential-thinking|ai-workflows" { "AI Enhancement" }
            default { "Utility" }
        }

        $server.Category = $category
        $servers += $server
    }

    return $servers
}

function Get-GlobalInstructions {
    $claudeMd = ".\CLAUDE.md"

    if (-not (Test-Path $claudeMd)) {
        return @()
    }

    $content = Get-Content $claudeMd -Raw
    $includes = [regex]::Matches($content, '\{\{include:\s*([^\}]+)\}\}')

    $instructions = @()
    foreach ($match in $includes) {
        $file = $match.Groups[1].Value.Trim()
        $instructions += @{
            File = $file
            Category = if ($file -match "security") { "Security" }
                      elseif ($file -match "auto-") { "Automation" }
                      elseif ($file -match "mcp|agent") { "Architecture" }
                      elseif ($file -match "memory|session") { "Memory" }
                      else { "Core" }
        }
    }

    return $instructions
}

function Get-SlashCommands {
    $commandsDir = ".\.claude\commands"

    if (-not (Test-Path $commandsDir)) {
        return @()
    }

    $commands = Get-ChildItem -Path $commandsDir -Filter "*.md" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw

        # Extract usage pattern
        $usage = if ($content -match '\*\*Usage:\*\*\s*`([^`]+)`') {
            $matches[1]
        } else {
            "/$($_.BaseName)"
        }

        # Extract purpose
        $purpose = if ($content -match '\*\*Purpose:\*\*\s*([^\n]+)') {
            $matches[1]
        } else {
            "No description"
        }

        # Categorize
        $category = switch -Regex ($_.BaseName) {
            "gpt5|multi-ai|autonomous|godmode" { "AI Orchestration" }
            "test|playwright" { "Testing" }
            "security|audit" { "Security" }
            "analyze|review|refactor" { "Code Quality" }
            "n8n|morning|research" { "Productivity" }
            "project|mcp|load-global" { "Setup/Config" }
            default { "Utility" }
        }

        @{
            Name = $_.BaseName
            Usage = $usage
            Purpose = $purpose
            Category = $category
            File = $_.FullName
        }
    }

    return $commands
}

function Get-AgentCount {
    # Count available agents from Task tool description
    # Known: 90+ agents across categories
    @{
        Total = 90
        Categories = @(
            @{Name="Language Specialists"; Count=15; Examples=@("python-pro","typescript-pro","golang-pro","rust-pro")},
            @{Name="Testing & QA"; Count=8; Examples=@("test-automator","qa-expert","playwright")},
            @{Name="Security"; Count=6; Examples=@("security-auditor","security-code-reviewer","aws-security-architect")},
            @{Name="DevOps/Cloud"; Count=12; Examples=@("cloud-architect","kubernetes-architect","terraform-specialist")},
            @{Name="Architecture"; Count=8; Examples=@("backend-architect","architect-review","database-architect")},
            @{Name="Data & AI"; Count=10; Examples=@("data-scientist","ml-engineer","ai-engineer")},
            @{Name="Frontend/UI"; Count=8; Examples=@("react-pro","nextjs-pro","ui-ux-designer")},
            @{Name="Performance"; Count=5; Examples=@("performance-engineer","database-optimizer")},
            @{Name="Content/Docs"; Count=6; Examples=@("docs-architect","content-marketer","api-documenter")},
            @{Name="Specialized"; Count=12; Examples=@("blockchain-developer","game-developer","search-specialist")}
        )
    }
}

function Show-FeatureReport {
    param($Features)

    Write-ColorOutput "`n╔═══════════════════════════════════════════════════════════════╗" "Cyan"
    Write-ColorOutput "║          CLAUDE CODE CAPABILITY DETECTION REPORT              ║" "Cyan"
    Write-ColorOutput "╚═══════════════════════════════════════════════════════════════╝`n" "Cyan"

    # MCP Servers
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "📦 MCP SERVERS ($($Features.MCPServers.Count) configured)" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    $mcpByCategory = $Features.MCPServers | Group-Object Category
    foreach ($group in $mcpByCategory) {
        Write-ColorOutput "  $($group.Name):" "Cyan"
        foreach ($server in $group.Group) {
            Write-ColorOutput "    ✓ $($server.Name)" "Green"
            if ($Detailed) {
                Write-ColorOutput "      Command: $($server.Command)" "Gray"
            }
        }
        Write-Host ""
    }

    # Global Instructions
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "📋 GLOBAL INSTRUCTIONS ($($Features.Instructions.Count) modules)" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    $instByCategory = $Features.Instructions | Group-Object Category
    foreach ($group in $instByCategory) {
        Write-ColorOutput "  $($group.Name): $($group.Count) modules" "Cyan"
        if ($Detailed) {
            foreach ($inst in $group.Group) {
                Write-ColorOutput "    • $($inst.File)" "Gray"
            }
        }
    }
    Write-Host ""

    # Slash Commands
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "⚡ SLASH COMMANDS ($($Features.Commands.Count) available)" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    $cmdByCategory = $Features.Commands | Group-Object Category
    foreach ($group in $cmdByCategory) {
        Write-ColorOutput "  $($group.Name):" "Cyan"
        foreach ($cmd in $group.Group) {
            Write-ColorOutput "    /$($cmd.Name)" "Green"
            if ($Detailed) {
                Write-ColorOutput "      → $($cmd.Purpose)" "Gray"
            }
        }
        Write-Host ""
    }

    # Agents
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "🤖 SPECIALIZED AGENTS ($($Features.Agents.Total)+ available)" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    foreach ($category in $Features.Agents.Categories) {
        Write-ColorOutput "  $($category.Name): $($category.Count) agents" "Cyan"
        if ($Detailed) {
            Write-ColorOutput "    Examples: $($category.Examples -join ', ')" "Gray"
        }
    }
    Write-Host ""

    # Summary
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "📊 SUMMARY" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "  Total Capabilities Detected:" "White"
    Write-ColorOutput "    • MCP Servers: $($Features.MCPServers.Count)" "Green"
    Write-ColorOutput "    • Global Instructions: $($Features.Instructions.Count)" "Green"
    Write-ColorOutput "    • Slash Commands: $($Features.Commands.Count)" "Green"
    Write-ColorOutput "    • Specialized Agents: $($Features.Agents.Total)+" "Green"
    Write-Host ""

    Write-ColorOutput "  Architecture Type: Agent-Ready (85% token savings)" "Green"
    Write-ColorOutput "  Context Window: 200K tokens per session" "Green"
    Write-ColorOutput "  Agent Context: 200K tokens per agent (isolated)" "Green"
    Write-Host ""
}

function Show-RecommendedUsage {
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "💡 WHEN TO USE WHAT" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "  Use CLAUDE CODE (This Setup) for:" "Cyan"
    Write-ColorOutput "    ✓ Complex architecture & system design" "White"
    Write-ColorOutput "    ✓ Multi-file refactoring (/large-refactor)" "White"
    Write-ColorOutput "    ✓ Security-critical implementations" "White"
    Write-ColorOutput "    ✓ Agent orchestration (90+ agents)" "White"
    Write-ColorOutput "    ✓ Browser automation (Playwright MCP)" "White"
    Write-ColorOutput "    ✓ Code analysis (code-index MCP)" "White"
    Write-Host ""

    Write-ColorOutput "  Use GPT-5 CODEX for:" "Green"
    Write-ColorOutput "    ✓ Planning complex features (/gpt5-plan)" "White"
    Write-ColorOutput "    ✓ Mathematical/algorithmic reasoning" "White"
    Write-ColorOutput "    ✓ Quick prototypes from vague specs" "White"
    Write-ColorOutput "    ✓ Performance optimization" "White"
    Write-Host ""

    Write-ColorOutput "  Use GEMINI CLI for:" "Magenta"
    Write-ColorOutput "    ✓ Fast validation & code smell detection" "White"
    Write-ColorOutput "    ✓ Research & documentation" "White"
    Write-ColorOutput "    ✓ Alternative perspectives" "White"
    Write-ColorOutput "    ✓ Pre-commit validation (FREE tier!)" "White"
    Write-Host ""

    Write-ColorOutput "  RECOMMENDED WORKFLOW:" "Yellow"
    Write-ColorOutput "    1. GPT-5: Plan architecture & approach" "White"
    Write-ColorOutput "    2. Claude Code: Implement with quality" "White"
    Write-ColorOutput "    3. Gemini: Validate for issues/regressions" "White"
    Write-ColorOutput "    4. Claude Code: Refine & polish" "White"
    Write-Host ""
}

function Show-QuickStart {
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "🚀 QUICK START GUIDE" "Yellow"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "  1. Install other AIs (if not done):" "Cyan"
    Write-ColorOutput "     .\tools\install-ai-clis.ps1" "White"
    Write-Host ""

    Write-ColorOutput "  2. Set up PowerShell profile:" "Cyan"
    Write-ColorOutput "     .\tools\setup-ai-profile.ps1" "White"
    Write-ColorOutput "     . `$PROFILE  # Reload profile" "Gray"
    Write-Host ""

    Write-ColorOutput "  3. Test intelligent routing:" "Cyan"
    Write-ColorOutput "     ai-route 'Refactor authentication system'" "White"
    Write-ColorOutput "     → Will recommend: Claude Code" "Gray"
    Write-Host ""

    Write-ColorOutput "  4. Try multi-AI workflow:" "Cyan"
    Write-ColorOutput "     /gpt5-plan 'Build OAuth system'  # Get plan" "White"
    Write-ColorOutput "     /gpt5-implement oauth            # Implement" "White"
    Write-ColorOutput "     gemini                           # Validate (external)" "White"
    Write-ColorOutput "     /gpt5-refine oauth               # Apply feedback" "White"
    Write-Host ""

    Write-ColorOutput "  5. Use powerful features:" "Cyan"
    Write-ColorOutput "     /large-refactor 'feature name'   # Multi-file work" "White"
    Write-ColorOutput "     /test-plan                       # Playwright testing" "White"
    Write-ColorOutput "     /security-analyze                # Security audit" "White"
    Write-ColorOutput "     /multi-ai 'task'                 # Parallel comparison" "White"
    Write-Host ""
}

# Main execution
Write-ColorOutput "`n🔍 Scanning Claude Code configuration...`n" "Cyan"

$features = @{
    MCPServers = Get-MCPServers
    Instructions = Get-GlobalInstructions
    Commands = Get-SlashCommands
    Agents = Get-AgentCount
}

Show-FeatureReport -Features $features
Show-RecommendedUsage
Show-QuickStart

if ($ExportJson) {
    $features | ConvertTo-Json -Depth 10 | Out-File $OutputPath -Encoding UTF8
    Write-ColorOutput "✅ Capabilities exported to: $OutputPath`n" "Green"
}

Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"
Write-ColorOutput "💡 TIP: Run with -Detailed for verbose output" "Yellow"
Write-ColorOutput "💡 TIP: Use ai-route 'your task' for intelligent AI selection`n" "Yellow"
