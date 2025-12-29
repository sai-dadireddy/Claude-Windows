# Batch Setup Enforcement for All Projects (PowerShell)
# Automates PROJECT-TRACKER, .claude-project.md, and RAG setup

param(
    [switch]$DryRun = $false
)

# Ensure we're in the root directory
$scriptDir = Split-Path -Parent $PSCommandPath
$rootDir = Split-Path -Parent $scriptDir

# Change to root directory if we're in tools/
if ((Get-Location).Path -ne $rootDir) {
    Write-Host "📁 Changing to root directory: $rootDir" -ForegroundColor Cyan
    Set-Location $rootDir
}

Write-Host "🚀 Batch Enforcement Setup - All Projects" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📂 Working directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

# List of projects to setup (excluding ERPAGPT and AGUPGRADE - already complete)
$projects = @(
    "projects\aarp",
    "projects\PeopleSoft-RAG",
    "projects\aws-chatbot",
    "projects\strivacity",
    "projects\langchain-learning",
    "projects\web-research-mcp",
    "projects\mcp-servers",
    "projects\n8n",
    "projects\multi-ai-orchestration",
    "projects\playwright-agents",
    "projects\agentic-rag",
    "projects\ai-runbooks",
    "projects\ai-workflows",
    "projects\chatgpt-mcp",
    "projects\unified-memory"
)

$total = $projects.Count
$success = 0
$failed = 0
$skipped = 0

Write-Host "📋 Found $total projects to setup" -ForegroundColor Yellow
Write-Host ""

foreach ($project in $projects) {
    $projectName = Split-Path $project -Leaf
    $currentNum = $success + $failed + $skipped + 1

    Write-Host "[$currentNum/$total] Processing: $projectName" -ForegroundColor Yellow

    # Skip if project doesn't exist
    if (-not (Test-Path $project)) {
        Write-Host "  ⚠️  Directory not found, skipping" -ForegroundColor Red
        $skipped++
        continue
    }

    # Check if already has PROJECT-TRACKER.md
    if (Test-Path "$project\PROJECT-TRACKER.md") {
        Write-Host "  ℹ️  PROJECT-TRACKER.md exists, skipping" -ForegroundColor Yellow
        $skipped++
        continue
    }

    if ($DryRun) {
        Write-Host "  [DRY RUN] Would generate PROJECT-TRACKER.md" -ForegroundColor Cyan
        Write-Host "  [DRY RUN] Would create .claude-project.md" -ForegroundColor Cyan
        Write-Host "  [DRY RUN] Would create RAG tools" -ForegroundColor Cyan
        $success++
        continue
    }

    # Step 1: Generate PROJECT-TRACKER.md
    Write-Host "  📄 Generating PROJECT-TRACKER.md..." -ForegroundColor Gray
    try {
        python tools\create-project-tracker.py --project-name "$projectName" --project-dir "$project" 2>&1 | Select-String -Pattern "✅|❌" | Out-Null
    } catch {
        Write-Host "  ❌ Failed to generate PROJECT-TRACKER.md: $_" -ForegroundColor Red
        $failed++
        continue
    }

    # Step 2: Create .claude-project.md if missing
    if (-not (Test-Path "$project\.claude-project.md")) {
        Write-Host "  📝 Creating .claude-project.md from template..." -ForegroundColor Gray

        $claudeProjectContent = @'
# {0} Project Instructions

## 🎯 **SESSION START PROTOCOL (MANDATORY - EXECUTE FIRST!)**

### **Step 1: Read Project Tracker (REQUIRED)**
```bash
# ALWAYS read this file at session start - it's the single source of truth
Read: PROJECT-TRACKER.md
```

### **Step 2: RAG-First Documentation Access (MANDATORY)**
```bash
# Query RAG BEFORE reading files (if RAG exists)
# python tools\query-{1}-rag.py "your question"
```

### **Step 3: Update Project Tracker After Task Completion (MANDATORY)**
After completing ANY task:
- Update PROJECT-TRACKER.md with task status
- Add lessons learned
- Update timestamp

---

**Status**: Initial setup - customize this file for project needs
**Last Updated**: {2}
'@ -f $projectName, $projectName.ToLower(), (Get-Date -Format "yyyy-MM-dd")

        Set-Content -Path "$project\.claude-project.md" -Value $claudeProjectContent -Encoding UTF8
    }

    # Step 3: Create RAG tools directory structure
    if (-not (Test-Path "$project\tools")) {
        Write-Host "  📁 Creating tools\ directory..." -ForegroundColor Gray
        New-Item -ItemType Directory -Path "$project\tools" -Force | Out-Null
    }

    # Step 4: Create placeholder RAG scripts
    if (-not (Test-Path "$project\tools\query-rag.py")) {
        Write-Host "  🔧 Creating RAG script templates..." -ForegroundColor Gray

        $ragQueryContent = @'
#!/usr/bin/env python3
"""
Query RAG collection for {0}
TODO: Customize for your project's RAG collection
"""
import sys

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "status"
    print(f"TODO: Implement RAG query for: {{query}}")
    print("See projects\\erpa\\AGUPGRADE\\tools\\query-rag.py for example")

if __name__ == "__main__":
    main()
'@ -f $projectName

        Set-Content -Path "$project\tools\query-rag.py" -Value $ragQueryContent -Encoding UTF8
    }

    # Step 5: Create README for RAG setup
    if (-not (Test-Path "$project\tools\README-RAG.md")) {
        $ragReadmeContent = @'
# RAG Setup Guide

## Quick Start

1. **Implement query-rag.py**:
   - See `projects\erpa\AGUPGRADE\tools\query-rag.py` as example
   - Configure ChromaDB collection name
   - Add project-specific categories

2. **Create ingest script**:
   - Copy from AGUPGRADE or ERPAGPT
   - Customize for your documentation structure

3. **Index documents**:
   ```bash
   python tools\ingest-rag.py
   ```

4. **Test queries**:
   ```bash
   python tools\query-rag.py "your question"
   ```

**Status**: Template created - customize for your project
'@

        Set-Content -Path "$project\tools\README-RAG.md" -Value $ragReadmeContent -Encoding UTF8
    }

    Write-Host "  ✅ Project setup complete!" -ForegroundColor Green
    $success++
    Write-Host ""
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📊 Batch Setup Summary" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ Success: $success" -ForegroundColor Green
Write-Host "⏭️  Skipped: $skipped" -ForegroundColor Yellow
Write-Host "❌ Failed: $failed" -ForegroundColor Red
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Review generated PROJECT-TRACKER.md files"
Write-Host "  2. Customize .claude-project.md for each project"
Write-Host "  3. Implement RAG scripts (see tools\README-RAG.md)"
Write-Host "  4. Run initial RAG indexing"
Write-Host ""
Write-Host "✅ Batch enforcement setup complete!" -ForegroundColor Green
