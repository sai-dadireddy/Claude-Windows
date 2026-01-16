#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Stop Hook - Auto-verification on response complete (Boris-style)

Features:
- Auto-triggers verification when Claude stops
- Checks for uncommitted changes that need tests
- Suggests verification commands based on context
- Summarizes any quality issues from the session
- Emits terminal bell for notification
- Logs session completion
- Parses session transcript and outputs trace summary (NEW)
"""

import json
import sys
import os
import subprocess
import glob as glob_module
from pathlib import Path
from datetime import datetime
from typing import Optional

VERBOSE = False
LOG_DIR = Path.home() / ".claude" / "logs"
CLAUDE_DIR = Path.home() / ".claude"

def log(msg: str):
    if VERBOSE:
        print(f"[Stop] {msg}", file=sys.stderr)


def find_transcript_file(session_id: str) -> Optional[Path]:
    """Find the transcript file for a given session ID"""
    if not session_id:
        return None

    projects_dir = CLAUDE_DIR / "projects"
    if not projects_dir.exists():
        return None

    # Search all project directories for the session file
    # Session files can be: {session_id}.jsonl or agent-{short_id}.jsonl
    patterns = [
        f"*/{session_id}.jsonl",
        f"*/{session_id[:8]}*.jsonl",
        f"*/agent-{session_id[:7]}*.jsonl"
    ]

    for pattern in patterns:
        matches = list(projects_dir.glob(pattern))
        if matches:
            # Return the most recently modified file
            matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return matches[0]

    return None


def parse_transcript_last_turn(transcript_path: Path, max_entries: int = 50) -> dict:
    """Parse the last N entries of a transcript to extract trace info"""
    trace = {
        "thinking_blocks": [],
        "tool_calls": [],
        "tokens": {"input": 0, "output": 0, "cache_read": 0, "cache_create": 0}
    }

    if not transcript_path or not transcript_path.exists():
        return trace

    try:
        # Read last N lines efficiently
        lines = []
        with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read all lines and take last N
            all_lines = f.readlines()
            lines = all_lines[-max_entries:] if len(all_lines) > max_entries else all_lines

        # Find user messages (excluding pure tool_result entries)
        user_indices = []
        for i, line in enumerate(lines):
            try:
                entry = json.loads(line.strip())
                if entry.get("type") == "user" and entry.get("message", {}).get("role") == "user":
                    content = entry.get("message", {}).get("content")
                    if isinstance(content, str):
                        user_indices.append(i)
                    elif isinstance(content, list):
                        # Check if there's any non-tool_result content
                        has_real_content = any(
                            isinstance(c, dict) and c.get("type") != "tool_result"
                            for c in content
                        )
                        if has_real_content:
                            user_indices.append(i)
            except:
                pass

        # Use second-to-last user message to capture the complete last turn
        # (The very last user message may be the one that just ended, with no response yet)
        if len(user_indices) >= 2:
            start_idx = user_indices[-2]
        elif user_indices:
            start_idx = user_indices[0]
        else:
            start_idx = 0

        for line in lines[start_idx:]:
            try:
                entry = json.loads(line.strip())
                msg = entry.get("message", {})
                entry_type = entry.get("type")

                # Extract token usage from assistant messages
                if entry_type == "assistant":
                    usage = msg.get("usage", {})
                    if usage:
                        trace["tokens"]["input"] += usage.get("input_tokens", 0)
                        trace["tokens"]["output"] += usage.get("output_tokens", 0)
                        trace["tokens"]["cache_read"] += usage.get("cache_read_input_tokens", 0)

                        # Cache creation tokens
                        cache_create = usage.get("cache_creation_input_tokens", 0)
                        if not cache_create:
                            cache_creation = usage.get("cache_creation", {})
                            cache_create = cache_creation.get("ephemeral_5m_input_tokens", 0)
                        trace["tokens"]["cache_create"] += cache_create

                    # Extract content blocks (thinking, tool_use)
                    content = msg.get("content", [])
                    if isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict):
                                block_type = block.get("type")

                                if block_type == "thinking":
                                    # Extract thinking text (truncate for display)
                                    thinking_text = block.get("thinking", "")[:80]
                                    if len(block.get("thinking", "")) > 80:
                                        thinking_text += "..."
                                    trace["thinking_blocks"].append({
                                        "text": thinking_text,
                                        "timestamp": entry.get("timestamp", "")
                                    })

                                elif block_type == "tool_use":
                                    tool_name = block.get("name", "unknown")
                                    tool_input = block.get("input", {})

                                    # Create brief summary of tool use
                                    tool_summary = tool_name
                                    if tool_name == "Read":
                                        file_path = tool_input.get("file_path", "")
                                        tool_summary = f"Read: {Path(file_path).name}" if file_path else "Read"
                                    elif tool_name == "Write":
                                        file_path = tool_input.get("file_path", "")
                                        tool_summary = f"Write: {Path(file_path).name}" if file_path else "Write"
                                    elif tool_name == "Edit":
                                        file_path = tool_input.get("file_path", "")
                                        tool_summary = f"Edit: {Path(file_path).name}" if file_path else "Edit"
                                    elif tool_name == "Bash":
                                        cmd = tool_input.get("command", "")[:40]
                                        tool_summary = f"Bash: {cmd}"
                                    elif tool_name == "Glob":
                                        pattern = tool_input.get("pattern", "")
                                        tool_summary = f"Glob: {pattern}"
                                    elif tool_name == "Grep":
                                        pattern = tool_input.get("pattern", "")[:30]
                                        tool_summary = f"Grep: {pattern}"

                                    trace["tool_calls"].append({
                                        "name": tool_name,
                                        "summary": tool_summary,
                                        "timestamp": entry.get("timestamp", "")
                                    })

                                elif block_type == "text":
                                    # Check if this is the initial text before tools
                                    text = block.get("text", "")
                                    if text and not trace["thinking_blocks"] and not trace["tool_calls"]:
                                        # This might be the assistant's initial response text
                                        pass

                # Get tool result timing from toolUseResult
                if entry_type == "user":
                    tool_result = entry.get("toolUseResult")
                    if isinstance(tool_result, dict) and "durationMs" in tool_result:
                        duration_ms = tool_result.get("durationMs", 0)
                        # Try to attach duration to the last tool call
                        if trace["tool_calls"]:
                            trace["tool_calls"][-1]["duration_ms"] = duration_ms

            except json.JSONDecodeError:
                pass
            except Exception as e:
                log(f"Error parsing entry: {e}")

    except Exception as e:
        log(f"Error reading transcript: {e}")

    return trace


def format_duration(ms: int) -> str:
    """Format milliseconds as human-readable duration"""
    if ms < 1000:
        return f"{ms}ms"
    elif ms < 60000:
        return f"{ms/1000:.1f}s"
    else:
        minutes = ms // 60000
        seconds = (ms % 60000) / 1000
        return f"{minutes}m{seconds:.0f}s"


def build_trace_summary(trace: dict) -> str:
    """Build a human-readable trace summary"""
    lines = ["--- Turn Trace ---"]

    # Combine thinking and tool calls in chronological order
    events = []

    for tb in trace.get("thinking_blocks", []):
        events.append(("think", tb.get("text", ""), tb.get("timestamp", ""), 0))

    for tc in trace.get("tool_calls", []):
        duration = tc.get("duration_ms", 0)
        events.append(("tool", tc.get("summary", ""), tc.get("timestamp", ""), duration))

    # Sort by timestamp if available
    events.sort(key=lambda x: x[2] if x[2] else "")

    for event_type, text, ts, duration in events:
        duration_str = f" ({format_duration(duration)})" if duration > 0 else ""
        if event_type == "think":
            lines.append(f"[think] {text}{duration_str}")
        else:
            lines.append(f"[tool] {text}{duration_str}")

    # Token summary
    tokens = trace.get("tokens", {})
    token_in = tokens.get("input", 0)
    token_out = tokens.get("output", 0)
    cache_read = tokens.get("cache_read", 0)
    cache_create = tokens.get("cache_create", 0)

    if token_in > 0 or token_out > 0:
        token_parts = [f"{token_in:,} in", f"{token_out:,} out"]
        if cache_read > 0:
            token_parts.append(f"{cache_read:,} cache")
        lines.append(f"--- Tokens: {' / '.join(token_parts)} ---")

    return "\n".join(lines)


def log_trace_to_file(session_id: str, trace: dict) -> None:
    """Log trace to traces.jsonl"""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        traces_file = LOG_DIR / "traces.jsonl"

        trace_entry = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "trace": {
                "thinking_count": len(trace.get("thinking_blocks", [])),
                "tool_calls": [tc.get("summary", "") for tc in trace.get("tool_calls", [])],
                "tool_durations_ms": [tc.get("duration_ms", 0) for tc in trace.get("tool_calls", []) if tc.get("duration_ms")]
            },
            "tokens": trace.get("tokens", {})
        }

        with open(traces_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace_entry) + "\n")
    except Exception as e:
        log(f"Error logging trace: {e}")


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


def detect_verification_needs(cwd: str) -> dict:
    """Detect what verification is needed based on changed files"""
    verification = {
        "needs_tests": False,
        "needs_lint": False,
        "needs_typecheck": False,
        "needs_build": False,
        "suggestions": []
    }

    cwd_path = Path(cwd)

    try:
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Also check staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=cwd, capture_output=True, text=True, timeout=5
        )
        staged_files = result.stdout.strip().split("\n") if result.stdout.strip() else []

        all_changed = set(changed_files + staged_files)

        if not all_changed:
            return verification

        # Detect file types changed
        py_changed = any(f.endswith('.py') for f in all_changed)
        ts_changed = any(f.endswith(('.ts', '.tsx', '.js', '.jsx')) for f in all_changed)

        # Check for test files
        has_pytest = (cwd_path / "pytest.ini").exists() or (cwd_path / "pyproject.toml").exists()
        has_jest = (cwd_path / "jest.config.js").exists() or (cwd_path / "jest.config.ts").exists()
        has_package_json = (cwd_path / "package.json").exists()

        # Suggest verification based on changes
        if py_changed:
            verification["needs_lint"] = True
            verification["needs_typecheck"] = True
            if has_pytest:
                verification["needs_tests"] = True
                verification["suggestions"].append("pytest -x --tb=short")
            verification["suggestions"].append("python -m py_compile <changed_files>")

        if ts_changed:
            verification["needs_lint"] = True
            verification["needs_typecheck"] = True
            if has_jest:
                verification["needs_tests"] = True
                verification["suggestions"].append("npm test")
            if has_package_json:
                verification["needs_build"] = True
                verification["suggestions"].append("npm run build")

    except Exception as e:
        log(f"Error detecting verification needs: {e}")

    return verification


def check_recent_edits(cwd: str) -> int:
    """Count files edited in this session"""
    try:
        edit_log = LOG_DIR / "edits.jsonl"
        if not edit_log.exists():
            return 0

        lines = edit_log.read_text().strip().split("\n")
        # Count edits in last 10 minutes
        recent = 0
        cutoff = datetime.now().timestamp() - 600
        for line in reversed(lines[-50:]):  # Last 50 entries
            try:
                entry = json.loads(line)
                if entry.get("ts", 0) > cutoff:
                    recent += 1
            except:
                pass
        return recent
    except:
        return 0


def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    stop_ts = datetime.now().strftime("%H:%M:%S")
    session_id = data.get("session_id", "")
    session_id_short = session_id[:8] if session_id else ""
    cwd = data.get("cwd", os.getcwd())

    log(f"Response complete at {stop_ts}")

    # Log completion
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_DIR / "events.jsonl", "a") as f:
            f.write(json.dumps({
                "e": "stop",
                "t": stop_ts,
                "session": session_id_short,
                "cwd": cwd
            }) + "\n")
    except:
        pass

    # === NEW: Parse transcript and build trace ===
    trace_summary = ""
    if session_id:
        transcript_path = find_transcript_file(session_id)
        if transcript_path:
            log(f"Found transcript: {transcript_path}")
            trace = parse_transcript_last_turn(transcript_path)

            # Only show trace if there's content
            if trace.get("thinking_blocks") or trace.get("tool_calls"):
                trace_summary = build_trace_summary(trace)
                log_trace_to_file(session_id, trace)

    # Check for session issues
    issues = get_session_issues()

    # Auto-verification detection (Boris-style)
    verification = detect_verification_needs(cwd)
    recent_edits = check_recent_edits(cwd)

    # Build verification reminder
    verify_msg = ""
    if verification["needs_tests"] or verification["needs_build"]:
        if verification["suggestions"]:
            verify_msg = f" | Verify: {verification['suggestions'][0]}"

    # Build user message
    parts = ["[OK] Complete"]

    if recent_edits > 3:
        parts.append(f"{recent_edits} edits")

    if issues:
        parts.append(f"[WARN] {', '.join(issues[:2])}")

    if verify_msg:
        parts.append(verify_msg)
    elif verification["needs_tests"]:
        parts.append("[TIP] Run tests to verify")

    msg = " | ".join(parts)

    # Add verification hint for significant sessions
    system_msg = msg
    if verification["suggestions"] and recent_edits > 2:
        system_msg += f"\n\n[AUTO-VERIFY] Consider running: {' && '.join(verification['suggestions'][:2])}"

    # Append trace summary if available
    if trace_summary:
        system_msg += f"\n\n{trace_summary}"

    output = {"systemMessage": system_msg}
    print(json.dumps(output))

    # Emit terminal bell - propagates through SSH/SSM
    sys.stderr.write("\a")
    sys.stderr.flush()

    sys.exit(0)

if __name__ == "__main__":
    main()
