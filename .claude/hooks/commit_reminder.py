#!/usr/bin/env python
"""Remind to commit changes frequently - PostToolUse hook."""
import json
import sys
import os
import subprocess
from pathlib import Path

# Track edits in session
COUNTER_FILE = Path.home() / ".claude" / "edit_counter.json"
EDIT_THRESHOLD = 10  # Remind after this many edits

def get_counter():
    """Get current edit counter."""
    try:
        if COUNTER_FILE.exists():
            data = json.loads(COUNTER_FILE.read_text())
            return data.get("count", 0), data.get("last_commit_reminder", 0)
    except:
        pass
    return 0, 0

def save_counter(count, reminder_count):
    """Save edit counter."""
    try:
        COUNTER_FILE.write_text(json.dumps({
            "count": count,
            "last_commit_reminder": reminder_count
        }))
    except:
        pass

def has_uncommitted_changes():
    """Check if there are uncommitted changes."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=5
        )
        return bool(result.stdout.strip())
    except:
        return False

def main():
    try:
        hook_data = json.load(sys.stdin)
    except:
        return

    tool_name = hook_data.get("tool_name", "")

    # Only track file edits
    if tool_name not in ["Edit", "Write", "MultiEdit"]:
        return

    count, reminder_count = get_counter()
    count += 1

    # Check if we should remind
    if count >= EDIT_THRESHOLD and (count - reminder_count) >= EDIT_THRESHOLD:
        if has_uncommitted_changes():
            result = {
                "additionalContext": f"[GIT] {count} edits since last commit. Consider: git add -A && git commit -m 'WIP'"
            }
            print(json.dumps(result))
            save_counter(count, count)  # Reset reminder
            return

    save_counter(count, reminder_count)

if __name__ == "__main__":
    main()
