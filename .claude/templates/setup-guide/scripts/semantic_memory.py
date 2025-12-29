#!/usr/bin/env python3
"""
Semantic Memory System for Claude Code
Uses Gemini API for embeddings and SQLite for vector storage.

Features:
- Vector embeddings for semantic search
- Automatic similarity matching
- Knowledge graph relationships
- Cross-session memory persistence
"""

import json
import sys
import os
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from typing import Optional

# Configuration
MEMORY_DIR = Path.home() / ".claude" / "memory"
DB_PATH = MEMORY_DIR / "semantic.db"
ENV_PATH = MEMORY_DIR / ".env"
SIMILARITY_THRESHOLD = 0.3  # Lowered for better recall
MAX_RESULTS = 5

def load_api_key() -> Optional[str]:
    """Load Gemini API key from .env file."""
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("GEMINI_API_KEY")

def get_embedding(text: str, api_key: str) -> Optional[list]:
    """Get embedding vector from Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={api_key}"

    payload = {
        "model": "models/text-embedding-004",
        "content": {"parts": [{"text": text[:8000]}]}  # Limit text length
    }

    try:
        request = Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("embedding", {}).get("values", [])
    except (URLError, HTTPError, json.JSONDecodeError) as e:
        print(f"Embedding error: {e}", file=sys.stderr)
        return None

def cosine_similarity(vec1: list, vec2: list) -> float:
    """Calculate cosine similarity between two vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)

def init_db():
    """Initialize SQLite database with vector storage."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Memories table with embeddings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            project TEXT NOT NULL,
            memory_type TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT,
            metadata TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    # Sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            project TEXT NOT NULL,
            summary TEXT,
            embedding TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    # Knowledge graph edges
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            target_id TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            created_at TEXT NOT NULL
        )
    ''')

    # Indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_project ON memories(project)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project)')

    conn.commit()
    conn.close()

def generate_id(content: str) -> str:
    """Generate unique ID from content hash."""
    return hashlib.md5(content.encode()).hexdigest()[:12]

# === MEMORY OPERATIONS ===

def save_memory(project: str, memory_type: str, content: str, metadata: dict = None) -> dict:
    """Save memory with embedding."""
    init_db()
    api_key = load_api_key()

    memory_id = generate_id(f"{project}:{memory_type}:{content}")
    now = datetime.now().isoformat()

    # Get embedding if API key available
    embedding = None
    if api_key:
        embedding = get_embedding(content, api_key)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO memories
        (id, project, memory_type, content, embedding, metadata, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        memory_id,
        project,
        memory_type,
        content,
        json.dumps(embedding) if embedding else None,
        json.dumps(metadata) if metadata else None,
        now,
        now
    ))

    conn.commit()
    conn.close()

    return {
        "status": "saved",
        "id": memory_id,
        "has_embedding": embedding is not None
    }

def search_memories(project: str, query: str, max_results: int = MAX_RESULTS) -> list:
    """Search memories using semantic similarity."""
    init_db()
    api_key = load_api_key()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all memories for project (and global)
    cursor.execute('''
        SELECT id, project, memory_type, content, embedding, metadata, created_at
        FROM memories
        WHERE project = ? OR project = 'global'
        ORDER BY updated_at DESC
    ''', (project,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    # If we have API key and query, do semantic search
    if api_key and query:
        query_embedding = get_embedding(query, api_key)

        if query_embedding:
            results = []
            for row in rows:
                memory_embedding = json.loads(row[4]) if row[4] else None

                if memory_embedding:
                    similarity = cosine_similarity(query_embedding, memory_embedding)
                    if similarity >= SIMILARITY_THRESHOLD:
                        results.append({
                            "id": row[0],
                            "project": row[1],
                            "type": row[2],
                            "content": row[3],
                            "similarity": round(similarity, 3),
                            "created_at": row[6]
                        })
                else:
                    # Fallback: keyword match for memories without embeddings
                    if query.lower() in row[3].lower():
                        results.append({
                            "id": row[0],
                            "project": row[1],
                            "type": row[2],
                            "content": row[3],
                            "similarity": 0.5,
                            "created_at": row[6]
                        })

            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:max_results]

    # Fallback: keyword search
    results = []
    for row in rows:
        if not query or query.lower() in row[3].lower():
            results.append({
                "id": row[0],
                "project": row[1],
                "type": row[2],
                "content": row[3],
                "similarity": 1.0 if not query else 0.5,
                "created_at": row[6]
            })

    return results[:max_results]

def get_context_for_message(project: str, message: str) -> str:
    """Get relevant context for a user message."""
    memories = search_memories(project, message, max_results=5)

    if not memories:
        return ""

    context_parts = []
    for mem in memories:
        context_parts.append(f"[{mem['type']}] {mem['content']}")

    return "\n".join(context_parts)

# === SESSION OPERATIONS ===

def save_session(session_id: str, project: str, summary: str) -> dict:
    """Save session with embedding."""
    init_db()
    api_key = load_api_key()

    now = datetime.now().isoformat()

    embedding = None
    if api_key:
        embedding = get_embedding(summary, api_key)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR REPLACE INTO sessions (id, project, summary, embedding, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        session_id[:12],
        project,
        summary,
        json.dumps(embedding) if embedding else None,
        now
    ))

    conn.commit()
    conn.close()

    return {"status": "saved", "session_id": session_id[:12]}

def get_last_session(project: str) -> Optional[dict]:
    """Get the most recent session for a project."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, project, summary, created_at
        FROM sessions
        WHERE project = ?
        ORDER BY created_at DESC
        LIMIT 1
    ''', (project,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "project": row[1],
            "summary": row[2],
            "created_at": row[3]
        }
    return None

# === RELATIONSHIP OPERATIONS ===

def add_relationship(source_id: str, target_id: str, relation_type: str, weight: float = 1.0):
    """Add relationship between memories."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO relationships (source_id, target_id, relation_type, weight, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (source_id, target_id, relation_type, weight, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def get_related_memories(memory_id: str) -> list:
    """Get memories related to a given memory."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT m.id, m.content, m.memory_type, r.relation_type, r.weight
        FROM relationships r
        JOIN memories m ON r.target_id = m.id
        WHERE r.source_id = ?
        ORDER BY r.weight DESC
    ''', (memory_id,))

    rows = cursor.fetchall()
    conn.close()

    return [{"id": r[0], "content": r[1], "type": r[2], "relation": r[3], "weight": r[4]} for r in rows]

# === STATS ===

def get_stats(project: str = None) -> dict:
    """Get memory statistics."""
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if project:
        cursor.execute('SELECT COUNT(*) FROM memories WHERE project = ?', (project,))
        memory_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE project = ?', (project,))
        session_count = cursor.fetchone()[0]
    else:
        cursor.execute('SELECT COUNT(*) FROM memories')
        memory_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM sessions')
        session_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM relationships')
    relationship_count = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM memories WHERE embedding IS NOT NULL')
    embedded_count = cursor.fetchone()[0]

    conn.close()

    return {
        "memories": memory_count,
        "sessions": session_count,
        "relationships": relationship_count,
        "with_embeddings": embedded_count,
        "db_path": str(DB_PATH)
    }

# === CLI ===

def main():
    if len(sys.argv) < 2:
        print("Usage: semantic_memory.py <command> [args]")
        print("Commands: save, search, context, session-save, session-get, stats")
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "save":
            project, mem_type, content = sys.argv[2], sys.argv[3], sys.argv[4]
            result = save_memory(project, mem_type, content)
            print(json.dumps(result))

        elif command == "search":
            project = sys.argv[2]
            query = sys.argv[3] if len(sys.argv) > 3 else ""
            results = search_memories(project, query)
            print(json.dumps(results, indent=2))

        elif command == "context":
            project, message = sys.argv[2], sys.argv[3]
            context = get_context_for_message(project, message)
            print(context)

        elif command == "session-save":
            session_id, project, summary = sys.argv[2], sys.argv[3], sys.argv[4]
            result = save_session(session_id, project, summary)
            print(json.dumps(result))

        elif command == "session-get":
            project = sys.argv[2]
            result = get_last_session(project)
            print(json.dumps(result) if result else "")

        elif command == "stats":
            project = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_stats(project)
            print(json.dumps(result, indent=2))

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except IndexError:
        print(f"Missing arguments for {command}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
