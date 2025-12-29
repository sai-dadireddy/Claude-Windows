#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""SessionEnd Hook - Notify when session ends + memory reminder"""

import json, sys, os
from pathlib import Path
from datetime import datetime

LOG = Path.home() / ".claude" / "logs"

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    reason = data.get("reason", "other")  # clear, logout, prompt_input_exit, other
    session_id = data.get("session_id", "")[:8]
    cwd = data.get("cwd", os.getcwd())
    end_ts = datetime.now().strftime("%H:%M:%S")

    # Log
    LOG.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG / "events.jsonl", "a") as f:
            f.write(json.dumps({
                "e": "session_end",
                "reason": reason,
                "session": session_id,
                "t": end_ts
            }) + "\n")
    except:
        pass

    # User-visible message based on reason
    reason_msgs = {
        "clear": "🧹 Session cleared",
        "logout": "👋 Logged out",
        "prompt_input_exit": "👋 Goodbye!",
        "other": "👋 Session ended"
    }
    msg = reason_msgs.get(reason, f"👋 Session ended ({reason})")

    # Add memory reminder
    msg += " | [TIP] Use /session-save before ending to preserve state"

    output = {"systemMessage": msg}
    print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
