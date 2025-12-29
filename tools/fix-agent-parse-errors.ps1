# Fix Agent Parse Errors
# This script adds proper frontmatter to agent files that are missing it

$ErrorActionPreference = "Stop"

# Files that should be excluded (documentation, not agents)
$excludeFiles = @(
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md"
)

# Files that should have "hidden" frontmatter (tools and workflows)
$toolsAndWorkflows = @(
    "tools/*.md",
    "workflows/*.md"
)

# Get all problematic .md files in .claude/agents
$agentsPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents"

Write-Host "🔧 Fixing agent parse errors..." -ForegroundColor Cyan

# Function to add hidden frontmatter to tools/workflows
function Add-HiddenFrontmatter {
    param($filePath)

    $content = Get-Content $filePath -Raw
    $fileName = Split-Path $filePath -Leaf
    $baseName = $fileName -replace '\.md$', ''

    # Check if already has frontmatter
    if ($content -match '^---\s*\n') {
        Write-Host "  ⏭️  Already has frontmatter: $fileName" -ForegroundColor Yellow
        return
    }

    $frontmatter = "---`nname: $baseName`ndescription: Internal tool/workflow - not a standalone agent`nhidden: true`n---`n`n"

    $newContent = $frontmatter + $content
    Set-Content $filePath -Value $newContent -NoNewline
    Write-Host "  ✅ Fixed: $fileName" -ForegroundColor Green
}

# Function to skip README files (add ignore marker)
function Add-IgnoreMarker {
    param($filePath)

    $content = Get-Content $filePath -Raw
    $fileName = Split-Path $filePath -Leaf

    # Check if already has frontmatter or ignore marker
    if ($content -match '^---\s*\n' -or $content -match '^<!-- agent-ignore -->') {
        return
    }

    $marker = "<!-- agent-ignore -->`n`n"
    $newContent = $marker + $content
    Set-Content $filePath -Value $newContent -NoNewline
    Write-Host "  ✅ Ignored: $fileName" -ForegroundColor Gray
}

# Fix tools directory
$toolsPath = Join-Path $agentsPath "tools"
if (Test-Path $toolsPath) {
    Write-Host "`n📁 Fixing tools..." -ForegroundColor Cyan
    Get-ChildItem $toolsPath -Filter "*.md" | ForEach-Object {
        Add-HiddenFrontmatter $_.FullName
    }
}

# Fix workflows directory
$workflowsPath = Join-Path $agentsPath "workflows"
if (Test-Path $workflowsPath) {
    Write-Host "`n📁 Fixing workflows..." -ForegroundColor Cyan
    Get-ChildItem $workflowsPath -Filter "*.md" | ForEach-Object {
        Add-HiddenFrontmatter $_.FullName
    }
}

# Fix README files
Write-Host "`n📄 Marking README files as ignored..." -ForegroundColor Cyan
Get-ChildItem $agentsPath -Filter "README.md" -Recurse | ForEach-Object {
    Add-IgnoreMarker $_.FullName
}

# Fix .github files
$githubPath = Join-Path $agentsPath ".github"
if (Test-Path $githubPath) {
    Write-Host "`n📁 Marking .github files as ignored..." -ForegroundColor Cyan
    Get-ChildItem $githubPath -Filter "*.md" -Recurse | ForEach-Object {
        Add-IgnoreMarker $_.FullName
    }
}

# Fix the example file with missing description
$exampleFile = Join-Path $agentsPath "examples\tdd-usage.md"
if (Test-Path $exampleFile) {
    Write-Host "`n📝 Fixing example file..." -ForegroundColor Cyan
    $content = Get-Content $exampleFile -Raw

    # Add description to existing frontmatter
    if ($content -match '^---\s*\n(.*?)\n---' -and $content -notmatch 'description:') {
        $newContent = $content -replace '^(---\s*\n)', "`$1description: Example TDD workflow usage`n"
        Set-Content $exampleFile -Value $newContent -NoNewline
        Write-Host "  ✅ Fixed: tdd-usage.md" -ForegroundColor Green
    }
}

Write-Host "`n✅ All agent parse errors fixed!" -ForegroundColor Green
Write-Host "   Restart Claude Code to see the changes." -ForegroundColor Yellow
