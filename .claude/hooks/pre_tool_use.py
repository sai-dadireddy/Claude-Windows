#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PreToolUse Hook - Security, Auto-permissions & Token Optimization

Features:
- Blocks dangerous commands
- Auto-allows safe operations (reduces permission prompts)
- Prevents MD file clutter
- Caches repeated tool checks for performance
- Minimal JSON output to reduce token usage
"""

import json
import sys
import os
import re
import hashlib
import time
from pathlib import Path

# Simple in-memory cache for this session
_cache = {}
CACHE_TTL = 300  # 5 minutes

def get_cache(key: str):
    """Get from cache if not expired"""
    if key in _cache:
        ts, val = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return val
    return None

def set_cache(key: str, val):
    """Set cache value"""
    _cache[key] = (time.time(), val)

VERBOSE = False  # Set to False to disable terminal output
HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

def log(msg: str):
    """Log to file (tail -f ~/.claude/logs/hooks.log to watch)"""
    if VERBOSE:
        try:
            HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(HOOK_LOG, "a") as f:
                from datetime import datetime
                f.write(f"{datetime.now().strftime('%H:%M:%S')} {msg}\n")
                f.flush()
        except:
            pass
        print(f"\033[33m[Hook] {msg}\033[0m", file=sys.stderr, flush=True)

def deny(reason: str):
    """Deny tool - with user-visible message"""
    log(f"🚫 DENIED: {reason}")
    output = {
        "systemMessage": f"🚫 Blocked: {reason}",
        "hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}
    }
    print(json.dumps(output))
    sys.exit(0)

def allow(reason: str, updated_input: dict = None, tool_name: str = ""):
    """Allow tool - with optional input modification (v2.0.10+)"""
    log(f"[OK] ALLOWED: {reason}")
    output = {
        "systemMessage": f"[OK] {tool_name}: {reason}" if tool_name else f"[OK] {reason}",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": reason
        }
    }
    # Add modified input if provided (input modification feature)
    if updated_input:
        output["hookSpecificOutput"]["updatedInput"] = updated_input
        log(f"[NOTE] Modified input")
    print(json.dumps(output))
    sys.exit(0)

def sanitize_bash_command(cmd: str) -> str:
    """Sanitize bash command - remove dangerous parts while keeping intent"""
    # Remove sudo if not necessary
    if cmd.startswith("sudo ") and not any(x in cmd for x in ["apt", "systemctl", "service"]):
        cmd = cmd[5:]

    # Replace rm -rf with safer rm -ri (interactive)
    cmd = re.sub(r'\brm\s+-rf\b', 'rm -ri', cmd)

    return cmd

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {})

    # Show what tool is being checked
    log(f"Checking: {tool}")

    # Cache key for this check
    cache_key = hashlib.md5(f"{tool}:{json.dumps(inp, sort_keys=True)}".encode()).hexdigest()[:12]
    cached = get_cache(cache_key)
    if cached:
        print(json.dumps(cached))
        sys.exit(0)

    # === BASH SECURITY ===
    if tool == "Bash":
        cmd = inp.get("command", "")

        # Dangerous patterns - DENY
        danger = [
            (r"rm\s+(-rf|-fr)\s+[/~.]", "rm -rf unsafe"),
            (r"rm\s+(-rf|-fr)\s+\*", "rm -rf wildcard"),
            (r"mkfs\.", "format disk"),
            (r"dd\s+if=.+of=/dev/", "dd to device"),
            (r">\s*/dev/sd", "write device"),
            (r"git\s+push\s+.*(-f|--force).*\s*(main|master)", "force push main"),
            (r"DROP\s+(DATABASE|TABLE)", "SQL DROP"),
            (r"chmod\s+(-R\s+)?777\s+/", "chmod 777 root"),
        ]
        for pat, desc in danger:
            if re.search(pat, cmd, re.I):
                deny(f"Blocked: {desc}")

        # Safe patterns - ALLOW
        safe = [
            r"^(ls|pwd|cat|head|tail|wc|which|whoami|date|uname|file|stat)\b",
            r"^git\s+(status|log|diff|branch|show|remote|fetch|stash\s+list)\b",
            r"^(npm|yarn|pnpm)\s+(list|ls|outdated|audit|run\s+(build|test|lint))\b",
            r"^(node|python[3]?|ruby|go|cargo|uv)\s+--version",
            r"^(pip|uv|cargo)\s+(list|show|freeze)\b",
            r"^mkdir\s+-p?\s+", r"^touch\s+", r"^cp\s+", r"^mv\s+",
        ]
        for pat in safe:
            if re.match(pat, cmd.strip()):
                short_cmd = cmd.strip()[:40] + "..." if len(cmd.strip()) > 40 else cmd.strip()
                result = {
                    "systemMessage": f"[OK] Bash: {short_cmd}",
                    "hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow", "permissionDecisionReason": "safe"}
                }
                set_cache(cache_key, result)
                print(json.dumps(result))
                sys.exit(0)

    # === FILE SECURITY ===
    if tool in ["Read", "Edit", "Write"]:
        path = inp.get("file_path", "")

        # Sensitive files - DENY
        sensitive = [r"\.env($|\.)", r"\.(pem|key)$", r"id_(rsa|ed25519)", r"credentials\.json", r"secrets?\.", r"\.aws/credentials", r"\.ssh/", r"\.gnupg/"]
        for pat in sensitive:
            if re.search(pat, path, re.I):
                deny(f"Blocked: sensitive file")

    # === MD CLUTTER PREVENTION ===
    if tool == "Write" and inp.get("file_path", "").endswith(".md"):
        path = inp.get("file_path", "")
        name = os.path.basename(path)
        allowed = ["CLAUDE.md", "README.md", "CHANGELOG.md", "LICENSE.md", "CONTRIBUTING.md"]
        if not os.path.exists(path) and name not in allowed:
            deny(f"Blocked: new .md file '{name}'. Use: {', '.join(allowed)}")

    # === AUTO-ALLOW READS ===
    if tool == "Read":
        path = inp.get("file_path", "")
        auto = [r"\.(md|txt|json|ya?ml|toml|ini|conf|cfg)$", r"README|CHANGELOG|LICENSE", r"package\.json$", r"\.claude/"]
        for pat in auto:
            if re.search(pat, path, re.I):
                allow("auto-read", tool_name="Read")

    # === AUTO-ALLOW SEARCH ===
    if tool in ["Glob", "Grep"]:
        allow("search", tool_name=tool)

    # === SKILL USAGE: Show when a skill is being invoked ===
    if tool == "Skill":
        skill_name = inp.get("skill", "")
        if skill_name:
            msg = f"[FAST] Using skill: {skill_name}"
            print(f"\033[32m{msg}\033[0m", file=sys.stderr)
            print(json.dumps({"systemMessage": msg}))

    # === TASK TOOL: Show when launching agents ===
    if tool == "Task":
        agent_type = inp.get("subagent_type", "general")
        desc = inp.get("description", "")[:30]
        msg = f"[BOT] Launching agent: {agent_type} - {desc}"
        print(f"\033[34m{msg}\033[0m", file=sys.stderr)
        print(json.dumps({"systemMessage": msg}))

    # === MULTI-MODEL: Show when using multi:chat ===
    if tool == "Bash":
        cmd = inp.get("command", "")
        if "multi:chat" in cmd or "multi:compare" in cmd:
            model = cmd.split()[1] if len(cmd.split()) > 1 else "unknown"
            msg = f"🔀 Multi-model: Routing to {model}"
            print(f"\033[36m{msg}\033[0m", file=sys.stderr)
            print(json.dumps({"systemMessage": msg}))
            sys.exit(0)

    # === DEFAULT: Show tool being checked (passthrough) ===
    # Brief indicator that hook ran
    short_info = ""
    if tool == "Bash":
        cmd = inp.get("command", "")[:30]
        short_info = f": {cmd}..." if cmd else ""
    elif tool in ["Read", "Edit", "Write"]:
        path = inp.get("file_path", "")
        short_info = f": {os.path.basename(path)}" if path else ""

    print(json.dumps({"systemMessage": f"[SEARCH] {tool}{short_info}"}))
    sys.exit(0)

if __name__ == "__main__":
    main()
