#!/usr/bin/env python3
"""
Token Guard Hook - Prevents Runaway Token Consumption

Features:
- Warns about potentially expensive operations BEFORE execution
- Detects broad glob/grep patterns that return many results
- Guards sensitive file modifications
- Tracks operation costs over session
- Provides deliberate friction for expensive operations

Runs as: PreToolUse hook
"""

import sys
import json
from pathlib import Path
from datetime import datetime

LOG_DIR = Path.home() / ".claude" / "logs"
GUARD_LOG = LOG_DIR / "token_guard.jsonl"
GUARD_STATE = LOG_DIR / ".guard_state.json"

# Operation cost estimates (tokens)
COST_ESTIMATES = {
    "Read": {"base": 500, "per_line": 10},
    "Glob": {"base": 100, "per_match": 50},
    "Grep": {"base": 200, "per_match": 100},
    "Bash": {"base": 300, "high_risk": 2000},
    "Task": {"base": 5000},  # Spawning agents is expensive
    "WebFetch": {"base": 3000},
    "WebSearch": {"base": 1000},
}

# Patterns that indicate expensive operations
EXPENSIVE_PATTERNS = [
    "**/*",           # Recursive glob all files
    "*.*",            # All files with extension
    "**/*.ts",        # Recursive typescript (often many files)
    "**/*.tsx",
    "**/*.js",
    "**/*.py",
]

HIGH_RISK_BASH = [
    "find / ",        # Search entire filesystem
    "find . -name",   # Recursive find
    "grep -r",        # Recursive grep
    "npm install",    # Package install (slow + output)
    "pip install",
]

SENSITIVE_FILES = [
    "settings.json",
    "CLAUDE.md",
    "package.json",
    "package-lock.json",
    ".gitignore",
    "tsconfig.json",
    "pyproject.toml",
]

def load_guard_state() -> dict:
    """Load guard state for session tracking"""
    try:
        if GUARD_STATE.exists():
            return json.loads(GUARD_STATE.read_text())
    except:
        pass
    return {"warnings_issued": 0, "estimated_cost": 0, "operations": []}

def save_guard_state(state: dict):
    """Save guard state"""
    try:
        GUARD_STATE.parent.mkdir(parents=True, exist_ok=True)
        GUARD_STATE.write_text(json.dumps(state))
    except:
        pass

def log_guard_event(tool: str, warning: str, estimated_cost: int):
    """Log guard events"""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "warning": warning,
            "estimated_cost": estimated_cost
        }
        with open(GUARD_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

def estimate_cost(tool_name: str, tool_input: dict):
    """Estimate token cost of operation and return warning if expensive"""
    cost = COST_ESTIMATES.get(tool_name, {}).get("base", 100)
    warning = None

    if tool_name == "Glob":
        pattern = tool_input.get("pattern", "")
        if any(exp in pattern for exp in EXPENSIVE_PATTERNS):
            cost = 2000  # Potentially many matches
            warning = f"Broad glob pattern '{pattern}' may return many files"

    elif tool_name == "Grep":
        pattern = tool_input.get("pattern", "")
        path = tool_input.get("path", "")
        output_mode = tool_input.get("output_mode", "files_with_matches")

        if output_mode == "content" and not tool_input.get("head_limit"):
            cost = 3000
            warning = "Grep with content mode without head_limit may return large output"

        if "**" in (path or "") or not path:
            cost += 1000
            warning = warning or "Grep searching many directories"

    elif tool_name == "Bash":
        cmd = tool_input.get("command", "")
        for risk in HIGH_RISK_BASH:
            if risk in cmd:
                cost = COST_ESTIMATES["Bash"]["high_risk"]
                warning = f"High-cost bash operation: {risk}"
                break

    elif tool_name in ["Write", "Edit"]:
        file_path = tool_input.get("file_path", "")
        for sensitive in SENSITIVE_FILES:
            if sensitive in file_path:
                warning = f"Modifying sensitive file: {sensitive}"
                break

    elif tool_name == "Task":
        # Spawning subagents is expensive
        cost = 5000
        agent_type = tool_input.get("subagent_type", "")
        if "heavy" in agent_type.lower():
            cost = 10000
            warning = f"Spawning heavy agent: {agent_type}"

    elif tool_name == "Read":
        # Large file reads
        limit = tool_input.get("limit")
        if not limit or limit > 1000:
            cost = 1500
            # Don't warn for reads - they're usually necessary

    return cost, warning

def should_warn(tool_name: str, tool_input: dict, state: dict):
    """Determine if operation should trigger warning"""
    cost, warning = estimate_cost(tool_name, tool_input)

    # Always warn for very expensive operations
    if cost >= 5000:
        return True, warning or f"High-cost {tool_name} operation", cost

    # Warn if cumulative cost is getting high
    cumulative = state.get("estimated_cost", 0) + cost
    if cumulative > 50000 and state.get("warnings_issued", 0) < 3:
        return True, f"Session cost high (~{cumulative//1000}K tokens estimated)", cost

    # Specific warnings
    if warning:
        return True, warning, cost

    return False, None, cost

def main():
    """Main hook execution"""
    try:
        hook_input = json.load(sys.stdin)
    except:
        sys.exit(0)

    # Handle both old and new hook data formats
    tool_name = hook_input.get("tool_name") or hook_input.get("toolName", "")
    tool_input = hook_input.get("tool_input") or hook_input.get("toolInput", {})

    if not tool_name:
        sys.exit(0)

    # Load state
    state = load_guard_state()

    # Check if we should warn
    should_issue_warning, warning_msg, cost = should_warn(tool_name, tool_input, state)

    # Update state
    state["estimated_cost"] = state.get("estimated_cost", 0) + cost
    state["operations"].append({
        "tool": tool_name,
        "cost": cost,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    # Keep only last 100 operations
    state["operations"] = state["operations"][-100:]

    output = {}

    if should_issue_warning:
        state["warnings_issued"] = state.get("warnings_issued", 0) + 1

        # Log the warning
        log_guard_event(tool_name, warning_msg or "expensive operation", cost)

        # Output warning to user AND inject context to model (2.1.9 feature)
        output["systemMessage"] = f"[GUARD] {warning_msg} (~{cost} tokens)"
        output["hookSpecificOutput"] = {
            "hookEventName": "PreToolUse",
            "additionalContext": f"""<token-guard tool="{tool_name}" cost="{cost}">
{warning_msg}
Consider: Use head_limit for Grep, specific patterns for Glob, or break into smaller operations.
Session estimated cost: ~{state.get('estimated_cost', 0)//1000}K tokens
</token-guard>"""
        }

        # Don't block - just warn and inform
        # To block, we would add: output["hookSpecificOutput"]["permissionDecision"] = "deny"

    save_guard_state(state)

    if output:
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
