#!/usr/bin/env python3
"""
Enhanced Migration Script - Consolidate ALL Data
Migrates LLM sessions, memory files, project notes to unified memory
Uses data-scan-report.json for comprehensive migration
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import shutil
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")
GLOBAL_DB = BASE_PATH / "unified-memory/databases/global.db"
PROJECTS_DB = BASE_PATH / "unified-memory/databases/projects-index.db"
SCAN_REPORT = BASE_PATH / "data-scan-report.json"
BACKUP_DIR = BASE_PATH / "backup-before-full-migration"

# Migration tracking
migration_stats = {
    "llm_sessions_migrated": 0,
    "memory_files_migrated": 0,
    "project_notes_migrated": 0,
    "total_entries_created": 0,
    "errors": [],
    "files_migrated": []
}

def connect_db(db_path):
    """Connect to SQLite database"""
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        print("Run: python scripts/initialize-unified-memory.py")
        return None
    return sqlite3.connect(str(db_path))

def extract_project_from_path(filepath):
    """Extract project name from file path"""
    parts = Path(filepath).parts
    if 'projects' in parts:
        idx = parts.index('projects')
        if len(parts) > idx + 1:
            return parts[idx + 1]
    return 'general'

def extract_date_from_filename(filename):
    """Extract date from filename (e.g., bootstrap-2025-09-30-122511.txt)"""
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1)
    return datetime.now().strftime('%Y-%m-%d')

def migrate_llm_sessions(conn, scan_data):
    """Migrate all LLM session files"""
    print("\n" + "="*60)
    print("📋 MIGRATING LLM SESSION FILES")
    print("="*60)

    llm_files = scan_data.get('llm_sessions', [])
    print(f"Found {len(llm_files)} LLM session files")

    for relative_path in llm_files:
        try:
            filepath = BASE_PATH / relative_path
            if not filepath.exists():
                continue

            # Read file content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Skip empty files
            if not content.strip():
                continue

            # Extract metadata
            filename = filepath.name
            project = extract_project_from_path(relative_path)
            date = extract_date_from_filename(filename)
            file_type = 'bootstrap' if 'bootstrap' in filename.lower() else \
                       'checkpoint' if 'checkpoint' in filename.lower() else \
                       'session_notes' if 'session_notes' in filename.lower() else \
                       'codex' if 'codex' in filepath.parent.name.lower() else \
                       'metrics' if 'metrics' in filepath.parent.name.lower() else \
                       'session_log'

            # Create entry with unique ID (add counter to avoid collisions)
            import time
            entry_id = f"llm_{int(time.time() * 1000000)}_{hash(str(filepath)) % 10000}"
            tags = ['llm_session', file_type, project, date]

            # Determine importance
            importance = 3 if file_type == 'checkpoint' else \
                        2 if file_type in ['bootstrap', 'codex'] else \
                        1

            # Store in global memory
            conn.execute("""
                INSERT INTO global_knowledge
                (entry_id, content, entity_name, entity_type, importance, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                content[:50000],  # Limit to 50K chars
                filename,
                'llm_session',
                importance,
                ','.join(tags),
                date
            ))

            migration_stats['llm_sessions_migrated'] += 1
            migration_stats['total_entries_created'] += 1
            migration_stats['files_migrated'].append(str(relative_path))

            if migration_stats['llm_sessions_migrated'] % 10 == 0:
                print(f"  Migrated {migration_stats['llm_sessions_migrated']} sessions...")

        except Exception as e:
            error_msg = f"Error migrating {relative_path}: {str(e)}"
            print(f"  ❌ {error_msg}")
            migration_stats['errors'].append(error_msg)

    conn.commit()
    print(f"\n✅ Migrated {migration_stats['llm_sessions_migrated']} LLM session files")

def migrate_memory_files(conn, scan_data):
    """Migrate memory JSON files"""
    print("\n" + "="*60)
    print("🧠 MIGRATING MEMORY FILES")
    print("="*60)

    memory_files = scan_data.get('memory_files', [])
    print(f"Found {len(memory_files)} memory files")

    for relative_path in memory_files:
        try:
            filepath = BASE_PATH / relative_path
            if not filepath.exists():
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different memory formats
            if isinstance(data, dict):
                for key, value in data.items():
                    content = value if isinstance(value, str) else json.dumps(value)

                    import time
                    entry_id = f"mem_{int(time.time() * 1000000)}_{hash(key) % 10000}"
                    conn.execute("""
                        INSERT INTO global_knowledge
                        (entry_id, content, entity_name, entity_type, importance, tags, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        entry_id,
                        content,
                        key,
                        'legacy_memory',
                        2,
                        'memory,legacy,migrated',
                        datetime.now().isoformat()
                    ))

                    migration_stats['total_entries_created'] += 1

            migration_stats['memory_files_migrated'] += 1
            migration_stats['files_migrated'].append(str(relative_path))

        except Exception as e:
            error_msg = f"Error migrating {relative_path}: {str(e)}"
            print(f"  ❌ {error_msg}")
            migration_stats['errors'].append(error_msg)

    conn.commit()
    print(f"✅ Migrated {migration_stats['memory_files_migrated']} memory files")

def migrate_project_notes(conn, scan_data):
    """Migrate project notes and READMEs"""
    print("\n" + "="*60)
    print("📝 MIGRATING PROJECT NOTES & READMEs")
    print("="*60)

    notes = scan_data.get('project_notes', [])
    print(f"Found {len(notes)} project documentation files")

    for relative_path in notes:
        try:
            filepath = BASE_PATH / relative_path
            if not filepath.exists():
                continue

            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Skip empty or very short files
            if len(content.strip()) < 50:
                continue

            filename = filepath.name
            project = extract_project_from_path(relative_path)

            # Determine type
            if 'readme' in filename.lower():
                doc_type = 'readme'
                importance = 3
            elif 'notes.md' in filename.lower():
                doc_type = 'session_notes'
                importance = 2
            else:
                doc_type = 'documentation'
                importance = 2

            import time
            entry_id = f"doc_{int(time.time() * 1000000)}_{hash(str(filepath)) % 10000}"
            tags = [doc_type, project, 'documentation']

            conn.execute("""
                INSERT INTO global_knowledge
                (entry_id, content, entity_name, entity_type, importance, tags, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_id,
                content[:50000],  # Limit to 50K chars
                filename,
                doc_type,
                importance,
                ','.join(tags),
                datetime.now().isoformat()
            ))

            migration_stats['project_notes_migrated'] += 1
            migration_stats['total_entries_created'] += 1
            migration_stats['files_migrated'].append(str(relative_path))

            if migration_stats['project_notes_migrated'] % 10 == 0:
                print(f"  Migrated {migration_stats['project_notes_migrated']} notes...")

        except Exception as e:
            error_msg = f"Error migrating {relative_path}: {str(e)}"
            migration_stats['errors'].append(error_msg)

    conn.commit()
    print(f"✅ Migrated {migration_stats['project_notes_migrated']} project notes")

def create_backup(scan_data, auto_mode=False):
    """Create backup of all files to be migrated"""
    print("\n" + "="*60)
    print("💾 CREATING BACKUP")
    print("="*60)

    if BACKUP_DIR.exists():
        print(f"⚠️  Backup directory exists: {BACKUP_DIR}")
        if not auto_mode:
            response = input("Overwrite? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Backup cancelled")
                return False
        else:
            print("✅ Auto mode: Overwriting backup...")
        shutil.rmtree(BACKUP_DIR)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup all file types
    all_files = (
        scan_data.get('llm_sessions', []) +
        scan_data.get('memory_files', []) +
        scan_data.get('project_notes', [])
    )

    backed_up = 0
    for relative_path in all_files:
        try:
            source = BASE_PATH / relative_path
            if not source.exists():
                continue

            dest = BACKUP_DIR / relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            backed_up += 1

            if backed_up % 20 == 0:
                print(f"  Backed up {backed_up} files...")

        except Exception as e:
            print(f"  ⚠️  Could not backup {relative_path}: {e}")

    print(f"\n✅ Backed up {backed_up} files to: {BACKUP_DIR}")
    return True

def generate_cleanup_script(scan_data):
    """Generate PowerShell cleanup script"""
    print("\n" + "="*60)
    print("🧹 GENERATING CLEANUP SCRIPT")
    print("="*60)

    cleanup_script = BASE_PATH / "cleanup-all-migrated-files.ps1"

    all_files = migration_stats['files_migrated']

    script_content = f"""# Cleanup Script - Delete ALL Migrated Files
# Generated: {datetime.now().isoformat()}
# IMPORTANT: Only run AFTER verifying migration succeeded!

Write-Host "WARNING: This will delete {len(all_files)} migrated files" -ForegroundColor Yellow
Write-Host "Backup location: {BACKUP_DIR}" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files to delete:" -ForegroundColor Yellow
Write-Host "  - {migration_stats['llm_sessions_migrated']} LLM session files"
Write-Host "  - {migration_stats['memory_files_migrated']} memory files"
Write-Host "  - {migration_stats['project_notes_migrated']} project notes"
Write-Host ""
$confirm = Read-Host "Type 'DELETE ALL' to confirm deletion"

if ($confirm -ne 'DELETE ALL') {{
    Write-Host "Cancelled - nothing deleted" -ForegroundColor Green
    exit
}}

Write-Host "Deleting migrated files..." -ForegroundColor Yellow

"""

    # Add delete commands
    for filepath in all_files:
        full_path = BASE_PATH / filepath
        script_content += f'Remove-Item "{full_path}" -Force -ErrorAction SilentlyContinue\n'

    script_content += f"""
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "Deleted: {len(all_files)} files" -ForegroundColor Cyan
Write-Host "Backup preserved at: {BACKUP_DIR}" -ForegroundColor Cyan
"""

    with open(cleanup_script, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"✅ Cleanup script: {cleanup_script}")
    print("⚠️  DO NOT RUN until migration verified!")

def generate_migration_report():
    """Generate detailed migration report"""
    print("\n" + "="*60)
    print("📊 GENERATING REPORT")
    print("="*60)

    report = {
        "migration_date": datetime.now().isoformat(),
        "statistics": {
            "llm_sessions_migrated": migration_stats['llm_sessions_migrated'],
            "memory_files_migrated": migration_stats['memory_files_migrated'],
            "project_notes_migrated": migration_stats['project_notes_migrated'],
            "total_entries_created": migration_stats['total_entries_created'],
            "total_files_migrated": len(migration_stats['files_migrated']),
            "errors_count": len(migration_stats['errors'])
        },
        "files_migrated": migration_stats['files_migrated'],
        "errors": migration_stats['errors']
    }

    report_file = BASE_PATH / "full-migration-report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved: {report_file}")

    # Print summary
    print("\n" + "="*60)
    print("📈 MIGRATION SUMMARY")
    print("="*60)
    print(f"\n✅ LLM Session Files: {migration_stats['llm_sessions_migrated']}")
    print(f"✅ Memory Files: {migration_stats['memory_files_migrated']}")
    print(f"✅ Project Notes/READMEs: {migration_stats['project_notes_migrated']}")
    print(f"✅ Total Database Entries: {migration_stats['total_entries_created']}")
    print(f"⚠️  Errors: {len(migration_stats['errors'])}")

    if migration_stats['errors']:
        print("\n❌ Errors encountered (first 5):")
        for err in migration_stats['errors'][:5]:
            print(f"  • {err}")

def main():
    """Main migration workflow"""
    import argparse
    parser = argparse.ArgumentParser(description='Migrate all data to unified memory')
    parser.add_argument('--auto', action='store_true', help='Run without prompts')
    args = parser.parse_args()

    print("="*60)
    print("🚀 COMPREHENSIVE DATA MIGRATION")
    print("="*60)
    print("\nMigrates ALL discovered data to unified memory:")
    print("  • LLM session files → SQLite (searchable)")
    print("  • Memory files → SQLite (searchable)")
    print("  • Project notes/READMEs → SQLite (searchable)")
    print("\n⚠️  Files will NOT be deleted automatically")
    print("="*60)

    # Check for scan report
    if not SCAN_REPORT.exists():
        print(f"\n❌ Scan report not found: {SCAN_REPORT}")
        print("Run: python tools/scan-all-data.py")
        return

    # Load scan data
    with open(SCAN_REPORT, 'r', encoding='utf-8') as f:
        scan_data = json.load(f)

    total_files = (
        len(scan_data.get('llm_sessions', [])) +
        len(scan_data.get('memory_files', [])) +
        len(scan_data.get('project_notes', []))
    )

    print(f"\n📊 Files to migrate: {total_files}")

    if not args.auto:
        response = input("\nProceed? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return
    else:
        print("\n✅ Auto mode enabled")

    # Connect to database
    conn = connect_db(GLOBAL_DB)
    if not conn:
        return

    # Create backup
    if not create_backup(scan_data, auto_mode=args.auto):
        print("❌ Migration aborted")
        return

    # Migrate all data
    migrate_llm_sessions(conn, scan_data)
    migrate_memory_files(conn, scan_data)
    migrate_project_notes(conn, scan_data)

    conn.close()

    # Generate outputs
    generate_migration_report()
    generate_cleanup_script(scan_data)

    # Final summary
    print("\n" + "="*60)
    print("✅ MIGRATION COMPLETE")
    print("="*60)
    print("\n📋 Next Steps:")
    print(f"  1. ✅ Backup: {BACKUP_DIR}")
    print(f"  2. ✅ Migrated {migration_stats['total_entries_created']} entries to SQLite")
    print("  3. 🧪 Test: Ask me 'search global memory for sessions'")
    print("  4. 📄 Review: full-migration-report.json")
    print("  5. 🗑️  After verification: Run cleanup-all-migrated-files.ps1")
    print("\n⚠️  IMPORTANT: Test before cleanup!")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
