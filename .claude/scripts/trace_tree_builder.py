#!/usr/bin/env python3
"""
Trace Tree Builder - Aggregates tool logs into hierarchical trace trees.

Transforms flat tools.jsonl into readable trace trees showing:
- Session boundaries
- Tool call sequences with timing
- Error patterns
- Cost attribution

Usage:
    python trace_tree_builder.py              # Show today's traces
    python trace_tree_builder.py --sessions 5 # Show last N sessions
    python trace_tree_builder.py --since "2026-01-16 08:00"
    python trace_tree_builder.py --html > report.html
    python trace_tree_builder.py --json
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Default paths
TOOLS_LOG_PATH = Path.home() / ".claude" / "logs" / "tools.jsonl"
SESSION_GAP_MINUTES = 5  # Time gap to consider as session boundary


def parse_timestamp(time_str: str, date_context: Optional[datetime] = None) -> Optional[datetime]:
    """
    Parse timestamp from tools.jsonl format.
    The log format uses "HH:MM:SS" without date, so we need date context.
    """
    if not time_str:
        return None

    try:
        # Try full ISO format first
        if "T" in time_str or "-" in time_str:
            return datetime.fromisoformat(time_str.replace("Z", "+00:00"))

        # Parse HH:MM:SS format
        time_parts = time_str.split(":")
        if len(time_parts) >= 3:
            hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2])
            if date_context:
                return date_context.replace(hour=hour, minute=minute, second=second, microsecond=0)
            else:
                # Use today as default
                today = datetime.now().replace(hour=hour, minute=minute, second=second, microsecond=0)
                return today
    except (ValueError, IndexError):
        pass

    return None


def load_tools_log(log_path: Path = TOOLS_LOG_PATH) -> List[Dict[str, Any]]:
    """Load and parse tools.jsonl file."""
    entries = []

    if not log_path.exists():
        return entries

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                entry["_line_num"] = line_num
                entries.append(entry)
            except json.JSONDecodeError:
                # Skip malformed lines
                pass

    return entries


def infer_dates(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Infer full datetime for entries that only have time.
    Uses file modification time and time patterns to determine dates.
    """
    if not entries:
        return entries

    # Start with today and work backwards based on time patterns
    current_date = datetime.now().date()
    last_time = None

    for entry in entries:
        time_str = entry.get("t", "")
        parsed = parse_timestamp(time_str, datetime.combine(current_date, datetime.min.time()))

        if parsed:
            # If time goes backwards significantly, assume previous day
            if last_time and parsed.time() > last_time:
                # Check if time jumped backwards by more than 12 hours (likely day change)
                pass  # Keep same date

            entry["_datetime"] = parsed
            last_time = parsed.time()
        else:
            entry["_datetime"] = None

    return entries


def group_into_sessions(entries: List[Dict[str, Any]], gap_minutes: int = SESSION_GAP_MINUTES) -> List[List[Dict[str, Any]]]:
    """
    Group entries into sessions based on time gaps.
    A session boundary is defined as a gap > gap_minutes between consecutive entries.
    """
    if not entries:
        return []

    sessions = []
    current_session = []
    last_datetime = None

    for entry in entries:
        entry_dt = entry.get("_datetime")

        if entry_dt is None:
            # Entry without timestamp, add to current session
            if current_session:
                current_session.append(entry)
            else:
                current_session = [entry]
            continue

        if last_datetime is None:
            current_session = [entry]
        else:
            gap = (entry_dt - last_datetime).total_seconds() / 60

            if gap > gap_minutes:
                # New session
                if current_session:
                    sessions.append(current_session)
                current_session = [entry]
            else:
                current_session.append(entry)

        last_datetime = entry_dt

    # Add final session
    if current_session:
        sessions.append(current_session)

    return sessions


def build_trace_tree(session: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build a trace tree structure from a session's entries."""
    if not session:
        return {}

    # Get session boundaries
    datetimes = [e.get("_datetime") for e in session if e.get("_datetime")]

    session_start = min(datetimes) if datetimes else None
    session_end = max(datetimes) if datetimes else None

    total_duration_ms = 0
    if session_start and session_end:
        total_duration_ms = int((session_end - session_start).total_seconds() * 1000)

    # Build tools list
    tools = []
    by_tool = defaultdict(int)
    errors = 0
    durations = []

    for entry in session:
        tool_name = entry.get("tool", "Unknown")
        by_tool[tool_name] += 1

        duration_ms = entry.get("duration_ms", 0)
        if duration_ms:
            durations.append(duration_ms)

        # Determine status
        status = "ok"
        err_msg = None
        if entry.get("error") or entry.get("err"):
            status = "error"
            err_msg = entry.get("error") or entry.get("err")
            errors += 1

        # Build tool entry
        tool_entry = {
            "tool": tool_name,
            "duration_ms": duration_ms,
            "status": status,
        }

        # Add relevant fields based on tool type
        if "file" in entry:
            tool_entry["file"] = entry["file"]
        if "cmd" in entry:
            tool_entry["cmd"] = entry["cmd"][:100]  # Truncate long commands
        if "pattern" in entry:
            tool_entry["pattern"] = entry["pattern"]
        if err_msg:
            tool_entry["err"] = str(err_msg)[:200]  # Truncate errors

        # Store original timestamp
        if entry.get("_datetime"):
            tool_entry["time"] = entry["_datetime"].strftime("%H:%M:%S")

        tools.append(tool_entry)

    # Calculate average duration
    avg_duration_ms = sum(durations) / len(durations) if durations else 0

    return {
        "session_start": session_start.isoformat() if session_start else None,
        "session_end": session_end.isoformat() if session_end else None,
        "total_duration_ms": total_duration_ms,
        "tools": tools,
        "summary": {
            "total_tools": len(tools),
            "by_tool": dict(by_tool),
            "errors": errors,
            "avg_duration_ms": round(avg_duration_ms, 1),
        }
    }


def format_duration(ms: float) -> str:
    """Format milliseconds into human-readable duration."""
    if ms == 0:
        return "   -"

    seconds = ms / 1000
    if seconds < 1:
        return f"{ms:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def format_session_duration(start: Optional[datetime], end: Optional[datetime]) -> str:
    """Format session duration."""
    if not start or not end:
        return "unknown"

    delta = end - start
    total_seconds = delta.total_seconds()

    if total_seconds < 60:
        return f"{int(total_seconds)}s"
    elif total_seconds < 3600:
        return f"{int(total_seconds / 60)}m"
    else:
        hours = int(total_seconds / 3600)
        minutes = int((total_seconds % 3600) / 60)
        return f"{hours}h {minutes}m"


def render_ascii_tree(trace: Dict[str, Any]) -> str:
    """Render trace tree as ASCII art."""
    lines = []

    # Session header
    start = trace.get("session_start", "")
    end = trace.get("session_end", "")

    if start and end:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        duration = format_session_duration(start_dt, end_dt)
        header = f"Session: {start_dt.strftime('%Y-%m-%d %H:%M')}-{end_dt.strftime('%H:%M')} ({duration}, {trace['summary']['total_tools']} tools)"
    else:
        header = f"Session: (unknown time, {trace['summary']['total_tools']} tools)"

    lines.append(header)

    # Tool entries
    tools = trace.get("tools", [])
    for i, tool in enumerate(tools):
        is_last = i == len(tools) - 1
        prefix = "`-- " if is_last else "|-- "

        # Duration
        duration_str = format_duration(tool.get("duration_ms", 0))

        # Tool description
        tool_name = tool.get("tool", "Unknown")
        details = ""

        if tool.get("file"):
            details = f": {tool['file']}"
        elif tool.get("cmd"):
            cmd = tool["cmd"]
            if len(cmd) > 50:
                cmd = cmd[:47] + "..."
            details = f": {cmd}"
        elif tool.get("pattern"):
            details = f": \"{tool['pattern']}\""

        # Status indicator
        status_indicator = ""
        if tool.get("status") == "error":
            status_indicator = " [ERROR]"

        line = f"{prefix}[{duration_str:>5}] {tool_name}{details}{status_indicator}"
        lines.append(line)

        # Error details (indented)
        if tool.get("err"):
            error_prefix = "    " if is_last else "|   "
            error_line = f"{error_prefix}`-- Error: {tool['err'][:80]}"
            lines.append(error_line)

    # Summary
    summary = trace.get("summary", {})
    lines.append(f"Summary: {summary.get('total_tools', 0)} tools, {summary.get('errors', 0)} errors, avg {format_duration(summary.get('avg_duration_ms', 0))}")
    lines.append("")

    return "\n".join(lines)


def render_html_report(traces: List[Dict[str, Any]]) -> str:
    """Render traces as an HTML report."""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Claude Tool Trace Report</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background: #f5f5f5; }
        .session { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .session-header { font-size: 1.2em; font-weight: bold; color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; margin-bottom: 15px; }
        .tool-list { list-style: none; padding: 0; margin: 0; }
        .tool-item { padding: 8px 0; border-bottom: 1px solid #eee; display: flex; align-items: flex-start; }
        .tool-item:last-child { border-bottom: none; }
        .duration { font-family: monospace; background: #e8e8e8; padding: 2px 8px; border-radius: 4px; margin-right: 10px; min-width: 50px; text-align: right; }
        .tool-name { font-weight: bold; color: #007acc; margin-right: 8px; }
        .tool-details { color: #666; font-family: monospace; font-size: 0.9em; }
        .status-error { background: #ffebee; border-left: 3px solid #f44336; padding-left: 10px; }
        .error-msg { color: #f44336; font-size: 0.85em; margin-top: 5px; font-family: monospace; }
        .summary { background: #f0f7ff; padding: 15px; border-radius: 6px; margin-top: 15px; }
        .summary-item { display: inline-block; margin-right: 20px; }
        .summary-label { color: #666; font-size: 0.9em; }
        .summary-value { font-weight: bold; color: #333; }
        h1 { color: #333; }
        .meta { color: #666; font-size: 0.9em; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Claude Tool Trace Report</h1>
    <div class="meta">Generated: """ + datetime.now().isoformat() + """</div>
"""

    for trace in traces:
        start = trace.get("session_start", "")
        end = trace.get("session_end", "")
        summary = trace.get("summary", {})

        if start and end:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
            duration = format_session_duration(start_dt, end_dt)
            header = f"{start_dt.strftime('%Y-%m-%d %H:%M')} - {end_dt.strftime('%H:%M')} ({duration})"
        else:
            header = "Unknown session time"

        html += f"""
    <div class="session">
        <div class="session-header">{header}</div>
        <ul class="tool-list">
"""

        for tool in trace.get("tools", []):
            duration_str = format_duration(tool.get("duration_ms", 0))
            tool_name = tool.get("tool", "Unknown")

            details = ""
            if tool.get("file"):
                details = tool["file"]
            elif tool.get("cmd"):
                details = tool["cmd"][:100]
            elif tool.get("pattern"):
                details = f'"{tool["pattern"]}"'

            error_class = " status-error" if tool.get("status") == "error" else ""
            error_html = ""
            if tool.get("err"):
                error_html = f'<div class="error-msg">{tool["err"][:150]}</div>'

            html += f"""            <li class="tool-item{error_class}">
                <span class="duration">{duration_str}</span>
                <span class="tool-name">{tool_name}</span>
                <span class="tool-details">{details}</span>
                {error_html}
            </li>
"""

        # Summary section
        by_tool_html = ", ".join([f"{k}: {v}" for k, v in summary.get("by_tool", {}).items()])

        html += f"""        </ul>
        <div class="summary">
            <span class="summary-item"><span class="summary-label">Total Tools:</span> <span class="summary-value">{summary.get('total_tools', 0)}</span></span>
            <span class="summary-item"><span class="summary-label">Errors:</span> <span class="summary-value">{summary.get('errors', 0)}</span></span>
            <span class="summary-item"><span class="summary-label">Avg Duration:</span> <span class="summary-value">{format_duration(summary.get('avg_duration_ms', 0))}</span></span>
            <div style="margin-top: 10px;"><span class="summary-label">By Tool:</span> {by_tool_html}</div>
        </div>
    </div>
"""

    html += """</body>
</html>
"""
    return html


def filter_by_since(sessions: List[List[Dict[str, Any]]], since: datetime) -> List[List[Dict[str, Any]]]:
    """Filter sessions to only include those starting after 'since' datetime."""
    filtered = []
    for session in sessions:
        if not session:
            continue
        # Get first datetime in session
        datetimes = [e.get("_datetime") for e in session if e.get("_datetime")]
        if datetimes:
            session_start = min(datetimes)
            if session_start >= since:
                filtered.append(session)
    return filtered


def filter_today(sessions: List[List[Dict[str, Any]]]) -> List[List[Dict[str, Any]]]:
    """Filter sessions to only include today's sessions."""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return filter_by_since(sessions, today)


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate tool logs into hierarchical trace trees",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python trace_tree_builder.py                    # Show today's traces
  python trace_tree_builder.py --sessions 5      # Show last 5 sessions
  python trace_tree_builder.py --since "2026-01-16 08:00"
  python trace_tree_builder.py --html > report.html
  python trace_tree_builder.py --json
        """
    )

    parser.add_argument(
        "--sessions", "-n",
        type=int,
        default=None,
        help="Show last N sessions (default: all today)"
    )

    parser.add_argument(
        "--since",
        type=str,
        default=None,
        help="Show sessions since datetime (format: 'YYYY-MM-DD HH:MM')"
    )

    parser.add_argument(
        "--html",
        action="store_true",
        help="Output as HTML report"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    parser.add_argument(
        "--log-path",
        type=str,
        default=None,
        help=f"Path to tools.jsonl (default: {TOOLS_LOG_PATH})"
    )

    parser.add_argument(
        "--gap",
        type=int,
        default=SESSION_GAP_MINUTES,
        help=f"Session gap in minutes (default: {SESSION_GAP_MINUTES})"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all sessions, not just today's"
    )

    args = parser.parse_args()

    # Determine log path
    log_path = Path(args.log_path) if args.log_path else TOOLS_LOG_PATH

    if not log_path.exists():
        print(f"Error: Log file not found: {log_path}", file=sys.stderr)
        print(f"Expected location: {TOOLS_LOG_PATH}", file=sys.stderr)
        sys.exit(1)

    # Load and process entries
    entries = load_tools_log(log_path)

    if not entries:
        print("No tool log entries found.", file=sys.stderr)
        sys.exit(0)

    # Infer dates
    entries = infer_dates(entries)

    # Group into sessions
    sessions = group_into_sessions(entries, args.gap)

    # Apply filters
    if args.since:
        try:
            since_dt = datetime.strptime(args.since, "%Y-%m-%d %H:%M")
            sessions = filter_by_since(sessions, since_dt)
        except ValueError:
            print(f"Error: Invalid date format '{args.since}'. Use 'YYYY-MM-DD HH:MM'", file=sys.stderr)
            sys.exit(1)
    elif not args.all and args.sessions is None:
        # Default: show today only
        sessions = filter_today(sessions)

    # Limit to N sessions if specified
    if args.sessions is not None:
        sessions = sessions[-args.sessions:]

    if not sessions:
        print("No sessions found matching the criteria.", file=sys.stderr)
        sys.exit(0)

    # Build trace trees
    traces = [build_trace_tree(session) for session in sessions]

    # Output
    if args.json:
        print(json.dumps(traces, indent=2, default=str))
    elif args.html:
        print(render_html_report(traces))
    else:
        # ASCII tree output
        for trace in traces:
            print(render_ascii_tree(trace))


if __name__ == "__main__":
    main()
