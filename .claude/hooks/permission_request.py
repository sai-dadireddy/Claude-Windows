#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
PermissionRequest Hook - Auto-handle permission dialogs

Features:
- Auto-approve known safe operations (reduces interruptions)
- Auto-deny dangerous operations
- Let user decide for ambiguous cases
"""

import json
import sys
import re
import os

VERBOSE = False

def log(msg: str):
    if VERBOSE:
        print(f"[PermissionRequest] {msg}", file=sys.stderr)

def allow(reason: str = "auto-approved"):
    """Auto-approve the permission request"""
    log(f"[OK] ALLOWED: {reason}")
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "allow"}
        }
    }
    print(json.dumps(output))
    sys.exit(0)

def deny(reason: str, interrupt: bool = False):
    """Auto-deny the permission request"""
    log(f"🚫 DENIED: {reason}")
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {
                "behavior": "deny",
                "message": reason,
                "interrupt": interrupt
            }
        }
    }
    print(json.dumps(output))
    sys.exit(0)

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    log(f"Checking permission for: {tool}")

    # === AUTO-APPROVE: Safe read-only tools ===
    safe_tools = ["Read", "Glob", "Grep", "WebSearch", "WebFetch"]
    if tool in safe_tools:
        allow(f"{tool} is read-only")

    # === AUTO-APPROVE: Task tool (subagents) ===
    if tool == "Task":
        allow("Task tool for subagents")

    # === AUTO-APPROVE: TodoWrite ===
    if tool == "TodoWrite":
        allow("Todo management")

    # === BASH: Selective approval ===
    if tool == "Bash":
        cmd = tool_input.get("command", "")

        # Safe bash commands - auto-approve
        safe_patterns = [
            r"^(ls|pwd|cat|head|tail|wc|which|whoami|date|uname|file|stat)\b",
            r"^git\s+(status|log|diff|branch|show|remote|fetch|stash\s+list)\b",
            r"^(npm|yarn|pnpm)\s+(list|ls|outdated|audit|run\s+(build|test|lint|dev|start))\b",
            r"^(node|python[3]?|ruby|go|cargo|uv)\s+--version",
            r"^(pip|uv|cargo)\s+(list|show|freeze)\b",
            r"^mkdir\s+", r"^touch\s+", r"^echo\s+",
            r"^(pytest|jest|npm\s+test|cargo\s+test)\b",
            r"^(ruff|black|prettier|eslint)\s+",
        ]
        for pat in safe_patterns:
            if re.match(pat, cmd.strip(), re.I):
                allow(f"Safe bash: {cmd[:30]}")

        # Dangerous bash commands - auto-deny
        danger_patterns = [
            (r"rm\s+(-rf|-fr)\s+[/~]", "rm -rf on root/home"),
            (r"rm\s+(-rf|-fr)\s+\*", "rm -rf wildcard"),
            (r"mkfs\.", "format disk"),
            (r"dd\s+if=.+of=/dev/", "dd to device"),
            (r">\s*/dev/sd", "write to device"),
            (r"chmod\s+(-R\s+)?777\s+/", "chmod 777 root"),
            (r":(){ :|:& };:", "fork bomb"),
        ]
        for pat, desc in danger_patterns:
            if re.search(pat, cmd, re.I):
                deny(f"Dangerous: {desc}", interrupt=True)

    # === FILE OPERATIONS: Check paths ===
    if tool in ["Write", "Edit", "MultiEdit"]:
        file_path = tool_input.get("file_path", "")
        # Normalize path for cross-platform matching (Windows backslash -> forward slash)
        file_path_normalized = file_path.replace("\\", "/")

        # Auto-deny sensitive files
        sensitive_patterns = [
            r"\.env($|\.)",
            r"\.(pem|key)$",
            r"id_(rsa|ed25519)",
            r"credentials\.json",
            r"secrets?\.",
            r"\.aws/credentials",
            r"\.ssh/",
            r"\.gnupg/",
        ]
        for pat in sensitive_patterns:
            if re.search(pat, file_path_normalized, re.I):
                deny(f"Sensitive file: {os.path.basename(file_path)}")

        # Auto-approve common development files
        safe_extensions = [".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".rb",
                          ".java", ".c", ".cpp", ".h", ".css", ".scss", ".html",
                          ".json", ".yaml", ".yml", ".toml", ".md", ".txt", ".sh"]
        ext = os.path.splitext(file_path)[1].lower()
        if ext in safe_extensions:
            # Check if in safe directories (use forward slashes for cross-platform)
            safe_dirs = ["src/", "lib/", "app/", "components/", "pages/",
                        "hooks/", "utils/", "helpers/", "tests/", "test/",
                        "__tests__/", "scripts/", ".claude/", "templates/",
                        "commands/", "agents/", "skills/", "memory/"]
            for safe_dir in safe_dirs:
                if safe_dir in file_path_normalized:
                    allow(f"Dev file in {safe_dir}")

    # === DEFAULT: Let user decide ===
    log("⏸️ Letting user decide")
    sys.exit(0)

if __name__ == "__main__":
    main()
