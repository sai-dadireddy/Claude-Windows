#!/usr/bin/env python3
"""
Block auto compaction hook.
Exit code 2 = block the operation
"""
import sys
import json
import os
from datetime import datetime

def main():
    # Log the attempt
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "hooks.log")
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Get hook input
    hook_input = {}
    try:
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                hook_input = json.loads(raw)
    except:
        pass

    compact_type = hook_input.get("compactType", "unknown")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} [BlockAutoCompact] Blocking {compact_type} compaction\n")

    # Exit 2 = block the operation
    sys.exit(2)

if __name__ == "__main__":
    main()
