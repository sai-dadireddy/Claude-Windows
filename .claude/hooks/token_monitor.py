#!/usr/bin/env python3
"""
Token Monitor Hook - Real-time token usage tracking and alerts

Features:
- Tracks token usage from session transcripts
- Alerts at configurable thresholds (70%, 80%, 90%)
- Logs token metrics to tokens.jsonl
- Model-aware context limits
- Provides burn rate estimation

Runs as: PostToolUse hook (after each tool execution)
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Configuration
LOG_DIR = Path.home() / ".claude" / "logs"
TOKEN_LOG = LOG_DIR / "tokens.jsonl"
TOKEN_STATE = LOG_DIR / ".token_state.json"

# Model context limits (as of Jan 2026)
MODEL_LIMITS = {
    "claude-opus-4-5": 200000,
    "claude-sonnet-4-5": 200000,
    "claude-haiku-4-5": 200000,
    "claude-3-opus": 200000,
    "claude-3-sonnet": 200000,
    "claude-3-haiku": 200000,
    "default": 200000
}

# Alert thresholds
THRESHOLDS = {
    "healthy": 0.70,   # < 70% - green
    "caution": 0.80,   # 70-80% - yellow
    "warning": 0.90,   # 80-90% - orange
    "critical": 0.95   # > 90% - red
}

def get_model_limit(model_name: str = None) -> int:
    """Get context limit for model"""
    if not model_name:
        model_name = os.environ.get("ANTHROPIC_MODEL", "default")

    for key, limit in MODEL_LIMITS.items():
        if key in model_name.lower():
            return limit
    return MODEL_LIMITS["default"]

def find_session_transcript(session_id: str):
    """Find the transcript file for current session"""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.exists():
        return None

    # Search all project directories
    for project_dir in projects_dir.iterdir():
        if not project_dir.is_dir():
            continue
        sessions_dir = project_dir / "sessions"
        if not sessions_dir.exists():
            continue

        # Find session file
        for session_file in sessions_dir.glob(f"{session_id}*.jsonl"):
            return session_file
        # Also try partial match
        for session_file in sessions_dir.glob("*.jsonl"):
            if session_id[:8] in session_file.name:
                return session_file

    return None

def parse_transcript_tokens(transcript_path) -> dict:
    """Parse token usage from transcript file"""
    tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_creation_tokens": 0,
        "total_tokens": 0,
        "entries": 0
    }

    if not transcript_path or not transcript_path.exists():
        return tokens

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    tokens["entries"] += 1

                    # Look for usage data in various locations
                    usage = None
                    if "usage" in entry:
                        usage = entry["usage"]
                    elif "message" in entry and isinstance(entry["message"], dict):
                        usage = entry["message"].get("usage")

                    if usage:
                        tokens["input_tokens"] += usage.get("input_tokens", 0)
                        tokens["output_tokens"] += usage.get("output_tokens", 0)
                        tokens["cache_read_tokens"] += usage.get("cache_read_input_tokens", 0)
                        tokens["cache_creation_tokens"] += usage.get("cache_creation_input_tokens", 0)
                except:
                    continue

        tokens["total_tokens"] = tokens["input_tokens"] + tokens["output_tokens"]
    except Exception as e:
        pass

    return tokens

def load_token_state() -> dict:
    """Load current token state"""
    try:
        if TOKEN_STATE.exists():
            return json.loads(TOKEN_STATE.read_text())
    except:
        pass
    return {"session_id": None, "tokens": {}, "alerts_sent": []}

def save_token_state(state: dict):
    """Save token state"""
    try:
        TOKEN_STATE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_STATE.write_text(json.dumps(state))
    except:
        pass

def log_tokens(session_id: str, tokens: dict, alert_level: str = None):
    """Log token metrics"""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id[:8] if session_id else "unknown",
            "tokens": tokens,
            "alert": alert_level
        }
        with open(TOKEN_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

def get_alert_level(usage_ratio: float):
    """Determine alert level based on usage ratio"""
    if usage_ratio >= THRESHOLDS["critical"]:
        return "critical"
    elif usage_ratio >= THRESHOLDS["warning"]:
        return "warning"
    elif usage_ratio >= THRESHOLDS["caution"]:
        return "caution"
    return None

def format_tokens(n: int) -> str:
    """Format token count for display"""
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    elif n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    session_id = data.get("session_id", "")

    # Find and parse transcript
    transcript = find_session_transcript(session_id)
    tokens = parse_transcript_tokens(transcript)

    if tokens["total_tokens"] == 0:
        # No token data available yet
        sys.exit(0)

    # Calculate usage ratio
    limit = get_model_limit()
    usage_ratio = tokens["total_tokens"] / limit

    # Load state to track alerts
    state = load_token_state()
    if state.get("session_id") != session_id:
        state = {"session_id": session_id, "tokens": {}, "alerts_sent": []}

    # Check alert level
    alert_level = get_alert_level(usage_ratio)

    # Log token metrics
    log_tokens(session_id, tokens, alert_level)

    output = {}

    # Send alert if crossing threshold (only once per level)
    if alert_level and alert_level not in state["alerts_sent"]:
        state["alerts_sent"].append(alert_level)
        save_token_state(state)

        pct = int(usage_ratio * 100)
        total = format_tokens(tokens["total_tokens"])
        limit_str = format_tokens(limit)

        if alert_level == "critical":
            msg = f"[CRITICAL] Context {pct}% full ({total}/{limit_str}) - Consider /compact"
            context = f"""<token-alert level="critical" usage="{pct}%">
CRITICAL: Context is {pct}% full. You have ~{format_tokens(limit - tokens['total_tokens'])} tokens remaining.
Consider:
1. Running /compact-context to summarize and free space
2. Completing current task and starting fresh session
3. Being more concise in responses
</token-alert>"""
        elif alert_level == "warning":
            msg = f"[WARN] Context {pct}% full ({total}/{limit_str})"
            context = f"<token-alert level=\"warning\" usage=\"{pct}%\">Context at {pct}%. Monitor usage.</token-alert>"
        else:  # caution
            msg = f"[INFO] Context {pct}% ({total}/{limit_str})"
            context = None

        output["systemMessage"] = msg
        if context:
            output["hookSpecificOutput"] = {
                "hookEventName": "PostToolUse",
                "additionalContext": context
            }

    # Update state
    state["tokens"] = tokens
    save_token_state(state)

    if output:
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
