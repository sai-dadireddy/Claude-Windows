# Ralph Loop - PowerShell Version
# Spawns fresh Claude Code instances for each iteration
# Based on Ryan Carson's implementation
#
# Usage: .\ralph_loop.ps1 [-PrdFile path] [-MaxIterations n]
#

param(
    [string]$PrdFile = ".ralph\prd.json",
    [int]$MaxIterations = 10
)

$ErrorActionPreference = "Stop"

# Configuration
$RalphDir = ".ralph"
$ProgressFile = "$RalphDir\progress.txt"
$LogFile = "$RalphDir\loop.log"
$ArchiveDir = "$RalphDir\archive"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Level : $Message"
    Write-Host "[$Level] $Message" -ForegroundColor $(switch ($Level) {
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
        "WARN" { "Yellow" }
        default { "Cyan" }
    })
    Add-Content -Path $LogFile -Value $logEntry
}

function Initialize-Ralph {
    # Create directories
    New-Item -ItemType Directory -Force -Path $RalphDir | Out-Null
    New-Item -ItemType Directory -Force -Path $ArchiveDir | Out-Null

    if (-not (Test-Path $PrdFile)) {
        Write-Log "PRD file not found: $PrdFile" "ERROR"
        Write-Host "Create a prd.json file first using: /prd-to-stories"
        exit 1
    }

    # Initialize progress file
    if (-not (Test-Path $ProgressFile)) {
        @"
# Ralph Progress Log
Started: $(Get-Date)

"@ | Set-Content $ProgressFile
    }

    Write-Log "Initialized Ralph in $RalphDir"
}

function Get-NextStory {
    $prd = Get-Content $PrdFile | ConvertFrom-Json
    $story = $prd.stories | Where-Object { $_.passes -eq $false } | Select-Object -First 1
    return $story
}

function Get-RemainingCount {
    $prd = Get-Content $PrdFile | ConvertFrom-Json
    return ($prd.stories | Where-Object { $_.passes -eq $false }).Count
}

function New-SystemPrompt {
    param([string]$StoryId, [int]$Iteration)

    return @"
You are an autonomous coding agent working on this project.

## Your Task

1. Read the PRD file: $PrdFile
2. Read the progress log: $ProgressFile
3. Focus on story: $StoryId
4. Implement the story according to its acceptance criteria
5. Test your implementation
6. Commit your changes with a descriptive message
7. Update $PrdFile - set passes: true for this story
8. Update $ProgressFile with what you did

## Rules

- Complete ONE story per iteration
- Each story must pass ALL acceptance criteria before marking complete
- If you learn something important about the codebase, update agents.md in that folder
- If you hit a blocker, log it and move to the next story
- Run tests after implementation
- Commit with format: "feat(story-id): description"

## Progress Report Format

Append to $ProgressFile :

---
## Iteration $Iteration - Story: $StoryId
Thread: [timestamp]
Implemented: [what you built]
Files Changed: [list of files]
Tests: [pass/fail]
Learnings: [any insights for future iterations]
---

## Completion Signal

When done with this story, output exactly:
RALPH_ITERATION_COMPLETE

This signals the loop to continue to the next iteration.
"@
}

function Invoke-Iteration {
    param([int]$Iteration, [object]$Story)

    $storyId = $Story.id
    Write-Log "=== Iteration $Iteration : $storyId ===" "INFO"

    # Create system prompt
    $prompt = New-SystemPrompt -StoryId $storyId -Iteration $Iteration
    $promptFile = "$ArchiveDir\iteration-$Iteration-prompt.txt"
    $prompt | Set-Content $promptFile

    $outputFile = "$ArchiveDir\iteration-$Iteration-output.txt"

    Write-Log "Starting Claude Code for story: $storyId"

    # Check if claude command exists
    $claudePath = Get-Command claude -ErrorAction SilentlyContinue

    if ($claudePath) {
        # Run Claude Code
        $userPrompt = "Implement story $storyId from $PrdFile. Follow the system instructions exactly."

        try {
            $output = & claude --print --dangerously-skip-permissions `
                --system-prompt $prompt `
                $userPrompt 2>&1

            $output | Set-Content $outputFile
            $output | Write-Host
        }
        catch {
            Write-Log "Claude execution failed: $_" "ERROR"
            return $false
        }

        # Check completion
        if (Select-String -Path $outputFile -Pattern "RALPH_ITERATION_COMPLETE" -Quiet) {
            Write-Log "Iteration $Iteration completed" "SUCCESS"
            return $true
        }
        else {
            Write-Log "Iteration $Iteration did not complete cleanly" "WARN"
            return $false
        }
    }
    else {
        Write-Log "Claude command not found. Install Claude Code CLI." "ERROR"
        Write-Host "Would run: claude --print --dangerously-skip-permissions 'Implement story $storyId'"
        "RALPH_ITERATION_COMPLETE" | Set-Content $outputFile
        return $true
    }
}

function Start-RalphLoop {
    Write-Log "Starting Ralph Loop"
    Write-Log "PRD: $PrdFile"
    Write-Log "Max iterations: $MaxIterations"

    Initialize-Ralph

    $iteration = 1

    while ($iteration -le $MaxIterations) {
        $story = Get-NextStory

        if (-not $story) {
            Write-Log "All stories complete!" "SUCCESS"
            break
        }

        $remaining = Get-RemainingCount
        Write-Log "Stories remaining: $remaining"

        $result = Invoke-Iteration -Iteration $iteration -Story $story
        $iteration++

        # Small delay between iterations
        Start-Sleep -Seconds 2
    }

    if ($iteration -gt $MaxIterations) {
        Write-Log "Reached max iterations ($MaxIterations)" "WARN"
    }

    # Final status
    $finalRemaining = Get-RemainingCount
    if ($finalRemaining -eq 0) {
        Write-Log "FEATURE_COMPLETE - All stories implemented!" "SUCCESS"
    }
    else {
        Write-Log "Finished with $finalRemaining stories remaining"
    }

    Write-Log "Run archived to: $ArchiveDir"
}

# Show help
if ($args -contains "-h" -or $args -contains "--help") {
    @"
Ralph Loop - Autonomous Feature Builder (PowerShell)

Usage: .\ralph_loop.ps1 [-PrdFile path] [-MaxIterations n]

Parameters:
  -PrdFile        Path to PRD JSON file (default: .ralph\prd.json)
  -MaxIterations  Maximum iterations to run (default: 10)

Setup:
  1. Create PRD: Use /prd skill to generate PRD markdown
  2. Convert: Use /prd-to-stories to create prd.json
  3. Run: .\ralph_loop.ps1

Example:
  .\ralph_loop.ps1 -PrdFile .ralph\prd.json -MaxIterations 15

The script will:
  - Read user stories from prd.json
  - Spawn fresh Claude Code instance for each story
  - Track progress in .ralph\progress.txt
  - Archive each iteration's output
  - Stop when all stories pass or max iterations reached
"@
    exit 0
}

# Run
Start-RalphLoop
