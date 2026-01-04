#!/usr/bin/env python
"""
Stop Hook - Send Windows notification when Claude needs input

This replicates Boris's iTerm2 notification setup for Windows.
Triggers when Claude completes a task and is waiting for user input.
"""

import json
import sys
import subprocess
from pathlib import Path

def send_notification(title: str, message: str):
    """Send Windows toast notification."""
    script = Path.home() / ".claude" / "scripts" / "notify.ps1"
    if script.exists():
        try:
            subprocess.run(
                ["pwsh", "-ExecutionPolicy", "Bypass", "-File", str(script), title, message],
                capture_output=True,
                timeout=5
            )
        except:
            pass

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    stop_reason = data.get("stop_reason", "")
    session_id = data.get("session_id", "")[:6]

    # Only notify when Claude is done and waiting for input
    if stop_reason == "end_turn":
        send_notification(
            f"Claude [{session_id}]",
            "Task complete - awaiting input"
        )
    elif stop_reason == "tool_use":
        # Don't notify for tool use - Claude is still working
        pass
    elif stop_reason == "max_tokens":
        send_notification(
            f"Claude [{session_id}]",
            "Hit token limit - needs /compact or /clear"
        )

    # Output empty JSON (no modification needed)
    print(json.dumps({}))
    sys.exit(0)

if __name__ == "__main__":
    main()
