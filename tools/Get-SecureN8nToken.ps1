# Helper function to retrieve n8n API token from secure storage
# Returns the token for use in scripts

function Get-SecureN8nToken {
    try {
        # Method 1: Try cmdkey (Windows Credential Manager)
        $credentialName = "claude-code-n8n-api-token"

        # Check if credential exists using cmdkey
        $cmdkeyOutput = cmdkey /list:$credentialName 2>&1

        if ($cmdkeyOutput -match "Target: $credentialName") {
            # Credential exists, but cmdkey can't retrieve password
            # We need to use PowerShell's native credential retrieval

            # Try using [System.Net.NetworkCredential] with stored credential
            try {
                Add-Type -AssemblyName System.Security

                # Read credential using Windows API
                $target = $credentialName
                $nativeCred = [CredentialManagement.Credential]::Load($target)

                if ($nativeCred) {
                    return $nativeCred.Password
                }
            } catch {
                # Native method failed, try CredentialManager module
                if (Get-Module -ListAvailable -Name CredentialManager) {
                    Import-Module CredentialManager -ErrorAction SilentlyContinue
                    $cred = Get-StoredCredential -Target $credentialName -ErrorAction SilentlyContinue
                    if ($cred) {
                        return $cred.GetNetworkCredential().Password
                    }
                }
            }
        }

        # Method 2: Try environment variable
        if ($env:N8N_API_TOKEN) {
            return $env:N8N_API_TOKEN
        }

        # Method 3: Try .env file
        $envFile = Join-Path $PSScriptRoot "..\claude\projects\n8n\.env"
        if (Test-Path $envFile) {
            $content = Get-Content $envFile -Raw
            if ($content -match 'N8N_API_TOKEN=(.+)') {
                return $matches[1].Trim()
            }
        }

        # No token found
        return $null

    } catch {
        return $null
    }
}

# If run directly, output the token
if ($MyInvocation.InvocationName -ne '.') {
    $token = Get-SecureN8nToken
    if ($token) {
        Write-Host "Token retrieved successfully" -ForegroundColor Green
        return $token
    } else {
        exit 1
    }
}
