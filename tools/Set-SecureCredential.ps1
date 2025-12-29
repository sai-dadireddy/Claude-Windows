# Secure Credential Management for n8n API
# Uses Windows Credential Manager for secure storage
# Version: 1.0

param(
    [Parameter(Mandatory=$false)]
    [string]$CredentialName = "n8n-api-token",

    [Parameter(Mandatory=$false)]
    [string]$ApiToken,

    [switch]$Get,
    [switch]$Remove
)

$ErrorActionPreference = "Stop"

Write-Host "Secure Credential Manager" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Gray
Write-Host ""

# Function to store credential securely
function Set-SecureCredential {
    param($Name, $Token)

    try {
        # Store in Windows Credential Manager
        cmdkey /generic:"claude-code-$Name" /user:"n8n" /pass:"$Token" | Out-Null

        Write-Host "SUCCESS: Credential stored securely" -ForegroundColor Green
        Write-Host "  Name: $Name" -ForegroundColor Gray
        Write-Host "  Location: Windows Credential Manager" -ForegroundColor Gray
        Write-Host ""
        Write-Host "To retrieve: .\Set-SecureCredential.ps1 -Get" -ForegroundColor Yellow

        return $true
    } catch {
        Write-Host "ERROR: Failed to store credential" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Gray
        return $false
    }
}

# Function to retrieve credential securely
function Get-SecureCredential {
    param($Name)

    try {
        # Try to retrieve from Windows Credential Manager
        $credentialName = "claude-code-$Name"

        # Use cmdkey to list credentials
        $cmdkeyOutput = cmdkey /list:$credentialName 2>&1

        if ($cmdkeyOutput -match "Currently stored credentials") {
            Write-Host "SUCCESS: Credential found" -ForegroundColor Green
            Write-Host "  Name: $Name" -ForegroundColor Gray
            Write-Host "  Location: Windows Credential Manager" -ForegroundColor Gray
            Write-Host ""
            Write-Host "To use in PowerShell:" -ForegroundColor Yellow
            Write-Host '  $cred = Get-StoredCredential -Target "claude-code-' + $Name + '"' -ForegroundColor Gray
            Write-Host '  $token = $cred.GetNetworkCredential().Password' -ForegroundColor Gray

            return $true
        } else {
            Write-Host "WARNING: Credential not found" -ForegroundColor Yellow
            Write-Host "  Run: .\Set-SecureCredential.ps1 -ApiToken 'your-token'" -ForegroundColor Gray
            return $false
        }
    } catch {
        Write-Host "ERROR: Failed to retrieve credential" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Gray
        return $false
    }
}

# Function to remove credential
function Remove-SecureCredential {
    param($Name)

    try {
        cmdkey /delete:"claude-code-$Name" | Out-Null
        Write-Host "SUCCESS: Credential removed" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "WARNING: Credential not found or already removed" -ForegroundColor Yellow
        return $false
    }
}

# Main logic
if ($Get) {
    Get-SecureCredential -Name $CredentialName

} elseif ($Remove) {
    Remove-SecureCredential -Name $CredentialName

} elseif ($ApiToken) {
    Set-SecureCredential -Name $CredentialName -Token $ApiToken

} else {
    Write-Host "Secure Credential Manager for n8n API" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  Store credential:" -ForegroundColor White
    Write-Host "    .\Set-SecureCredential.ps1 -ApiToken 'your-n8n-api-token'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Retrieve credential:" -ForegroundColor White
    Write-Host "    .\Set-SecureCredential.ps1 -Get" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Remove credential:" -ForegroundColor White
    Write-Host "    .\Set-SecureCredential.ps1 -Remove" -ForegroundColor Gray
    Write-Host ""
    Write-Host "How to get n8n API token:" -ForegroundColor Yellow
    Write-Host "  1. Open n8n: http://localhost:5678" -ForegroundColor Gray
    Write-Host "  2. Go to Settings > API" -ForegroundColor Gray
    Write-Host "  3. Create new API key" -ForegroundColor Gray
    Write-Host "  4. Copy the token" -ForegroundColor Gray
    Write-Host "  5. Run: .\Set-SecureCredential.ps1 -ApiToken 'paste-token-here'" -ForegroundColor Gray
    Write-Host ""

    exit 0
}
