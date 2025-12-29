# Validate Enforcement Status Across All Projects
# Checks PROJECT-TRACKER.md, .claude-project.md, and RAG tools

Write-Host "🔍 Enforcement Validation Report" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Get all project directories
$projectDirs = Get-ChildItem -Path "projects" -Directory -Recurse -Depth 2 |
    Where-Object { $_.Name -ne "tools" -and $_.Name -ne "docs" -and $_.Name -ne ".git" }

$stats = @{
    Total = 0
    FullEnforcement = 0
    PartialEnforcement = 0
    NoEnforcement = 0
}

$results = @()

foreach ($project in $projectDirs) {
    $stats.Total++

    $hasTracker = Test-Path "$($project.FullName)\PROJECT-TRACKER.md"
    $hasClaudeProject = Test-Path "$($project.FullName)\.claude-project.md"
    $hasRagTools = (Get-ChildItem -Path "$($project.FullName)\tools" -Filter "*rag*.py" -ErrorAction SilentlyContinue).Count -gt 0

    $status = "❌ None"
    $statusColor = "Red"

    if ($hasTracker -and $hasClaudeProject -and $hasRagTools) {
        $status = "✅ Full"
        $statusColor = "Green"
        $stats.FullEnforcement++
    }
    elseif ($hasTracker -or $hasClaudeProject) {
        $status = "⚠️  Partial"
        $statusColor = "Yellow"
        $stats.PartialEnforcement++
    }
    else {
        $stats.NoEnforcement++
    }

    $results += [PSCustomObject]@{
        Project = $project.Name
        Path = $project.FullName.Replace((Get-Location).Path + "\", "")
        Tracker = if ($hasTracker) { "✅" } else { "❌" }
        ClaudeProject = if ($hasClaudeProject) { "✅" } else { "❌" }
        RAGTools = if ($hasRagTools) { "✅" } else { "❌" }
        Status = $status
        StatusColor = $statusColor
    }
}

# Display results
Write-Host "📊 Project Enforcement Status" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

foreach ($result in $results | Sort-Object Status -Descending) {
    Write-Host "$($result.Status) " -ForegroundColor $result.StatusColor -NoNewline
    Write-Host "$($result.Project)" -ForegroundColor White
    Write-Host "    Path: $($result.Path)" -ForegroundColor Gray
    Write-Host "    PROJECT-TRACKER: $($result.Tracker)  .claude-project.md: $($result.ClaudeProject)  RAG Tools: $($result.RAGTools)" -ForegroundColor Gray
    Write-Host ""
}

# Summary statistics
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📈 Summary Statistics" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Total Projects: $($stats.Total)" -ForegroundColor White
$fullPct = [math]::Round($stats.FullEnforcement / $stats.Total * 100, 1)
$partialPct = [math]::Round($stats.PartialEnforcement / $stats.Total * 100, 1)
$nonePct = [math]::Round($stats.NoEnforcement / $stats.Total * 100, 1)

$fullMsg = "✅ Full Enforcement: {0} ({1} percent)" -f $stats.FullEnforcement, $fullPct
$partialMsg = "⚠️  Partial Enforcement: {0} ({1} percent)" -f $stats.PartialEnforcement, $partialPct
$noneMsg = "❌ No Enforcement: {0} ({1} percent)" -f $stats.NoEnforcement, $nonePct

Write-Host $fullMsg -ForegroundColor Green
Write-Host $partialMsg -ForegroundColor Yellow
Write-Host $noneMsg -ForegroundColor Red
Write-Host ""

# Recommendations
if ($stats.NoEnforcement -gt 0) {
    Write-Host "💡 Recommendations:" -ForegroundColor Cyan
    Write-Host "  Run: .\tools\batch-setup-enforcement.ps1" -ForegroundColor Yellow
    Write-Host "  This will setup $($stats.NoEnforcement) projects missing enforcement" -ForegroundColor Gray
    Write-Host ""
}

if ($stats.PartialEnforcement -gt 0) {
    Write-Host "⚠️  Partial Projects Need:" -ForegroundColor Yellow
    $partialProjects = $results | Where-Object { $_.Status -eq "⚠️  Partial" }
    foreach ($proj in $partialProjects) {
        Write-Host "  $($proj.Project):" -ForegroundColor White
        if ($proj.Tracker -eq "❌") { Write-Host "    - Add PROJECT-TRACKER.md" -ForegroundColor Gray }
        if ($proj.ClaudeProject -eq "❌") { Write-Host "    - Add .claude-project.md" -ForegroundColor Gray }
        if ($proj.RAGTools -eq "❌") { Write-Host "    - Implement RAG tools" -ForegroundColor Gray }
    }
    Write-Host ""
}

Write-Host "✅ Validation complete!" -ForegroundColor Green
