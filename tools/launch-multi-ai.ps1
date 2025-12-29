# Multi-AI Launcher with Git Worktrees
# Enables parallel AI development with Claude, Codex, and Gemini

param(
    [string]$Task = "",
    [switch]$Clean = $false
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-GitRepo {
    try {
        git rev-parse --git-dir 2>&1 | Out-Null
        return $true
    } catch {
        return $false
    }
}

function Initialize-Worktrees {
    Write-ColorOutput "`n🚀 Multi-AI Launcher" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    if (-not (Test-GitRepo)) {
        Write-ColorOutput "⚠️  Not in a git repository" "Yellow"
        Write-ColorOutput "Running without worktrees (simple multi-terminal mode)`n" "Gray"
        Show-SimpleInstructions
        return
    }

    $currentBranch = git branch --show-current
    Write-ColorOutput "📂 Current branch: $currentBranch" "Cyan"

    $ais = @(
        @{Name="claude"; Color="Blue"; CLI="claude"},
        @{Name="gpt5"; Color="Green"; CLI="codex"},
        @{Name="gemini"; Color="Magenta"; CLI="gemini"}
    )

    Write-ColorOutput "`n📦 Creating isolated worktrees...`n" "Cyan"

    foreach ($ai in $ais) {
        $worktreeName = "$($ai.Name)-worktree"
        $branchName = "$($ai.Name)-branch"

        if (Test-Path $worktreeName) {
            Write-ColorOutput "  ✓ $worktreeName already exists" $ai.Color
            continue
        }

        Write-ColorOutput "  → Creating $worktreeName..." $ai.Color

        # Create branch if it doesn't exist
        $branchExists = git branch --list $branchName
        if (-not $branchExists) {
            git branch $branchName $currentBranch 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                Write-ColorOutput "    ✗ Failed to create branch $branchName" "Red"
                continue
            }
        }

        # Create worktree
        git worktree add $worktreeName $branchName 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-ColorOutput "    ✗ Failed to create worktree" "Red"
            # Cleanup branch if worktree creation failed
            git branch -D $branchName 2>&1 | Out-Null
            continue
        }

        Write-ColorOutput "    ✓ Created $worktreeName" $ai.Color
    }

    Write-ColorOutput "`n✅ Worktrees ready!`n" "Green"
    Show-WorktreeInstructions $ais
}

function Show-WorktreeInstructions {
    param($ais)

    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "📋 NEXT STEPS" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "Open 3 terminal windows and run:" "Yellow"

    $i = 1
    foreach ($ai in $ais) {
        $worktreeName = "$($ai.Name)-worktree"
        Write-ColorOutput "`n  Terminal $i ($($ai.Name.ToUpper())):" $ai.Color
        Write-ColorOutput "    cd $worktreeName" "White"
        Write-ColorOutput "    $($ai.CLI)" "White"
        $i++
    }

    Write-ColorOutput "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "💡 WORKFLOW" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "1. Type the SAME prompt in all 3 terminals" "White"
    Write-ColorOutput "2. Each AI works in isolated worktree" "White"
    Write-ColorOutput "3. Compare results from each AI" "White"
    Write-ColorOutput "4. Cherry-pick the best parts" "White"
    Write-ColorOutput "5. Merge winning solution to main branch`n" "White"

    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "🔧 MANAGEMENT" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "List worktrees:" "Yellow"
    Write-ColorOutput "  git worktree list`n" "White"

    Write-ColorOutput "Remove worktrees when done:" "Yellow"
    Write-ColorOutput "  .\tools\launch-multi-ai.ps1 -Clean`n" "White"

    Write-ColorOutput "View results from each AI:" "Yellow"
    Write-ColorOutput "  cd claude-worktree && git diff" "White"
    Write-ColorOutput "  cd gpt5-worktree && git diff" "White"
    Write-ColorOutput "  cd gemini-worktree && git diff`n" "White"
}

function Show-SimpleInstructions {
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "📋 SIMPLE MULTI-TERMINAL MODE" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "Open 3 terminal windows and run:" "Yellow"
    Write-ColorOutput "`n  Terminal 1: claude" "Blue"
    Write-ColorOutput "  Terminal 2: codex" "Green"
    Write-ColorOutput "  Terminal 3: gemini`n" "Magenta"

    Write-ColorOutput "Then type the same prompt in each and compare results!`n" "White"
}

function Remove-Worktrees {
    Write-ColorOutput "`n🧹 Cleaning up worktrees..." "Yellow"

    $ais = @("claude", "gpt5", "gemini")

    foreach ($ai in $ais) {
        $worktreeName = "$ai-worktree"
        $branchName = "$ai-branch"

        if (Test-Path $worktreeName) {
            Write-ColorOutput "  → Removing $worktreeName..." "Gray"
            git worktree remove $worktreeName --force 2>&1 | Out-Null
        }

        $branchExists = git branch --list $branchName
        if ($branchExists) {
            Write-ColorOutput "  → Deleting branch $branchName..." "Gray"
            git branch -D $branchName 2>&1 | Out-Null
        }
    }

    Write-ColorOutput "`n✅ Cleanup complete!`n" "Green"
}

function Show-TaskHelp {
    Write-ColorOutput "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Gray"
    Write-ColorOutput "🤖 MULTI-AI LAUNCHER" "Cyan"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" "Gray"

    Write-ColorOutput "USAGE:" "Yellow"
    Write-ColorOutput "  .\tools\launch-multi-ai.ps1              # Setup worktrees" "White"
    Write-ColorOutput "  .\tools\launch-multi-ai.ps1 -Clean       # Remove worktrees`n" "White"

    Write-ColorOutput "WHAT IT DOES:" "Yellow"
    Write-ColorOutput "  Creates isolated git worktrees for parallel AI development" "White"
    Write-ColorOutput "  - claude-worktree/ (Claude Code)" "Blue"
    Write-ColorOutput "  - gpt5-worktree/ (Codex)" "Green"
    Write-ColorOutput "  - gemini-worktree/ (Gemini CLI)`n" "Magenta"

    Write-ColorOutput "BENEFITS:" "Yellow"
    Write-ColorOutput "  ✓ Each AI works independently" "Green"
    Write-ColorOutput "  ✓ No conflicts or overwrites" "Green"
    Write-ColorOutput "  ✓ Easy to compare results" "Green"
    Write-ColorOutput "  ✓ Cherry-pick best solutions`n" "Green"

    Write-ColorOutput "EXAMPLES:" "Yellow"
    Write-ColorOutput "  # Setup and get instructions" "Gray"
    Write-ColorOutput "  .\tools\launch-multi-ai.ps1`n" "White"

    Write-ColorOutput "  # Clean up when done" "Gray"
    Write-ColorOutput "  .\tools\launch-multi-ai.ps1 -Clean`n" "White"
}

# Main execution
if ($Clean) {
    Remove-Worktrees
} elseif ($Task -eq "help" -or $Task -eq "--help" -or $Task -eq "-h") {
    Show-TaskHelp
} else {
    Initialize-Worktrees
}
