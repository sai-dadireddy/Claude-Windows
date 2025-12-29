# Trigger AI News Workflow and Wait for Completion
param([switch]$WaitForCompletion = $true)

$n8nUrl = "http://localhost:5678"
$ErrorActionPreference = "Stop"

Write-Host "AI News Aggregator - Automated Workflow" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Gray
Write-Host ""

try {
    # Step 1: Find the workflow
    Write-Host "[1/3] Finding AI News workflow..." -ForegroundColor Yellow
    $workflows = Invoke-RestMethod -Uri "$n8nUrl/rest/workflows" -Method Get
    $workflow = $workflows.data | Where-Object { $_.name -like "*AI News*" } | Select-Object -First 1

    if (-not $workflow) {
        Write-Host "ERROR: AI News workflow not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Available workflows:" -ForegroundColor Yellow
        $workflows.data | ForEach-Object { Write-Host "  - $($_.name)" -ForegroundColor Gray }
        exit 1
    }

    Write-Host "SUCCESS: Found $($workflow.name)" -ForegroundColor Green
    Write-Host "         ID: $($workflow.id)" -ForegroundColor Gray
    Write-Host ""

    # Step 2: Execute the workflow
    Write-Host "[2/3] Executing workflow..." -ForegroundColor Yellow
    $execution = Invoke-RestMethod -Uri "$n8nUrl/rest/workflows/$($workflow.id)/execute" -Method Post

    Write-Host "SUCCESS: Workflow started!" -ForegroundColor Green
    Write-Host "         Execution ID: $($execution.data.executionId)" -ForegroundColor Gray
    Write-Host ""

    if ($WaitForCompletion) {
        Write-Host "[3/3] Waiting for completion (may take 2-3 minutes)..." -ForegroundColor Cyan
        Write-Host ""

        $maxAttempts = 36
        $attempt = 0
        $completed = $false

        while (-not $completed -and $attempt -lt $maxAttempts) {
            Start-Sleep -Seconds 5
            $attempt++

            try {
                $status = Invoke-RestMethod -Uri "$n8nUrl/rest/executions/$($execution.data.executionId)" -Method Get

                if ($status.data.finished) {
                    $completed = $true

                    if ($status.data.stoppedAt) {
                        Write-Host ""
                        Write-Host "SUCCESS: Workflow completed!" -ForegroundColor Green
                        $duration = [math]::Round(((Get-Date $status.data.stoppedAt) - (Get-Date $status.data.startedAt)).TotalSeconds, 1)
                        Write-Host "         Duration: $duration seconds" -ForegroundColor Gray
                        Write-Host ""
                        Write-Host "RESULT_SUCCESS=$($execution.data.executionId)"
                        exit 0
                    } else {
                        Write-Host ""
                        Write-Host "ERROR: Workflow failed!" -ForegroundColor Red
                        Write-Host ""
                        Write-Host "RESULT_FAILED=$($execution.data.executionId)"
                        exit 1
                    }
                } else {
                    $elapsed = $attempt * 5
                    Write-Host "`r  Running... ${elapsed}s elapsed ($attempt/$maxAttempts)" -NoNewline -ForegroundColor Gray
                }
            } catch {
                Write-Host ""
                Write-Host "WARNING: Error checking status: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }

        if (-not $completed) {
            Write-Host ""
            Write-Host ""
            Write-Host "WARNING: Timeout waiting for completion" -ForegroundColor Yellow
            Write-Host "         Workflow is still running" -ForegroundColor Gray
            Write-Host "         Check n8n UI: $n8nUrl" -ForegroundColor Gray
            Write-Host ""
            Write-Host "RESULT_TIMEOUT=$($execution.data.executionId)"
            exit 2
        }
    }

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. n8n is running at $n8nUrl" -ForegroundColor Gray
    Write-Host "  2. Workflow is imported and saved" -ForegroundColor Gray
    Write-Host ""
    exit 1
}
