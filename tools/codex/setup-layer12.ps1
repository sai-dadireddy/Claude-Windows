<#
.SYNOPSIS
Exports the Codex Layer 12 starter kit into a ready-to-share bundle.

.DESCRIPTION
Copies the canonical Codex configuration, instructions, and examples listed in
.ai-workspace/codex/starter-kit/manifest.json into a destination folder. The
script also includes the onboarding message, copies the Codex startup prompt to
the clipboard (unless skipped), and prints a quick FAQ recap for the recipient.

.PARAMETER Destination
Optional output folder. Defaults to ./starter-kit-output relative to the current
working directory when not provided.

.PARAMETER SkipClipboard
Skip copying the Codex startup command to the clipboard.

.PARAMETER NoBanner
Suppress the friendly banner output.

.EXAMPLE
pwsh tools/codex/setup-layer12.ps1

.EXAMPLE
pwsh tools/codex/setup-layer12.ps1 -Destination C:\Share\CodexKit -SkipClipboard
#>
[CmdletBinding()]
param(
    [string]$Destination,
    [switch]$SkipClipboard,
    [switch]$NoBanner
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Banner {
    param([string]$Message)

    if ($NoBanner) { return }
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
}

try {
    $scriptPath = $MyInvocation.MyCommand.Path
    $scriptDir = Split-Path -Parent $scriptPath
    $repoRoot = (Resolve-Path (Join-Path $scriptDir "..\..")).Path

    if (-not $Destination) {
        $Destination = Join-Path (Get-Location) "starter-kit-output"
    } elseif (-not [System.IO.Path]::IsPathRooted($Destination)) {
        $Destination = Join-Path (Get-Location) $Destination
    }

    $starterKitDir = Join-Path $repoRoot ".ai-workspace\codex\starter-kit"
    $manifestPath = Join-Path $starterKitDir "manifest.json"
    $readmePath = Join-Path $starterKitDir "README.md"
    $onboardingPath = Join-Path $starterKitDir "onboarding-message.txt"

    if (-not (Test-Path $manifestPath)) {
        throw "Starter kit manifest not found at $manifestPath"
    }

    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    if (-not $manifest.files) {
        throw "Manifest does not contain any file entries."
    }

    if (-not (Test-Path $Destination)) {
        New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }

    $copiedItems = @()
    foreach ($entry in $manifest.files) {
        $sourcePath = Join-Path $repoRoot $entry.source
        if (-not (Test-Path $sourcePath)) {
            Write-Warning "Source missing: $($entry.source)"
            continue
        }

        $targetPath = Join-Path $Destination $entry.target
        $targetDir = Split-Path -Parent $targetPath
        if (-not (Test-Path $targetDir)) {
            New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
        }

        Copy-Item -Path $sourcePath -Destination $targetPath -Force

        $copiedItems += [pscustomobject]@{
            Source      = $entry.source
            Destination = $entry.target
            Label       = $entry.label
        }
    }

    if (Test-Path $readmePath) {
        Copy-Item -Path $readmePath -Destination (Join-Path $Destination "README.md") -Force
    }

    if (Test-Path $onboardingPath) {
        Copy-Item -Path $onboardingPath -Destination (Join-Path $Destination "onboarding-message.txt") -Force
    }

    $startupSource = ".ai-workspace\codex\STARTUP-COMMAND.txt"
    $startupPath = Join-Path $repoRoot $startupSource
    $startupPrompt = $null
    if (Test-Path $startupPath) {
        $startupPrompt = Get-Content $startupPath -Raw
        $destPromptPath = Join-Path $Destination "prompts\STARTUP-COMMAND.txt"
        $destPromptDir = Split-Path -Parent $destPromptPath
        if (-not (Test-Path $destPromptDir)) {
            New-Item -ItemType Directory -Path $destPromptDir -Force | Out-Null
        }
        Copy-Item -Path $startupPath -Destination $destPromptPath -Force

        if (-not $SkipClipboard) {
            try {
                Set-Clipboard -Value $startupPrompt
            } catch {
                Write-Warning "Unable to copy startup command to clipboard: $($_.Exception.Message)"
            }
        }
    } else {
        Write-Warning "Startup command file not found at $startupSource"
    }

    Write-Banner "Codex Layer 12 starter kit exported"

    Write-Host "[INFO] Destination: $Destination" -ForegroundColor Cyan
    Write-Host "[INFO] Files exported:" -ForegroundColor Cyan
    foreach ($item in $copiedItems) {
        Write-Host ("  - {0} -> {1}" -f $item.Source, $item.Destination) -ForegroundColor White
        if ($item.Label) {
            Write-Host ("    {0}" -f $item.Label) -ForegroundColor DarkGray
        }
    }

    if ($startupPrompt) {
        Write-Host ""
        Write-Host "[INFO] Codex startup prompt:" -ForegroundColor Cyan
        Write-Host ("  {0}" -f $startupPrompt.Trim()) -ForegroundColor White
        if (-not $SkipClipboard) {
            Write-Host "  (Copied to clipboard for easy sharing.)" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "[INFO] Share the onboarding message located at: onboarding-message.txt" -ForegroundColor Cyan
    Write-Host "       It includes quick instructions for new Codex operators." -ForegroundColor DarkGray

    Write-Host ""
    Write-Host "[NEXT] Zip the contents of $Destination and send it with the onboarding message." -ForegroundColor Yellow
    Write-Host "[NEXT] Recipient runs: pwsh tools/codex/setup-layer12.ps1 -Destination <path>" -ForegroundColor Yellow
    Write-Host ""
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
