# Claude Code Headless Mode Wrapper
# Provides convenient interface for headless automation

param(
    [Parameter(Mandatory=$true)]
    [string]$Task,

    [switch]$SkipPermissions,
    [switch]$Verbose,
    [switch]$DryRun,
    [switch]$SkipHooks,
    [string]$Model = "claude-sonnet-4-5",
    [string]$ConfigDir = "",
    [string]$OutputFile = ""
)

Write-Host "🤖 Claude Code Headless Mode" -ForegroundColor Cyan
Write-Host "Task: $Task" -ForegroundColor Gray
Write-Host ""

# Build command arguments
$args = @()

# Add task with -p flag
$args += "-p"
$args += "`"$Task`""

# Add optional flags
if ($SkipPermissions) {
    $args += "--skip-permissions"
    Write-Host "✓ Skip permissions: Enabled" -ForegroundColor Yellow
}

if ($Verbose) {
    $args += "--verbose"
    Write-Host "✓ Verbose mode: Enabled" -ForegroundColor Yellow
}

if ($DryRun) {
    $args += "--dry-run"
    Write-Host "✓ Dry run: Enabled (preview only)" -ForegroundColor Yellow
}

if ($SkipHooks) {
    $args += "--skip-hooks"
    Write-Host "✓ Skip hooks: Enabled" -ForegroundColor Yellow
}

if ($Model -ne "claude-sonnet-4-5") {
    $args += "--model"
    $args += $Model
    Write-Host "✓ Model: $Model" -ForegroundColor Yellow
}

if ($ConfigDir) {
    $args += "--config-dir"
    $args += $ConfigDir
    Write-Host "✓ Config directory: $ConfigDir" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Executing Claude Code..." -ForegroundColor Cyan

# Execute Claude Code
try {
    $result = & claude @args 2>&1

    # Save output to file if specified
    if ($OutputFile) {
        $result | Out-File -FilePath $OutputFile -Encoding UTF8
        Write-Host ""
        Write-Host "✅ Output saved to: $OutputFile" -ForegroundColor Green
    }

    # Display result
    Write-Host ""
    Write-Host $result

    Write-Host ""
    Write-Host "✅ Task completed successfully" -ForegroundColor Green

} catch {
    Write-Host ""
    Write-Host "❌ Error executing Claude Code:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
