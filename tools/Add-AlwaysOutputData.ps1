# Add alwaysOutputData to all nodes in workflow JSON

$workflowPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\claude\projects\n8n\ai-news-aggregator\workflows\ai-news-free-rag-http.json"

Write-Host "Adding alwaysOutputData to all nodes..." -ForegroundColor Cyan

$json = Get-Content $workflowPath -Raw | ConvertFrom-Json

$nodesUpdated = 0

foreach ($node in $json.nodes) {
    if (-not $node.PSObject.Properties['alwaysOutputData']) {
        $node | Add-Member -MemberType NoteProperty -Name 'alwaysOutputData' -Value $true
        $nodesUpdated++
    } elseif ($node.alwaysOutputData -eq $false) {
        $node.alwaysOutputData = $true
        $nodesUpdated++
    }
}

$json | ConvertTo-Json -Depth 100 | Set-Content $workflowPath

Write-Host "SUCCESS: Updated $nodesUpdated nodes" -ForegroundColor Green
Write-Host "All nodes now have alwaysOutputData: true" -ForegroundColor Gray
