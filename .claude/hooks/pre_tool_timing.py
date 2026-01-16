#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PreToolUse Hook - Tool Timing (Start Time Recording)

Records tool start times for duration tracking.
The PostToolUse hook reads these times to calculate execution duration.

Storage: ~/.claude/logs/.tool_timing.json
Format: {"{session_id}_{tool_use_id}": timestamp_ms, ...}

Auto-prunes entries older than 1 hour to keep the file small.
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

TIMING_FILE = Path.home() / ".claude" / "logs" / ".tool_timing.json"
PRUNE_AGE_MS = 3600000  # 1 hour in milliseconds


def load_timing_data() -> dict:
    """Load existing timing data from file."""
    try:
        if TIMING_FILE.exists():
            return json.loads(TIMING_FILE.read_text())
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def save_timing_data(data: dict):
    """Save timing data to file."""
    try:
        TIMING_FILE.parent.mkdir(parents=True, exist_ok=True)
        TIMING_FILE.write_text(json.dumps(data))
    except IOError:
        pass


def prune_old_entries(data: dict) -> dict:
    """Remove entries older than PRUNE_AGE_MS."""
    now_ms = int(time.time() * 1000)
    cutoff = now_ms - PRUNE_AGE_MS
    return {k: v for k, v in data.items() if v > cutoff}


def generate_timing_key(data: dict) -> str:
    """
    Generate a unique key for this tool invocation.
    Uses tool_use_id if available, otherwise generates from session_id + tool_name + timestamp.
    """
    session_id = data.get("session_id", "unknown")[:8]
    tool_name = data.get("tool_name", "unknown")

    # Try to use tool_use_id if available in the hook data
    tool_use_id = data.get("tool_use_id") or data.get("invocation_id")

    if tool_use_id:
        return f"{session_id}_{tool_use_id}"
    else:
        # Fallback: generate from session + tool + timestamp
        # This is less reliable but works when tool_use_id isn't available
        ts = int(time.time() * 1000)
        return f"{session_id}_{tool_name}_{ts}"


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if not tool_name:
        sys.exit(0)

    # Generate timing key
    timing_key = generate_timing_key(data)

    # Record start time in milliseconds
    start_time_ms = int(time.time() * 1000)

    # Load existing data, prune old entries, add new entry
    timing_data = load_timing_data()
    timing_data = prune_old_entries(timing_data)
    timing_data[timing_key] = start_time_ms

    # Save updated timing data
    save_timing_data(timing_data)

    # No output needed - this hook just records timing
    # (We don't want to interfere with other PreToolUse hooks)
    sys.exit(0)


if __name__ == "__main__":
    main()
