# Claude Code Output Style Selector
# Interactive, humorous style selection at startup

function Show-StyleMenu {
    Clear-Host

    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║           🎭 CHOOSE YOUR CLAUDE PERSONALITY 🎭            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  How should Claude vibe today? Pick your flavor:" -ForegroundColor Yellow
    Write-Host ""

    # Style 1: Fun Coworker (Default)
    Write-Host "  [1] 🚀 " -NoNewline -ForegroundColor Green
    Write-Host "Fun Coworker" -NoNewline -ForegroundColor White
    Write-Host " (Default)" -ForegroundColor DarkGray
    Write-Host "      → Your smartest, funniest teammate" -ForegroundColor DarkGray
    Write-Host "      → Humor, analogies, 'Let's gooooo!' energy" -ForegroundColor DarkGray
    Write-Host "      → Perfect for: Daily coding, having a good time" -ForegroundColor DarkGray
    Write-Host ""

    # Style 2: Professional
    Write-Host "  [2] 💼 " -NoNewline -ForegroundColor Blue
    Write-Host "Professional Mode" -ForegroundColor White
    Write-Host "      → Enterprise-grade, exec-ready" -ForegroundColor DarkGray
    Write-Host "      → Formal reports, data-driven, no jokes" -ForegroundColor DarkGray
    Write-Host "      → Perfect for: Client work, stakeholder demos" -ForegroundColor DarkGray
    Write-Host ""

    # Style 3: Teacher
    Write-Host "  [3] 📚 " -NoNewline -ForegroundColor Magenta
    Write-Host "Teacher Mode" -ForegroundColor White
    Write-Host "      → Patient educator, deep learning" -ForegroundColor DarkGray
    Write-Host "      → Step-by-step, examples, exercises" -ForegroundColor DarkGray
    Write-Host "      → Perfect for: Learning new tech, tutorials" -ForegroundColor DarkGray
    Write-Host ""

    # Random joke option
    Write-Host "  [4] 🎲 " -NoNewline -ForegroundColor Yellow
    Write-Host "Surprise Me!" -ForegroundColor White
    Write-Host "      → Let the AI gods decide your fate" -ForegroundColor DarkGray
    Write-Host "      → (Randomly picks a style - living dangerously!)" -ForegroundColor DarkGray
    Write-Host ""

    # Skip option
    Write-Host "  [5] ⚡ " -NoNewline -ForegroundColor DarkGray
    Write-Host "Just Launch (Default)" -ForegroundColor White
    Write-Host "      → Skip this menu, use fun-coworker" -ForegroundColor DarkGray
    Write-Host ""

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  💡 Pro tip: " -NoNewline -ForegroundColor Yellow
    Write-Host "You can switch styles anytime during the session!" -ForegroundColor Gray
    Write-Host "     Just tell Claude: " -NoNewline -ForegroundColor Gray
    Write-Host "'Use professional mode'" -ForegroundColor White
    Write-Host ""
}

function Get-HumorousStylePrompt {
    param([string]$Style)

    $prompts = @{
        'fun-coworker' = @(
            "🎉 Activating FUN MODE! Time to code and vibe!",
            "🚀 Let's gooooo! Fun coworker mode engaged!",
            "😎 Strapping on the humor thrusters - ready to make coding fun!",
            "🔥 Fun mode activated! Prepare for quality code with dad jokes!",
            "💪 Smart + Funny mode enabled! Let's ship some awesome stuff!"
        )
        'professional' = @(
            "💼 Professional mode activated. Time to impress the stakeholders.",
            "👔 Suit and tie mode ON. No jokes, just results.",
            "📊 Executive mode engaged. Let's make the board proud.",
            "🏢 Enterprise-grade Claude reporting for duty.",
            "📈 Professional excellence mode activated. Delivering business value."
        )
        'teacher' = @(
            "📚 Teacher mode activated! Let's learn something awesome today!",
            "🎓 Education mode ON! Every expert was once a beginner!",
            "👨‍🏫 Professor Claude in the house! Ready to explain ALL the things!",
            "🧠 Learning mode engaged! Time to build some knowledge!",
            "✏️ Teaching mode activated! No question too basic, no concept too complex!"
        )
    }

    $messages = $prompts[$Style]
    return $messages | Get-Random
}

function Select-OutputStyle {
    Show-StyleMenu

    # Get user input with timeout (auto-select default after 10 seconds)
    Write-Host "  Your choice (1-5): " -NoNewline -ForegroundColor Cyan

    $choice = $null
    $timeout = 10 # seconds
    $timer = [Diagnostics.Stopwatch]::StartNew()

    # Read with timeout
    while ($timer.Elapsed.TotalSeconds -lt $timeout -and $null -eq $choice) {
        if ([Console]::KeyAvailable) {
            $choice = [Console]::ReadKey($true).KeyChar
            break
        }
        Start-Sleep -Milliseconds 100
    }

    $timer.Stop()

    # Handle timeout
    if ($null -eq $choice) {
        Write-Host "⚡ (timed out)" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "  ⏰ Took too long! Defaulting to Fun Coworker mode..." -ForegroundColor Yellow
        Start-Sleep -Seconds 1
        $choice = '1'
    } else {
        Write-Host $choice -ForegroundColor Green
        Write-Host ""
    }

    # Process choice
    $style = switch ($choice) {
        '1' {
            $msg = Get-HumorousStylePrompt -Style 'fun-coworker'
            Write-Host "  $msg" -ForegroundColor Green
            'fun-coworker'
        }
        '2' {
            $msg = Get-HumorousStylePrompt -Style 'professional'
            Write-Host "  $msg" -ForegroundColor Blue
            'professional'
        }
        '3' {
            $msg = Get-HumorousStylePrompt -Style 'teacher'
            Write-Host "  $msg" -ForegroundColor Magenta
            'teacher'
        }
        '4' {
            # Random selection
            $styles = @('fun-coworker', 'professional', 'teacher')
            $randomStyle = $styles | Get-Random
            Write-Host "  🎲 The AI gods have chosen: " -NoNewline -ForegroundColor Yellow
            Write-Host "$randomStyle!" -ForegroundColor White
            Write-Host ""
            $msg = Get-HumorousStylePrompt -Style $randomStyle
            Write-Host "  $msg" -ForegroundColor Cyan
            $randomStyle
        }
        '5' {
            Write-Host "  ⚡ Quick launch! Using fun-coworker (default)" -ForegroundColor Gray
            'fun-coworker'
        }
        default {
            Write-Host "  🤔 '$choice' is not a valid option..." -ForegroundColor Red
            Write-Host "  🎯 Defaulting to Fun Coworker (because why not!)" -ForegroundColor Yellow
            'fun-coworker'
        }
    }

    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  💾 Style saved for this session: " -NoNewline -ForegroundColor Cyan
    Write-Host "$style" -ForegroundColor White
    Write-Host ""
    Start-Sleep -Seconds 1

    return $style
}

# Main execution
$selectedStyle = Select-OutputStyle

# Save to environment variable for Claude Code to pick up
$env:CLAUDE_OUTPUT_STYLE = $selectedStyle

# Save to a temp file that Claude can read
$styleConfigPath = Join-Path $env:TEMP "claude-session-style.txt"
$selectedStyle | Out-File -FilePath $styleConfigPath -Encoding UTF8 -NoNewline

Write-Host "  ✅ Output style configured!" -ForegroundColor Green
Write-Host "  📂 Session config: $styleConfigPath" -ForegroundColor DarkGray
Write-Host ""
Start-Sleep -Milliseconds 500

# Output the selected style as the LAST line (for capture)
Write-Output $selectedStyle
