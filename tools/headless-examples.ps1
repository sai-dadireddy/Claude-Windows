# Claude Code Headless Mode - Examples
# Collection of useful headless automation tasks

# Example 1: Automated Code Review
function Invoke-CodeReview {
    param([string]$TargetDir = "./src")

    Write-Host "📝 Running automated code review..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Review all files in $TargetDir and create a REVIEW.md with findings" -OutputFile "REVIEW.md"
}

# Example 2: Automated Testing
function Invoke-AutoTest {
    Write-Host "🧪 Running automated testing..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Run all tests, fix any failures, and create a summary report" -SkipPermissions
}

# Example 3: Documentation Update
function Update-Documentation {
    Write-Host "📚 Updating documentation..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Update README.md with latest changes from git log and code analysis"
}

# Example 4: Security Scan
function Invoke-SecurityScan {
    Write-Host "🔒 Running security scan..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "/security-scan and generate SECURITY-REPORT.md" -OutputFile "SECURITY-REPORT.md"
}

# Example 5: Code Formatting
function Format-Codebase {
    param([string]$FilePattern = "*.py")

    Write-Host "🎨 Formatting codebase..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Format all $FilePattern files using best practices" -SkipPermissions
}

# Example 6: Dependency Audit
function Invoke-DependencyAudit {
    Write-Host "📦 Auditing dependencies..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Analyze package.json/requirements.txt for outdated or vulnerable dependencies"
}

# Example 7: Git Commit Message Generator
function New-CommitMessage {
    Write-Host "📝 Generating commit message..." -ForegroundColor Cyan
    $changes = git diff --staged
    .\tools\claude-headless.ps1 -Task "Generate a concise commit message based on these changes: $changes" -OutputFile "COMMIT_MSG.txt"
}

# Example 8: API Documentation Generator
function New-APIDocumentation {
    param([string]$SourceDir = "./src")

    Write-Host "📖 Generating API documentation..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Generate OpenAPI/Swagger documentation from code in $SourceDir"
}

# Example 9: Performance Analysis
function Invoke-PerformanceAnalysis {
    Write-Host "⚡ Analyzing performance..." -ForegroundColor Cyan
    .\tools\claude-headless.ps1 -Task "Analyze codebase for performance bottlenecks and suggest optimizations"
}

# Example 10: Changelog Generator
function New-Changelog {
    param([string]$Version = "")

    Write-Host "📰 Generating changelog..." -ForegroundColor Cyan
    if ($Version) {
        .\tools\claude-headless.ps1 -Task "Generate CHANGELOG.md for version $Version from git history"
    } else {
        .\tools\claude-headless.ps1 -Task "Update CHANGELOG.md with latest changes from git log"
    }
}

# Example 11: Pre-Commit Hook
function Invoke-PreCommitCheck {
    Write-Host "✅ Running pre-commit checks..." -ForegroundColor Cyan

    # Run multiple checks
    Write-Host "  - Linting..." -ForegroundColor Gray
    .\tools\claude-headless.ps1 -Task "Lint all staged files and fix auto-fixable issues" -SkipPermissions

    Write-Host "  - Testing..." -ForegroundColor Gray
    .\tools\claude-headless.ps1 -Task "Run tests for modified files" -SkipPermissions

    Write-Host "  - Security check..." -ForegroundColor Gray
    .\tools\claude-headless.ps1 -Task "Check staged files for security issues" -Verbose
}

# Example 12: Daily Report Generator
function New-DailyReport {
    Write-Host "📊 Generating daily report..." -ForegroundColor Cyan

    $date = Get-Date -Format 'yyyy-MM-dd'
    $reportFile = "reports/daily-report-$date.md"

    $task = @"
Generate a daily development report including:
1. Git commits from today
2. Code changes summary
3. Test results
4. Open issues/PRs
5. Recommendations for tomorrow
"@

    .\tools\claude-headless.ps1 -Task $task -OutputFile $reportFile
}

# Usage Examples:
# .\tools\headless-examples.ps1 Invoke-CodeReview -TargetDir "./src"
# .\tools\headless-examples.ps1 Invoke-AutoTest
# .\tools\headless-examples.ps1 Update-Documentation
# .\tools\headless-examples.ps1 Invoke-SecurityScan
# .\tools\headless-examples.ps1 Format-Codebase -FilePattern "*.ts"

# Export functions for use in other scripts
Export-ModuleMember -Function *
