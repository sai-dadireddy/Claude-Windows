# Fix Agent Frontmatter - Add missing 'name' field
# Fixes the 62 agent parse errors by adding proper frontmatter

$agentDirs = @(
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\tools",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\workflows",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\examples"
)

$fixed = 0
$errors = 0

foreach ($dir in $agentDirs) {
    if (-not (Test-Path $dir)) {
        Write-Warning "Directory not found: $dir"
        continue
    }

    $mdFiles = Get-ChildItem -Path $dir -Filter "*.md" -File

    foreach ($file in $mdFiles) {
        try {
            $content = Get-Content $file.FullName -Raw

            # Skip if already has frontmatter with name field
            if ($content -match '(?s)^---.*?name:.*?---') {
                Write-Host "✓ Already has name field: $($file.Name)" -ForegroundColor Green
                continue
            }

            # Generate name from filename
            $baseName = $file.BaseName
            $displayName = ($baseName -replace '-', ' ' |
                           ForEach-Object { $_.Split(' ') | ForEach-Object {
                               $_.Substring(0,1).ToUpper() + $_.Substring(1).ToLower()
                           } }) -join ' '

            # Check if file has frontmatter at all
            if ($content -match '^---') {
                # Has frontmatter but missing name - add it
                $content = $content -replace '^---\s*\n', "---`nname: `"$displayName`"`n"
            } else {
                # No frontmatter at all - add complete frontmatter
                $newFrontmatter = "---`nname: `"$displayName`"`ndescription: `"Auto-generated from $baseName`"`n---`n`n"
                $content = $newFrontmatter + $content
            }

            # Save the fixed content
            Set-Content -Path $file.FullName -Value $content -NoNewline
            Write-Host "✓ Fixed: $($file.Name) -> '$displayName'" -ForegroundColor Cyan
            $fixed++

        } catch {
            $errMsg = $_.Exception.Message
            Write-Host "Error processing $($file.Name): $errMsg" -ForegroundColor Red
            $errors++
        }
    }
}

# Fix READMEs separately
$readmeFiles = @(
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\README.md",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\agents\README.md",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\.github\CODE_OF_CONDUCT.md",
    "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents\.github\CONTRIBUTING.md"
)

foreach ($file in $readmeFiles) {
    if (Test-Path $file) {
        try {
            $content = Get-Content $file -Raw
            $fileName = Split-Path $file -Leaf
            $displayName = $fileName -replace '\.md$', '' -replace '_', ' '

            if ($content -notmatch '^---') {
                $newFrontmatter = "---`nname: `"$displayName`"`ndescription: `"Documentation file`"`n---`n`n"
                $content = $newFrontmatter + $content
                Set-Content -Path $file -Value $content -NoNewline
                Write-Host "✓ Fixed: $fileName" -ForegroundColor Cyan
                $fixed++
            }
        } catch {
            $errMsg = $_.Exception.Message
            Write-Host "Error processing ${fileName}: $errMsg" -ForegroundColor Red
            $errors++
        }
    }
}

Write-Host "`n================================================" -ForegroundColor Yellow
Write-Host "Agent Frontmatter Fix Complete" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
Write-Host "✓ Fixed: $fixed files" -ForegroundColor Green
Write-Host "✗ Errors: $errors files" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Green" })
Write-Host "`nRestart Claude Code to see the changes." -ForegroundColor Cyan
