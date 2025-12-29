# Check n8n Workflow Execution Status
# Quick diagnostic tool

$apiToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4NTIzYjlkNy0yNzRiLTQyN2YtYjhjYi04MTQ2M2M0MzE5YTciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYwMzAxODQ0LCJleHAiOjE3NjgwMjEyMDB9.8Y_KCiW233I3uW2XyaUjZgZk9w3ik6xTSadzGPeo1ns"
$n8nUrl = "http://localhost:5678"

Write-Host "Checking Workflow Execution Status" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Gray
Write-Host ""

try {
    $headers = @{
        "X-N8N-API-KEY" = $apiToken
        "Content-Type" = "application/json"
    }

    # Get recent executions
    $executions = Invoke-RestMethod -Uri "$n8nUrl/api/v1/executions?limit=3" -Method Get -Headers $headers

    if ($executions.data.Count -eq 0) {
        Write-Host "No executions found!" -ForegroundColor Red
        Write-Host "The workflow may not have started." -ForegroundColor Yellow
        exit 1
    }

    $latest = $executions.data[0]

    Write-Host "Latest Execution:" -ForegroundColor Cyan
    Write-Host "  ID: $($latest.id)" -ForegroundColor Gray
    Write-Host "  Workflow: $($latest.workflowId)" -ForegroundColor Gray
    Write-Host "  Started: $($latest.startedAt)" -ForegroundColor Gray
    Write-Host "  Finished: $($latest.finished)" -ForegroundColor $(if ($latest.finished) { "Green" } else { "Yellow" })
    Write-Host "  Status: $($latest.status)" -ForegroundColor $(if ($latest.status -eq "success") { "Green" } elseif ($latest.status -eq "error") { "Red" } else { "Yellow" })
    Write-Host ""

    if ($latest.finished) {
        if ($latest.status -eq "success") {
            Write-Host "SUCCESS: Workflow completed!" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "ERROR: Workflow failed!" -ForegroundColor Red
            Write-Host "Check n8n UI for error details: $n8nUrl" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "RUNNING: Workflow still executing..." -ForegroundColor Yellow

        # Calculate elapsed time
        $startTime = [DateTime]::Parse($latest.startedAt)
        $elapsed = (Get-Date) - $startTime
        Write-Host "  Elapsed: $([math]::Round($elapsed.TotalMinutes, 1)) minutes" -ForegroundColor Gray
        exit 0
    }

} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
