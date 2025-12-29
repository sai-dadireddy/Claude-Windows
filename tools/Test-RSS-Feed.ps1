# Test RSS Feed Structure
# Quick diagnostic for RSS parsing issues

param(
    [string]$Url = "https://openai.com/news/rss.xml"
)

Write-Host "Fetching RSS Feed..." -ForegroundColor Cyan
Write-Host "URL: $Url" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-WebRequest -Uri $Url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    $xml = $response.Content

    Write-Host "SUCCESS: Feed fetched" -ForegroundColor Green
    Write-Host "Content Length: $($xml.Length) characters" -ForegroundColor Gray
    Write-Host ""

    # Check feed type
    if ($xml -match '<rss') {
        Write-Host "Feed Type: RSS" -ForegroundColor Cyan
        $itemTag = "item"
    } elseif ($xml -match '<feed') {
        Write-Host "Feed Type: Atom" -ForegroundColor Cyan
        $itemTag = "entry"
    } else {
        Write-Host "Feed Type: Unknown" -ForegroundColor Red
        $itemTag = "unknown"
    }

    # Count items
    $itemMatches = [regex]::Matches($xml, "<$itemTag>")
    Write-Host "Item count: $($itemMatches.Count)" -ForegroundColor White
    Write-Host ""

    # Show first 2000 characters
    Write-Host "First 2000 characters:" -ForegroundColor Yellow
    Write-Host "=====================" -ForegroundColor Gray
    $preview = $xml.Substring(0, [Math]::Min(2000, $xml.Length))
    Write-Host $preview

} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
