#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PreCompact Hook - Backup transcript and warn about compaction override

Addresses Reddit finding: Post-compaction prompt injection can override
user instructions with "continue without asking".

This hook:
1. Backs up transcript before compaction
2. Warns about the compaction override issue
3. Reminds Claude to check CLAUDE.md for compaction rules
"""

import json, sys, shutil
from pathlib import Path
from datetime import datetime

BACKUP = Path.home() / ".claude" / "backups" / "transcripts"
STATE_FILE = Path.home() / ".claude" / "memory" / "short-term" / "pre_compact_state.json"

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    sid = data.get("session_id", "")[:8]
    path = data.get("transcript_path", "")
    trigger = data.get("trigger", "manual")
    cwd = data.get("cwd", "")

    backed_up = False
    if path and Path(path).exists():
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            shutil.copy2(path, BACKUP / f"{sid}_{ts}.jsonl")
            backed_up = True
        except:
            pass

    # Save pre-compaction state for reference
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "session_id": sid,
            "timestamp": datetime.now().isoformat(),
            "trigger": trigger,
            "cwd": cwd,
            "transcript_backup": str(BACKUP / f"{sid}_{ts}.jsonl") if backed_up else None
        }
        STATE_FILE.write_text(json.dumps(state, indent=2))
    except:
        pass

    # Always notify about compaction (both manual and auto)
    # Include reminder about compaction override protection
    backup_note = " (transcript backed up)" if backed_up else ""
    msg = f"📦 Compacting context{backup_note}. Remember: CLAUDE.md has COMPACTION OVERRIDE rules - wait for user instruction after compaction."

    output = {"systemMessage": msg}
    print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
