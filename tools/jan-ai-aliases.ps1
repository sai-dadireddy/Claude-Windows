# Jan AI PowerShell Aliases
# Quick commands for managing Jan AI local LLM

# Start Jan AI
function jan-start {
    $process = Get-Process "jan" -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "✓ Jan AI already running" -ForegroundColor Green
        jan-status
    } else {
        Write-Host "Starting Jan AI..." -ForegroundColor Cyan
        Start-Process "$env:LOCALAPPDATA\Programs\jan\jan.exe" -WindowStyle Minimized
        Write-Host "✓ Jan AI starting (will be minimized to tray)" -ForegroundColor Green
        Write-Host "  API Server will start automatically if configured" -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        jan-status
    }
}

# Stop Jan AI
function jan-stop {
    $process = Get-Process "jan" -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Stopping Jan AI..." -ForegroundColor Yellow
        Stop-Process -Name "jan" -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
        Write-Host "✓ Jan AI stopped" -ForegroundColor Green
        Write-Host "  RAM freed" -ForegroundColor Cyan
    } else {
        Write-Host "✗ Jan AI not running" -ForegroundColor Yellow
    }
}

# Check Jan AI status
function jan-status {
    $process = Get-Process "jan" -ErrorAction SilentlyContinue

    Write-Host "`nJan AI Status:" -ForegroundColor Cyan
    Write-Host "─────────────────────" -ForegroundColor Gray

    if ($process) {
        $mem = [math]::Round($process.WorkingSet64 / 1GB, 2)
        Write-Host "✓ Process: Running" -ForegroundColor Green
        Write-Host "  RAM: ${mem} GB" -ForegroundColor White
        Write-Host "  PID: $($process.Id)" -ForegroundColor Gray

        # Check API server
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:1337/v1/models" `
                -Headers @{"Authorization"="Bearer jan-local-key"} `
                -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop

            $models = ($response.Content | ConvertFrom-Json).data
            Write-Host "✓ API Server: Running (port 1337)" -ForegroundColor Green
            Write-Host "  Models loaded: $($models.Count)" -ForegroundColor White
            foreach ($model in $models) {
                Write-Host "    - $($model.id)" -ForegroundColor Gray
            }
        } catch {
            Write-Host "✗ API Server: Not responding" -ForegroundColor Red
            Write-Host "  Start server in: Settings → Local API Server" -ForegroundColor Yellow
        }
    } else {
        Write-Host "✗ Process: Not running" -ForegroundColor Yellow
        Write-Host "✗ API Server: Not available" -ForegroundColor Yellow
        Write-Host "`n  Run: jan-start" -ForegroundColor Cyan
    }
    Write-Host ""
}

# Restart Jan AI
function jan-restart {
    Write-Host "Restarting Jan AI..." -ForegroundColor Cyan
    jan-stop
    Start-Sleep -Seconds 2
    jan-start
}

# Test Jan AI code generation
function jan-test {
    Write-Host "`nTesting Jan AI code generation..." -ForegroundColor Cyan
    Write-Host "─────────────────────────────────" -ForegroundColor Gray

    try {
        $body = @{
            model = "Qwen2_5-Coder-7B-Instruct-Q4_K_M"
            messages = @(
                @{
                    role = "user"
                    content = "Write a Python function to calculate fibonacci"
                }
            )
            max_tokens = 200
            temperature = 0.7
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "http://localhost:1337/v1/chat/completions" `
            -Method Post `
            -Headers @{
                "Authorization"="Bearer jan-local-key"
                "Content-Type"="application/json"
            } `
            -Body $body `
            -TimeoutSec 30

        Write-Host "✓ Generation successful!" -ForegroundColor Green
        Write-Host "`nResponse:" -ForegroundColor Cyan
        Write-Host $response.choices[0].message.content -ForegroundColor White
        Write-Host "`nTokens used: $($response.usage.total_tokens)" -ForegroundColor Gray

    } catch {
        Write-Host "✗ Test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
        Write-Host "  1. Check Jan AI is running: jan-status" -ForegroundColor White
        Write-Host "  2. Ensure API server is started in Settings" -ForegroundColor White
        Write-Host "  3. Verify model is downloaded (Qwen2.5-Coder-7B)" -ForegroundColor White
    }
}

# Display help
function jan-help {
    Write-Host "`nJan AI Quick Commands:" -ForegroundColor Cyan
    Write-Host "──────────────────────────" -ForegroundColor Gray
    Write-Host "  jan-start   " -ForegroundColor Green -NoNewline
    Write-Host "  - Start Jan AI" -ForegroundColor White
    Write-Host "  jan-stop    " -ForegroundColor Red -NoNewline
    Write-Host "  - Stop Jan AI" -ForegroundColor White
    Write-Host "  jan-restart " -ForegroundColor Yellow -NoNewline
    Write-Host "  - Restart Jan AI" -ForegroundColor White
    Write-Host "  jan-status  " -ForegroundColor Cyan -NoNewline
    Write-Host "  - Check status" -ForegroundColor White
    Write-Host "  jan-test    " -ForegroundColor Magenta -NoNewline
    Write-Host "  - Test code generation" -ForegroundColor White
    Write-Host "  jan-help    " -ForegroundColor White -NoNewline
    Write-Host "  - Show this help" -ForegroundColor White
    Write-Host ""
}

Write-Host "Jan AI aliases loaded! Type " -NoNewline -ForegroundColor Gray
Write-Host "jan-help" -NoNewline -ForegroundColor Cyan
Write-Host " for commands" -ForegroundColor Gray
