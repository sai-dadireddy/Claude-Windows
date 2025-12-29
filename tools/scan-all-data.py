#!/usr/bin/env python3
"""
Comprehensive Data Scanner
Finds all session logs, memory files, LLM logs, and project data
"""

import os
import sys
from pathlib import Path
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude")

# Data types to find
scan_results = {
    "llm_sessions": [],
    "session_logs": [],
    "memory_files": [],
    "project_notes": [],
    "context_files": [],
    "history_files": [],
    "log_files": [],
    "projects_found": []
}

# Directories to exclude
EXCLUDE_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    'backup-before-migration', 'backups', 'unified-memory',
    '.claude', 'dist', 'build'
}

def is_excluded(path):
    """Check if path should be excluded"""
    parts = Path(path).parts
    return any(excluded in parts for excluded in EXCLUDE_DIRS)

def scan_directory(directory):
    """Scan directory for relevant files"""
    print(f"\nScanning: {directory}")

    for root, dirs, files in os.walk(directory):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        if is_excluded(root):
            continue

        for file in files:
            filepath = Path(root) / file
            relative_path = filepath.relative_to(BASE_PATH)

            # Skip non-text files except JSON
            if not (file.endswith(('.json', '.txt', '.md', '.log'))):
                continue

            # Skip minified files
            if '.min.' in file:
                continue

            file_lower = file.lower()
            root_lower = root.lower()

            # Categorize files
            if 'llm_session' in root_lower or 'llm-session' in root_lower:
                scan_results['llm_sessions'].append(str(relative_path))

            elif 'session' in file_lower and file.endswith('.json'):
                scan_results['session_logs'].append(str(relative_path))

            elif 'memory' in file_lower and file.endswith('.json'):
                # Skip AWS SDK files
                if 'memorydb' not in file_lower and 'node_modules' not in root:
                    scan_results['memory_files'].append(str(relative_path))

            elif any(keyword in file_lower for keyword in ['note', 'notes', 'readme', 'todo']):
                if not file.endswith('.min.json'):
                    scan_results['project_notes'].append(str(relative_path))

            elif 'context' in file_lower:
                scan_results['context_files'].append(str(relative_path))

            elif 'history' in file_lower or 'log' in file_lower:
                scan_results['history_files'].append(str(relative_path))

            elif file.endswith('.log'):
                scan_results['log_files'].append(str(relative_path))

def find_projects():
    """Find all project directories"""
    print("\n" + "="*60)
    print("🔍 FINDING PROJECTS")
    print("="*60)

    # Look for .claude-project.md files
    for root, dirs, files in os.walk(BASE_PATH):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        if is_excluded(root):
            continue

        if '.claude-project.md' in files:
            project_path = Path(root)
            relative_path = project_path.relative_to(BASE_PATH)

            # Read project metadata
            project_file = project_path / '.claude-project.md'
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract project name from first line
                    first_line = content.split('\n')[0]
                    project_name = first_line.strip('# ').strip()
            except:
                project_name = project_path.name

            scan_results['projects_found'].append({
                'name': project_name,
                'path': str(relative_path),
                'config_file': str(relative_path / '.claude-project.md')
            })
            print(f"  📁 Found project: {project_name}")

def print_summary():
    """Print scan summary"""
    print("\n" + "="*60)
    print("📊 SCAN SUMMARY")
    print("="*60)

    print(f"\n✅ LLM Session Files: {len(scan_results['llm_sessions'])}")
    print(f"✅ Session Logs: {len(scan_results['session_logs'])}")
    print(f"✅ Memory Files: {len(scan_results['memory_files'])}")
    print(f"✅ Project Notes/READMEs: {len(scan_results['project_notes'])}")
    print(f"✅ Context Files: {len(scan_results['context_files'])}")
    print(f"✅ History/Log Files: {len(scan_results['history_files']) + len(scan_results['log_files'])}")
    print(f"✅ Projects Found: {len(scan_results['projects_found'])}")

    total_files = sum([
        len(scan_results['llm_sessions']),
        len(scan_results['session_logs']),
        len(scan_results['memory_files']),
        len(scan_results['project_notes']),
        len(scan_results['context_files']),
        len(scan_results['history_files']),
        len(scan_results['log_files'])
    ])

    print(f"\n📄 Total files to migrate: {total_files}")

def print_details():
    """Print detailed findings"""
    print("\n" + "="*60)
    print("📋 DETAILED FINDINGS")
    print("="*60)

    if scan_results['llm_sessions']:
        print(f"\n🔷 LLM Session Files ({len(scan_results['llm_sessions'])})")
        for f in scan_results['llm_sessions'][:10]:
            print(f"  • {f}")
        if len(scan_results['llm_sessions']) > 10:
            print(f"  ... and {len(scan_results['llm_sessions']) - 10} more")

    if scan_results['session_logs']:
        print(f"\n🔷 Session Logs ({len(scan_results['session_logs'])})")
        for f in scan_results['session_logs'][:10]:
            print(f"  • {f}")
        if len(scan_results['session_logs']) > 10:
            print(f"  ... and {len(scan_results['session_logs']) - 10} more")

    if scan_results['memory_files']:
        print(f"\n🔷 Memory Files ({len(scan_results['memory_files'])})")
        for f in scan_results['memory_files'][:10]:
            print(f"  • {f}")
        if len(scan_results['memory_files']) > 10:
            print(f"  ... and {len(scan_results['memory_files']) - 10} more")

    if scan_results['project_notes']:
        print(f"\n🔷 Project Notes/READMEs ({len(scan_results['project_notes'])})")
        for f in scan_results['project_notes'][:10]:
            print(f"  • {f}")
        if len(scan_results['project_notes']) > 10:
            print(f"  ... and {len(scan_results['project_notes']) - 10} more")

    if scan_results['projects_found']:
        print(f"\n🔷 Projects ({len(scan_results['projects_found'])})")
        for proj in scan_results['projects_found']:
            print(f"  • {proj['name']} ({proj['path']})")

def save_report():
    """Save detailed report to JSON"""
    report_file = BASE_PATH / "data-scan-report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(scan_results, f, indent=2)
    print(f"\n💾 Detailed report saved to: {report_file}")

def main():
    print("="*60)
    print("🔍 COMPREHENSIVE DATA SCANNER")
    print("="*60)
    print("\nScanning for all session logs, memory files, and project data...")
    print(f"Base path: {BASE_PATH}")
    print(f"Excluding: {', '.join(EXCLUDE_DIRS)}")

    # Find projects first
    find_projects()

    # Scan main directories
    scan_directory(BASE_PATH)

    # Print results
    print_summary()
    print_details()
    save_report()

    print("\n" + "="*60)
    print("✅ SCAN COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("  1. Review data-scan-report.json for all findings")
    print("  2. Run enhanced migration script to consolidate all data")
    print("  3. All data will be stored in unified memory (short/long term)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Scan cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
