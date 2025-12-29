#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Beads Integration Hook (PostToolUse) - Auto-create and update issues

Features:
- Auto-creates issues when bugs/errors are encountered
- Links discovered issues to parent tasks
- Updates issue status based on work progress
- Syncs with beads database automatically

Works alongside beads plugin to provide seamless issue tracking.
"""

import json
import sys
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

VERBOSE = True
LOG_DIR = Path.home() / ".claude" / "logs"
BD_PATH = Path.home() / ".local" / "bin" / "bd"

def log(msg: str):
    if VERBOSE:
        print(f"[BeadsIntegration] {msg}", file=sys.stderr)

def bd_available() -> bool:
    """Check if bd CLI is available."""
    return BD_PATH.exists() or subprocess.run(
        ["which", "bd"], capture_output=True
    ).returncode == 0

def beads_initialized(cwd: str) -> bool:
    """Check if beads is initialized in the project."""
    return (Path(cwd) / ".beads").exists()

def run_bd(args: list, cwd: str) -> tuple:
    """Run bd command and return (success, output)."""
    try:
        env = os.environ.copy()
        env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"

        result = subprocess.run(
            ["bd"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def create_issue(title: str, issue_type: str, priority: int, cwd: str, parent_id: str = None) -> str:
    """Create a new beads issue and return its ID."""
    args = ["create", title, "-t", issue_type, "-p", str(priority), "--json"]

    success, output = run_bd(args, cwd)

    if success and output:
        try:
            data = json.loads(output)
            issue_id = data.get("id", "")

            # Link to parent if provided
            if parent_id and issue_id:
                run_bd(["dep", "add", issue_id, parent_id, "--discovered"], cwd)

            return issue_id
        except:
            pass

    return ""

def get_current_issue(cwd: str) -> str:
    """Get the current in-progress issue ID."""
    success, output = run_bd(["list", "--status", "in_progress", "--json"], cwd)

    if success and output:
        try:
            issues = json.loads(output)
            if issues and len(issues) > 0:
                return issues[0].get("id", "")
        except:
            pass

    return ""

def update_issue_status(issue_id: str, status: str, cwd: str):
    """Update issue status."""
    run_bd(["update", issue_id, "--status", status], cwd)

def close_issue(issue_id: str, reason: str, cwd: str):
    """Close an issue with reason."""
    run_bd(["close", issue_id, "--reason", reason], cwd)

def extract_error_info(output: str) -> dict:
    """Extract error information from tool output."""
    error_patterns = [
        (r"(Error|ERROR|error):\s*(.+)", "error"),
        (r"(Exception|exception):\s*(.+)", "exception"),
        (r"(Failed|FAILED|failed):\s*(.+)", "failure"),
        (r"(TypeError|SyntaxError|ValueError|KeyError|AttributeError):\s*(.+)", "type_error"),
        (r"(ENOENT|EACCES|EPERM):\s*(.+)", "fs_error"),
    ]

    for pattern, error_type in error_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return {
                "type": error_type,
                "message": match.group(2)[:100].strip()
            }

    return {}

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_output = data.get("tool_response", {})
    cwd = data.get("cwd", os.getcwd())

    # Check if beads is available and initialized
    if not bd_available():
        sys.exit(0)

    if not beads_initialized(cwd):
        sys.exit(0)

    log(f"Checking: {tool}")

    # Get output as string
    output_str = ""
    if isinstance(tool_output, dict):
        output_str = json.dumps(tool_output)
    elif isinstance(tool_output, str):
        output_str = tool_output

    # === BASH ERRORS: Auto-create bug issues ===
    if tool == "Bash":
        error_info = extract_error_info(output_str)

        if error_info:
            command = tool_input.get("command", "")[:50]
            title = f"Bug: {error_info['message'][:60]}"

            # Get current working issue as parent
            parent_id = get_current_issue(cwd)

            issue_id = create_issue(title, "bug", 2, cwd, parent_id)

            if issue_id:
                log(f"🐛 Created bug issue: {issue_id}")

                # Show user in console
                output = {"systemMessage": f"🐛 Beads: Auto-created bug {issue_id}"}
                print(json.dumps(output))

                # Log to file
                LOG_DIR.mkdir(parents=True, exist_ok=True)
                try:
                    with open(LOG_DIR / "beads_auto_issues.jsonl", "a") as f:
                        f.write(json.dumps({
                            "timestamp": datetime.now().isoformat(),
                            "issue_id": issue_id,
                            "type": "bug",
                            "trigger": "bash_error",
                            "error": error_info
                        }) + "\n")
                except:
                    pass

    # === TEST FAILURES: Create test fix issues ===
    if tool == "Bash":
        command = tool_input.get("command", "")

        # Detect test runs
        test_patterns = ["pytest", "jest", "npm test", "cargo test", "go test"]
        is_test_run = any(p in command for p in test_patterns)

        if is_test_run:
            # Check for failures
            failure_indicators = ["FAILED", "FAIL ", "failed", "Error:", "error:"]
            has_failures = any(ind in output_str for ind in failure_indicators)

            if has_failures:
                # Extract test name if possible
                test_match = re.search(r"(test_\w+|it\(['\"](.+?)['\"])", output_str)
                test_name = test_match.group(1) if test_match else "tests"

                title = f"Fix failing {test_name}"
                parent_id = get_current_issue(cwd)

                issue_id = create_issue(title, "bug", 1, cwd, parent_id)

                if issue_id:
                    log(f"🧪 Created test fix issue: {issue_id}")
                    output = {"systemMessage": f"🧪 Beads: Test failure → {issue_id}"}
                    print(json.dumps(output))

    # === FILE OPERATIONS: Track significant work ===
    if tool in ["Write", "Edit"]:
        file_path = tool_input.get("file_path", "")
        filename = os.path.basename(file_path)

        # Track new file creation as potential subtask
        if tool == "Write" and not os.path.exists(file_path):
            # Don't create issues for every file, just log
            log(f"📄 New file: {filename}")

    sys.exit(0)

if __name__ == "__main__":
    main()
