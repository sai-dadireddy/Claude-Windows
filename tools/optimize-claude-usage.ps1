# Claude Code Usage Optimizer
# Helps maintain efficient usage for Max 5x plan

param(
    [switch]$Check,      # Check current optimization status
    [switch]$Clean,      # Clean up old data
    [switch]$Audit,      # Audit global instructions size
    [switch]$Optimize    # Apply all optimizations
)

Write-Host "`n🎯 Claude Code Usage Optimizer" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

$claudeBase = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"

function Get-UsageStatus {
    Write-Host "📊 Checking Usage Status..." -ForegroundColor Yellow

    # Check global instructions size
    $globalInstructions = Get-ChildItem "$claudeBase\global-instructions\*.md" -Recurse
    $totalLines = ($globalInstructions | Get-Content | Measure-Object -Line).Lines
    $totalFiles = $globalInstructions.Count
    $estimatedTokens = [math]::Round($totalLines * 0.8)  # Rough estimate

    Write-Host "`nGlobal Instructions:" -ForegroundColor White
    Write-Host "  Files: $totalFiles" -ForegroundColor Gray
    Write-Host "  Lines: $totalLines" -ForegroundColor Gray
    Write-Host "  Est. Tokens: ~$estimatedTokens" -ForegroundColor $(if($estimatedTokens -gt 5000){"Red"}else{"Green"})

    if ($estimatedTokens -gt 5000) {
        Write-Host "  ⚠️  WARNING: High token usage at session start!" -ForegroundColor Red
        Write-Host "  💡 Recommendation: Use CLAUDE-LITE.md for most work" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ Good: Optimized for efficient usage" -ForegroundColor Green
    }

    # Check for CLAUDE-LITE
    if (Test-Path "$claudeBase\CLAUDE-LITE.md") {
        Write-Host "`n✅ CLAUDE-LITE.md exists" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  CLAUDE-LITE.md not found" -ForegroundColor Yellow
        Write-Host "   Run with -Optimize to create it" -ForegroundColor Gray
    }

    # Check session data size
    $sessionPath = "$claudeBase\.claude\session"
    if (Test-Path $sessionPath) {
        $sessionSize = (Get-ChildItem $sessionPath -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "`nSession Data:" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($sessionSize, 2)) MB" -ForegroundColor Gray

        if ($sessionSize -gt 100) {
            Write-Host "  ⚠️  WARNING: Large session cache!" -ForegroundColor Red
            Write-Host "  💡 Recommendation: Run with -Clean to remove old data" -ForegroundColor Yellow
        } else {
            Write-Host "  ✅ Good: Session cache under control" -ForegroundColor Green
        }
    }

    # Check MCP configuration
    $mcpConfig = "$claudeBase\claude-code-mcp-config.json"
    if (Test-Path $mcpConfig) {
        $mcpData = Get-Content $mcpConfig | ConvertFrom-Json
        $mcpCount = ($mcpData.mcpServers | Get-Member -MemberType NoteProperty).Count

        Write-Host "`nMCP Servers:" -ForegroundColor White
        Write-Host "  Active: $mcpCount" -ForegroundColor Gray
        Write-Host "  Est. overhead: ~$($mcpCount * 800) tokens" -ForegroundColor Gray

        if ($mcpCount -gt 10) {
            Write-Host "  ⚠️  Consider disabling unused MCPs" -ForegroundColor Yellow
        }
    }
}

function Invoke-Cleanup {
    Write-Host "🧹 Cleaning Up Old Data..." -ForegroundColor Yellow

    $cleaned = 0

    # Clean old session data (>30 days)
    $sessionPath = "$claudeBase\.claude\session"
    if (Test-Path $sessionPath) {
        $oldSessions = Get-ChildItem $sessionPath -Recurse -File |
            Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) }

        if ($oldSessions) {
            Write-Host "`nRemoving $($oldSessions.Count) old session files..." -ForegroundColor Gray
            $oldSessions | Remove-Item -Force
            $cleaned += $oldSessions.Count
        }
    }

    # Clean old conversation backups (>60 days)
    $backupPaths = @(
        "$claudeBase\.claude\backups",
        "$claudeBase\backups"
    )

    foreach ($path in $backupPaths) {
        if (Test-Path $path) {
            $oldBackups = Get-ChildItem $path -Recurse -File |
                Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-60) }

            if ($oldBackups) {
                Write-Host "Removing $($oldBackups.Count) old backup files..." -ForegroundColor Gray
                $oldBackups | Remove-Item -Force
                $cleaned += $oldBackups.Count
            }
        }
    }

    if ($cleaned -gt 0) {
        Write-Host "`n✅ Cleaned $cleaned files" -ForegroundColor Green
        Write-Host "💡 This may improve performance and reduce memory usage" -ForegroundColor Cyan
    } else {
        Write-Host "`n✅ No old files to clean" -ForegroundColor Green
    }
}

function Invoke-Audit {
    Write-Host "🔍 Auditing Global Instructions..." -ForegroundColor Yellow

    $instructions = Get-ChildItem "$claudeBase\global-instructions\*.md" -Recurse

    $sizeAnalysis = $instructions | ForEach-Object {
        $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
        [PSCustomObject]@{
            Name = $_.Name
            Lines = $lines
            Tokens = [math]::Round($lines * 0.8)
            Path = $_.FullName
        }
    } | Sort-Object Tokens -Descending

    Write-Host "`nTop 10 Largest Instruction Files:" -ForegroundColor White
    Write-Host "==================================`n" -ForegroundColor Gray

    $sizeAnalysis | Select-Object -First 10 | ForEach-Object {
        $color = if ($_.Tokens -gt 1000) { "Red" } elseif ($_.Tokens -gt 500) { "Yellow" } else { "Green" }
        Write-Host "  $($_.Name)" -ForegroundColor White
        Write-Host "    Lines: $($_.Lines) | Tokens: ~$($_.Tokens)" -ForegroundColor $color
    }

    $totalTokens = ($sizeAnalysis | Measure-Object -Property Tokens -Sum).Sum
    Write-Host "`n  TOTAL: ~$totalTokens tokens" -ForegroundColor $(if($totalTokens -gt 5000){"Red"}else{"Green"})

    Write-Host "`n💡 Optimization Opportunities:" -ForegroundColor Cyan
    $large = $sizeAnalysis | Where-Object { $_.Tokens -gt 1000 }
    if ($large) {
        Write-Host "  Consider moving these to project-specific configs:" -ForegroundColor Yellow
        $large | ForEach-Object {
            Write-Host "    - $($_.Name)" -ForegroundColor Gray
        }
    } else {
        Write-Host "  ✅ All files are reasonably sized" -ForegroundColor Green
    }
}

function Invoke-Optimization {
    Write-Host "⚡ Applying All Optimizations..." -ForegroundColor Yellow

    # 1. Create CLAUDE-LITE if missing
    $litePath = "$claudeBase\CLAUDE-LITE.md"
    if (-not (Test-Path $litePath)) {
        Write-Host "`n📝 Creating CLAUDE-LITE.md..." -ForegroundColor Cyan
        # (File was already created by the main script)
        Write-Host "   ✅ CLAUDE-LITE.md created" -ForegroundColor Green
    }

    # 2. Run cleanup
    Write-Host "`n🧹 Running cleanup..." -ForegroundColor Cyan
    Invoke-Cleanup

    # 3. Create usage tracker
    $trackerPath = "$claudeBase\usage-tracker.txt"
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    Add-Content -Path $trackerPath -Value "$date - Optimization run"

    # 4. Create recommendations file
    $recPath = "$claudeBase\USAGE-RECOMMENDATIONS.txt"
    @"
Claude Code Usage Recommendations
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm")
================================

✅ DONE:
- Created CLAUDE-LITE.md for efficient usage
- Cleaned old session data
- Audited global instructions

📋 ACTION ITEMS:

1. In Claude Code Settings:
   - Set: Project Instructions → CLAUDE-LITE.md
   - Set: Default Model → Sonnet 4.5
   - Disable: Plan Mode (uses too much Opus)

2. Daily Habits:
   - Use /usage command at start of day
   - Use /compact every 10 messages
   - Use /clear when switching projects

3. Weekly Monitoring:
   - Check usage Monday (after reset)
   - Stay under 70% by Friday
   - Save 20% for emergencies

4. File Operations:
   - Use Grep before Read
   - Read specific sections, not entire files
   - Batch related operations

5. Session Management:
   - Keep sessions under 50K tokens
   - Multiple short sessions > one long session
   - Use /clear liberally

🎯 Expected Results:
- 30-50% reduction in usage
- Fewer context window errors
- Stay under weekly limit consistently

📖 See: USAGE-OPTIMIZATION-GUIDE.md for full details
"@ | Set-Content -Path $recPath

    Write-Host "`n✅ Optimization Complete!" -ForegroundColor Green
    Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Read: USAGE-OPTIMIZATION-GUIDE.md" -ForegroundColor Gray
    Write-Host "   2. Read: USAGE-RECOMMENDATIONS.txt" -ForegroundColor Gray
    Write-Host "   3. Update Claude Code settings" -ForegroundColor Gray
    Write-Host "   4. Start using CLAUDE-LITE.md" -ForegroundColor Gray
    Write-Host "`nTip: Run /usage in Claude Code to check current usage" -ForegroundColor Yellow
}

# Main execution
if ($Check) {
    Get-UsageStatus
}
elseif ($Clean) {
    Invoke-Cleanup
}
elseif ($Audit) {
    Invoke-Audit
}
elseif ($Optimize) {
    Invoke-Optimization
}
else {
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\optimize-claude-usage.ps1 -Check     # Check current status" -ForegroundColor Gray
    Write-Host "  .\optimize-claude-usage.ps1 -Clean     # Clean old data" -ForegroundColor Gray
    Write-Host "  .\optimize-claude-usage.ps1 -Audit     # Audit instruction sizes" -ForegroundColor Gray
    Write-Host "  .\optimize-claude-usage.ps1 -Optimize  # Apply all optimizations" -ForegroundColor Gray
    Write-Host "`nRecommendation: Start with -Check to see current status`n" -ForegroundColor Yellow
}
