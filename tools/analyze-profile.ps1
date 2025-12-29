$profilePath = 'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'

# Parse the file
$errors = $null
$tokens = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($profilePath, [ref]$tokens, [ref]$errors)

# Show errors
if ($errors) {
    Write-Host "`n=== PARSE ERRORS FOUND ===" -ForegroundColor Red
    foreach ($err in $errors) {
        Write-Host "`nError: $($err.Message)" -ForegroundColor Yellow
        Write-Host "Location: Line $($err.Extent.StartLineNumber), Column $($err.Extent.StartColumnNumber)" -ForegroundColor Cyan
        Write-Host "Code: $($err.Extent.Text)" -ForegroundColor Gray
    }
} else {
    Write-Host "No parse errors found" -ForegroundColor Green
}

# Find all try statements
$tryStatements = $ast.FindAll({ param($node) $node -is [System.Management.Automation.Language.TryStatementAst] }, $true)

Write-Host "`n=== TRY STATEMENT ANALYSIS ===" -ForegroundColor Cyan
Write-Host "Total try statements found: $($tryStatements.Count)"

foreach ($try in $tryStatements) {
    $line = $try.Extent.StartLineNumber
    $hasCatch = $try.CatchClauses.Count -gt 0
    $hasFinally = $null -ne $try.Finally

    if (-not $hasCatch -and -not $hasFinally) {
        Write-Host "`nINCOMPLETE TRY at line $line - NO CATCH OR FINALLY!" -ForegroundColor Red
        Write-Host "Start: $($try.Extent.Text.Substring(0, [Math]::Min(100, $try.Extent.Text.Length)))" -ForegroundColor Gray
    }
}
