#!/usr/bin/env python3
"""
Memory Manager for Claude Code
Handles short-term (session) and long-term (persistent) memory storage.
Now with semantic search via Gemini embeddings!

Usage:
  memory_manager.py save-session <session_id> <project> <content>
  memory_manager.py load-session <session_id> <project>
  memory_manager.py save-memory <project> <type> <content>
  memory_manager.py load-memories <project> [query]
  memory_manager.py search <project> <query>  # Semantic search
  memory_manager.py context <project> <message>  # Get context for message
  memory_manager.py list-sessions <project>
  memory_manager.py get-last-session <project>
  memory_manager.py stats [project]
"""

import json
import sys
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

# Semantic memory script
SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"

def use_semantic(command: str, *args) -> str:
    """Call semantic memory system."""
    if not SEMANTIC_SCRIPT.exists():
        return ""
    try:
        result = subprocess.run(
            ["python3", str(SEMANTIC_SCRIPT), command] + list(args),
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip()
    except:
        return ""

# Directories
MEMORY_DIR = Path.home() / ".claude" / "memory"
SHORT_TERM = MEMORY_DIR / "short-term"
LONG_TERM = MEMORY_DIR / "long-term"

def ensure_dirs():
    """Ensure memory directories exist."""
    SHORT_TERM.mkdir(parents=True, exist_ok=True)
    LONG_TERM.mkdir(parents=True, exist_ok=True)
    (LONG_TERM / "global").mkdir(exist_ok=True)

def get_project_dir(project: str) -> Path:
    """Get or create project memory directory."""
    project_dir = LONG_TERM / sanitize_name(project)
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir

def sanitize_name(name: str) -> str:
    """Sanitize name for filesystem."""
    return re.sub(r'[^\w\-]', '_', name.lower())[:50]

def get_timestamp() -> str:
    """Get ISO timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date_stamp() -> str:
    """Get date stamp for filenames."""
    return datetime.now().strftime("%Y-%m-%d")

# === SHORT-TERM MEMORY (Session) ===

def save_session(session_id: str, project: str, content: str) -> dict:
    """Save session state to short-term memory."""
    ensure_dirs()

    session_file = SHORT_TERM / f"{sanitize_name(project)}_{session_id[:8]}.md"

    # Build session document
    doc = f"""# Session: {session_id[:8]}
**Project**: {project}
**Saved**: {get_timestamp()}

## Session State
{content}
"""

    session_file.write_text(doc)

    # Also update last session pointer
    pointer_file = SHORT_TERM / f"{sanitize_name(project)}_last.txt"
    pointer_file.write_text(session_id[:8])

    return {"status": "saved", "file": str(session_file)}

def load_session(session_id: str, project: str) -> str:
    """Load session from short-term memory."""
    ensure_dirs()

    # If session_id is "last", get the last session
    if session_id == "last":
        pointer_file = SHORT_TERM / f"{sanitize_name(project)}_last.txt"
        if pointer_file.exists():
            session_id = pointer_file.read_text().strip()
        else:
            return ""

    session_file = SHORT_TERM / f"{sanitize_name(project)}_{session_id[:8]}.md"

    if session_file.exists():
        return session_file.read_text()
    return ""

def list_sessions(project: str) -> list:
    """List all sessions for a project."""
    ensure_dirs()

    prefix = sanitize_name(project)
    sessions = []

    for f in SHORT_TERM.glob(f"{prefix}_*.md"):
        stat = f.stat()
        sessions.append({
            "file": f.name,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "size": stat.st_size
        })

    return sorted(sessions, key=lambda x: x["modified"], reverse=True)

def get_last_session(project: str) -> str:
    """Get the last session ID for a project."""
    pointer_file = SHORT_TERM / f"{sanitize_name(project)}_last.txt"
    if pointer_file.exists():
        return pointer_file.read_text().strip()
    return ""

# === LONG-TERM MEMORY ===

def save_memory(project: str, memory_type: str, content: str) -> dict:
    """Save to long-term memory (both file and semantic DB)."""
    ensure_dirs()

    # Memory types map to files
    type_files = {
        "decision": "decisions.md",
        "learning": "learnings.md",
        "context": "context.md",
        "preference": "preferences.md",
        "architecture": "architecture.md",
        "bug": "bugs_and_fixes.md",
        "todo": "todos.md",
    }

    filename = type_files.get(memory_type.lower(), "notes.md")

    if project.lower() == "global":
        memory_file = LONG_TERM / "global" / filename
    else:
        project_dir = get_project_dir(project)
        memory_file = project_dir / filename

    # Append to file with timestamp
    entry = f"\n## [{get_timestamp()}]\n{content}\n"

    with open(memory_file, "a") as f:
        f.write(entry)

    # Also save to semantic DB with embeddings
    semantic_result = use_semantic("save", project, memory_type, content)

    result = {"status": "saved", "file": str(memory_file), "type": memory_type}
    if semantic_result:
        try:
            sem_data = json.loads(semantic_result)
            result["semantic"] = sem_data.get("has_embedding", False)
        except:
            pass

    return result

def load_memories(project: str, query: str = "") -> str:
    """Load long-term memories, optionally filtered by query."""
    ensure_dirs()

    # Try semantic search first if query provided
    if query:
        semantic_results = use_semantic("search", project, query)
        if semantic_results:
            try:
                results = json.loads(semantic_results)
                if results:
                    formatted = []
                    for r in results:
                        sim = r.get("similarity", 0)
                        formatted.append(f"[{r['type']}|{sim:.0%}] {r['content']}")
                    return "\n\n".join(formatted)
            except:
                pass

    # Fallback to file-based search
    memories = []

    # Load global memories
    global_dir = LONG_TERM / "global"
    for f in global_dir.glob("*.md"):
        content = f.read_text()
        if not query or query.lower() in content.lower():
            memories.append(f"### Global: {f.stem}\n{content}")

    # Load project memories
    if project and project.lower() != "global":
        project_dir = get_project_dir(project)
        if project_dir.exists():
            for f in project_dir.glob("*.md"):
                content = f.read_text()
                if not query or query.lower() in content.lower():
                    memories.append(f"### {project}: {f.stem}\n{content}")

    return "\n\n---\n\n".join(memories) if memories else ""

def get_memory_summary(project: str) -> str:
    """Get a brief summary of available memories."""
    ensure_dirs()

    summary = []

    # Global memories
    global_dir = LONG_TERM / "global"
    global_files = list(global_dir.glob("*.md"))
    if global_files:
        summary.append(f"**Global**: {', '.join(f.stem for f in global_files)}")

    # Project memories
    if project and project.lower() != "global":
        project_dir = get_project_dir(project)
        if project_dir.exists():
            project_files = list(project_dir.glob("*.md"))
            if project_files:
                summary.append(f"**{project}**: {', '.join(f.stem for f in project_files)}")

    # Recent sessions
    sessions = list_sessions(project)[:3]
    if sessions:
        summary.append(f"**Recent sessions**: {len(sessions)} available")

    return "\n".join(summary) if summary else "No memories stored yet."

# === CLI Interface ===

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "save-session":
            session_id, project, content = sys.argv[2], sys.argv[3], sys.argv[4]
            result = save_session(session_id, project, content)
            print(json.dumps(result))

        elif command == "load-session":
            session_id, project = sys.argv[2], sys.argv[3]
            result = load_session(session_id, project)
            print(result)

        elif command == "save-memory":
            project, mem_type, content = sys.argv[2], sys.argv[3], sys.argv[4]
            result = save_memory(project, mem_type, content)
            print(json.dumps(result))

        elif command == "load-memories":
            project = sys.argv[2]
            query = sys.argv[3] if len(sys.argv) > 3 else ""
            result = load_memories(project, query)
            print(result)

        elif command == "list-sessions":
            project = sys.argv[2]
            result = list_sessions(project)
            print(json.dumps(result, indent=2))

        elif command == "get-last-session":
            project = sys.argv[2]
            result = get_last_session(project)
            print(result)

        elif command == "summary":
            project = sys.argv[2] if len(sys.argv) > 2 else ""
            result = get_memory_summary(project)
            print(result)

        elif command == "search":
            # Semantic search
            project = sys.argv[2]
            query = sys.argv[3] if len(sys.argv) > 3 else ""
            result = use_semantic("search", project, query)
            print(result if result else "[]")

        elif command == "context":
            # Get context for a message (for hook injection)
            project = sys.argv[2]
            message = sys.argv[3] if len(sys.argv) > 3 else ""
            result = use_semantic("context", project, message)
            print(result)

        elif command == "stats":
            # Get stats from semantic DB
            project = sys.argv[2] if len(sys.argv) > 2 else ""
            result = use_semantic("stats", project) if project else use_semantic("stats")
            print(result if result else "{}")

        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)

    except IndexError:
        print(f"Missing arguments for {command}")
        print(__doc__)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
