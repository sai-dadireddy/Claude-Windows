# Test Startup Features
# Verifies all enhanced startup components work correctly

Write-Host "`n🧪 Testing Enhanced Startup Features" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

$baseDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
$passed = 0
$failed = 0

# Test 1: Style Selector Script
Write-Host "[Test 1] Style Selector Script..." -ForegroundColor Cyan
$styleSelectorPath = Join-Path $baseDir "tools\select-output-style.ps1"
if (Test-Path $styleSelectorPath) {
    Write-Host "  ✓ Script exists" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ Script missing!" -ForegroundColor Red
    $failed++
}

# Test 2: Output Style Files
Write-Host "`n[Test 2] Output Style Files..." -ForegroundColor Cyan
$stylesDir = Join-Path $baseDir ".claude\output-styles"
$requiredStyles = @("fun-coworker.md", "professional.md", "teacher.md")

foreach ($style in $requiredStyles) {
    $stylePath = Join-Path $stylesDir $style
    if (Test-Path $stylePath) {
        Write-Host "  ✓ $style exists" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ $style missing!" -ForegroundColor Red
        $failed++
    }
}

# Test 3: PowerShell Profile Integration
Write-Host "`n[Test 3] PowerShell Profile Integration..." -ForegroundColor Cyan
$profilePath = "$HOME\OneDrive - ERPA\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw

    # Check for style selector call
    if ($profileContent -match 'select-output-style\.ps1') {
        Write-Host "  ✓ Style selector integrated" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ Style selector not integrated!" -ForegroundColor Red
        $failed++
    }

    # Check for AI news
    if ($profileContent -match 'AI News Flash') {
        Write-Host "  ✓ AI news integrated" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ AI news not integrated!" -ForegroundColor Red
        $failed++
    }
} else {
    Write-Host "  ✗ PowerShell profile not found!" -ForegroundColor Red
    $failed += 2
}

# Test 4: CLAUDE.md Configuration
Write-Host "`n[Test 4] CLAUDE.md Configuration..." -ForegroundColor Cyan
$claudeMdPath = Join-Path $baseDir "CLAUDE.md"
if (Test-Path $claudeMdPath) {
    $claudeContent = Get-Content $claudeMdPath -Raw

    # Check for output style loader
    if ($claudeContent -match 'output-style-loader\.md') {
        Write-Host "  ✓ Style loader configured" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ Style loader not configured!" -ForegroundColor Red
        $failed++
    }

    # Check for auto god mode detection
    if ($claudeContent -match 'auto-godmode-detection\.md') {
        Write-Host "  ✓ Auto god mode configured" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ Auto god mode not configured!" -ForegroundColor Red
        $failed++
    }
} else {
    Write-Host "  ✗ CLAUDE.md not found!" -ForegroundColor Red
    $failed += 2
}

# Test 5: Autonomous Mode Files
Write-Host "`n[Test 5] Autonomous Mode..." -ForegroundColor Cyan
$autonomousFiles = @(
    ".claude\commands\autonomous.md",
    ".claude\commands\godmode.md",
    ".claude\commands\turbo.md",
    ".claude\commands\stop.md"
)

foreach ($file in $autonomousFiles) {
    $filePath = Join-Path $baseDir $file
    if (Test-Path $filePath) {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ $file missing!" -ForegroundColor Red
        $failed++
    }
}

# Test 6: Global Instructions
Write-Host "`n[Test 6] Global Instructions..." -ForegroundColor Cyan
$instructionFiles = @(
    "global-instructions\output-style-loader.md",
    "global-instructions\auto-godmode-detection.md",
    "global-instructions\personality-tone.md",
    "global-instructions\autonomous-mode.md"
)

foreach ($file in $instructionFiles) {
    $filePath = Join-Path $baseDir $file
    if (Test-Path $filePath) {
        Write-Host "  ✓ $file exists" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ $file missing!" -ForegroundColor Red
        $failed++
    }
}

# Summary
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "📊 Test Results:" -ForegroundColor Cyan
Write-Host "  ✓ Passed: $passed" -ForegroundColor Green
Write-Host "  ✗ Failed: $failed" -ForegroundColor Red

if ($failed -eq 0) {
    Write-Host "`n🎉 All tests passed! System ready to use." -ForegroundColor Green
    Write-Host "`n💡 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Close this PowerShell window" -ForegroundColor White
    Write-Host "  2. Open a NEW PowerShell window (to reload profile)" -ForegroundColor White
    Write-Host "  3. Run: scl" -ForegroundColor White
    Write-Host "  4. You should see:" -ForegroundColor White
    Write-Host "     - Style selector menu" -ForegroundColor Gray
    Write-Host "     - AI news flash" -ForegroundColor Gray
    Write-Host "     - Fun personality from Claude" -ForegroundColor Gray
} else {
    Write-Host "`n⚠ Some tests failed. Review the errors above." -ForegroundColor Yellow
    Write-Host "`n🔧 Troubleshooting:" -ForegroundColor Cyan
    Write-Host "  - Re-run the setup scripts" -ForegroundColor White
    Write-Host "  - Check file paths are correct" -ForegroundColor White
    Write-Host "  - Verify PowerShell profile reloaded" -ForegroundColor White
}

Write-Host ""
