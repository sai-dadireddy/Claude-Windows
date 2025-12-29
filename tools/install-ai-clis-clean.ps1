# AI CLI Installation Script (Clean Version)
# Installs and configures Codex CLI (GPT-5) and Gemini CLI

param(
    [switch]$SkipCodex = $false,
    [switch]$SkipGemini = $false,
    [switch]$Force = $false
)

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-CommandExists {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

Write-ColorOutput "`nAI CLI INSTALLATION WIZARD" "Cyan"
Write-ColorOutput "======================================`n" "Gray"

# Check Node.js
Write-ColorOutput "Checking prerequisites..." "Yellow"
if (-not (Test-CommandExists "node")) {
    Write-ColorOutput "[X] Node.js not found! Please install Node.js 18+ first." "Red"
    Write-ColorOutput "    Download from: https://nodejs.org/`n" "White"
    exit 1
}

$nodeVersion = node --version
Write-ColorOutput "  [OK] Node.js: $nodeVersion" "Green"

# Install Codex CLI (GPT-5)
if (-not $SkipCodex) {
    Write-ColorOutput "`n======================================" "Gray"
    Write-ColorOutput "INSTALLING CODEX CLI (GPT-5)" "Cyan"
    Write-ColorOutput "======================================`n" "Gray"

    if ((Test-CommandExists "codex") -and -not $Force) {
        Write-ColorOutput "  [INFO] Codex CLI already installed" "Yellow"
        try {
            $codexVersion = codex --version 2>&1
            Write-ColorOutput "         Version: $codexVersion" "Gray"
        } catch {
            Write-ColorOutput "         Status: Installed" "Gray"
        }
        Write-ColorOutput "         Use -Force to reinstall`n" "Gray"
    } else {
        Write-ColorOutput "  -> Installing globally via npm..." "White"
        npm install -g @openai/codex

        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  [OK] Codex CLI installed successfully!" "Green"

            Write-ColorOutput "`n  AUTHENTICATION OPTIONS:" "Yellow"
            Write-ColorOutput "     Option 1: ChatGPT subscription (recommended)" "White"
            Write-ColorOutput "       - Run: codex" "Gray"
            Write-ColorOutput "       - Sign in with your ChatGPT Plus/Pro account" "Gray"
            Write-ColorOutput "`n     Option 2: OpenAI API key" "White"
            Write-ColorOutput "       - Get key from: https://platform.openai.com/api-keys" "Gray"
            Write-ColorOutput "       - Set: `$env:OPENAI_API_KEY = 'your-key'" "Gray"
            Write-ColorOutput "       - Or add to profile for persistence" "Gray"
        } else {
            Write-ColorOutput "  [X] Failed to install Codex CLI" "Red"
        }
    }
}

# Install Gemini CLI
if (-not $SkipGemini) {
    Write-ColorOutput "`n======================================" "Gray"
    Write-ColorOutput "INSTALLING GEMINI CLI" "Cyan"
    Write-ColorOutput "======================================`n" "Gray"

    if ((Test-CommandExists "gemini") -and -not $Force) {
        Write-ColorOutput "  [INFO] Gemini CLI already installed" "Yellow"
        try {
            $geminiVersion = gemini --version 2>&1
            Write-ColorOutput "         Version: $geminiVersion" "Gray"
        } catch {
            Write-ColorOutput "         Status: Installed" "Gray"
        }
        Write-ColorOutput "         Use -Force to reinstall`n" "Gray"
    } else {
        Write-ColorOutput "  -> Installing globally via npm..." "White"
        npm install -g @google/gemini-cli

        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  [OK] Gemini CLI installed successfully!" "Green"

            Write-ColorOutput "`n  AUTHENTICATION:" "Yellow"
            Write-ColorOutput "     Free Tier: Login with Google account" "White"
            Write-ColorOutput "       - Run: gemini" "Gray"
            Write-ColorOutput "       - Sign in with Google (opens browser)" "Gray"
            Write-ColorOutput "       - Includes generous free quota!" "Gray"
            Write-ColorOutput "`n     API Key (optional):" "White"
            Write-ColorOutput "       - Get from: https://makersuite.google.com/app/apikey" "Gray"
            Write-ColorOutput "       - Set: `$env:GEMINI_API_KEY = 'your-key'" "Gray"
        } else {
            Write-ColorOutput "  [X] Failed to install Gemini CLI" "Red"
        }
    }
}

# Summary
Write-ColorOutput "`n======================================" "Gray"
Write-ColorOutput "INSTALLATION SUMMARY" "Cyan"
Write-ColorOutput "======================================`n" "Gray"

$installed = @()
$notInstalled = @()

if (Test-CommandExists "claude") {
    $installed += "Claude Code (via your subscription)"
} else {
    $notInstalled += "Claude Code"
}

if (Test-CommandExists "codex") {
    $installed += "Codex CLI (GPT-5)"
} else {
    $notInstalled += "Codex CLI"
}

if (Test-CommandExists "gemini") {
    $installed += "Gemini CLI"
} else {
    $notInstalled += "Gemini CLI"
}

Write-ColorOutput "INSTALLED:" "Green"
foreach ($tool in $installed) {
    Write-ColorOutput "   * $tool" "White"
}

if ($notInstalled.Count -gt 0) {
    Write-ColorOutput "`nNOT INSTALLED:" "Yellow"
    foreach ($tool in $notInstalled) {
        Write-ColorOutput "   * $tool" "White"
    }
}

Write-ColorOutput "`n======================================" "Gray"
Write-ColorOutput "NEXT STEPS" "Cyan"
Write-ColorOutput "======================================`n" "Gray"

Write-ColorOutput "1. Authenticate each CLI:" "Yellow"
Write-ColorOutput "   codex    # Sign in with ChatGPT" "White"
Write-ColorOutput "   gemini   # Sign in with Google" "White"

Write-ColorOutput "`n2. Test installations:" "Yellow"
Write-ColorOutput "   codex --version" "White"
Write-ColorOutput "   gemini --version" "White"

Write-ColorOutput "`n3. Test PowerShell integration:" "Yellow"
Write-ColorOutput "   ai-status" "White"

Write-ColorOutput "`n4. Try intelligent routing:" "Yellow"
Write-ColorOutput "   ai-route 'your task here'" "White"

Write-ColorOutput "`n======================================`n" "Gray"

Write-ColorOutput "COST SUMMARY:" "Cyan"
Write-ColorOutput "   * Claude Code: $100/month (your existing subscription)" "White"
Write-ColorOutput "   * Codex CLI: Included with ChatGPT Plus/Pro ($20-200/month)" "White"
Write-ColorOutput "   * Gemini CLI: FREE (generous quota)" "Green"
Write-ColorOutput "`n   TIP: Use Gemini for high-volume tasks to save costs!" "Yellow"

Write-ColorOutput "`nInstallation complete! Ready to supercharge your workflow!`n" "Green"
