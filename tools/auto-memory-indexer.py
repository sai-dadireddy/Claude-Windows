#!/usr/bin/env python3
"""
Auto Memory Indexer - Automatically updates memory.db and vector stores
Runs after Claude Code sessions to capture conversation context
"""

import sqlite3
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(os.getenv('BASE_DIR', 'C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/claude'))
VECTOR_STORE = Path(os.getenv('VECTOR_STORE', 'C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/unified-memory/vector-store'))

class AutoMemoryIndexer:
    """Automatically index conversations and updates to memory systems"""

    def __init__(self, project_name=None):
        self.project_name = project_name or os.getenv('PROJECT_NAME', 'default')
        self.project_dir = BASE_DIR / 'projects' / self.project_name.lower()
        self.memory_db = self.project_dir / 'memory.db'
        self.global_db = BASE_DIR.parent / 'unified-memory' / 'databases' / 'global.db'

    def initialize_memory_db(self):
        """Create memory.db if it doesn't exist"""
        self.memory_db.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_name TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            content TEXT NOT NULL,
            importance INTEGER DEFAULT 1,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_entity_name ON project_memory(entity_name)
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_entity_type ON project_memory(entity_type)
        ''')

        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_importance ON project_memory(importance)
        ''')

        conn.commit()
        conn.close()
        print(f"[OK] Memory DB initialized: {self.memory_db}")

    def store_memory(self, entity_name, entity_type, content, importance=2, tags=None):
        """Store a memory entry"""
        if not self.memory_db.exists():
            self.initialize_memory_db()

        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        tags_str = json.dumps(tags) if tags else '[]'

        # Check if exists
        cursor.execute('''
        SELECT id FROM project_memory WHERE entity_name = ? AND entity_type = ?
        ''', (entity_name, entity_type))

        existing = cursor.fetchone()

        if existing:
            # Update
            cursor.execute('''
            UPDATE project_memory
            SET content = ?, importance = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''', (content, importance, tags_str, existing[0]))
            print(f"[UPDATE] Memory updated: {entity_name}")
        else:
            # Insert
            cursor.execute('''
            INSERT INTO project_memory (entity_name, entity_type, content, importance, tags)
            VALUES (?, ?, ?, ?, ?)
            ''', (entity_name, entity_type, content, importance, tags_str))
            print(f"[NEW] Memory created: {entity_name}")

        conn.commit()
        conn.close()

    def index_session_files(self, session_dir):
        """Index all files from a session directory"""
        session_path = Path(session_dir)

        if not session_path.exists():
            print(f"[WARN] Session directory not found: {session_dir}")
            return

        # Find all artifacts
        artifacts_dir = session_path / 'artifacts'
        if not artifacts_dir.exists():
            print(f"[WARN] No artifacts directory found")
            return

        indexed_count = 0

        # Index all files
        for file_path in artifacts_dir.rglob('*'):
            if file_path.is_file():
                try:
                    # Read file content
                    if file_path.suffix in ['.md', '.txt', '.json', '.py', '.js', '.ts']:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Store to memory.db
                        relative_path = file_path.relative_to(self.project_dir)
                        self.store_memory(
                            entity_name=str(relative_path),
                            entity_type='file',
                            content=content[:1000],  # Store first 1000 chars
                            importance=2,
                            tags=[self.project_name, file_path.suffix[1:], 'session-artifact']
                        )

                        indexed_count += 1

                except Exception as e:
                    print(f"[ERROR] Error indexing {file_path}: {e}")

        print(f"[OK] Indexed {indexed_count} files from session")

    def capture_session_context(self, session_id, summary, importance=3):
        """Capture high-level session context"""
        self.store_memory(
            entity_name=f"session_{session_id}",
            entity_type='session_summary',
            content=summary,
            importance=importance,
            tags=[self.project_name, 'session', datetime.now().strftime('%Y-%m-%d')]
        )
        print(f"[OK] Session context captured: {session_id}")

    def get_stats(self):
        """Get memory statistics"""
        if not self.memory_db.exists():
            return {"total": 0, "by_type": {}, "by_importance": {}}

        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        # Total count
        cursor.execute('SELECT COUNT(*) FROM project_memory')
        total = cursor.fetchone()[0]

        # By type
        cursor.execute('SELECT entity_type, COUNT(*) FROM project_memory GROUP BY entity_type')
        by_type = dict(cursor.fetchall())

        # By importance
        cursor.execute('SELECT importance, COUNT(*) FROM project_memory GROUP BY importance')
        by_importance = dict(cursor.fetchall())

        conn.close()

        return {
            "total": total,
            "by_type": by_type,
            "by_importance": by_importance
        }


def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description='Auto Memory Indexer')
    parser.add_argument('--project', type=str, help='Project name')
    parser.add_argument('--session', type=str, help='Session directory to index')
    parser.add_argument('--init', action='store_true', help='Initialize memory.db')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--capture', type=str, help='Capture session summary')

    args = parser.parse_args()

    project_name = args.project or os.getenv('PROJECT_NAME', 'default')
    indexer = AutoMemoryIndexer(project_name)

    if args.init:
        indexer.initialize_memory_db()

    if args.session:
        print(f"[INDEX] Indexing session: {args.session}")
        indexer.index_session_files(args.session)

    if args.capture:
        session_id = datetime.now().strftime('%Y-%m-%d_%H%M')
        indexer.capture_session_context(session_id, args.capture)

    if args.stats:
        stats = indexer.get_stats()
        print(f"\n[STATS] Memory Statistics for {project_name}:")
        print(f"   Total entries: {stats['total']}")
        print(f"   By type: {stats['by_type']}")
        print(f"   By importance: {stats['by_importance']}")


if __name__ == '__main__':
    main()
