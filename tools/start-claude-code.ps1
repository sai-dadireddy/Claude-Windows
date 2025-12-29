# Claude Code Enhanced Startup System
# Initializes all systems before starting Claude Code

param(
    [string]$ProjectName = "",
    [string]$ProjectPath = "",
    [switch]$SkipMemoryLoad = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

# ═══════════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════════

$SCRIPT_VERSION = "1.0.0"
$BASE_DIR = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude"
$ROOT_MCP = "C:\Users\SainathreddyDadiredd\.mcp.json"

# ═══════════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

function Write-Step {
    param([string]$Message, [string]$Color = "Yellow")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "  [+] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "  [!] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "  [X] $Message" -ForegroundColor Red
}

function Write-Info {
    param([string]$Message)
    Write-Host "  [>] $Message" -ForegroundColor Cyan
}

# ═══════════════════════════════════════════════════════════════════════════════
# Banner
# ═══════════════════════════════════════════════════════════════════════════════

Clear-Host
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Claude Code Enhanced Startup System v$SCRIPT_VERSION" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
if ($ProjectName) {
    Write-Info "Project: $ProjectName"
} else {
    Write-Info "Mode: Global (no specific project)"
}
Write-Info "Starting comprehensive system initialization..."
Write-Host ""

# ═══════════════════════════════════════════════════════════════════════════════
# Step 1: Validate Prerequisites
# ═══════════════════════════════════════════════════════════════════════════════

Write-Step "[1/7] Validating Prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python installed: $pythonVersion"
} catch {
    Write-Error "Python not found! Please install Python 3.8+"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Success "Node.js installed: $nodeVersion"
} catch {
    Write-Error "Node.js not found! Please install Node.js 18+"
    exit 1
}

# Check npm
try {
    $npmVersion = npm --version 2>&1
    Write-Success "npm installed: v$npmVersion"
} catch {
    Write-Error "npm not found!"
    exit 1
}

# ═══════════════════════════════════════════════════════════════════════════════
# Step 2: Check MCP Configuration
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[2/7] Checking MCP Configuration..."

$PROJECT_DIR = "$BASE_DIR\projects\$ProjectName"
$PROJECT_MCP = "$PROJECT_DIR\.mcp.json"

# Check Root MCP
if (Test-Path $ROOT_MCP) {
    $rootConfig = Get-Content $ROOT_MCP | ConvertFrom-Json
    $rootServers = $rootConfig.mcpServers.PSObject.Properties.Name
    Write-Success "Root MCP config found ($($rootServers.Count) servers)"

    if ($Verbose) {
        $serverList = $rootServers -join ", "
        Write-Info "Root MCP Servers: $serverList"
    }

    # Verify essential servers
    $essentialServers = @("playwright", "puppeteer", "context7", "sequential-thinking", "memory_short", "memory_long")
    $missing = $essentialServers | Where-Object { $_ -notin $rootServers }

    if ($missing.Count -gt 0) {
        $missingList = $missing -join ", "
        Write-Warning "Missing servers: $missingList"
    } else {
        Write-Success "All essential MCP servers configured"
    }
} else {
    Write-Error "Root MCP config missing at $ROOT_MCP"
}

# Check Project MCP (only if project specified)
if ($ProjectName) {
    if (Test-Path $PROJECT_MCP) {
        $projectConfig = Get-Content $PROJECT_MCP | ConvertFrom-Json
        $projectServers = $projectConfig.mcpServers.PSObject.Properties.Name
        Write-Success "Project MCP config found ($($projectServers.Count) servers)"

        if ($Verbose) {
            $projectServerList = $projectServers -join ", "
            Write-Info "Project MCP Servers: $projectServerList"
        }
    } else {
        Write-Info "No project-specific MCP config (using root only)"
    }
} else {
    Write-Info "No project specified - using root MCP only"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Step 3: Initialize Memory System
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[3/7] Initializing Memory System..."

$MEMORY_DB = "$PROJECT_DIR\memory.db"
$INDEXER_SCRIPT = "$BASE_DIR\tools\auto-memory-indexer.py"

# Check if indexer exists and project name is provided
if ($ProjectName -and (-not (Test-Path $INDEXER_SCRIPT))) {
    Write-Error "Auto-memory-indexer.py not found!"
} elseif ($ProjectName) {
    # Initialize or check memory.db (only for specific projects)
    if (Test-Path $MEMORY_DB) {
        if (-not $SkipMemoryLoad) {
            try {
                $statsOutput = python $INDEXER_SCRIPT --project $ProjectName --stats 2>&1

                # Parse stats
                if ($statsOutput -match "Total entries: (\d+)") {
                    $entryCount = $matches[1]
                    Write-Success "Memory database loaded: $entryCount entries"

                    if ($Verbose -and $statsOutput) {
                        Write-Host "  $statsOutput" -ForegroundColor Gray
                    }
                } else {
                    Write-Success "Memory database initialized"
                }
            } catch {
                Write-Warning "Could not load memory stats: $_"
            }
        } else {
            Write-Info "Skipping memory load (--SkipMemoryLoad specified)"
        }
    } else {
        Write-Info "Creating new memory.db for project '$ProjectName'..."
        try {
            python $INDEXER_SCRIPT --project $ProjectName --init 2>&1 | Out-Null
            Write-Success "Memory database created"
        } catch {
            Write-Error "Failed to create memory.db: $_"
        }
    }
} else {
    Write-Info "No project specified - skipping project-specific memory database"
}

# Check memory JSON files
$SHORT_MEMORY = "$BASE_DIR\memory\short.json"
$LONG_MEMORY = "$BASE_DIR\memory\long.json"

if (Test-Path $SHORT_MEMORY) {
    $shortSize = (Get-Item $SHORT_MEMORY).Length / 1KB
    Write-Success "Short-term memory ready ($([math]::Round($shortSize, 2)) KB)"
} else {
    Write-Info "Creating short-term memory file..."
    New-Item -Path $SHORT_MEMORY -ItemType File -Force | Out-Null
    Set-Content -Path $SHORT_MEMORY -Value "{}" -Force
    Write-Success "Short-term memory initialized"
}

if (Test-Path $LONG_MEMORY) {
    $longSize = (Get-Item $LONG_MEMORY).Length / 1KB
    Write-Success "Long-term memory ready ($([math]::Round($longSize, 2)) KB)"
} else {
    Write-Info "Creating long-term memory file..."
    New-Item -Path $LONG_MEMORY -ItemType File -Force | Out-Null
    Set-Content -Path $LONG_MEMORY -Value "{}" -Force
    Write-Success "Long-term memory initialized"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Step 4: Check Agent System
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[4/7] Loading Agent System..."

$ROOT_AGENTS_DIR = "$BASE_DIR\..\.claude\agents"
$PROJECT_AGENTS_DIR = "$PROJECT_DIR\.claude\agents"

# Count root agents
if (Test-Path $ROOT_AGENTS_DIR) {
    $rootAgents = Get-ChildItem -Path $ROOT_AGENTS_DIR -Filter "*.md" -Recurse -File
    $rootAgentCount = $rootAgents.Count
    Write-Success "Root agents loaded: $rootAgentCount agents"

    if ($Verbose) {
        $categories = $rootAgents | ForEach-Object { $_.Directory.Name } | Select-Object -Unique
        $categoryList = $categories -join ", "
        Write-Info "Categories: $categoryList"
    }
} else {
    Write-Warning "Root agents directory not found"
    $rootAgentCount = 0
}

# Count project agents (only if project specified)
if ($ProjectName -and (Test-Path $PROJECT_AGENTS_DIR)) {
    $projectAgents = Get-ChildItem -Path $PROJECT_AGENTS_DIR -Filter "*.md" -File
    $projectAgentCount = $projectAgents.Count
    Write-Success "Project agents loaded: $projectAgentCount agents"

    if ($Verbose -and $projectAgents) {
        $agentNames = $projectAgents | ForEach-Object { $_.BaseName }
        $agentList = $agentNames -join ", "
        Write-Info "Agents: $agentList"
    }
} else {
    if ($ProjectName) {
        Write-Info "No project-specific agents"
    }
    $projectAgentCount = 0
}

$totalAgents = $rootAgentCount + $projectAgentCount
Write-Success "Total agents available: $totalAgents"

# ═══════════════════════════════════════════════════════════════════════════════
# Step 5: Check Vector Store
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[5/7] Checking Vector Store..."

$VECTOR_STORE = "$BASE_DIR\..\unified-memory\vector-store"

if (Test-Path $VECTOR_STORE) {
    $chromaDb = "$VECTOR_STORE\chroma.sqlite3"
    if (Test-Path $chromaDb) {
        $dbSize = (Get-Item $chromaDb).Length / 1MB
        Write-Success "Vector store ready ($([math]::Round($dbSize, 2)) MB)"
    } else {
        Write-Warning "Vector store exists but no chroma.sqlite3 found"
    }
} else {
    Write-Info "Vector store not initialized (will be created on first use)"
}

# ═══════════════════════════════════════════════════════════════════════════════
# Step 6: Environment Setup
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[6/7] Setting Environment Variables..."

# Set project-specific environment variables
$env:PROJECT_NAME = $ProjectName
$env:PROJECT_ROOT = $PROJECT_DIR
$env:CLAUDE_BASE_DIR = $BASE_DIR

Write-Success "Environment variables configured"

# ═══════════════════════════════════════════════════════════════════════════════
# Step 7: Finalize Setup
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Step "[7/7] Finalizing Setup..."

# Determine path to open
if ($ProjectPath -and (Test-Path $ProjectPath)) {
    $openPath = $ProjectPath
    Write-Info "Opening custom path: $ProjectPath"
} elseif ($ProjectName -and (Test-Path $PROJECT_DIR)) {
    $openPath = $PROJECT_DIR
    Write-Info "Opening project directory: $ProjectName"
} else {
    $openPath = $BASE_DIR
    if ($ProjectName) {
        Write-Warning "Project directory not found, using base directory"
    } else {
        Write-Info "Using base directory (global mode)"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  Claude Code Enhanced System Ready!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""

Write-Host "System Capabilities:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [MCP] MCP Servers" -ForegroundColor White
Write-Host "     - Browser Automation (playwright, puppeteer)" -ForegroundColor Gray
Write-Host "     - Documentation Access (context7)" -ForegroundColor Gray
Write-Host "     - Advanced Reasoning (sequential-thinking)" -ForegroundColor Gray
Write-Host "     - Memory Management (memory_short, memory_long)" -ForegroundColor Gray
Write-Host ""

Write-Host "  [AI] AI Agents" -ForegroundColor White
Write-Host "     - Global Agents: $rootAgentCount" -ForegroundColor Gray
Write-Host "     - Project Agents: $projectAgentCount" -ForegroundColor Gray
Write-Host "     - Total Available: $totalAgents" -ForegroundColor Gray
Write-Host ""

Write-Host "  [MEM] Memory System" -ForegroundColor White
if (Test-Path $MEMORY_DB) {
    Write-Host "     - Structured Memory: $entryCount entries loaded" -ForegroundColor Gray
}
Write-Host "     - Short-term Memory: Ready" -ForegroundColor Gray
Write-Host "     - Long-term Memory: Ready" -ForegroundColor Gray
if (Test-Path "$VECTOR_STORE\chroma.sqlite3") {
    Write-Host "     - Vector Store: Ready" -ForegroundColor Gray
}
Write-Host ""

Write-Host "  [PRJ] Project" -ForegroundColor White
if ($ProjectName) {
    Write-Host "     - Name: $ProjectName" -ForegroundColor Gray
    Write-Host "     - Path: $openPath" -ForegroundColor Gray
} else {
    Write-Host "     - Mode: Global (no project)" -ForegroundColor Gray
    Write-Host "     - Path: $openPath" -ForegroundColor Gray
}
Write-Host ""

Write-Host "System initialization complete!" -ForegroundColor Green
Write-Host ""

# Note: VS Code launch removed - use Claude Code CLI directly
# To launch with a specific project, run: claude code <project-path>

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Tip: Use ``Use [agent-name] to [task]`` for specific expertise" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
