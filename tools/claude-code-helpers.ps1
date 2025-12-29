# ================== Claude Code Helpers - Project Navigation and Context =================
# Additional functions for Claude Code workflows and project management
# Version: 1.0

$script:ClaudeRootPath = "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude"

# -------- Project Navigation --------
function Switch-ToProject {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$ProjectName,
        [switch]$StartClaudeCode
    )

    # Query projects database for project path
    $projectsDb = Join-Path $script:ClaudeRootPath "unified-memory\databases\projects-index.db"

    if (-not (Test-Path $projectsDb)) {
        Write-Error "Projects database not found: $projectsDb"
        return
    }

    try {
        # Get project path from database
        $projectPath = & py -c @"
import sqlite3
conn = sqlite3.connect('$projectsDb')
cursor = conn.execute('SELECT path FROM projects WHERE name = ? OR display_name LIKE ?', ('$ProjectName', '%$ProjectName%'))
result = cursor.fetchone()
conn.close()
print(result[0] if result else '')
"@

        if ([string]::IsNullOrEmpty($projectPath)) {
            Write-Error "Project not found: $ProjectName"
            Write-Host "`nAvailable projects:"
            List-AllProjects
            return
        }

        Set-Location $projectPath
        Write-Host "Switched to: $ProjectName" -ForegroundColor Green
        Write-Host "Location: $projectPath" -ForegroundColor Gray

        # Show project info
        if (Test-Path ".claude-project.md") {
            Write-Host ".claude-project.md: Found" -ForegroundColor Cyan
        } else {
            Write-Host ".claude-project.md: Not found" -ForegroundColor Yellow
        }

        if ($StartClaudeCode) {
            Write-Host "`nStarting Claude Code..." -ForegroundColor Cyan
            Start-Process code .
        }

    } catch {
        Write-Error "Failed to switch project: $($_.Exception.Message)"
    }
}

function List-AllProjects {
    [CmdletBinding()]
    param()

    $projectsDb = Join-Path $script:ClaudeRootPath "unified-memory\databases\projects-index.db"

    try {
        & py -c @"
import sqlite3
conn = sqlite3.connect('$projectsDb')
cursor = conn.execute('SELECT name, display_name, path FROM projects WHERE status = ''active'' ORDER BY name')
print('\nRegistered Projects:\n')
for i, (name, display, path) in enumerate(cursor.fetchall(), 1):
    print(f'{i}. {display or name}')
    print(f'   ID: {name}')
    print(f'   Path: {path}')
    print()
conn.close()
"@
    } catch {
        Write-Error "Failed to list projects: $($_.Exception.Message)"
    }
}

# -------- Document Management --------
function New-ProjectDocument {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Title,

        [Parameter(Mandatory=$true)]
        [ValidateSet('architecture', 'api', 'reports', 'guides', 'artifacts', 'research', 'planning')]
        [string]$Category,

        [string]$ProjectName = "",
        [switch]$Open
    )

    # Determine project name from current directory if not specified
    if ([string]::IsNullOrEmpty($ProjectName)) {
        $currentPath = (Get-Location).Path
        $ProjectName = & py -c @"
import sqlite3
from pathlib import Path
current_path = Path('$currentPath')
db_path = Path('$script:ClaudeRootPath') / 'unified-memory/databases/projects-index.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.execute('SELECT name FROM projects WHERE path = ?', (str(current_path),))
result = cursor.fetchone()
conn.close()
print(result[0] if result else '')
"@

        if ([string]::IsNullOrEmpty($ProjectName)) {
            Write-Error "Not in a registered project directory. Use -ProjectName parameter."
            return
        }
    }

    # Create document path
    $docsRoot = Join-Path $script:ClaudeRootPath "documents\$ProjectName\$Category"
    $date = Get-Date -Format "yyyy-MM-dd"
    $filename = "$Title-$date.md".ToLower() -replace '[^a-z0-9-]', '-'
    $fullPath = Join-Path $docsRoot $filename

    # Ensure directory exists
    if (-not (Test-Path $docsRoot)) {
        New-Item -ItemType Directory -Path $docsRoot -Force | Out-Null
    }

    # Create document template
    $template = @"
---
title: $Title
date: $date
author: Claude + User
project: $ProjectName
category: $Category
status: draft
---

# $Title

## Overview

[Brief description of the document purpose]

## Contents

[Document contents here]

---

**Document Location:** documents/$ProjectName/$Category/$filename
**Last Updated:** $date
"@

    $template | Set-Content -Path $fullPath -Encoding UTF8

    Write-Host "Created document: $fullPath" -ForegroundColor Green

    if ($Open) {
        code $fullPath
    }
}

function Open-ProjectDocs {
    [CmdletBinding()]
    param(
        [string]$ProjectName = ""
    )

    if ([string]::IsNullOrEmpty($ProjectName)) {
        $currentPath = (Get-Location).Path
        $ProjectName = & py -c @"
import sqlite3
from pathlib import Path
current_path = Path('$currentPath')
db_path = Path('$script:ClaudeRootPath') / 'unified-memory/databases/projects-index.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.execute('SELECT name FROM projects WHERE path = ?', (str(current_path),))
result = cursor.fetchone()
conn.close()
print(result[0] if result else '')
"@

        if ([string]::IsNullOrEmpty($ProjectName)) {
            Write-Error "Not in a registered project directory. Use -ProjectName parameter."
            return
        }
    }

    $docsPath = Join-Path $script:ClaudeRootPath "documents\$ProjectName"

    if (Test-Path $docsPath) {
        code $docsPath
        Write-Host "Opened: $docsPath" -ForegroundColor Green
    } else {
        Write-Error "Document folder not found: $docsPath"
    }
}

# -------- Claude Code Integration --------
function Start-ClaudeCode {
    [CmdletBinding()]
    param(
        [string]$ProjectName = "",
        [string]$Goal = "",
        [switch]$SyncMemory
    )

    if ([string]::IsNullOrEmpty($ProjectName)) {
        # Use current directory
        if ($SyncMemory) {
            Sync-ClaudeMemory
        }

        if (Get-Command code -ErrorAction SilentlyContinue) {
            code .
            Write-Host "Opened Claude Code in current directory" -ForegroundColor Green
        } else {
            Write-Error "VS Code not found in PATH"
        }
    } else {
        # Switch to project first
        Switch-ToProject -ProjectName $ProjectName

        if ($SyncMemory) {
            Sync-ClaudeMemory
        }

        if (Get-Command code -ErrorAction SilentlyContinue) {
            code .
            Write-Host "Opened Claude Code for project: $ProjectName" -ForegroundColor Green
        } else {
            Write-Error "VS Code not found in PATH"
        }
    }

    if ($Goal) {
        Write-Host "`nSession Goal: $Goal" -ForegroundColor Cyan
    }
}

function Show-ProjectContext {
    [CmdletBinding()]
    param()

    $currentPath = (Get-Location).Path

    Write-Host "`nProject Context" -ForegroundColor Green
    Write-Host "===============" -ForegroundColor Green

    Write-Host "`nCurrent Directory:" -ForegroundColor Cyan
    Write-Host "  $currentPath" -ForegroundColor White

    # Check if in registered project
    $projectInfo = & py -c @"
import sqlite3
from pathlib import Path
current_path = Path('$currentPath')
db_path = Path('$script:ClaudeRootPath') / 'unified-memory/databases/projects-index.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.execute('SELECT name, display_name, db_path FROM projects WHERE path = ?', (str(current_path),))
result = cursor.fetchone()
conn.close()
if result:
    print(f'{result[0]}|{result[1]}|{result[2]}')
"@

    if ($projectInfo) {
        $parts = $projectInfo -split '\|'
        Write-Host "`nProject Status:" -ForegroundColor Cyan
        Write-Host "  Registered: Yes" -ForegroundColor Green
        Write-Host "  Name: $($parts[0])" -ForegroundColor White
        Write-Host "  Display: $($parts[1])" -ForegroundColor White
        Write-Host "  Memory DB: $($parts[2])" -ForegroundColor Gray

        # Check for project config
        if (Test-Path ".claude-project.md") {
            Write-Host "`nProject Config:" -ForegroundColor Cyan
            Write-Host "  .claude-project.md: Found" -ForegroundColor Green
        } else {
            Write-Host "`nProject Config:" -ForegroundColor Cyan
            Write-Host "  .claude-project.md: Not found" -ForegroundColor Yellow
        }

        # Check documents folder
        $docsPath = Join-Path $script:ClaudeRootPath "documents\$($parts[0])"
        if (Test-Path $docsPath) {
            $docCount = (Get-ChildItem -Path $docsPath -Recurse -Filter "*.md").Count
            Write-Host "`nDocuments:" -ForegroundColor Cyan
            Write-Host "  Folder: $docsPath" -ForegroundColor Gray
            Write-Host "  Count: $docCount files" -ForegroundColor White
        }
    } else {
        Write-Host "`nProject Status:" -ForegroundColor Cyan
        Write-Host "  Registered: No" -ForegroundColor Yellow
        Write-Host "  (Not in a registered project directory)" -ForegroundColor Gray
    }

    # Git status
    if (Get-Command git -ErrorAction SilentlyContinue) {
        try {
            $branch = git branch --show-current 2>$null
            $status = git status --porcelain 2>$null
            Write-Host "`nGit Status:" -ForegroundColor Cyan
            Write-Host "  Branch: $branch" -ForegroundColor White
            if ($status) {
                $changeCount = ($status -split "`n").Count
                Write-Host "  Changes: $changeCount file(s)" -ForegroundColor Yellow
            } else {
                Write-Host "  Status: Clean" -ForegroundColor Green
            }
        } catch {
            Write-Host "`nGit: Not a repository" -ForegroundColor Gray
        }
    }

    Write-Host "`nAvailable Commands:" -ForegroundColor Green
    Write-Host "  goto <project>      - Switch to project" -ForegroundColor White
    Write-Host "  projects            - List all projects" -ForegroundColor White
    Write-Host "  new-doc <title>     - Create new document" -ForegroundColor White
    Write-Host "  open-docs           - Open documents folder" -ForegroundColor White
    Write-Host "  ccode [project]     - Start Claude Code" -ForegroundColor White
    Write-Host "  context             - Show this info" -ForegroundColor White
}

function Get-QuickHelp {
    Write-Host "`nClaude Code Helpers - Quick Reference" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green

    Write-Host "`nProject Navigation:" -ForegroundColor Cyan
    Write-Host "  goto <project>              - Switch to project directory" -ForegroundColor White
    Write-Host "  projects                    - List all registered projects" -ForegroundColor White
    Write-Host "  context                     - Show current project context" -ForegroundColor White

    Write-Host "`nDocument Management:" -ForegroundColor Cyan
    Write-Host "  new-doc <title> -Category architecture" -ForegroundColor White
    Write-Host "                              - Create new document" -ForegroundColor White
    Write-Host "  open-docs [project]         - Open documents folder" -ForegroundColor White

    Write-Host "`nClaude Code:" -ForegroundColor Cyan
    Write-Host "  ccode                       - Open Claude Code in current directory" -ForegroundColor White
    Write-Host "  ccode <project>             - Open Claude Code in specific project" -ForegroundColor White
    Write-Host "  ccode -SyncMemory           - Open with memory sync" -ForegroundColor White

    Write-Host "`nSession Management:" -ForegroundColor Cyan
    Write-Host "  scl-sync                    - Start enhanced Claude session" -ForegroundColor White
    Write-Host "  sync-memory                 - Manual memory consolidation" -ForegroundColor White
    Write-Host "  claude-status               - Show system status" -ForegroundColor White

    Write-Host "`nExamples:" -ForegroundColor Yellow
    Write-Host "  goto smart-mcp" -ForegroundColor Gray
    Write-Host "  new-doc 'API Design' -Category architecture -Open" -ForegroundColor Gray
    Write-Host "  ccode peoplesoft-rag -SyncMemory" -ForegroundColor Gray

    Write-Host "`nFor detailed help: Get-Help <command> -Detailed" -ForegroundColor Gray
}

# -------- Aliases --------
Set-Alias -Name goto -Value Switch-ToProject -Option AllScope
Set-Alias -Name projects -Value List-AllProjects -Option AllScope
Set-Alias -Name new-doc -Value New-ProjectDocument -Option AllScope
Set-Alias -Name open-docs -Value Open-ProjectDocs -Option AllScope
Set-Alias -Name ccode -Value Start-ClaudeCode -Option AllScope
Set-Alias -Name context -Value Show-ProjectContext -Option AllScope
Set-Alias -Name help-claude -Value Get-QuickHelp -Option AllScope

# Welcome message
Write-Host "Claude Code Helpers Loaded" -ForegroundColor Green
Write-Host "Type 'help-claude' for commands" -ForegroundColor Gray

# ================== END Claude Code Helpers ==================