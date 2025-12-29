# Fix Agent Frontmatter - Batch Processor
# Adds proper frontmatter to workflow and tool files

$ErrorActionPreference = "Stop"

# Define files to fix (from /doctor output)
$filesToFix = @(
    ".claude\agents\examples\tdd-usage.md",
    ".claude\agents\.github\CODE_OF_CONDUCT.md",
    ".claude\agents\.github\CONTRIBUTING.md",
    ".claude\agents\workflows\workflow-automate.md",
    ".claude\agents\workflows\tdd-cycle.md",
    ".claude\agents\workflows\smart-fix.md",
    ".claude\agents\workflows\security-hardening.md",
    ".claude\agents\workflows\performance-optimization.md",
    ".claude\agents\workflows\multi-platform.md",
    ".claude\agents\workflows\ml-pipeline.md",
    ".claude\agents\workflows\legacy-modernize.md",
    ".claude\agents\workflows\incident-response.md",
    ".claude\agents\workflows\improve-agent.md",
    ".claude\agents\workflows\git-workflow.md",
    ".claude\agents\workflows\full-stack-feature.md",
    ".claude\agents\workflows\full-review.md",
    ".claude\agents\workflows\feature-development.md",
    ".claude\agents\workflows\data-driven-feature.md",
    ".claude\agents\README.md",
    ".claude\agents\agents\README.md",
    ".claude\agents\tools\data-validation.md",
    ".claude\agents\tools\data-pipeline.md",
    ".claude\agents\tools\cost-optimize.md",
    ".claude\agents\tools\context-save.md",
    ".claude\agents\tools\context-restore.md",
    ".claude\agents\tools\config-validate.md",
    ".claude\agents\tools\compliance-check.md",
    ".claude\agents\tools\code-migrate.md",
    ".claude\agents\tools\code-explain.md",
    ".claude\agents\tools\api-scaffold.md",
    ".claude\agents\tools\api-mock.md",
    ".claude\agents\tools\ai-review.md",
    ".claude\agents\tools\ai-assistant.md",
    ".claude\agents\tools\accessibility-audit.md",
    ".claude\agents\tools\docker-optimize.md",
    ".claude\agents\tools\doc-generate.md",
    ".claude\agents\tools\deps-upgrade.md",
    ".claude\agents\tools\deps-audit.md",
    ".claude\agents\tools\deploy-checklist.md",
    ".claude\agents\tools\debug-trace.md",
    ".claude\agents\tools\db-migrate.md",
    ".claude\agents\tools\k8s-manifest.md",
    ".claude\agents\tools\issue.md",
    ".claude\agents\tools\error-trace.md",
    ".claude\agents\tools\error-analysis.md",
    ".claude\agents\tools\monitor-setup.md",
    ".claude\agents\tools\langchain-agent.md",
    ".claude\agents\tools\multi-agent-optimize.md",
    ".claude\agents\tools\test-harness.md",
    ".claude\agents\tools\tech-debt.md",
    ".claude\agents\tools\tdd-refactor.md",
    ".claude\agents\tools\tdd-red.md",
    ".claude\agents\tools\tdd-green.md",
    ".claude\agents\tools\standup-notes.md",
    ".claude\agents\tools\smart-debug.md",
    ".claude\agents\tools\slo-implement.md",
    ".claude\agents\tools\security-scan.md",
    ".claude\agents\tools\refactor-clean.md",
    ".claude\agents\tools\prompt-optimize.md",
    ".claude\agents\tools\pr-enhance.md",
    ".claude\agents\tools\onboard.md",
    ".claude\agents\tools\multi-agent-review.md"
)

$baseDir = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"
$fixed = 0
$skipped = 0
$errors = 0

Write-Host "Starting batch frontmatter fix for 62 files..." -ForegroundColor Cyan

foreach ($file in $filesToFix) {
    $fullPath = Join-Path $baseDir $file

    if (-not (Test-Path $fullPath)) {
        Write-Host "  [SKIP] File not found: $file" -ForegroundColor Yellow
        $skipped++
        continue
    }

    try {
        $content = Get-Content $fullPath -Raw -ErrorAction Stop

        # Check if already has frontmatter
        if ($content -match '^---\r?\n') {
            Write-Host "  [SKIP] Already has frontmatter: $file" -ForegroundColor Gray
            $skipped++
            continue
        }

        # Generate name from filename
        $filename = [System.IO.Path]::GetFileNameWithoutExtension($file)
        $name = $filename -replace '-', ' ' | ForEach-Object { (Get-Culture).TextInfo.ToTitleCase($_) }

        # Determine type based on path
        $type = if ($file -match '\\tools\\') { "tool" }
                elseif ($file -match '\\workflows\\') { "workflow" }
                elseif ($file -match '\\agents\\') { "documentation" }
                elseif ($file -match 'README') { "documentation" }
                else { "utility" }

        # Generate description
        $description = if ($file -match 'README') {
            "Documentation for $name"
        } elseif ($type -eq "tool") {
            "Helper tool for $name operations"
        } elseif ($type -eq "workflow") {
            "Workflow for $name process"
        } else {
            "Documentation for $name"
        }

        # Create frontmatter
        $frontmatter = @"
---
name: $name
description: $description
type: $type
---

"@

        # Add frontmatter
        $newContent = $frontmatter + $content

        # Write back
        Set-Content -Path $fullPath -Value $newContent -NoNewline -ErrorAction Stop

        Write-Host "  [FIXED] $file" -ForegroundColor Green
        $fixed++

    } catch {
        Write-Host "  [ERROR] Failed to fix $file`: $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "Batch Fix Complete!" -ForegroundColor Cyan
Write-Host "  Fixed: $fixed files" -ForegroundColor Green
Write-Host "  Skipped: $skipped files" -ForegroundColor Yellow
Write-Host "  Errors: $errors files" -ForegroundColor Red
Write-Host ""
Write-Host "Next step: Run '/doctor' to verify all errors are fixed" -ForegroundColor Cyan
