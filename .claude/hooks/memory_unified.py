#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Memory Unified Hook (UserPromptSubmit) - CONSOLIDATED

Combines memory_search and decision_reminder functionality:
1. Searches memories for past work questions
2. Detects decisions/preferences and reminds to save them

Replaces: memory_search.py, decision_reminder.py
"""

import json
import sys
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime

HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"
SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"
HINT_FILE = Path.home() / ".claude" / "hints" / "current.txt"

def log_hook(msg: str):
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [MemoryUnified] {msg}\n")
    except:
        pass

def write_hint(hint_text: str):
    """Write hint to file for context injection"""
    try:
        HINT_FILE.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%H:%M:%S")
        with open(HINT_FILE, "a") as f:
            f.write(f"[{timestamp}] [memory] {hint_text}\n")
    except:
        pass

# === MEMORY SEARCH PATTERNS ===
PAST_WORK = re.compile(
    r"\b(what|how|when|where|why) did (we|you|i)\b"
    r"|\bremember when\b"
    r"|\b(last time|previously|earlier|before)\b"
    r"|\bwhat (was|happened)\b"
    r"|\bdid (we|you|i).+\?",
    re.I
)

DECISION_QUERY = re.compile(r"\b(why|what made us) (choose|pick|select|use)|decision .+ (about|on|for)", re.I)
BUG_QUERY = re.compile(r"\b(bug|error|issue).+(fix|solve|resolve)|\b(fixed|solved).+(bug|error)", re.I)

TECHNICAL_TOPICS = re.compile(
    r"\b(api|database|schema|auth|authentication|login|user|users|payment|"
    r"config|configuration|setup|deploy|deployment|server|client|"
    r"cache|caching|queue|redis|postgres|mysql|mongodb|"
    r"jwt|token|oauth|session|cookie|cors|"
    r"test|testing|tests|ci|pipeline|workflow|"
    r"migration|model|models|entity|entities|relationship|"
    r"endpoint|route|routes|controller|service|repository|"
    r"lambda|aws|s3|cloudfront|sqs|sns|dynamodb|"
    r"docker|kubernetes|k8s|container|pod|helm|"
    r"react|vue|angular|svelte|next|nuxt|"
    r"hook|hooks|context|state|store|redux|"
    r"graphql|rest|grpc|websocket|socket|"
    r"error handling|logging|monitoring|observability)\b",
    re.I
)

# === DECISION DETECTION PATTERNS ===
DECISION_PATTERNS = re.compile(
    r"\b(let'?s|we should|i want to|go with|choose|pick|select|use|prefer|switch to|install|set up|configure|enable|disable)\s+"
    r"|\b(yes|ok|okay|sure|do it|go ahead|sounds good|let'?s do)\b"
    r"|\b(i like|i prefer|i want|i need|i'?d rather)\b"
    r"|\b(decision|decided|choosing|picked|selected)\b",
    re.I
)

PREFERENCE_PATTERNS = re.compile(
    r"\b(i (always|usually|prefer|like|want|need|hate|don'?t like))\b"
    r"|\b(my (preference|style|way|approach))\b"
    r"|\b(prefer.+over|rather.+than|instead of)\b"
    r"|\b(don'?t|never|always|usually)\s+(use|want|like|do)\b",
    re.I
)

SETUP_PATTERNS = re.compile(
    r"\b(install|set ?up|configure|enable|add|create|init)\s+(it|this|that|\w+)\b"
    r"|\b(yes.*(install|set ?up|add|create))\b"
    r"|\b(do it|go ahead|proceed|implement)\b",
    re.I
)


def search_memories(project: str, query: str) -> list:
    """Search semantic memory database"""
    if not SEMANTIC_SCRIPT.exists():
        return []
    try:
        result = subprocess.run(
            [sys.executable, str(SEMANTIC_SCRIPT), "search", project, query],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except:
        pass
    return []


def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    prompt = data.get("prompt", "")
    cwd = data.get("cwd", os.getcwd())
    project = os.path.basename(cwd)

    if len(prompt) < 10:
        sys.exit(0)

    outputs = []
    context_parts = []
    hints = []

    # === PART 1: Memory Search ===
    search_intent = None
    if PAST_WORK.search(prompt):
        search_intent = "past_work"
    elif DECISION_QUERY.search(prompt):
        search_intent = "decision"
    elif BUG_QUERY.search(prompt):
        search_intent = "bug"
    elif TECHNICAL_TOPICS.search(prompt) and len(prompt) > 30:
        search_intent = "technical"

    if search_intent:
        results = search_memories(project, prompt)
        if not results:
            results = search_memories("global", prompt)

        if results:
            lines = ["<memories>"]
            for r in results[:5]:
                sim = r.get("similarity", 0)
                typ = r.get("type", "?")
                content = r.get("content", "")[:100]
                lines.append(f"[{typ}|{sim:.0%}] {content}")
            lines.append("</memories>")
            context_parts.append("\n".join(lines))

            if search_intent != "technical":
                outputs.append(f"[SEARCH] Found {len(results)} memories")

    # === PART 2: Decision/Preference Detection ===
    save_reminder = None

    if DECISION_PATTERNS.search(prompt):
        save_reminder = "decision"
        hints.append("SAVE decision: ~/.claude/scripts/memory_manager.py save-memory PROJECT decision \"...\"")
        log_hook(f"Decision detected: {prompt[:50]}...")

    elif PREFERENCE_PATTERNS.search(prompt):
        save_reminder = "preference"
        hints.append("SAVE preference: ~/.claude/scripts/memory_manager.py save-memory global preference \"...\"")
        log_hook(f"Preference detected: {prompt[:50]}...")

    elif SETUP_PATTERNS.search(prompt):
        save_reminder = "setup"
        hints.append("SAVE setup decision after completing")
        log_hook(f"Setup decision detected: {prompt[:50]}...")

    if save_reminder:
        outputs.append(f"[MEMORY] {save_reminder.title()} detected -> Save to memory!")

    # === Output ===
    if hints:
        write_hint(" | ".join(hints))
        print("[MEMORY] Hint written to ~/.claude/hints/current.txt")

    if context_parts:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(context_parts)
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
