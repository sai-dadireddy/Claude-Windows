# Check articles.json status

$articlesPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude\projects\n8n\ai-news-aggregator\data\articles.json"

if (Test-Path $articlesPath) {
    Write-Host "SUCCESS: articles.json exists" -ForegroundColor Green
    Write-Host ""

    $data = Get-Content $articlesPath | ConvertFrom-Json

    Write-Host "Total articles:" $data.metadata.totalArticles -ForegroundColor Cyan
    Write-Host "Last updated:" $data.metadata.lastUpdated -ForegroundColor Gray
    Write-Host "Avg relevance:" $data.statistics.avgRelevance"/10" -ForegroundColor Gray
    Write-Host ""

    if ($data.metadata.totalArticles -gt 0) {
        Write-Host "First 3 articles:" -ForegroundColor Yellow
        $data.articles | Select-Object -First 3 | ForEach-Object {
            Write-Host "  - $($_.title)" -ForegroundColor White
            Write-Host "    Source: $($_.source) | Score: $($_.relevanceScore)" -ForegroundColor Gray
            Write-Host ""
        }
    } else {
        Write-Host "WARNING: 0 articles in file!" -ForegroundColor Red
    }
} else {
    Write-Host "ERROR: articles.json not found!" -ForegroundColor Red
}
