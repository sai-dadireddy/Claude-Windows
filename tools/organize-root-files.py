#!/usr/bin/env python3
"""
Organize Root Files
Moves documentation to proper folders and identifies files to delete
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")

# File organization rules
ORGANIZE_RULES = {
    # Keep in root (important config files)
    'keep_root': [
        '.claude-project.md',
        'README.md',
        'claude.md',
        'CLAUDE.md'
    ],

    # Move to documents/setup/
    'setup_docs': [
        'AUTO_MEMORY_ACTIVATED.md',
        'CLEANUP_READY.md',
        'FIX_APPLIED.md',
        'CLAUDE_DESKTOP_FULL_INSTRUCTIONS.md',
        'CLAUDE_DESKTOP_FULL_INSTRUCTIONS.txt',
        'INSTRUCTIONS_MIGRATION_COMPLETE.md',
        'TEST_AND_CLEANUP_GUIDE.md',
        'QUICK_START.md'
    ],

    # Move to documents/reports/
    'reports': [
        'CHANGES_SUMMARY.md',
        'data-scan-report.json',
        'full-migration-report.json',
        'migration-report.json'
    ],

    # Move to documents/reference/
    'reference': [
        'index-documents-commands.txt'
    ],

    # Delete (temporary/duplicate files)
    'delete': [
        'cleanup-migrated-files.ps1',
        'cleanup-all-migrated-files.ps1',
        'onescriptsetup.ps1'
    ]
}

def scan_root_files():
    """Scan all markdown/text/json files in root"""
    print("="*60)
    print("📋 SCANNING ROOT DIRECTORY")
    print("="*60)

    files = {
        'markdown': [],
        'text': [],
        'json': [],
        'scripts': [],
        'other': []
    }

    for item in BASE_PATH.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            if ext == '.md':
                files['markdown'].append(item.name)
            elif ext == '.txt':
                files['text'].append(item.name)
            elif ext == '.json':
                files['json'].append(item.name)
            elif ext in ['.ps1', '.sh', '.bat']:
                files['scripts'].append(item.name)
            elif ext in ['.py']:
                files['other'].append(item.name)

    print(f"\nFound in root:")
    print(f"  Markdown: {len(files['markdown'])}")
    print(f"  Text: {len(files['text'])}")
    print(f"  JSON: {len(files['json'])}")
    print(f"  Scripts: {len(files['scripts'])}")
    print(f"  Other: {len(files['other'])}")

    return files

def organize_files(dry_run=True):
    """Organize files according to rules"""
    print("\n" + "="*60)
    print("📁 FILE ORGANIZATION PLAN")
    print("="*60)

    actions = {
        'keep': [],
        'move': [],
        'delete': []
    }

    # Scan all files in root
    for item in BASE_PATH.iterdir():
        if not item.is_file():
            continue

        filename = item.name

        # Check if should keep in root
        if filename in ORGANIZE_RULES['keep_root']:
            actions['keep'].append(filename)
            continue

        # Check if should move to setup docs
        if filename in ORGANIZE_RULES['setup_docs']:
            dest = BASE_PATH / "documents/setup" / filename
            actions['move'].append({
                'file': filename,
                'from': item,
                'to': dest,
                'category': 'setup'
            })
            continue

        # Check if should move to reports
        if filename in ORGANIZE_RULES['reports']:
            dest = BASE_PATH / "documents/reports" / filename
            actions['move'].append({
                'file': filename,
                'from': item,
                'to': dest,
                'category': 'reports'
            })
            continue

        # Check if should move to reference
        if filename in ORGANIZE_RULES['reference']:
            dest = BASE_PATH / "documents/reference" / filename
            actions['move'].append({
                'file': filename,
                'from': item,
                'to': dest,
                'category': 'reference'
            })
            continue

        # Check if should delete
        if filename in ORGANIZE_RULES['delete']:
            actions['delete'].append({
                'file': filename,
                'path': item,
                'reason': 'temporary/duplicate'
            })

    # Print plan
    print(f"\n✅ KEEP IN ROOT ({len(actions['keep'])} files):")
    for filename in actions['keep']:
        print(f"  • {filename}")

    print(f"\n📦 MOVE TO FOLDERS ({len(actions['move'])} files):")
    for action in actions['move']:
        print(f"  • {action['file']} → documents/{action['category']}/")

    print(f"\n🗑️  DELETE ({len(actions['delete'])} files):")
    for action in actions['delete']:
        print(f"  • {action['file']} ({action['reason']})")

    # Execute if not dry run
    if not dry_run:
        print("\n" + "="*60)
        print("📁 EXECUTING ORGANIZATION")
        print("="*60)

        # Create directories if needed
        (BASE_PATH / "documents/setup").mkdir(parents=True, exist_ok=True)
        (BASE_PATH / "documents/reports").mkdir(parents=True, exist_ok=True)
        (BASE_PATH / "documents/reference").mkdir(parents=True, exist_ok=True)

        # Move files
        for action in actions['move']:
            try:
                shutil.move(str(action['from']), str(action['to']))
                print(f"✅ Moved: {action['file']}")
            except Exception as e:
                print(f"❌ Error moving {action['file']}: {e}")

        # Delete files
        for action in actions['delete']:
            try:
                action['path'].unlink()
                print(f"🗑️  Deleted: {action['file']}")
            except Exception as e:
                print(f"❌ Error deleting {action['file']}: {e}")

        print("\n✅ Organization complete!")
    else:
        print("\n" + "="*60)
        print("ℹ️  DRY RUN - No changes made")
        print("="*60)
        print("\nTo execute, run with --execute flag")

    return actions

def find_duplicates():
    """Find duplicate documentation"""
    print("\n" + "="*60)
    print("🔍 CHECKING FOR DUPLICATES")
    print("="*60)

    # Check for duplicate setup guides
    setup_docs = list((BASE_PATH / "documents/setup").glob("*.md"))
    root_docs = [f for f in BASE_PATH.glob("*.md") if f.is_file()]

    duplicates = []
    for root_doc in root_docs:
        for setup_doc in setup_docs:
            if root_doc.name == setup_doc.name:
                # Check if content is similar
                if root_doc.stat().st_size == setup_doc.stat().st_size:
                    duplicates.append({
                        'name': root_doc.name,
                        'root': root_doc,
                        'existing': setup_doc
                    })

    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} potential duplicate(s):")
        for dup in duplicates:
            print(f"  • {dup['name']}")
            print(f"    Root: {dup['root']}")
            print(f"    Existing: {dup['existing']}")
    else:
        print("\n✅ No duplicates found")

    return duplicates

def main():
    """Main organization workflow"""
    import argparse
    parser = argparse.ArgumentParser(description='Organize root directory files')
    parser.add_argument('--execute', action='store_true', help='Execute the organization (default is dry run)')
    args = parser.parse_args()

    print("="*60)
    print("🗂️  ROOT DIRECTORY ORGANIZATION")
    print("="*60)
    print(f"\nBase path: {BASE_PATH}")
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY RUN'}")

    # Scan files
    files = scan_root_files()

    # Find duplicates
    find_duplicates()

    # Organize
    actions = organize_files(dry_run=not args.execute)

    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"\n✅ Keep in root: {len(actions['keep'])}")
    print(f"📦 Move to folders: {len(actions['move'])}")
    print(f"🗑️  Delete: {len(actions['delete'])}")

    if not args.execute:
        print("\n" + "="*60)
        print("ℹ️  To apply these changes, run:")
        print("  python tools/organize-root-files.py --execute")
        print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
