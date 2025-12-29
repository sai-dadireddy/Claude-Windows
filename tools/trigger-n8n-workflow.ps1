# Trigger n8n AI News Workflow via API
# This script triggers the workflow execution programmatically

$n8nUrl = "http://localhost:5678"

Write-Host "🚀 Triggering AI News Aggregator workflow..." -ForegroundColor Cyan

try {
    # Get list of workflows to find the workflow ID
    $workflows = Invoke-RestMethod -Uri "$n8nUrl/rest/workflows" -Method Get

    # Find our workflow by name
    $workflow = $workflows.data | Where-Object { $_.name -like "*AI News*" } | Select-Object -First 1

    if ($workflow) {
        Write-Host "✓ Found workflow: $($workflow.name) (ID: $($workflow.id))" -ForegroundColor Green

        # Execute the workflow
        $execution = Invoke-RestMethod -Uri "$n8nUrl/rest/workflows/$($workflow.id)/execute" -Method Post

        Write-Host "✓ Workflow execution started!" -ForegroundColor Green
        Write-Host "  Execution ID: $($execution.data.executionId)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "⏳ Waiting for execution to complete (this may take 2-3 minutes)..." -ForegroundColor Cyan

        # Poll for execution status
        $maxAttempts = 60  # 5 minutes max
        $attempt = 0
        $completed = $false

        while (-not $completed -and $attempt -lt $maxAttempts) {
            Start-Sleep -Seconds 5
            $attempt++

            $status = Invoke-RestMethod -Uri "$n8nUrl/rest/executions/$($execution.data.executionId)" -Method Get

            if ($status.data.finished) {
                $completed = $true
                if ($status.data.stoppedAt) {
                    Write-Host ""
                    Write-Host "✓ Workflow completed successfully!" -ForegroundColor Green
                    Write-Host "  Started: $($status.data.startedAt)" -ForegroundColor Gray
                    Write-Host "  Finished: $($status.data.stoppedAt)" -ForegroundColor Gray

                    # Show article count if available
                    if ($status.data.data) {
                        Write-Host ""
                        Write-Host "📊 Results:" -ForegroundColor Cyan
                        Write-Host "  Check articles.json for new articles" -ForegroundColor Yellow
                    }
                } else {
                    Write-Host ""
                    Write-Host "❌ Workflow failed!" -ForegroundColor Red
                }
            } else {
                Write-Host "  Still running... ($attempt/60)" -ForegroundColor Gray
            }
        }

        if (-not $completed) {
            Write-Host ""
            Write-Host "⚠ Timeout waiting for execution to complete" -ForegroundColor Yellow
            Write-Host "  Check n8n UI for status: $n8nUrl" -ForegroundColor Yellow
        }

    } else {
        Write-Host "❌ Could not find AI News workflow" -ForegroundColor Red
        Write-Host "  Available workflows:" -ForegroundColor Yellow
        $workflows.data | ForEach-Object { Write-Host "    - $($_.name)" -ForegroundColor Gray }
    }

} catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Make sure:" -ForegroundColor Yellow
    Write-Host "  1. n8n is running (http://localhost:5678)" -ForegroundColor Gray
    Write-Host "  2. The workflow is imported and saved" -ForegroundColor Gray
    Write-Host "  3. You have the correct API permissions" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
