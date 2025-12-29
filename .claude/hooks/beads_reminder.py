#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Beads Reminder Hook (UserPromptSubmit) - OPTIMIZED
Detects complex multi-step work and reminds to use Beads.
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
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [BeadsReminder] {msg}\n")
    except:
        pass

BD_PATH = Path.home() / ".local" / "bin" / "bd"

# Pre-compiled patterns for complex task detection
COMPLEX_PATTERNS = re.compile(
    r"\b(implement|build|create|develop)\s+(a\s+)?(new\s+)?(feature|system|module|service|api|auth)"
    r"|\b(refactor|migrate|upgrade|rewrite)\s+"
    r"|\b(add|implement)\s+.+\s+(and|then|after that|also)\s+"
    r"|\bmultiple\s+(steps|tasks|features)\b"
    r"|\b(full|complete|entire|whole)\s+(feature|system|implementation)\b"
    r"|\bdependenc(y|ies)\b"
    r"|\bblock(s|ed|ing)?\b",
    re.I
)

def beads_initialized(cwd: str) -> bool:
    return (Path(cwd) / ".beads").exists()

def get_ready_count(cwd: str) -> int:
    if not beads_initialized(cwd):
        return 0
    try:
        env = os.environ.copy()
        env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"
        result = subprocess.run(
            ["bd", "ready", "--json"],
            cwd=cwd, capture_output=True, text=True, timeout=5, env=env
        )
        if result.returncode == 0 and result.stdout.strip():
            return len(json.loads(result.stdout))
    except:
        pass
    return 0

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    prompt = data.get("prompt", "")
    cwd = data.get("cwd", os.getcwd())

    # Skip short prompts or if bd not available
    if len(prompt) < 20 or not BD_PATH.exists():
        sys.exit(0)

    # Check for complex task patterns or long prompt
    if not COMPLEX_PATTERNS.search(prompt) and len(prompt.split()) <= 50:
        sys.exit(0)

    # Build minimal reminder
    if beads_initialized(cwd):
        ready = get_ready_count(cwd)
        context = f"<beads>Ready: {ready} | Run: bd ready</beads>"
        user_msg = f"[LIST] Beads: {ready} ready tasks"
    else:
        context = "<beads>Complex task -> Consider: bd init && bd create \"task\" -t feature</beads>"
        user_msg = "[LIST] Beads: Complex task - consider bd init"

    log_hook(f"Writing hint: {user_msg}")

    # Write to signal file (workaround for broken context injection)
    hint_file = Path.home() / ".claude" / "hints" / "current.txt"
    hint_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%H:%M:%S")
    if beads_initialized(cwd):
        hint_text = f"BEADS: {ready} ready tasks - run 'bd ready'"
    else:
        hint_text = "BEADS: Complex task - consider 'bd init && bd create'"
    with open(hint_file, "a") as f:
        f.write(f"[{timestamp}] [beads] {hint_text}\n")

    print(f"[LIST] Beads hint written to ~/.claude/hints/current.txt")
    sys.exit(0)

if __name__ == "__main__":
    main()
