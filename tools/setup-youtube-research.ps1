# Setup YouTube Research Tools
# One-click setup for YouTube transcript extraction

Write-Host "`n🎥 YouTube Research Tools - Setup" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python..." -ForegroundColor Cyan
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "`n  Please install Python 3.8+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add Python to PATH' during installation`n" -ForegroundColor Yellow
    exit 1
}

# Check pip
Write-Host "`n[2/4] Checking pip..." -ForegroundColor Cyan
$pipVersion = python -m pip --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ pip found: $pipVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ pip not found!" -ForegroundColor Red
    exit 1
}

# Install youtube-transcript-api
Write-Host "`n[3/4] Installing youtube-transcript-api..." -ForegroundColor Cyan
$pipList = python -m pip list 2>$null | Out-String

if ($pipList -match 'youtube-transcript-api') {
    Write-Host "  ✓ youtube-transcript-api already installed" -ForegroundColor Green

    # Check for updates
    Write-Host "  → Checking for updates..." -ForegroundColor Gray
    python -m pip install --upgrade youtube-transcript-api --quiet
    Write-Host "  ✓ Package up to date" -ForegroundColor Green
} else {
    Write-Host "  → Installing package..." -ForegroundColor Yellow
    python -m pip install youtube-transcript-api

    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ youtube-transcript-api installed successfully" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Installation failed!" -ForegroundColor Red
        exit 1
    }
}

# Create research directories
Write-Host "`n[4/4] Creating research directories..." -ForegroundColor Cyan
$baseDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
$researchDir = Join-Path $baseDir "research\youtube-transcripts"
$memoryDir = Join-Path $baseDir "claude\memory"
$docsDir = Join-Path $baseDir "docs"

$directories = @($researchDir, $memoryDir, $docsDir)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Exists: $dir" -ForegroundColor Green
    }
}

# Test the installation
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Test with a video:" -ForegroundColor White
Write-Host "     Get-YouTubeTranscript `"https://www.youtube.com/watch?v=VIDEO_ID`"" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Or use the slash command in Claude Code:" -ForegroundColor White
Write-Host "     /research-video" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Read the guide:" -ForegroundColor White
Write-Host "     code `"$docsDir\youtube-research-guide.md`"" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 Quick Test:" -ForegroundColor Yellow
Write-Host "   python `"$baseDir\tools\youtube-transcript-extractor.py`" --help" -ForegroundColor White
Write-Host ""
