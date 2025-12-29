#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Log events to security-audit.log and operations.log

.DESCRIPTION
    PowerShell wrapper for the Python logging implementation.
    Provides easy logging functions for Claude Code operations.

.PARAMETER EventType
    Type of event to log (file_access, command_execution, agent_launch, etc.)

.PARAMETER Details
    Hashtable containing event details

.PARAMETER LogType
    Type of log (security or operations)

.EXAMPLE
    .\log-event.ps1 -LogType security -EventType file_access -Details @{file_path="test.txt"; operation="read"; result="success"}

.EXAMPLE
    .\log-event.ps1 -LogType operations -EventType agent_launch -Details @{agent_type="security-code-reviewer"; task="Review auth module"; status="started"}
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('security', 'operations')]
    [string]$LogType,

    [Parameter(Mandatory=$true)]
    [string]$EventType,

    [Parameter(Mandatory=$true)]
    [hashtable]$Details,

    [string]$Severity = "info",
    [int]$DurationMs = $null
)

# Get the Python script path
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "log-event-helper.py"

# Convert hashtable to JSON
$detailsJson = $Details | ConvertTo-Json -Compress

# Escape quotes for command line
$detailsJson = $detailsJson -replace '"', '\"'

# Build command
$command = "python `"$pythonScript`" --log-type $LogType --event-type $EventType --details `"$detailsJson`""

if ($Severity) {
    $command += " --severity $Severity"
}

if ($DurationMs) {
    $command += " --duration-ms $DurationMs"
}

# Execute logging
Invoke-Expression $command
