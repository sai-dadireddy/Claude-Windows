# Pre-Commit Security Check
# Automated security validation before git commits
# Version: 1.0

Write-Host "🔐 Running Pre-Commit Security Check..." -ForegroundColor Cyan

$exitCode = 0
$issues = @()

# 1. Check for secrets
Write-Host "`n1. Scanning for secrets..." -NoNewline
$secretPatterns = @(
    'password\s*=\s*[''"]',
    'api[_-]?key\s*=\s*[''"]',
    'secret\s*=\s*[''"]',
    'token\s*=\s*[''"]',
    'AWS_ACCESS_KEY',
    'PRIVATE[_-]?KEY',
    'BEGIN RSA PRIVATE KEY'
)

$stagedFiles = git diff --cached --name-only --diff-filter=ACM
foreach ($file in $stagedFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
        foreach ($pattern in $secretPatterns) {
            if ($content -match $pattern) {
                $issues += "🔴 CRITICAL: Potential secret in $file"
                $exitCode = 1
            }
        }
    }
}

if ($issues.Count -eq 0) {
    Write-Host " ✓" -ForegroundColor Green
} else {
    Write-Host " ✗" -ForegroundColor Red
}

# 2. Check for large files
Write-Host "2. Checking file sizes..." -NoNewline
foreach ($file in $stagedFiles) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1MB
        if ($size -gt 10) {
            $issues += "🟡 WARNING: Large file ($([math]::Round($size, 2)) MB): $file"
        }
    }
}
Write-Host " ✓" -ForegroundColor Green

# 3. Check for security vulnerabilities (if Claude is available)
Write-Host "3. Running security scan..." -NoNewline
$claudeAvailable = Get-Command claude -ErrorAction SilentlyContinue
if ($claudeAvailable) {
    # Run quick security scan on staged files
    $scanResult = claude /security-review --quick 2>&1
    if ($LASTEXITCODE -ne 0) {
        $issues += "🟠 WARNING: Security review found issues"
    }
    Write-Host " ✓" -ForegroundColor Green
} else {
    Write-Host " ⊘ (Claude not available)" -ForegroundColor Yellow
}

# 4. Check dependencies (if applicable)
Write-Host "4. Checking dependencies..." -NoNewline
if (Test-Path "package.json") {
    npm audit --audit-level=high 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $issues += "🟠 WARNING: High-severity npm vulnerabilities found"
    }
} elseif (Test-Path "requirements.txt") {
    pip-audit 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        $issues += "🟠 WARNING: Python package vulnerabilities found"
    }
}
Write-Host " ✓" -ForegroundColor Green

# 5. Check for .env files
Write-Host "5. Checking for sensitive files..." -NoNewline
foreach ($file in $stagedFiles) {
    if ($file -match '\.env$' -or $file -match 'credentials') {
        $issues += "🔴 CRITICAL: Attempting to commit sensitive file: $file"
        $exitCode = 1
    }
}

if ($issues.Count -eq 0) {
    Write-Host " ✓" -ForegroundColor Green
} else {
    Write-Host " ✗" -ForegroundColor Red
}

# Report
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
if ($issues.Count -eq 0) {
    Write-Host "✅ All security checks passed!" -ForegroundColor Green
    Write-Host "Proceeding with commit..." -ForegroundColor Green
} else {
    Write-Host "⚠️  Security Issues Detected:" -ForegroundColor Red
    foreach ($issue in $issues) {
        Write-Host "  $issue"
    }
    Write-Host "`nPlease fix these issues before committing." -ForegroundColor Yellow
    Write-Host "To bypass (NOT RECOMMENDED): git commit --no-verify" -ForegroundColor Yellow
}
Write-Host ("=" * 60) -ForegroundColor Cyan

exit $exitCode
