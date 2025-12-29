#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Memory Search Hook (UserPromptSubmit) - OPTIMIZED
Auto-invokes semantic search for past work questions.
"""

import json
import sys
import os
import subprocess
import re
from pathlib import Path

from datetime import datetime

HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

def log_hook(msg: str):
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [MemorySearch] {msg}\n")
    except:
        pass

SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"

# Pre-compiled patterns for memory search triggers
PAST_WORK = re.compile(
    r"\b(what|how|when|where|why) did (we|you|i)\b"
    r"|\bremember when\b"
    r"|\b(last time|previously|earlier|before)\b"
    r"|\bwhat (was|happened)\b"
    r"|\bdid (we|you|i).+\?",
    re.I
)

DECISION = re.compile(r"\b(why|what made us) (choose|pick|select|use)|decision .+ (about|on|for)", re.I)
BUG = re.compile(r"\b(bug|error|issue).+(fix|solve|resolve)|\b(fixed|solved).+(bug|error)", re.I)

# Technical topics that should auto-fetch context from memory
# These keywords suggest the user is working on a domain where prior decisions matter
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

def search_memories(project: str, query: str) -> list:
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

    if len(prompt) < 15:
        sys.exit(0)

    # Detect intent
    intent_type = None
    if PAST_WORK.search(prompt):
        intent_type = "past_work"
    elif DECISION.search(prompt):
        intent_type = "decision"
    elif BUG.search(prompt):
        intent_type = "bug"
    elif TECHNICAL_TOPICS.search(prompt):
        # Auto-query memory for technical topics where prior context matters
        intent_type = "technical"
        log_hook(f"Auto-memory query for technical topic in: {prompt[:50]}")

    if not intent_type:
        sys.exit(0)

    # Search memories
    results = search_memories(project, prompt)
    if not results:
        results = search_memories("global", prompt)

    if not results:
        sys.exit(0)

    # Build compact context
    lines = ["<memories>"]
    for r in results[:5]:
        sim = r.get("similarity", 0)
        typ = r.get("type", "?")
        content = r.get("content", "")[:100]
        lines.append(f"[{typ}|{sim:.0%}] {content}")
    lines.append("</memories>")

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(lines)
        }
    }
    print(json.dumps(output))

    # User-visible message (suppress for auto-queries to reduce noise)
    if intent_type != "technical":
        print(json.dumps({"systemMessage": f"[SEARCH] Found {len(results)} memories"}), file=sys.stderr)
    # For technical auto-queries, silently inject context without user message
    sys.exit(0)

if __name__ == "__main__":
    main()
