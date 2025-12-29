# Convert HTML to PDF using Chrome/Edge
# This script opens the HTML in a browser and prints it to PDF

param(
    [string]$HtmlFile = "..\claude-commands-cheatsheet.html",
    [string]$OutputFile = "..\claude-commands-cheatsheet.pdf"
)

$htmlPath = Resolve-Path $HtmlFile
$pdfPath = Join-Path (Split-Path $htmlPath -Parent) (Split-Path $OutputFile -Leaf)

Write-Host "Converting HTML to PDF..." -ForegroundColor Cyan
Write-Host "Source: $htmlPath" -ForegroundColor Gray
Write-Host "Output: $pdfPath" -ForegroundColor Gray
Write-Host ""

# Method 1: Try using Chrome with headless mode
$chromePaths = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($chrome) {
    Write-Host "✅ Found Chrome at: $chrome" -ForegroundColor Green
    Write-Host "Converting to PDF..." -ForegroundColor Yellow

    & $chrome --headless --disable-gpu --print-to-pdf="$pdfPath" "file:///$($htmlPath -replace '\\','/')"

    Start-Sleep -Seconds 2

    if (Test-Path $pdfPath) {
        Write-Host "✅ PDF created successfully!" -ForegroundColor Green
        Write-Host "Location: $pdfPath" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening PDF..." -ForegroundColor Cyan
        Start-Process $pdfPath
        exit 0
    }
}

# Method 2: Try using Edge
$edgePaths = @(
    "$env:ProgramFiles(x86)\Microsoft\Edge\Application\msedge.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
)

$edge = $edgePaths | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($edge) {
    Write-Host "✅ Found Edge at: $edge" -ForegroundColor Green
    Write-Host "Converting to PDF..." -ForegroundColor Yellow

    & $edge --headless --disable-gpu --print-to-pdf="$pdfPath" "file:///$($htmlPath -replace '\\','/')"

    Start-Sleep -Seconds 2

    if (Test-Path $pdfPath) {
        Write-Host "✅ PDF created successfully!" -ForegroundColor Green
        Write-Host "Location: $pdfPath" -ForegroundColor White
        Write-Host ""
        Write-Host "Opening PDF..." -ForegroundColor Cyan
        Start-Process $pdfPath
        exit 0
    }
}

# Method 3: Manual instructions
Write-Host "Could not find Chrome or Edge for automatic conversion" -ForegroundColor Red
Write-Host ""
Write-Host "Manual Instructions:" -ForegroundColor Yellow
Write-Host "1. Open the HTML file in your browser:" -ForegroundColor White
Write-Host "   $htmlPath" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Press Ctrl+P (Print)" -ForegroundColor White
Write-Host ""
Write-Host "3. Select Save as PDF as the destination" -ForegroundColor White
Write-Host ""
Write-Host "4. Save to:" -ForegroundColor White
Write-Host "   $pdfPath" -ForegroundColor Gray
Write-Host ""

# Open the HTML file in default browser
Write-Host "Opening HTML in your default browser..." -ForegroundColor Cyan
Start-Process $htmlPath

exit 1
