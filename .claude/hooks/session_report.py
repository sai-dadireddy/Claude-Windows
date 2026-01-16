#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Session Report Hook - Comprehensive session analytics on Stop

Generates a detailed report combining:
- Tool usage trace data from tools.jsonl
- Quality gate results from quality_gates.jsonl
- Checkpoints/commits from checkpoints.jsonl
- Observations captured from observations.jsonl
- Error patterns from recent_errors.json

Output:
1. Detailed JSON report to ~/.claude/logs/session_reports.jsonl
2. Brief summary in systemMessage for user feedback
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional

VERBOSE = False
LOG_DIR = Path.home() / ".claude" / "logs"
REPORT_FILE = LOG_DIR / "session_reports.jsonl"


def log(msg: str):
    """Debug logging"""
    if VERBOSE:
        print(f"[SessionReport] {msg}", file=sys.stderr)


def parse_timestamp(ts_str: str) -> Optional[datetime]:
    """Parse various timestamp formats"""
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%H:%M:%S",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(ts_str, fmt)
            # If only time, assume today
            if fmt == "%H:%M:%S":
                today = datetime.now().date()
                dt = datetime.combine(today, dt.time())
            return dt
        except ValueError:
            continue
    return None


def get_session_window(session_id: str) -> tuple[Optional[datetime], Optional[datetime]]:
    """Get session start and end times from sessions.jsonl and events.jsonl"""
    start_time = None
    end_time = None

    # Check sessions.jsonl for start
    sessions_file = LOG_DIR / "sessions.jsonl"
    if sessions_file.exists():
        try:
            for line in sessions_file.read_text().strip().split("\n"):
                if not line:
                    continue
                entry = json.loads(line)
                ts = entry.get("timestamp", "")
                if session_id[:8] in ts or session_id[:8] in str(entry):
                    parsed = parse_timestamp(ts)
                    if parsed and (not start_time or parsed < start_time):
                        start_time = parsed
        except Exception as e:
            log(f"Error reading sessions: {e}")

    # Check events.jsonl for stop events
    events_file = LOG_DIR / "events.jsonl"
    if events_file.exists():
        try:
            for line in events_file.read_text().strip().split("\n"):
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get("session", "").startswith(session_id[:8]):
                    if entry.get("e") == "stop":
                        ts = entry.get("t", "")
                        parsed = parse_timestamp(ts)
                        if parsed and (not end_time or parsed > end_time):
                            end_time = parsed
        except Exception as e:
            log(f"Error reading events: {e}")

    return start_time, end_time


def get_tool_usage(session_id: str, start_time: Optional[datetime], end_time: Optional[datetime]) -> dict:
    """Analyze tool usage from tools.jsonl"""
    tools_file = LOG_DIR / "tools.jsonl"
    tool_counts = defaultdict(int)
    tool_times = defaultdict(list)
    files_edited = set()
    files_read = set()
    bash_commands = []

    if not tools_file.exists():
        return {
            "total": 0,
            "breakdown": {},
            "files_edited": [],
            "files_read": [],
            "bash_commands": []
        }

    # Determine time window - use last 30 min if no session times
    cutoff = datetime.now() - timedelta(minutes=30)
    if start_time:
        cutoff = start_time

    try:
        lines = tools_file.read_text().strip().split("\n")
        for line in lines:
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = parse_timestamp(entry.get("t", ""))

                # Filter by time window
                if ts and ts < cutoff:
                    continue
                if end_time and ts and ts > end_time:
                    continue

                tool = entry.get("tool", "unknown")
                tool_counts[tool] += 1

                # Track duration if available
                duration = entry.get("duration_ms")
                if duration:
                    tool_times[tool].append(duration)

                # Track files
                if tool == "Edit":
                    file_path = entry.get("file", "")
                    if file_path:
                        files_edited.add(file_path)
                elif tool == "Read":
                    file_path = entry.get("file", "")
                    if file_path:
                        files_read.add(file_path)
                elif tool == "Bash":
                    cmd = entry.get("cmd", "")
                    if cmd:
                        bash_commands.append(cmd[:100])  # Truncate long commands

            except json.JSONDecodeError:
                continue
    except Exception as e:
        log(f"Error reading tools: {e}")

    # Calculate averages
    breakdown = {}
    for tool, count in tool_counts.items():
        avg_ms = 0
        if tool_times[tool]:
            avg_ms = int(sum(tool_times[tool]) / len(tool_times[tool]))
        breakdown[tool] = {"count": count, "avg_ms": avg_ms}

    return {
        "total": sum(tool_counts.values()),
        "breakdown": breakdown,
        "files_edited": list(files_edited)[:20],  # Limit to 20
        "files_read": list(files_read)[:20],
        "bash_commands": bash_commands[-10:]  # Last 10
    }


def get_commits(session_id: str, start_time: Optional[datetime]) -> list:
    """Get commits made during session from checkpoints.jsonl"""
    checkpoints_file = LOG_DIR / "checkpoints.jsonl"
    commits = []

    if not checkpoints_file.exists():
        return commits

    cutoff = datetime.now() - timedelta(minutes=60)
    if start_time:
        cutoff = start_time

    try:
        lines = checkpoints_file.read_text().strip().split("\n")
        for line in lines:
            if not line:
                continue
            try:
                entry = json.loads(line)

                # Check session match
                entry_session = entry.get("session_id", "")
                if session_id[:8] not in entry_session:
                    continue

                # Check success
                if not entry.get("success"):
                    continue

                ts = parse_timestamp(entry.get("timestamp", ""))
                if ts and ts < cutoff:
                    continue

                commits.append({
                    "hash": entry.get("commit", "")[:7],
                    "message": entry.get("message", "")[:100],
                    "files": entry.get("files", 0)
                })
            except json.JSONDecodeError:
                continue
    except Exception as e:
        log(f"Error reading checkpoints: {e}")

    return commits


def get_observations(session_id: str, start_time: Optional[datetime]) -> list:
    """Get observations captured during session"""
    obs_file = LOG_DIR / "observations.jsonl"
    observations = []

    if not obs_file.exists():
        return observations

    cutoff = datetime.now() - timedelta(minutes=60)
    if start_time:
        cutoff = start_time

    try:
        lines = obs_file.read_text().strip().split("\n")
        for line in lines[-50:]:  # Last 50 entries
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = parse_timestamp(entry.get("timestamp", ""))

                if ts and ts < cutoff:
                    continue

                observations.append({
                    "type": entry.get("type", "unknown"),
                    "concept": entry.get("concept", ""),
                    "content": entry.get("observation", "")[:200]  # Truncate
                })
            except json.JSONDecodeError:
                continue
    except Exception as e:
        log(f"Error reading observations: {e}")

    return observations[-10:]  # Return last 10


def get_quality_results(session_id: str) -> dict:
    """Get latest quality gate results"""
    quality_file = LOG_DIR / "quality_gates.jsonl"
    result = {
        "tests_passed": None,
        "lint_passed": None,
        "build_passed": None,
        "passed": [],
        "failed": [],
        "skipped": []
    }

    if not quality_file.exists():
        return result

    try:
        lines = quality_file.read_text().strip().split("\n")
        # Get entries matching session
        for line in reversed(lines[-20:]):
            if not line:
                continue
            try:
                entry = json.loads(line)
                entry_session = entry.get("session_id", "")

                if session_id[:8] in entry_session or not entry_session:
                    result["passed"] = entry.get("passed", [])
                    result["failed"] = entry.get("failed", [])
                    result["skipped"] = entry.get("skipped", [])

                    # Determine pass/fail
                    result["tests_passed"] = "pytest" in result["passed"] or "jest" in result["passed"]
                    result["lint_passed"] = "eslint" not in result["failed"] and "ruff" not in result["failed"]
                    result["build_passed"] = "typescript" not in result["failed"]
                    break
            except json.JSONDecodeError:
                continue
    except Exception as e:
        log(f"Error reading quality gates: {e}")

    return result


def get_error_stats() -> dict:
    """Get error statistics from recent_errors.json"""
    errors_file = LOG_DIR / "recent_errors.json"
    stats = {
        "encountered": 0,
        "resolved": 0,
        "patterns": []
    }

    if not errors_file.exists():
        return stats

    try:
        data = json.loads(errors_file.read_text())
        if isinstance(data, dict):
            stats["encountered"] = data.get("total_errors", 0)
            stats["resolved"] = data.get("resolved_errors", 0)
            patterns = data.get("patterns", [])
            if isinstance(patterns, list):
                stats["patterns"] = patterns[:5]  # Top 5 patterns
    except Exception as e:
        log(f"Error reading error stats: {e}")

    return stats


def generate_report(session_id: str, cwd: str) -> dict:
    """Generate comprehensive session report"""
    now = datetime.now()

    # Get session timing
    start_time, end_time = get_session_window(session_id)
    if not start_time:
        start_time = now - timedelta(minutes=15)  # Default to 15 min session
    if not end_time:
        end_time = now

    duration_min = int((end_time - start_time).total_seconds() / 60)
    if duration_min < 1:
        duration_min = 1

    # Gather data
    tool_usage = get_tool_usage(session_id, start_time, end_time)
    commits = get_commits(session_id, start_time)
    observations = get_observations(session_id, start_time)
    quality = get_quality_results(session_id)
    errors = get_error_stats()

    # Build report
    report = {
        "session_id": session_id[:8] if session_id else "unknown",
        "started": start_time.isoformat() if start_time else None,
        "ended": end_time.isoformat() if end_time else now.isoformat(),
        "duration_min": duration_min,
        "cwd": cwd,
        "summary": {
            "tools_used": tool_usage["total"],
            "files_edited": len(tool_usage["files_edited"]),
            "files_read": len(tool_usage["files_read"]),
            "commits_made": len(commits),
            "errors_encountered": errors["encountered"],
            "errors_resolved": errors["resolved"],
            "observations": len(observations)
        },
        "tools_breakdown": tool_usage["breakdown"],
        "files_touched": tool_usage["files_edited"],
        "commits": commits,
        "observations": observations,
        "quality": {
            "tests_passed": quality["tests_passed"],
            "lint_passed": quality["lint_passed"],
            "build_passed": quality["build_passed"],
            "passed": quality["passed"],
            "failed": quality["failed"],
            "skipped": quality["skipped"]
        },
        "errors": errors
    }

    return report


def save_report(report: dict) -> bool:
    """Save report to session_reports.jsonl"""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(REPORT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(report, default=str) + "\n")
        return True
    except Exception as e:
        log(f"Error saving report: {e}")
        return False


def format_summary(report: dict) -> str:
    """Format brief summary for systemMessage"""
    s = report["summary"]

    parts = [
        f"{report['duration_min']} min",
        f"{s['tools_used']} tools",
        f"{s['files_edited']} files"
    ]

    if s["commits_made"] > 0:
        parts.append(f"{s['commits_made']} commits")

    if s["errors_encountered"] > 0:
        if s["errors_resolved"] == s["errors_encountered"]:
            parts.append(f"{s['errors_encountered']} errors (all resolved)")
        else:
            unresolved = s["errors_encountered"] - s["errors_resolved"]
            parts.append(f"{unresolved} unresolved errors")

    # Quality status
    q = report["quality"]
    if q["failed"]:
        parts.append(f"FAILED: {', '.join(q['failed'][:2])}")
    elif q["passed"]:
        parts.append("quality OK")

    return "[Session Report] " + " | ".join(parts)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        log(f"Failed to read stdin: {e}")
        sys.exit(0)

    session_id = data.get("session_id", "")
    cwd = data.get("cwd", os.getcwd())

    log(f"Generating session report for {session_id[:8] if session_id else 'unknown'}")

    # Generate report
    report = generate_report(session_id, cwd)

    # Save to log file
    saved = save_report(report)
    log(f"Report saved: {saved}")

    # Format summary message
    summary = format_summary(report)

    # Output for hook chain
    # Note: This is complementary to stop.py, so we add to systemMessage
    output = {
        "systemMessage": summary
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
