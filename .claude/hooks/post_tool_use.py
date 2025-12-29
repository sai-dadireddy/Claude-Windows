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
import subprocess
from datetime import datetime
from pathlib import Path

LOG_DIR = Path.home() / ".claude" / "logs"
ERROR_COUNTER_FILE = LOG_DIR / "error_counter.json"
META_COGNITION_THRESHOLD = 3  # Trigger reflection after N consecutive errors

VERBOSE = False  # Set to False to disable terminal output
HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"


def get_error_count(session_id: str) -> int:
    """Get consecutive error count for session."""
    try:
        if ERROR_COUNTER_FILE.exists():
            data = json.loads(ERROR_COUNTER_FILE.read_text())
            return data.get(session_id, {}).get("count", 0)
    except:
        pass
    return 0


def update_error_count(session_id: str, is_error: bool) -> int:
    """Update error counter. Returns new count."""
    try:
        ERROR_COUNTER_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {}
        if ERROR_COUNTER_FILE.exists():
            data = json.loads(ERROR_COUNTER_FILE.read_text())

        if session_id not in data:
            data[session_id] = {"count": 0, "last_error": ""}

        if is_error:
            data[session_id]["count"] += 1
            data[session_id]["last_error"] = datetime.now().isoformat()
        else:
            # Reset on success
            data[session_id]["count"] = 0

        ERROR_COUNTER_FILE.write_text(json.dumps(data))
        return data[session_id]["count"]
    except:
        return 0

SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"


def search_error_fix(error_msg: str) -> str:
    """Search memory for past fixes to this error (Error-Correction RAG)."""
    if not SEMANTIC_SCRIPT.exists():
        return ""
    try:
        # Search for fixes related to this error
        query = f"fix for {error_msg[:100]}"
        result = subprocess.run(
            [sys.executable, str(SEMANTIC_SCRIPT), "search", "global", query],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            memories = json.loads(result.stdout)
            if memories:
                # Return the most relevant fix
                best = memories[0]
                content = best.get("content", "")[:150]
                similarity = best.get("similarity", 0)
                if similarity > 0.5:  # Only return if reasonably relevant
                    return content
    except:
        pass
    return ""


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

    # Track consecutive errors for meta-cognition
    error_count = update_error_count(sid, is_error)

    # Output to BOTH terminal (systemMessage) and Claude (additionalContext)
    output = {}

    if is_error and err_msg:
        # Error-Correction RAG: Search memory for past fixes
        past_fix = search_error_fix(err_msg)

        # Meta-cognition trigger (3+ consecutive errors)
        if error_count >= META_COGNITION_THRESHOLD:
            terminal_msg = f"[STOP] META-COGNITION TRIGGER: {error_count} consecutive failures detected."
            context_msg = f"""<meta-cognition errors="{error_count}">
STOP. Do not retry the same approach.

1. Read the systematic-debugging skill
2. Identify the ROOT CAUSE, not just the symptom
3. Save your analysis to memory
4. Try a DIFFERENT approach

Last error: {err_msg[:200]}
</meta-cognition>"""
            if past_fix:
                terminal_msg += f"\n[TIP] PAST FIX: {past_fix[:60]}"
                context_msg += f"\n<past-fix>{past_fix}</past-fix>"

            output["systemMessage"] = terminal_msg
            output["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": context_msg
            }
            log(f"META-COGNITION triggered after {error_count} errors")

        elif past_fix:
            # Found a past fix - show it with the error
            output["systemMessage"] = f"[FAIL] {tool} error ({error_count}/3): {err_msg[:60]}\n[TIP] Past fix: {past_fix[:60]}"
            output["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": f"<error-with-fix tool=\"{tool}\">\nError: {err_msg[:200]}\nPast fix: {past_fix}\n</error-with-fix>"
            }
            log(f"Error-Correction RAG found fix: {past_fix[:50]}")

        else:
            # Standard error message - also inject to Claude context
            output["systemMessage"] = f"[FAIL] {tool} error ({error_count}/3): {err_msg[:80]}"
            output["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": f"<tool-error tool=\"{tool}\" consecutive=\"{error_count}\">{err_msg[:300]}</tool-error>"
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

        # Success: Only terminal message, no context injection (to save tokens)
        print(json.dumps({"systemMessage": f"[?] {tool}{short_info}"}))

    sys.exit(0)

if __name__ == "__main__":
    main()
