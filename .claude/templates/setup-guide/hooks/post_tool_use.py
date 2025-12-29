#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PostToolUse Hook - Logging and error feedback

Features:
- Logs tool usage to tools.jsonl
- Reports errors to user

Note: Auto-ingestion moved to auto_capture_memory.py (more sophisticated)
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = Path.home() / ".claude" / "logs"

VERBOSE = True  # Set to False to disable terminal output
HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

def log(msg: str):
    """Log to file (tail -f ~/.claude/logs/hooks.log to watch)"""
    if VERBOSE:
        try:
            HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(HOOK_LOG, "a") as f:
                f.write(f"{datetime.now().strftime('%H:%M:%S')} {msg}\n")
                f.flush()
        except:
            pass
        print(f"\033[36m[Hook] {msg}\033[0m", file=sys.stderr, flush=True)

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})
    out = data.get("tool_output", {})
    sid = data.get("session_id", "")[:8]
    cwd = data.get("cwd", os.getcwd())

    # Show what tool completed
    log(f"Completed: {tool}")

    # Ensure log dir
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Compact log entry
    entry = {"t": datetime.now().strftime("%H:%M:%S"), "tool": tool}

    file_path = None
    if tool == "Bash":
        cmd = inp.get("command", "")[:50]
        entry["cmd"] = cmd
    elif tool in ["Read", "Edit", "Write", "MultiEdit"]:
        file_path = inp.get("file_path", "")
        entry["file"] = os.path.basename(file_path)

    # Check for errors
    is_error = False
    err_msg = ""
    if isinstance(out, dict):
        is_error = out.get("is_error", False)
        err_msg = out.get("error", "") or out.get("stderr", "")

    if is_error or err_msg:
        entry["err"] = err_msg[:100] if err_msg else "error"

    # Log to file (append)
    try:
        log_file = LOG_DIR / "tools.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

    # Note: Auto-ingest handled by auto_capture_memory.py hook

    # Output user-visible message
    if is_error and err_msg:
        output = {
            "systemMessage": f"❌ {tool} error: {err_msg[:80]}"
        }
        print(json.dumps(output))
    else:
        # Success message with brief info
        short_info = ""
        if tool == "Bash":
            cmd = inp.get("command", "")[:25]
            short_info = f": {cmd}..." if len(inp.get("command", "")) > 25 else f": {cmd}" if cmd else ""
        elif tool in ["Read", "Edit", "Write"]:
            path = file_path or inp.get("file_path", "")
            short_info = f": {os.path.basename(path)}" if path else ""
        elif tool == "Glob":
            pattern = inp.get("pattern", "")
            short_info = f": {pattern}" if pattern else ""
        elif tool == "Grep":
            pattern = inp.get("pattern", "")[:20]
            short_info = f": {pattern}" if pattern else ""

        print(json.dumps({"systemMessage": f"✓ {tool}{short_info}"}))

    sys.exit(0)

if __name__ == "__main__":
    main()
