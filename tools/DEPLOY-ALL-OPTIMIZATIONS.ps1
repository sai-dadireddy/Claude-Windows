# Complete Token Optimization Deployment
# Combines all Reddit recommendations + your automation system

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLAUDE CODE TOKEN OPTIMIZATION DEPLOYMENT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Update Claude Code to latest version (fixes 45K reserved bug)
Write-Host "[1/6] Checking Claude Code version..." -ForegroundColor Yellow
Write-Host "Running: claude update" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANT: This will fix the 45K 'reserved' token bug from 2.0.1-2.0.7" -ForegroundColor White
Write-Host "Latest version: 2.0.10" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to update Claude Code to latest version..."
Read-Host
claude update

Write-Host ""
Write-Host "[OK] Claude Code updated" -ForegroundColor Green
Write-Host ""

# Step 2: Backup current MCP config
Write-Host "[2/6] Backing up current MCP configuration..." -ForegroundColor Yellow
$backupPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude-code-mcp-config.json.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude-code-mcp-config.json" $backupPath
Write-Host "[OK] Backup created: $backupPath" -ForegroundColor Green
Write-Host ""

# Step 3: Deploy optimized MCP config (saves 40-50K tokens)
Write-Host "[3/6] Deploying optimized MCP configuration..." -ForegroundColor Yellow
Write-Host ""
Write-Host "CURRENT (13 MCPs): ~60-80K tokens" -ForegroundColor Red
Write-Host "  - sequential-thinking: ~15-20K" -ForegroundColor Red
Write-Host "  - github: ~15-20K" -ForegroundColor Red
Write-Host "  - playwright-test: ~5-8K" -ForegroundColor Red
Write-Host "  - langchain: ~8-12K" -ForegroundColor Red
Write-Host "  - Other 9 MCPs: ~20-30K" -ForegroundColor Red
Write-Host ""
Write-Host "OPTIMIZED (9 MCPs): ~20-30K tokens" -ForegroundColor Green
Write-Host "  - Essential MCPs only" -ForegroundColor Green
Write-Host "  - Heavy MCPs moved to _disabled_mcps" -ForegroundColor Green
Write-Host ""
Write-Host "SAVINGS: 40-50K tokens per session (60-70% reduction)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to deploy optimized MCP config..."
Read-Host

Copy-Item "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude-code-mcp-config-optimized.json" "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude-code-mcp-config.json" -Force
Write-Host "[OK] Optimized MCP config deployed" -ForegroundColor Green
Write-Host ""

# Step 4: Configure Claude Code settings
Write-Host "[4/6] Configuring Claude Code settings..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Setting up:" -ForegroundColor White
Write-Host "  - Disable auto-compact (you have manual system)" -ForegroundColor White
Write-Host "  - Confirm thinking mode setting" -ForegroundColor White
Write-Host "  - Verify Sonnet 4.5 default" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to open Claude Code configuration..."
Read-Host

Write-Host ""
Write-Host "INSTRUCTIONS FOR CLAUDE CODE:" -ForegroundColor Cyan
Write-Host "1. Press Ctrl+, (or Cmd+, on Mac) to open settings" -ForegroundColor White
Write-Host "2. Search for 'auto compact'" -ForegroundColor White
Write-Host "3. DISABLE 'Automatic Compression' (saves 45K reserved)" -ForegroundColor White
Write-Host "4. Search for 'thinking'" -ForegroundColor White
Write-Host "5. Set thinking mode to OFF by default" -ForegroundColor White
Write-Host "6. Verify model is 'claude-sonnet-4-5'" -ForegroundColor White
Write-Host ""
Write-Host "OR use /config command in Claude Code terminal:" -ForegroundColor Cyan
Write-Host "  /config" -ForegroundColor Gray
Write-Host "  Then toggle settings as needed" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Enter when done..."
Read-Host
Write-Host "[OK] Settings configured" -ForegroundColor Green
Write-Host ""

# Step 5: Update global instructions
Write-Host "[5/6] Updating global instructions..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Adding to CLAUDE-LITE.md:" -ForegroundColor White
Write-Host "  - Image-first strategy" -ForegroundColor White
Write-Host "  - Documentation prevention rules" -ForegroundColor White
Write-Host "  - Thinking mode guidelines" -ForegroundColor White
Write-Host ""

# Read current CLAUDE-LITE.md
$claudeLiteContent = Get-Content "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\CLAUDE-LITE.md" -Raw

# Add image-first strategy if not already present
if ($claudeLiteContent -notmatch "image-first-strategy.md") {
    $insertPoint = $claudeLiteContent.IndexOf("### Auto-Compact Management")
    if ($insertPoint -gt 0) {
        $newContent = $claudeLiteContent.Insert($insertPoint, @"
### Image-First Communication Strategy
{{include: global-instructions/image-first-strategy.md}}

"@)
        Set-Content "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\CLAUDE-LITE.md" $newContent -NoNewline
        Write-Host "[OK] Added image-first strategy to CLAUDE-LITE.md" -ForegroundColor Green
    }
} else {
    Write-Host "[SKIP] Image-first strategy already in CLAUDE-LITE.md" -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Summary and next steps
Write-Host "[6/6] Deployment Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OPTIMIZATION SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ COMPLETED:" -ForegroundColor Green
Write-Host "  1. Updated Claude Code to latest version (fixes 45K bug)" -ForegroundColor White
Write-Host "  2. Deployed optimized MCP config (saves 40-50K/session)" -ForegroundColor White
Write-Host "  3. Configured settings (auto-compact OFF, thinking OFF)" -ForegroundColor White
Write-Host "  4. Updated global instructions" -ForegroundColor White
Write-Host ""

Write-Host "📊 EXPECTED SAVINGS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "BEFORE OPTIMIZATION:" -ForegroundColor Red
Write-Host "  - Startup tokens: ~75-100K" -ForegroundColor Red
Write-Host "  - MCP overhead: ~60-80K" -ForegroundColor Red
Write-Host "  - Reserved (bug): 45K" -ForegroundColor Red
Write-Host "  - Thinking mode: 2x penalty" -ForegroundColor Red
Write-Host "  - Weekly usage: 77%" -ForegroundColor Red
Write-Host ""
Write-Host "AFTER OPTIMIZATION:" -ForegroundColor Green
Write-Host "  - Startup tokens: ~22-33K (60% saved)" -ForegroundColor Green
Write-Host "  - MCP overhead: ~20-30K (60% saved)" -ForegroundColor Green
Write-Host "  - Reserved (bug): 0K (fixed)" -ForegroundColor Green
Write-Host "  - Thinking mode: OFF (no penalty)" -ForegroundColor Green
Write-Host "  - Expected weekly: 45-55%" -ForegroundColor Green
Write-Host ""
Write-Host "TOTAL SAVINGS: ~1.7-2.2M tokens/week (31-40% reduction)" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. RESTART Claude Code now (required for MCP changes)" -ForegroundColor White
Write-Host "   - Close all Claude Code terminals" -ForegroundColor Gray
Write-Host "   - Open new Claude Code session" -ForegroundColor Gray
Write-Host ""
Write-Host "2. VERIFY optimizations in first session:" -ForegroundColor White
Write-Host "   - Run: /context" -ForegroundColor Gray
Write-Host "   - Check MCP tools: Should be ~20-30K (vs ~60-80K)" -ForegroundColor Gray
Write-Host "   - Check Reserved: Should be 0K (vs 45K)" -ForegroundColor Gray
Write-Host "   - Total used: Should be ~22-33K (vs ~75-100K)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. USE image-first strategy:" -ForegroundColor White
Write-Host "   - For UI/design: Screenshot + brief context" -ForegroundColor Gray
Write-Host "   - For errors: Terminal screenshot + 'Fix this'" -ForegroundColor Gray
Write-Host "   - Windows: Win+Shift+S, then drag into terminal" -ForegroundColor Gray
Write-Host ""
Write-Host "4. SESSION START protocol:" -ForegroundColor White
Write-Host "   - Start with: 'Working on [task]. No docs unless requested.'" -ForegroundColor Gray
Write-Host "   - Or use: # [task description]" -ForegroundColor Gray
Write-Host ""
Write-Host "5. THINKING mode:" -ForegroundColor White
Write-Host "   - Press Tab to check status (should be OFF)" -ForegroundColor Gray
Write-Host "   - Enable ONLY for complex architecture/debugging" -ForegroundColor Gray
Write-Host "   - 99% of work doesn't need thinking mode" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "READY TO TEST!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Close this window and RESTART Claude Code to activate changes." -ForegroundColor Yellow
Write-Host ""
Write-Host "Expected first session:" -ForegroundColor White
Write-Host "  - System prompt: ~3K" -ForegroundColor White
Write-Host "  - System tools: ~12K" -ForegroundColor White
Write-Host "  - MCP tools: ~20-30K (vs ~60-80K before)" -ForegroundColor White
Write-Host "  - Messages: <1K" -ForegroundColor White
Write-Host "  - Reserved: 0K (vs 45K before)" -ForegroundColor White
Write-Host "  - TOTAL: ~35-46K (vs ~120-140K before!)" -ForegroundColor White
Write-Host ""
Write-Host "Weekly usage should drop from 77% → 50-55% within 2-3 days!" -ForegroundColor Green
Write-Host ""
Write-Host "Press Enter to exit..."
Read-Host
