#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Codebase Map + Hint Injector (UserPromptSubmit)

Features:
- Generates a lightweight codebase structure map (once per session)
- FORCE-INJECTS hints on EVERY turn (not optional!)
- Ensures Claude never "forgets" to check hints
- Hints appear as system data, not suggestions
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from datetime import datetime

VERBOSE = False
SESSION_MARKER = Path.home() / ".claude" / "cache" / "codebase_map_session"
HINT_FILE = Path.home() / ".claude" / "hints" / "current.txt"

def log(msg: str):
    if VERBOSE:
        print(f"[CodebaseMap] {msg}", file=sys.stderr)

def should_run(session_id: str, cwd: str) -> bool:
    """Check if we should generate map (once per session per project)"""
    SESSION_MARKER.parent.mkdir(parents=True, exist_ok=True)

    marker_key = f"{session_id}:{cwd}"

    if SESSION_MARKER.exists():
        try:
            content = SESSION_MARKER.read_text()
            if marker_key in content:
                return False
        except:
            pass

    # Mark as run
    try:
        with open(SESSION_MARKER, "a") as f:
            f.write(marker_key + "\n")
    except:
        pass

    return True

def get_git_info(cwd: str) -> dict:
    """Get git repository info"""
    try:
        # Branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        branch = result.stdout.strip() if result.returncode == 0 else None

        # Recent commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        commits = result.stdout.strip().split("\n")[:5] if result.returncode == 0 else []

        # Changed files
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        changes = len([l for l in result.stdout.split("\n") if l.strip()]) if result.returncode == 0 else 0

        return {
            "branch": branch,
            "recent_commits": commits,
            "uncommitted_changes": changes
        }
    except:
        return {}

def get_directory_structure(cwd: str, max_depth: int = 3, max_files: int = 100) -> list:
    """Get directory structure (lightweight)"""
    structure = []
    file_count = 0

    # Directories to skip
    skip_dirs = {
        "node_modules", ".git", "__pycache__", ".venv", "venv",
        "dist", "build", ".next", ".nuxt", "target", ".cargo",
        ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage",
        ".idea", ".vscode", "*.egg-info"
    }

    # Important files to highlight
    important_files = {
        "package.json", "tsconfig.json", "pyproject.toml", "Cargo.toml",
        "go.mod", "Makefile", "Dockerfile", "docker-compose.yml",
        "README.md", "CLAUDE.md", ".env.example"
    }

    root = Path(cwd)

    for item in sorted(root.rglob("*")):
        if file_count >= max_files:
            structure.append("... (truncated)")
            break

        # Calculate depth
        rel_path = item.relative_to(root)
        depth = len(rel_path.parts)

        if depth > max_depth:
            continue

        # Skip unwanted directories
        if any(skip in str(rel_path) for skip in skip_dirs):
            continue

        # Format entry
        indent = "  " * (depth - 1)
        name = item.name

        if item.is_dir():
            structure.append(f"{indent}{name}/")
        else:
            # Mark important files
            marker = " ★" if name in important_files else ""
            structure.append(f"{indent}{name}{marker}")
            file_count += 1

    return structure[:50]  # Limit output

def detect_project_type(cwd: str) -> list:
    """Detect project type based on config files"""
    types = []
    root = Path(cwd)

    indicators = {
        "package.json": "Node.js",
        "tsconfig.json": "TypeScript",
        "pyproject.toml": "Python",
        "requirements.txt": "Python",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java/Maven",
        "build.gradle": "Java/Gradle",
        "Gemfile": "Ruby",
        "composer.json": "PHP",
        "Dockerfile": "Docker",
    }

    for file, proj_type in indicators.items():
        if (root / file).exists():
            types.append(proj_type)

    return list(set(types))

def get_active_hints() -> str:
    """Get active hints to force-inject into context."""
    if not HINT_FILE.exists():
        return ""

    try:
        content = HINT_FILE.read_text().strip()
        if not content:
            return ""

        # Format as unmissable system instruction
        lines = [
            "<agent-instructions priority=\"HIGH\">",
            "!!! ACTIVE HINTS - ACT ON THESE BEFORE RESPONDING !!!",
        ]
        for line in content.split('\n')[-5:]:  # Last 5 hints only
            lines.append(f"  {line}")
        lines.append("</agent-instructions>")

        return "\n".join(lines)
    except:
        return ""


def generate_codebase_map(cwd: str) -> str:
    """Generate a concise codebase map"""
    lines = ["<codebase-context>"]

    # Project types
    types = detect_project_type(cwd)
    if types:
        lines.append(f"Project: {', '.join(types)}")

    # Git info
    git_info = get_git_info(cwd)
    if git_info.get("branch"):
        lines.append(f"Branch: {git_info['branch']}")
        if git_info.get("uncommitted_changes"):
            lines.append(f"Uncommitted: {git_info['uncommitted_changes']} files")

    # Structure
    lines.append("\nStructure:")
    structure = get_directory_structure(cwd)
    lines.extend(structure)

    lines.append("</codebase-context>")

    return "\n".join(lines)

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    session_id = data.get("session_id", "")
    prompt = data.get("prompt", "")

    # Skip for very short prompts (likely commands)
    if len(prompt) < 10:
        sys.exit(0)

    context_parts = []

    # 1. ALWAYS inject hints (every turn) - this is the fix!
    hints = get_active_hints()
    if hints:
        context_parts.append(hints)
        log(f"💉 Injecting hints")

    # 2. Only inject codebase map once per session
    if should_run(session_id, cwd):
        log("Generating codebase map...")
        codebase_map = generate_codebase_map(cwd)
        context_parts.append(codebase_map)
        log(f"[FILE] Injected codebase context ({len(codebase_map)} chars)")

    # Output combined context
    if context_parts:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n\n".join(context_parts)
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
