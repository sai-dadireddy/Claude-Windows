#!/usr/bin/env python3
"""
Enhancement Tracker - Central coordination for parallel Workday agents
Tracks file processing status, RAG/KB updates, and agent assignments
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import time

DB_PATH = Path(__file__).parent.parent / "_data" / "enhancement_tracker.db"

def get_db():
    """Get database connection with WAL mode for concurrent access"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    return conn

def init_db():
    """Initialize the tracker database"""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            file_path TEXT UNIQUE NOT NULL,
            area TEXT NOT NULL,
            test_id TEXT NOT NULL,
            original_confidence TEXT,
            current_confidence TEXT,
            status TEXT DEFAULT 'pending',
            agent_id TEXT,
            claimed_at TEXT,
            completed_at TEXT,
            rag_updated INTEGER DEFAULT 0,
            kb_updated INTEGER DEFAULT 0,
            steps_added INTEGER DEFAULT 0,
            validation_added INTEGER DEFAULT 0,
            error_message TEXT,
            retry_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS agents (
            id TEXT PRIMARY KEY,
            area TEXT,
            status TEXT DEFAULT 'idle',
            files_processed INTEGER DEFAULT 0,
            files_failed INTEGER DEFAULT 0,
            started_at TEXT,
            last_activity TEXT,
            current_file TEXT
        );

        CREATE TABLE IF NOT EXISTS rag_updates (
            id INTEGER PRIMARY KEY,
            file_id INTEGER,
            content_type TEXT,
            content_summary TEXT,
            source_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id)
        );

        CREATE TABLE IF NOT EXISTS kb_updates (
            id INTEGER PRIMARY KEY,
            file_id INTEGER,
            kb_type TEXT,
            kb_path TEXT,
            content_hash TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id)
        );

        CREATE INDEX IF NOT EXISTS idx_files_status ON files(status);
        CREATE INDEX IF NOT EXISTS idx_files_area ON files(area);
        CREATE INDEX IF NOT EXISTS idx_files_confidence ON files(current_confidence);
    """)
    conn.commit()
    conn.close()
    print("Database initialized")

def populate_files(base_path: str, confidence_filter: List[str] = None):
    """Scan electron_tests and populate tracker with files needing enhancement"""
    if confidence_filter is None:
        confidence_filter = ['LOW', 'MEDIUM']

    base = Path(base_path)
    conn = get_db()

    added = 0
    skipped = 0

    for txt in base.rglob('*.txt'):
        area = txt.parent.name
        if area.startswith('_'):
            continue

        test_id = txt.stem

        try:
            content = txt.read_text(encoding='utf-8', errors='ignore')
        except:
            continue

        # Determine confidence
        confidence = None
        if 'CONFIDENCE: [LOW]' in content:
            confidence = 'LOW'
        elif 'CONFIDENCE: [MEDIUM]' in content:
            confidence = 'MEDIUM'
        elif 'CONFIDENCE: [HIGH]' in content:
            confidence = 'HIGH'

        # Skip if not in filter or already HIGH
        if confidence not in confidence_filter:
            skipped += 1
            continue

        # Insert or skip if exists
        try:
            conn.execute("""
                INSERT OR IGNORE INTO files
                (file_path, area, test_id, original_confidence, current_confidence, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            """, (str(txt), area, test_id, confidence, confidence))
            if conn.total_changes:
                added += 1
        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()
    conn.close()
    print(f"Added {added} files, skipped {skipped}")
    return added

def claim_file(agent_id: str, area: str = None, priority: str = 'LOW') -> Optional[Dict]:
    """Claim the next available file for processing (atomic operation)"""
    conn = get_db()

    # Build query based on filters
    where_clauses = ["status = 'pending'", "retry_count < 3"]
    params = []

    if area:
        where_clauses.append("area = ?")
        params.append(area)

    # Priority order: LOW first, then MEDIUM
    order_by = "CASE current_confidence WHEN 'LOW' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END"

    query = f"""
        SELECT * FROM files
        WHERE {' AND '.join(where_clauses)}
        ORDER BY {order_by}, id
        LIMIT 1
    """

    cursor = conn.execute(query, params)
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None

    # Claim the file
    now = datetime.now().isoformat()
    conn.execute("""
        UPDATE files SET
            status = 'in_progress',
            agent_id = ?,
            claimed_at = ?,
            updated_at = ?
        WHERE id = ? AND status = 'pending'
    """, (agent_id, now, now, row['id']))

    conn.commit()

    # Update agent status
    conn.execute("""
        INSERT OR REPLACE INTO agents (id, area, status, current_file, last_activity, started_at)
        VALUES (?, ?, 'working', ?, ?, COALESCE((SELECT started_at FROM agents WHERE id = ?), ?))
    """, (agent_id, area or row['area'], row['file_path'], now, agent_id, now))

    conn.commit()
    conn.close()

    return dict(row)

def complete_file(agent_id: str, file_id: int, success: bool,
                  new_confidence: str = None,
                  rag_updated: bool = False,
                  kb_updated: bool = False,
                  steps_added: int = 0,
                  validation_added: int = 0,
                  error_message: str = None):
    """Mark a file as completed or failed"""
    conn = get_db()
    now = datetime.now().isoformat()

    if success:
        conn.execute("""
            UPDATE files SET
                status = 'completed',
                current_confidence = COALESCE(?, current_confidence),
                completed_at = ?,
                rag_updated = ?,
                kb_updated = ?,
                steps_added = ?,
                validation_added = ?,
                updated_at = ?
            WHERE id = ?
        """, (new_confidence, now, rag_updated, kb_updated, steps_added, validation_added, now, file_id))

        # Update agent stats
        conn.execute("""
            UPDATE agents SET
                files_processed = files_processed + 1,
                current_file = NULL,
                status = 'idle',
                last_activity = ?
            WHERE id = ?
        """, (now, agent_id))
    else:
        conn.execute("""
            UPDATE files SET
                status = 'failed',
                error_message = ?,
                retry_count = retry_count + 1,
                updated_at = ?
            WHERE id = ?
        """, (error_message, now, file_id))

        # Reset to pending if retries available
        conn.execute("""
            UPDATE files SET status = 'pending'
            WHERE id = ? AND retry_count < 3
        """, (file_id,))

        conn.execute("""
            UPDATE agents SET
                files_failed = files_failed + 1,
                current_file = NULL,
                status = 'idle',
                last_activity = ?
            WHERE id = ?
        """, (now, agent_id))

    conn.commit()
    conn.close()

def log_rag_update(file_id: int, content_type: str, summary: str, source_url: str = None):
    """Log a RAG update for a file"""
    conn = get_db()
    conn.execute("""
        INSERT INTO rag_updates (file_id, content_type, content_summary, source_url)
        VALUES (?, ?, ?, ?)
    """, (file_id, content_type, summary, source_url))
    conn.commit()
    conn.close()

def log_kb_update(file_id: int, kb_type: str, kb_path: str, content_hash: str = None):
    """Log a KB update for a file"""
    conn = get_db()
    conn.execute("""
        INSERT INTO kb_updates (file_id, kb_type, kb_path, content_hash)
        VALUES (?, ?, ?, ?)
    """, (file_id, kb_type, kb_path, content_hash))
    conn.commit()
    conn.close()

def get_stats() -> Dict:
    """Get current processing statistics"""
    conn = get_db()

    stats = {
        'by_status': {},
        'by_area': {},
        'by_confidence': {},
        'agents': [],
        'recent_completions': [],
        'totals': {}
    }

    # By status
    for row in conn.execute("SELECT status, COUNT(*) as cnt FROM files GROUP BY status"):
        stats['by_status'][row['status']] = row['cnt']

    # By area (pending only)
    for row in conn.execute("""
        SELECT area,
               SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) as pending,
               SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
               SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) as in_progress
        FROM files GROUP BY area ORDER BY pending DESC
    """):
        stats['by_area'][row['area']] = {
            'pending': row['pending'],
            'completed': row['completed'],
            'in_progress': row['in_progress']
        }

    # By confidence
    for row in conn.execute("""
        SELECT current_confidence, COUNT(*) as cnt
        FROM files WHERE status='pending'
        GROUP BY current_confidence
    """):
        stats['by_confidence'][row['current_confidence'] or 'NONE'] = row['cnt']

    # Active agents
    for row in conn.execute("SELECT * FROM agents WHERE status='working' ORDER BY last_activity DESC"):
        stats['agents'].append(dict(row))

    # Recent completions
    for row in conn.execute("""
        SELECT file_path, area, original_confidence, current_confidence, completed_at
        FROM files WHERE status='completed'
        ORDER BY completed_at DESC LIMIT 10
    """):
        stats['recent_completions'].append(dict(row))

    # Totals
    row = conn.execute("""
        SELECT
            COUNT(*) as total,
            SUM(rag_updated) as rag_updates,
            SUM(kb_updated) as kb_updates,
            SUM(steps_added) as total_steps,
            SUM(validation_added) as total_validations
        FROM files WHERE status='completed'
    """).fetchone()
    stats['totals'] = dict(row)

    conn.close()
    return stats

def print_status():
    """Print a formatted status report"""
    stats = get_stats()

    print("\n" + "="*60)
    print("ENHANCEMENT TRACKER STATUS")
    print("="*60)

    print("\nBY STATUS:")
    for status, count in stats['by_status'].items():
        icon = {'pending': '[.]', 'in_progress': '[>]', 'completed': '[+]', 'failed': '[X]'}.get(status, '-')
        print(f"  {icon} {status}: {count}")

    print("\nBY AREA (pending/completed/in_progress):")
    for area, counts in sorted(stats['by_area'].items(), key=lambda x: x[1]['pending'], reverse=True)[:10]:
        print(f"  {area}: {counts['pending']}/{counts['completed']}/{counts['in_progress']}")

    print("\nPENDING BY CONFIDENCE:")
    for conf, count in stats['by_confidence'].items():
        print(f"  {conf}: {count}")

    if stats['agents']:
        print("\nACTIVE AGENTS:")
        for agent in stats['agents']:
            print(f"  {agent['id']}: {agent['current_file']}")

    if stats['totals']['total']:
        print(f"\nTOTALS (completed):")
        print(f"  Files: {stats['totals']['total']}")
        print(f"  RAG updates: {stats['totals']['rag_updates']}")
        print(f"  KB updates: {stats['totals']['kb_updates']}")
        print(f"  Steps added: {stats['totals']['total_steps']}")

    print("="*60 + "\n")

def reset_stuck_files(minutes: int = 30):
    """Reset files stuck in 'in_progress' for too long"""
    conn = get_db()
    conn.execute(f"""
        UPDATE files SET status = 'pending', agent_id = NULL
        WHERE status = 'in_progress'
        AND datetime(claimed_at) < datetime('now', '-{minutes} minutes')
    """)
    affected = conn.total_changes
    conn.commit()
    conn.close()
    print(f"Reset {affected} stuck files")
    return affected

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: enhancement_tracker.py <command>")
        print("Commands: init, populate, status, reset, claim <agent_id> [area]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        init_db()
    elif cmd == "populate":
        base = sys.argv[2] if len(sys.argv) > 2 else str(Path(__file__).parent.parent)
        populate_files(base)
    elif cmd == "status":
        print_status()
    elif cmd == "reset":
        reset_stuck_files()
    elif cmd == "claim":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else "test-agent"
        area = sys.argv[3] if len(sys.argv) > 3 else None
        file = claim_file(agent_id, area)
        if file:
            print(json.dumps(file, indent=2, default=str))
        else:
            print("No files available")
    else:
        print(f"Unknown command: {cmd}")
