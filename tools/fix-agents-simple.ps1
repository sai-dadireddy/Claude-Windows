# Simple Agent Frontmatter Fix
$fixed = 0

# Fix tools
Get-ChildItem "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\tools\*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch '^---') {
        $name = $_.BaseName -replace '-', ' '
        $front = "---`nname: `"$name`"`n---`n`n"
        Set-Content $_.FullName -Value ($front + $content) -NoNewline
        Write-Host "Fixed: $($_.Name)"
        $fixed++
    }
}

# Fix workflows
Get-ChildItem "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\workflows\*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch '^---') {
        $name = $_.BaseName -replace '-', ' '
        $front = "---`nname: `"$name`"`n---`n`n"
        Set-Content $_.FullName -Value ($front + $content) -NoNewline
        Write-Host "Fixed: $($_.Name)"
        $fixed++
    }
}

# Fix examples
Get-ChildItem "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\examples\*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -notmatch '^---') {
        $name = $_.BaseName -replace '-', ' '
        $front = "---`nname: `"$name`"`n---`n`n"
        Set-Content $_.FullName -Value ($front + $content) -NoNewline
        Write-Host "Fixed: $($_.Name)"
        $fixed++
    }
}

Write-Host "`nFixed $fixed files total"
