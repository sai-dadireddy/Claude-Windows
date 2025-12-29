#!/usr/bin/env python3
"""
Organize Documents - Move documentation to appropriate folders

This script moves documentation files from the root to the documents/ folder
while preserving the unified memory system documentation structure.
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

# UTF-8 for emojis
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude")
DOCS_ROOT = BASE / "documents"

# System-level documentation stays at root
KEEP_AT_ROOT = {
    'claude.md',  # Global config
    '.claude-project.md',  # Root project config
    'README.md',  # Main readme
    'Microsoft.PowerShell_profile.ps1',  # PowerShell profile
}

# Documentation organization mapping
DOC_MAPPING = {
    # Architecture & Design
    'ARCHITECTURE_DECISIONS.md': ('unified-memory-system', 'architecture'),

    # Implementation Reports
    'IMPLEMENTATION_REPORT.md': ('unified-memory-system', 'reports'),
    'CONSOLIDATION_REPORT.md': ('unified-memory-system', 'reports'),
    'FINAL_SUCCESS_SUMMARY.md': ('unified-memory-system', 'reports'),

    # User Guides
    'HOW_IT_WORKS.md': ('unified-memory-system', 'guides'),
    'QUICK_START.md': ('unified-memory-system', 'guides'),
    'QUICK_REFERENCE.md': ('unified-memory-system', 'guides'),
    'PROJECT_SETUP_GUIDE.md': ('unified-memory-system', 'guides'),
    'POST_IMPLEMENTATION_GUIDE.md': ('unified-memory-system', 'guides'),
    'CLEANUP_GUIDE.md': ('unified-memory-system', 'guides'),
    'SETUP_COMPLETE_SUMMARY.md': ('unified-memory-system', 'guides'),

    # System Documentation
    'SYSTEM_SUMMARY.md': ('unified-memory-system', 'reports'),
}

def create_unified_memory_docs():
    """Create unified-memory-system documentation folder"""

    project_docs = DOCS_ROOT / "unified-memory-system"

    # Create folders
    folders = ['architecture', 'guides', 'reports', 'planning']
    for folder in folders:
        (project_docs / folder).mkdir(parents=True, exist_ok=True)

    # Create README
    readme = project_docs / "README.md"
    readme_content = f"""# Unified Memory System - Documentation

This folder contains all documentation for the Claude Unified Memory System.

## Folder Structure

- **architecture/** - System architecture, design decisions, ADRs
- **guides/** - User guides, quick starts, references
- **reports/** - Implementation reports, status updates
- **planning/** - Project plans and roadmaps

## System Components

The unified memory system provides:
- Global memory across all projects
- Per-project isolated memory
- MCP tool integration
- Document management
- PowerShell integration

## Key Documents

### Getting Started
- **QUICK_START.md** - 15-minute setup guide
- **HOW_IT_WORKS.md** - Complete architecture explanation
- **PROJECT_SETUP_GUIDE.md** - Project configuration guide

### Reference
- **QUICK_REFERENCE.md** - Command cheat sheet
- **SYSTEM_SUMMARY.md** - Complete system reference

### Implementation
- **IMPLEMENTATION_REPORT.md** - Initial implementation details
- **CONSOLIDATION_REPORT.md** - Structure consolidation report
- **ARCHITECTURE_DECISIONS.md** - Design rationale

---

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**System:** Unified Memory System
**Projects:** 7 registered
"""
    readme.write_text(readme_content, encoding='utf-8')
    print(f"✅ Created: {project_docs}/")
    print(f"   └── README.md")

def organize_documents():
    """Organize root-level documents into appropriate folders"""

    print("=" * 60)
    print("ORGANIZE DOCUMENTS")
    print("=" * 60)

    # Create unified-memory-system docs
    create_unified_memory_docs()

    moved_count = 0
    skipped_count = 0

    print(f"\n📁 Processing root-level documents...")

    # Process each document
    for filename, (project, category) in DOC_MAPPING.items():
        source = BASE / filename

        if not source.exists():
            print(f"⚠️  Not found: {filename}")
            skipped_count += 1
            continue

        # Determine destination
        dest_dir = DOCS_ROOT / project / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / filename

        # Move file
        try:
            shutil.move(str(source), str(dest))
            print(f"✅ Moved: {filename}")
            print(f"   → documents/{project}/{category}/")
            moved_count += 1
        except Exception as e:
            print(f"❌ Failed to move {filename}: {e}")
            skipped_count += 1

    # Check for other markdown files (but don't move system files)
    print(f"\n🔍 Checking for other documents...")

    other_docs = []
    for md_file in BASE.glob("*.md"):
        if md_file.name not in KEEP_AT_ROOT and md_file.name not in DOC_MAPPING:
            other_docs.append(md_file.name)

    if other_docs:
        print(f"\n📝 Found {len(other_docs)} other documents at root:")
        for doc in other_docs:
            print(f"   - {doc}")
        print("\n💡 These files will stay at root unless you specify where to move them")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Moved: {moved_count} documents")
    print(f"⚠️  Skipped: {skipped_count} documents")
    print(f"📂 Kept at root: {len(KEEP_AT_ROOT)} system files")

    if other_docs:
        print(f"📝 Other files at root: {len(other_docs)}")

    print(f"\n📁 Document structure:")
    print(f"  documents/")
    print(f"  └── unified-memory-system/")
    print(f"      ├── architecture/     ({count_files(DOCS_ROOT / 'unified-memory-system/architecture')} files)")
    print(f"      ├── guides/           ({count_files(DOCS_ROOT / 'unified-memory-system/guides')} files)")
    print(f"      └── reports/          ({count_files(DOCS_ROOT / 'unified-memory-system/reports')} files)")

    print("\n✅ Organization complete!")
    print("\n📚 Access documents:")
    print("   - Via PowerShell: open-docs")
    print("   - Via file explorer: documents/unified-memory-system/")

def count_files(path):
    """Count files in a directory"""
    if not path.exists():
        return 0
    return len([f for f in path.iterdir() if f.is_file() and f.suffix == '.md'])

def main():
    print("📦 Document Organization Tool")
    print(f"📂 Base: {BASE}")
    print(f"📁 Docs: {DOCS_ROOT}\n")

    # Verify documents root exists
    if not DOCS_ROOT.exists():
        print(f"❌ Documents root not found: {DOCS_ROOT}")
        return

    organize_documents()

if __name__ == "__main__":
    main()