# Auto-Start Claude Code with Initial Command
# This script launches Claude and automatically sends the /load-global command

param(
    [string]$InitialCommand = "/load-global",
    [int]$DelaySeconds = 3
)

# Add required assembly for SendKeys
Add-Type -AssemblyName System.Windows.Forms

Write-Host "`n🚀 Auto-launching Claude Code..." -ForegroundColor Green
Write-Host "  Initial command: $InitialCommand" -ForegroundColor Cyan
Write-Host "  Delay: $DelaySeconds seconds" -ForegroundColor Gray
Write-Host ""

# Start Claude Code in background
$process = Start-Process -FilePath "claude" -PassThru -WindowStyle Normal

Write-Host "  ⏳ Waiting for Claude to start..." -ForegroundColor Yellow

# Wait for process to start and UI to be ready
Start-Sleep -Seconds $DelaySeconds

Write-Host "  📝 Sending command: $InitialCommand" -ForegroundColor Cyan

# Send the command
[System.Windows.Forms.SendKeys]::SendWait($InitialCommand)
Start-Sleep -Milliseconds 500

# Send Enter key
[System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

Write-Host "  ✅ Command sent successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Claude Code should now be running $InitialCommand..." -ForegroundColor Cyan
Write-Host ""
