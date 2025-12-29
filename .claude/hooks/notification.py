#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Notification Hook - Forward notifications to user"""

import json, sys
from pathlib import Path

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    msg = data.get("message", "")

    LOG = Path.home() / ".claude" / "logs"
    LOG.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG / "events.jsonl", "a") as f:
            f.write(json.dumps({"e": "notify", "m": msg[:50]}) + "\n")
    except:
        pass

    # Show notification to user
    if msg:
        output = {"systemMessage": f"[ALERT] {msg[:150]}"}
        print(json.dumps(output))

    # Emit terminal bell - may propagate through SSH/SSM to PowerShell
    sys.stderr.write("\a")
    sys.stderr.flush()

    sys.exit(0)

if __name__ == "__main__":
    main()
