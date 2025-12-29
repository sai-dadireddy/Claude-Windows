#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Stop Hook - Response complete with quality summary

Features:
- Shows "Response complete" notification
- Summarizes any quality issues from the session
- Emits terminal bell for notification
- Logs session completion
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

VERBOSE = True
LOG_DIR = Path.home() / ".claude" / "logs"

def log(msg: str):
    if VERBOSE:
        print(f"[Stop] {msg}", file=sys.stderr)

def get_session_issues() -> list:
    """Check for any issues logged during this session"""
    issues = []

    # Check quality gates log for recent issues
    quality_log = LOG_DIR / "quality_gates.jsonl"
    if quality_log.exists():
        try:
            lines = quality_log.read_text().strip().split("\n")
            if lines:
                # Get last entry
                last = json.loads(lines[-1])
                failed = last.get("failed", [])
                if failed:
                    issues.extend(failed)
        except:
            pass

    return issues

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    stop_ts = datetime.now().strftime("%H:%M:%S")
    session_id = data.get("session_id", "")[:8]
    cwd = data.get("cwd", os.getcwd())

    log(f"Response complete at {stop_ts}")

    # Log completion
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_DIR / "events.jsonl", "a") as f:
            f.write(json.dumps({
                "e": "stop",
                "t": stop_ts,
                "session": session_id,
                "cwd": cwd
            }) + "\n")
    except:
        pass

    # Check for session issues
    issues = get_session_issues()

    # Build user message
    if issues:
        msg = f"✅ Complete | ⚠️ Issues: {', '.join(issues)}"
    else:
        msg = "✅ Response complete"

    output = {"systemMessage": msg}
    print(json.dumps(output))

    # Emit terminal bell - propagates through SSH/SSM
    sys.stderr.write("\a")
    sys.stderr.flush()

    sys.exit(0)

if __name__ == "__main__":
    main()
