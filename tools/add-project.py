#!/usr/bin/env python3
"""
Add New Project to Unified Memory System

Usage:
    py add-project.py my-new-project "My New Project"
    py add-project.py my-new-project "My New Project" --location root
    py add-project.py my-new-project "My New Project" --location "custom/path"
"""

import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import argparse

# UTF-8 for emojis
sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude")
PROJECTS_DB = BASE / "unified-memory/databases/projects-index.db"
DEFAULT_LOCATION = BASE / "claude/projects"

def create_project_memory_db(db_path):
    """Initialize a new project memory database with WAL mode"""
    conn = sqlite3.connect(db_path)

    # Create schema
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memory_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            importance INTEGER DEFAULT 2,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accessed_count INTEGER DEFAULT 0
        )
    """)

    # Enable WAL mode
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-10000")

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_importance ON memory_entries(importance)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tags ON memory_entries(tags)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON memory_entries(created_at)")

    conn.commit()
    conn.close()

def register_project(name, display_name, location):
    """Register project in projects-index.db"""

    # Determine project path
    if location == "root":
        project_path = BASE / name
    elif location == "default":
        project_path = DEFAULT_LOCATION / name
    else:
        project_path = Path(location)
        if not project_path.is_absolute():
            project_path = BASE / location / name

    # Create project folder
    project_path.mkdir(parents=True, exist_ok=True)

    # Create memory database
    memory_db = project_path / "memory.db"
    if memory_db.exists():
        print(f"⚠️  Warning: {memory_db} already exists, skipping creation")
    else:
        create_project_memory_db(memory_db)
        print(f"✅ Created: {memory_db}")

    # Generate project ID
    project_id = hashlib.md5(name.encode()).hexdigest()[:16]

    # Register in projects-index
    conn = sqlite3.connect(PROJECTS_DB)

    # Check if already exists
    cursor = conn.execute("SELECT name FROM projects WHERE name = ?", (name,))
    if cursor.fetchone():
        print(f"❌ Error: Project '{name}' already registered!")
        print("   Use 'list-projects' to see all registered projects")
        conn.close()
        return False

    # Insert new project
    now = datetime.now().isoformat()
    conn.execute("""
        INSERT INTO projects
        (project_id, name, display_name, path, status, db_path, created_at, updated_at)
        VALUES (?, ?, ?, ?, 'active', ?, ?, ?)
    """, (
        project_id,
        name,
        display_name,
        str(project_path),
        str(memory_db),
        now,
        now
    ))

    conn.commit()
    conn.close()

    print(f"\n✅ Project registered successfully!")
    print(f"\n📁 Project: {display_name}")
    print(f"   ID: {name}")
    print(f"   Location: {project_path}")
    print(f"   Memory DB: {memory_db}")
    print(f"\n🎯 You can now use:")
    print(f"   - 'Store in {name}: <content>'")
    print(f"   - 'Search {name} for <query>'")
    print(f"   - 'Get project info for {name}'")

    return True

def list_projects():
    """List all registered projects"""
    conn = sqlite3.connect(PROJECTS_DB)
    cursor = conn.execute("""
        SELECT name, display_name, path, status
        FROM projects
        ORDER BY name
    """)

    projects = cursor.fetchall()
    conn.close()

    print(f"\n📁 Registered Projects ({len(projects)}):\n")
    for name, display, path, status in projects:
        status_icon = "✅" if status == "active" else "📦"
        print(f"{status_icon} {display or name}")
        print(f"   ID: {name}")
        print(f"   Path: {path}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Add new project to unified memory system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add project in default location (claude/projects/)
  py add-project.py my-api "My API Project"

  # Add project at root level (like PeopleSoft-RAG)
  py add-project.py my-big-project "My Big Project" --location root

  # Add project in custom location
  py add-project.py experimental "Experimental" --location "experiments"

  # List all projects
  py add-project.py --list
        """
    )

    parser.add_argument("name", nargs="?", help="Project name (lowercase-with-hyphens)")
    parser.add_argument("display_name", nargs="?", help="Display name (My Project)")
    parser.add_argument(
        "--location",
        default="default",
        help="Location: 'default' (claude/projects/), 'root', or custom path"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered projects"
    )

    args = parser.parse_args()

    # List projects
    if args.list:
        list_projects()
        return

    # Validate inputs
    if not args.name:
        parser.print_help()
        return

    if not args.display_name:
        print("❌ Error: Display name is required")
        print(f"\nUsage: py add-project.py {args.name} \"Display Name\"")
        return

    # Validate name format
    if not all(c.islower() or c.isdigit() or c == '-' for c in args.name):
        print("❌ Error: Project name must be lowercase-with-hyphens")
        print(f"   Got: {args.name}")
        print(f"   Example: my-project-name")
        return

    print("=" * 60)
    print("ADD NEW PROJECT")
    print("=" * 60)
    print(f"\nName: {args.name}")
    print(f"Display: {args.display_name}")
    print(f"Location: {args.location}")
    print()

    # Register project
    success = register_project(args.name, args.display_name, args.location)

    if success:
        print("\n" + "=" * 60)
        print("✅ COMPLETE")
        print("=" * 60)
        print("\nProject is now available in:")
        print("  - Claude Desktop (via MCP tools)")
        print("  - Claude Code (via MCP tools)")
        print("\nTest it:")
        print(f"  'List all projects' → Should show {args.name}")
        print(f"  'Store in {args.name}: Test memory' → Should work")

if __name__ == "__main__":
    main()