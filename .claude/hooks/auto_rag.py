#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Auto-RAG Hook (UserPromptSubmit) - Proactive Context Injection

Detects uncertainty or architectural questions and automatically
injects relevant memories without user explicitly asking.

This is "Ephemeral RAG" - fetch, inject, done. No manual search needed.

Exit codes:
- 0: Always exit 0 (success or pass-through)
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"
HINTS_FILE = Path.home() / ".claude" / "hints" / "current.txt"
HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

# Auto-RAG triggers: patterns that indicate need for historical context
AUTO_RAG_TRIGGERS = [
    # Decision context
    (r"(?i)\b(how did we|what was the decision|why did we choose|what made us pick)\b", "decision"),
    (r"(?i)\b(we decided|we chose|the choice was)\b", "decision"),

    # Architecture context
    (r"(?i)\b(context for|background on|what is the architecture|how does .+ work)\b", "architecture"),
    (r"(?i)\b(system design|data flow|component|module)\b", "architecture"),

    # Bug/Fix context
    (r"(?i)\b(fix for|solution to|how to resolve|workaround for)\b", "bug"),
    (r"(?i)\b(this error|this bug|similar issue|seen before)\b", "bug"),

    # Implementation patterns
    (r"(?i)\b(pattern for|how to implement|best practice|convention)\b", "learning"),
    (r"(?i)\b(like we did|similar to what we|same approach)\b", "learning"),
]

# Minimum prompt length to trigger (avoid short commands)
MIN_PROMPT_LEN = 25


def log(msg: str):
    """Log to hook log file."""
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [AutoRAG] {msg}\n")
    except Exception:
        pass


def search_memories(category: str, query: str) -> list:
    """Search semantic memory for relevant context."""
    if not SEMANTIC_SCRIPT.exists():
        log(f"Semantic script not found: {SEMANTIC_SCRIPT}")
        return []
    try:
        # Use sys.executable for cross-platform compatibility
        result = subprocess.run(
            [sys.executable, str(SEMANTIC_SCRIPT), "search", "global", query],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            memories = json.loads(result.stdout)
            # Filter by category if specified
            if category and memories:
                filtered = [m for m in memories if m.get("type") == category]
                return filtered if filtered else memories[:3]
            return memories[:3]
        elif result.returncode != 0:
            log(f"Semantic search failed: {result.stderr}")
    except json.JSONDecodeError as e:
        log(f"JSON parse error: {e}")
    except subprocess.TimeoutExpired:
        log("Semantic search timeout")
    except Exception as e:
        log(f"Search error: {e}")
    return []


def write_hint(content: str):
    """Write to the signal file for CLAUDE.md to pick up."""
    try:
        HINTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%H:%M:%S")
        existing = ""
        if HINTS_FILE.exists():
            existing = HINTS_FILE.read_text()
        lines = existing.strip().split('\n')[-4:] if existing.strip() else []
        lines.append(f"[{timestamp}] [auto-rag] {content}")
        HINTS_FILE.write_text('\n'.join(lines))
    except Exception:
        pass


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        # Pass-through on parse error
        sys.exit(0)

    prompt = data.get("prompt", "")

    # Skip short prompts - pass-through
    if len(prompt) < MIN_PROMPT_LEN:
        sys.exit(0)

    # Detect which category needs RAG
    triggered_category = None
    for pattern, category in AUTO_RAG_TRIGGERS:
        if re.search(pattern, prompt):
            triggered_category = category
            log(f"Triggered for category: {category}")
            break

    # No trigger matched - pass-through
    if not triggered_category:
        sys.exit(0)

    # Perform the RAG search
    memories = search_memories(triggered_category, prompt)

    # No memories found - pass-through
    if not memories:
        log("No memories found")
        sys.exit(0)

    # Build ephemeral context
    lines = [f"<auto-rag category=\"{triggered_category}\">"]
    for m in memories[:3]:
        content = m.get("content", "")[:200]
        similarity = m.get("similarity", 0)
        mem_type = m.get("type", "?")
        lines.append(f"[{mem_type}|{similarity:.0%}] {content}")
    lines.append("</auto-rag>")

    context = "\n".join(lines)

    # Write to hints for visibility
    write_hint(f"Injected {len(memories)} {triggered_category} memories")

    # Output the context injection
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }
    print(json.dumps(output))
    log(f"Injected {len(memories)} memories for {triggered_category}")
    sys.exit(0)


if __name__ == "__main__":
    main()
