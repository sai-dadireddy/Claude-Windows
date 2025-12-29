# Get-YouTubeTranscript.ps1
# PowerShell wrapper for YouTube transcript extraction

<#
.SYNOPSIS
    Extract YouTube video transcripts for research with Claude Code

.DESCRIPTION
    Downloads and saves YouTube video transcripts for analysis.
    Automatically stores in research directory and adds to Claude memory.

.PARAMETER VideoUrl
    YouTube video URL or video ID

.PARAMETER Language
    Transcript language code (default: en)

.PARAMETER Format
    Output format: text (with timestamps), clean (no timestamps), json (default: clean)

.PARAMETER OutputPath
    Custom output path (default: auto-generated in research folder)

.PARAMETER AddToMemory
    Add transcript summary to Claude memory (default: true)

.PARAMETER ShowMetadata
    Display video metadata and available transcripts

.EXAMPLE
    Get-YouTubeTranscript -VideoUrl "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

.EXAMPLE
    Get-YouTubeTranscript "dQw4w9WgXcQ" -Format text -Language es

.EXAMPLE
    Get-YouTubeTranscript "https://youtu.be/dQw4w9WgXcQ" -ShowMetadata
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$VideoUrl,

    [Parameter(Mandatory=$false)]
    [string]$Language = "en",

    [Parameter(Mandatory=$false)]
    [ValidateSet('text', 'clean', 'json')]
    [string]$Format = "clean",

    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "",

    [Parameter(Mandatory=$false)]
    [bool]$AddToMemory = $true,

    [Parameter(Mandatory=$false)]
    [switch]$ShowMetadata
)

# Configuration
$script:PythonScript = Join-Path $PSScriptRoot "youtube-transcript-extractor.py"
$script:ResearchDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\research\youtube-transcripts"
$script:MemoryDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude\memory"

function Test-Dependencies {
    # Check Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Error "Python not found. Please install Python 3.8+."
        return $false
    }

    # Check if youtube-transcript-api is installed
    $pipList = python -m pip list 2>$null | Out-String
    if ($pipList -notmatch 'youtube-transcript-api') {
        Write-Host "Installing youtube-transcript-api..." -ForegroundColor Cyan
        python -m pip install youtube-transcript-api --quiet

        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install youtube-transcript-api"
            return $false
        }

        Write-Host "[OK] youtube-transcript-api installed" -ForegroundColor Green
    }

    # Check Python script exists
    if (-not (Test-Path $script:PythonScript)) {
        Write-Error "Python script not found: $script:PythonScript"
        return $false
    }

    return $true
}

function Extract-VideoId {
    param([string]$Url)

    # Extract video ID from various YouTube URL formats
    if ($Url -match '(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})') {
        return $Matches[1]
    }
    elseif ($Url -match '^([a-zA-Z0-9_-]{11})$') {
        return $Url
    }

    throw "Could not extract video ID from: $Url"
}

function Get-TranscriptFileName {
    param(
        [string]$VideoId,
        [string]$Format
    )

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $extension = switch ($Format) {
        'json' { 'json' }
        default { 'txt' }
    }

    return "${VideoId}_${timestamp}.$extension"
}

function Add-ToMemory {
    param(
        [string]$VideoId,
        [string]$VideoUrl,
        [string]$TranscriptPath,
        [string]$Summary
    )

    if (-not (Test-Path $script:MemoryDir)) {
        New-Item -ItemType Directory -Path $script:MemoryDir -Force | Out-Null
    }

    $memoryEntry = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        type = "youtube_research"
        video_id = $VideoId
        video_url = $VideoUrl
        transcript_path = $TranscriptPath
        summary = $Summary
        tags = @("research", "youtube", "transcript")
    }

    # Append to research memory file
    $memoryFile = Join-Path $script:MemoryDir "research_youtube.json"

    $existingMemory = @()
    if (Test-Path $memoryFile) {
        $existingMemory = Get-Content $memoryFile -Raw | ConvertFrom-Json
    }

    $existingMemory += $memoryEntry
    $existingMemory | ConvertTo-Json -Depth 10 | Set-Content $memoryFile -Encoding UTF8

    Write-Host "[OK] Added to research memory" -ForegroundColor Green
}

function Show-TranscriptSummary {
    param([string]$TranscriptPath)

    if (Test-Path $TranscriptPath) {
        $content = Get-Content $TranscriptPath -Raw
        $wordCount = ($content -split '\s+').Count
        $lineCount = ($content -split "`n").Count

        Write-Host "`n[SUMMARY] Transcript Summary:" -ForegroundColor Cyan
        Write-Host "   File: $TranscriptPath" -ForegroundColor White
        Write-Host "   Words: $wordCount" -ForegroundColor White
        Write-Host "   Lines: $lineCount" -ForegroundColor White

        # Show first few lines as preview
        $preview = ($content -split "`n" | Select-Object -First 5) -join "`n"
        Write-Host "`n   Preview:" -ForegroundColor Yellow
        Write-Host "   $($preview.Substring(0, [Math]::Min(200, $preview.Length)))..." -ForegroundColor Gray
    }
}

# Main execution
try {
    Write-Host "`n[VIDEO] YouTube Transcript Extractor" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""

    # Check dependencies
    Write-Host "Checking dependencies..." -ForegroundColor Cyan
    if (-not (Test-Dependencies)) {
        exit 1
    }
    Write-Host "[OK] All dependencies ready" -ForegroundColor Green
    Write-Host ""

    # Extract video ID
    $videoId = Extract-VideoId -Url $VideoUrl
    $videoFullUrl = "https://www.youtube.com/watch?v=$videoId"
    Write-Host "Video ID: $videoId" -ForegroundColor Cyan
    Write-Host "URL: $videoFullUrl" -ForegroundColor Cyan
    Write-Host ""

    # Set output path if not provided
    if ([string]::IsNullOrEmpty($OutputPath)) {
        # Create research directory
        if (-not (Test-Path $script:ResearchDir)) {
            New-Item -ItemType Directory -Path $script:ResearchDir -Force | Out-Null
        }

        $fileName = Get-TranscriptFileName -VideoId $videoId -Format $Format
        $OutputPath = Join-Path $script:ResearchDir $fileName
    }

    # Build Python command
    $pythonArgs = @(
        $script:PythonScript,
        $VideoUrl,
        "--output", "`"$OutputPath`"",
        "--language", $Language,
        "--format", $Format
    )

    if ($ShowMetadata) {
        $pythonArgs += "--metadata"
    }

    # Execute Python script
    Write-Host "Extracting transcript..." -ForegroundColor Cyan
    $output = & python $pythonArgs 2>&1

    if ($LASTEXITCODE -eq 0) {
        # Show Python script output
        $output | ForEach-Object { Write-Host $_ }

        Write-Host ""
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green

        # Show summary
        Show-TranscriptSummary -TranscriptPath $OutputPath

        # Add to memory if requested
        if ($AddToMemory) {
            Write-Host "`nAdding to Claude memory..." -ForegroundColor Cyan
            $summary = "YouTube video transcript: $videoFullUrl"
            Add-ToMemory -VideoId $videoId -VideoUrl $videoFullUrl -TranscriptPath $OutputPath -Summary $summary
        }

        Write-Host "`n[SUCCESS] Transcript saved and ready for research!" -ForegroundColor Green
        Write-Host "`n[NEXT STEPS]:" -ForegroundColor Yellow
        Write-Host "   1. Open transcript: code `"$OutputPath`"" -ForegroundColor White
        Write-Host "   2. Ask Claude to analyze it: 'Analyze the YouTube transcript at $OutputPath'" -ForegroundColor White
        Write-Host "   3. Use in research: Include findings in your project documentation" -ForegroundColor White
        Write-Host ""

        # Return transcript path for scripting
        return @{
            Success = $true
            VideoId = $videoId
            VideoUrl = $videoFullUrl
            TranscriptPath = $OutputPath
            Format = $Format
        }
    }
    else {
        Write-Error "Failed to extract transcript"
        $output | ForEach-Object { Write-Error $_ }
        exit 1
    }
}
catch {
    Write-Error "Error: $($_.Exception.Message)"
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check if video has captions/subtitles enabled" -ForegroundColor Gray
    Write-Host "  2. Try a different language: -Language 'es' or 'auto'" -ForegroundColor Gray
    Write-Host "  3. Verify the video URL is correct" -ForegroundColor Gray
    Write-Host "  4. Run with -ShowMetadata to see available transcripts" -ForegroundColor Gray
    exit 1
}
