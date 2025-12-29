# Monitor n8n Workflow Completion
# Polls articles.json and notifies when workflow completes
# Version: 1.0

param(
    [int]$PollIntervalSeconds = 30,
    [int]$MaxWaitMinutes = 15
)

$articlesPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude\projects\n8n\ai-news-aggregator\data\articles.json"
$maxAttempts = [math]::Ceiling(($MaxWaitMinutes * 60) / $PollIntervalSeconds)
$attempt = 0

Write-Host "Monitoring AI News Workflow Completion" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Gray
Write-Host ""
Write-Host "Checking: $articlesPath" -ForegroundColor Gray
Write-Host "Poll interval: $PollIntervalSeconds seconds" -ForegroundColor Gray
Write-Host "Max wait: $MaxWaitMinutes minutes" -ForegroundColor Gray
Write-Host ""

while ($attempt -lt $maxAttempts) {
    $attempt++
    $elapsed = $attempt * $PollIntervalSeconds

    if (Test-Path $articlesPath) {
        $data = Get-Content $articlesPath | ConvertFrom-Json
        $totalArticles = $data.metadata.totalArticles

        if ($totalArticles -gt 0) {
            Write-Host ""
            Write-Host "SUCCESS: Workflow completed!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Results:" -ForegroundColor Cyan
            Write-Host "  Total articles: $totalArticles" -ForegroundColor White
            Write-Host "  Last updated: $($data.metadata.lastUpdated)" -ForegroundColor Gray
            Write-Host "  Average relevance: $($data.statistics.avgRelevance)/10" -ForegroundColor Gray
            Write-Host ""
            Write-Host "Next step: Type '/ai-news' to view dashboard!" -ForegroundColor Yellow
            Write-Host ""
            exit 0
        }
    }

    Write-Host "[${elapsed}s] Still running... ($attempt/$maxAttempts)" -ForegroundColor Gray
    Start-Sleep -Seconds $PollIntervalSeconds
}

Write-Host ""
Write-Host "TIMEOUT: Workflow exceeded $MaxWaitMinutes minutes" -ForegroundColor Yellow
Write-Host "Check n8n UI for status: http://localhost:5678" -ForegroundColor Gray
Write-Host ""
exit 1
