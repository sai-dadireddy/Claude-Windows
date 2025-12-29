# Pilot - Autonomous Beads Task Executor
# PowerShell launcher for Windows

param(
    [switch]$Watch,
    [switch]$List,
    [int]$Interval = 30
)

$ScriptPath = "$env:USERPROFILE\.claude\scripts\pilot.py"

if (-not (Test-Path $ScriptPath)) {
    Write-Error "pilot.py not found at $ScriptPath"
    exit 1
}

$args = @()
if ($Watch) { $args += "--watch" }
if ($List) { $args += "--list" }
if ($Interval -ne 30) { $args += "--interval", $Interval }

python $ScriptPath @args
