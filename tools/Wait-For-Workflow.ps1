# Wait for workflow to complete and check results
# Run this after workflow finishes

Write-Host "Checking workflow results..." -ForegroundColor Cyan
Write-Host ""

$articlesPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude\projects\n8n\ai-news-aggregator\data\articles.json"

if (Test-Path $articlesPath) {
    $data = Get-Content $articlesPath | ConvertFrom-Json

    Write-Host "SUCCESS: articles.json updated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Results:" -ForegroundColor Cyan
    Write-Host "  Total articles: $($data.metadata.totalArticles)" -ForegroundColor White
    Write-Host "  Last updated: $($data.metadata.lastUpdated)" -ForegroundColor Gray
    Write-Host "  Avg relevance: $($data.statistics.avgRelevance)/10" -ForegroundColor Gray
    Write-Host ""

    if ($data.metadata.totalArticles -gt 0) {
        Write-Host "Top 3 articles:" -ForegroundColor Yellow
        $data.articles | Select-Object -First 3 | ForEach-Object {
            Write-Host "  ✓ $($_.title)" -ForegroundColor White
            Write-Host "    Source: $($_.source) | Score: $($_.relevanceScore)/10" -ForegroundColor Gray
            Write-Host ""
        }

        Write-Host "Next step: Type '/ai-news' in Claude Code!" -ForegroundColor Green
    }
} else {
    Write-Host "Waiting for workflow to complete..." -ForegroundColor Yellow
}
