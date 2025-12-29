#!/usr/bin/env python3
"""
Migration Script: Session Logs & Files → Unified Memory System
Consolidates all session logs, memory files, and documents into:
- Memory MCP (SQLite) for structured data
- LangChain MCP (Vector store) for documents

After migration, suggests safe-to-delete files.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import shutil

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuration
BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")
GLOBAL_DB = BASE_PATH / "unified-memory/databases/global.db"
PROJECTS_DB = BASE_PATH / "unified-memory/databases/projects-index.db"

# Directories to scan
SESSION_LOGS_DIR = BASE_PATH / "sessions"
MEMORY_LOGS_DIR = BASE_PATH / "memory"
DOCUMENTS_DIR = BASE_PATH / "documents"
BACKUP_DIR = BASE_PATH / "backup-before-migration"

# Track what we migrate
migration_report = {
    "session_logs": [],
    "memory_files": [],
    "documents_indexed": [],
    "files_safe_to_delete": [],
    "errors": []
}


def connect_db(db_path):
    """Connect to SQLite database"""
    if not db_path.exists():
        print(f"❌ Database not found: {db_path}")
        return None
    return sqlite3.connect(str(db_path))


def migrate_session_logs():
    """Migrate session logs to Memory MCP"""
    print("\n" + "="*60)
    print("📋 MIGRATING SESSION LOGS")
    print("="*60)

    if not SESSION_LOGS_DIR.exists():
        print(f"⚠️  Session logs directory not found: {SESSION_LOGS_DIR}")
        return

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return

    session_files = list(SESSION_LOGS_DIR.glob("**/*.json"))
    print(f"Found {len(session_files)} session log files")

    migrated = 0
    for session_file in session_files:
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract key information
            session_id = data.get('session_id', session_file.stem)
            project = data.get('project', 'general')
            summary = data.get('summary', '')
            date = data.get('date', 'unknown')

            # Store in global memory
            content = f"Session {session_id}: {summary}"

            conn.execute("""
                INSERT OR REPLACE INTO global_memory
                (key, value, tags, importance, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"session_{session_id}",
                content,
                json.dumps(['session', project, 'history']),
                1,  # Lower importance for old sessions
                json.dumps({
                    'type': 'session_log',
                    'project': project,
                    'date': date,
                    'source_file': str(session_file)
                }),
                datetime.now().isoformat()
            ))

            migrated += 1
            migration_report['session_logs'].append({
                'file': str(session_file),
                'session_id': session_id,
                'project': project
            })

        except Exception as e:
            print(f"❌ Error processing {session_file}: {e}")
            migration_report['errors'].append({
                'file': str(session_file),
                'error': str(e)
            })

    conn.commit()
    conn.close()

    print(f"✅ Migrated {migrated} session logs to Memory MCP")

    # Mark session files as safe to delete after backup
    if migrated > 0:
        migration_report['files_safe_to_delete'].extend([
            str(f) for f in session_files
        ])


def migrate_memory_files():
    """Migrate old memory files to Memory MCP"""
    print("\n" + "="*60)
    print("🧠 MIGRATING MEMORY FILES")
    print("="*60)

    if not MEMORY_LOGS_DIR.exists():
        print(f"⚠️  Memory logs directory not found: {MEMORY_LOGS_DIR}")
        return

    conn = connect_db(GLOBAL_DB)
    if not conn:
        return

    memory_files = list(MEMORY_LOGS_DIR.glob("**/*.json"))
    print(f"Found {len(memory_files)} memory files")

    migrated = 0
    for mem_file in memory_files:
        try:
            with open(mem_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle different memory file formats
            if isinstance(data, dict):
                for key, value in data.items():
                    content = value if isinstance(value, str) else json.dumps(value)

                    conn.execute("""
                        INSERT OR REPLACE INTO global_memory
                        (key, value, tags, importance, metadata, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        key,
                        content,
                        json.dumps(['migrated', 'legacy']),
                        2,  # Medium importance
                        json.dumps({
                            'type': 'legacy_memory',
                            'source_file': str(mem_file)
                        }),
                        datetime.now().isoformat()
                    ))
                    migrated += 1

            migration_report['memory_files'].append({
                'file': str(mem_file),
                'entries': migrated
            })

        except Exception as e:
            print(f"❌ Error processing {mem_file}: {e}")
            migration_report['errors'].append({
                'file': str(mem_file),
                'error': str(e)
            })

    conn.commit()
    conn.close()

    print(f"✅ Migrated {migrated} memory entries to Memory MCP")

    # Mark memory files as safe to delete after backup
    if migrated > 0:
        migration_report['files_safe_to_delete'].extend([
            str(f) for f in memory_files
        ])


def analyze_documents():
    """Analyze documents and suggest which to index"""
    print("\n" + "="*60)
    print("📄 ANALYZING DOCUMENTS")
    print("="*60)

    if not DOCUMENTS_DIR.exists():
        print(f"⚠️  Documents directory not found: {DOCUMENTS_DIR}")
        return

    # Find important documents to index
    doc_patterns = [
        "**/*.md",
        "**/*.txt",
        "**/*.pdf",
        "**/*.docx"
    ]

    important_docs = []
    for pattern in doc_patterns:
        important_docs.extend(DOCUMENTS_DIR.glob(pattern))

    print(f"Found {len(important_docs)} documents")

    # Categorize documents
    setup_docs = []
    guides = []
    reports = []
    other = []

    for doc in important_docs:
        doc_str = str(doc).lower()
        if 'setup' in doc_str or 'install' in doc_str or 'config' in doc_str:
            setup_docs.append(doc)
        elif 'guide' in doc_str or 'tutorial' in doc_str or 'how' in doc_str:
            guides.append(doc)
        elif 'report' in doc_str or 'summary' in doc_str or 'status' in doc_str:
            reports.append(doc)
        else:
            other.append(doc)

    print(f"\n📊 Document Breakdown:")
    print(f"  - Setup/Config: {len(setup_docs)}")
    print(f"  - Guides/Tutorials: {len(guides)}")
    print(f"  - Reports/Summaries: {len(reports)}")
    print(f"  - Other: {len(other)}")

    # Store recommendations
    migration_report['documents_indexed'] = {
        'total_found': len(important_docs),
        'recommended_to_index': {
            'setup_docs': [str(d) for d in setup_docs[:10]],  # Top 10
            'guides': [str(d) for d in guides[:10]],
            'reports': [str(d) for d in reports[:5]]
        }
    }

    return important_docs


def create_backup(auto_mode=False):
    """Create backup before any deletion"""
    print("\n" + "="*60)
    print("💾 CREATING BACKUP")
    print("="*60)

    if BACKUP_DIR.exists():
        print(f"⚠️  Backup directory already exists: {BACKUP_DIR}")
        if not auto_mode:
            response = input("Overwrite existing backup? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Backup cancelled")
                return False
        else:
            print("✅ Auto mode: Overwriting existing backup...")
        shutil.rmtree(BACKUP_DIR)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Backup session logs
    if SESSION_LOGS_DIR.exists():
        backup_sessions = BACKUP_DIR / "sessions"
        shutil.copytree(SESSION_LOGS_DIR, backup_sessions)
        print(f"✅ Backed up sessions to: {backup_sessions}")

    # Backup memory files
    if MEMORY_LOGS_DIR.exists():
        backup_memory = BACKUP_DIR / "memory"
        shutil.copytree(MEMORY_LOGS_DIR, backup_memory)
        print(f"✅ Backed up memory to: {backup_memory}")

    print(f"\n✅ Backup complete: {BACKUP_DIR}")
    return True


def generate_migration_report():
    """Generate detailed migration report"""
    print("\n" + "="*60)
    print("📊 MIGRATION REPORT")
    print("="*60)

    report_file = BASE_PATH / "migration-report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(migration_report, f, indent=2)

    print(f"\n📄 Detailed report saved to: {report_file}")

    # Summary
    print("\n" + "="*60)
    print("📈 MIGRATION SUMMARY")
    print("="*60)

    print(f"\n✅ Session Logs Migrated: {len(migration_report['session_logs'])}")
    print(f"✅ Memory Files Migrated: {len(migration_report['memory_files'])}")
    print(f"📄 Documents Found: {migration_report['documents_indexed'].get('total_found', 0)}")
    print(f"⚠️  Errors: {len(migration_report['errors'])}")

    if migration_report['errors']:
        print("\n❌ Errors encountered:")
        for err in migration_report['errors'][:5]:  # Show first 5
            print(f"  - {err['file']}: {err['error']}")

    # Files safe to delete
    safe_count = len(migration_report['files_safe_to_delete'])
    print(f"\n🗑️  Files Safe to Delete: {safe_count}")

    if safe_count > 0:
        print("\n⚠️  IMPORTANT: Verify backup before deleting!")
        print(f"Backup location: {BACKUP_DIR}")


def generate_cleanup_script():
    """Generate script to safely delete migrated files"""
    print("\n" + "="*60)
    print("🧹 GENERATING CLEANUP SCRIPT")
    print("="*60)

    cleanup_script = BASE_PATH / "cleanup-migrated-files.ps1"

    script_content = """# Cleanup Script - Delete Migrated Files
# Generated: {date}
# IMPORTANT: Only run this AFTER verifying:
#   1. Backup exists at: {backup}
#   2. Data migrated successfully to Memory MCP
#   3. You've tested searching the new unified memory

Write-Host "WARNING: This will delete {count} files" -ForegroundColor Yellow
Write-Host "Backup location: {backup}" -ForegroundColor Cyan
Write-Host ""
$confirm = Read-Host "Type 'DELETE' to confirm deletion"

if ($confirm -ne 'DELETE') {{
    Write-Host "Cancelled" -ForegroundColor Green
    exit
}}

Write-Host "Deleting migrated files..." -ForegroundColor Yellow

""".format(
        date=datetime.now().isoformat(),
        backup=BACKUP_DIR,
        count=len(migration_report['files_safe_to_delete'])
    )

    # Add delete commands
    for file_path in migration_report['files_safe_to_delete']:
        script_content += f'Remove-Item "{file_path}" -Force\n'

    script_content += """
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "Backup preserved at: {backup}" -ForegroundColor Cyan
""".format(backup=BACKUP_DIR)

    with open(cleanup_script, 'w', encoding='utf-8') as f:
        f.write(script_content)

    print(f"✅ Cleanup script created: {cleanup_script}")
    print(f"\n⚠️  DO NOT RUN until you've verified the migration!")


def generate_index_documents_script():
    """Generate Claude commands to index important documents"""
    print("\n" + "="*60)
    print("📚 GENERATING DOCUMENT INDEXING COMMANDS")
    print("="*60)

    commands_file = BASE_PATH / "index-documents-commands.txt"

    commands = """# Commands to Index Documents into LangChain MCP
# Copy these commands and run them in Claude Code/Desktop
# This uses FREE HuggingFace embeddings (no API key needed)

"""

    docs = migration_report['documents_indexed']

    if docs.get('recommended_to_index'):
        commands += "# Setup Documentation:\n"
        for doc in docs['recommended_to_index'].get('setup_docs', []):
            commands += f'Index the file: {doc}\n'

        commands += "\n# Guides and Tutorials:\n"
        for doc in docs['recommended_to_index'].get('guides', []):
            commands += f'Index the file: {doc}\n'

        commands += "\n# Reports and Summaries:\n"
        for doc in docs['recommended_to_index'].get('reports', []):
            commands += f'Index the file: {doc}\n'

    commands += """
# Or index entire directories:
Index all markdown files in documents/setup
Index all markdown files in documents/guides
Index all PDF files in documents/architecture

# After indexing, test with:
Search for setup instructions
Search for AWS best practices
Search for project architecture
"""

    with open(commands_file, 'w', encoding='utf-8') as f:
        f.write(commands)

    print(f"✅ Indexing commands saved to: {commands_file}")


def main():
    """Main migration workflow"""
    import argparse
    parser = argparse.ArgumentParser(description='Migrate legacy files to unified memory')
    parser.add_argument('--auto', action='store_true', help='Run without confirmation prompts')
    args = parser.parse_args()

    print("="*60)
    print("🚀 UNIFIED MEMORY MIGRATION TOOL")
    print("="*60)
    print("\nThis tool will:")
    print("  1. Migrate session logs → Memory MCP (SQLite)")
    print("  2. Migrate old memory files → Memory MCP")
    print("  3. Analyze documents for LangChain indexing")
    print("  4. Create backup of all original files")
    print("  5. Generate cleanup script (for later use)")
    print("\n⚠️  No files will be deleted automatically!")
    print("="*60)

    if not args.auto:
        response = input("\nProceed with migration? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Migration cancelled")
            return
    else:
        print("\n✅ Auto mode enabled - proceeding with migration...")

    # Step 1: Create backup
    if not create_backup(auto_mode=args.auto):
        print("❌ Migration aborted - backup failed")
        return

    # Step 2: Migrate session logs
    migrate_session_logs()

    # Step 3: Migrate memory files
    migrate_memory_files()

    # Step 4: Analyze documents
    analyze_documents()

    # Step 5: Generate reports and scripts
    generate_migration_report()
    generate_cleanup_script()
    generate_index_documents_script()

    # Final summary
    print("\n" + "="*60)
    print("✅ MIGRATION COMPLETE")
    print("="*60)
    print("\n📋 Next Steps:")
    print("  1. ✅ Backup created at: {}".format(BACKUP_DIR))
    print("  2. ✅ Data migrated to Memory MCP (SQLite)")
    print("  3. 📄 Review migration report: migration-report.json")
    print("  4. 🧪 Test searching: Ask Claude 'search global memory for sessions'")
    print("  5. 📚 Index documents: See index-documents-commands.txt")
    print("  6. 🗑️  After verification, run: cleanup-migrated-files.ps1")
    print("\n⚠️  IMPORTANT: Test the migration before running cleanup!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
