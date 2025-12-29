#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
TypeCheck Changed Files (PostToolUse) - Run type checking on modified files

Features:
- Runs tsc on TypeScript files after Write/Edit
- Runs mypy/pyright on Python files
- Fast incremental checking
- Reports errors immediately
"""

import json
import sys
import subprocess
import os
from pathlib import Path

VERBOSE = False

def log(msg: str):
    if VERBOSE:
        print(f"[TypeCheck] {msg}", file=sys.stderr)

def run_cmd(cmd: list, cwd: str, timeout: int = 30) -> tuple:
    """Run command and return (success, output)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except FileNotFoundError:
        return None, "Not found"
    except Exception as e:
        return False, str(e)

def check_typescript_file(file_path: str, cwd: str) -> dict:
    """Type check a single TypeScript file"""
    # Check if tsconfig exists
    tsconfig = Path(cwd) / "tsconfig.json"
    if not tsconfig.exists():
        return {"skip": True, "reason": "No tsconfig.json"}

    log(f"Type checking {os.path.basename(file_path)}...")

    # Run tsc on the specific file
    success, output = run_cmd(
        ["npx", "tsc", "--noEmit", file_path],
        cwd,
        timeout=60
    )

    if success is None:
        return {"skip": True, "reason": "tsc not found"}

    if success:
        return {"pass": True}
    else:
        error_count = output.count("error TS")
        errors = []
        for line in output.split("\n"):
            if "error TS" in line:
                errors.append(line.strip()[:100])
        return {
            "pass": False,
            "errors": error_count,
            "details": errors[:3]
        }

def check_python_file(file_path: str, cwd: str) -> dict:
    """Type check a single Python file with mypy or pyright"""
    log(f"Type checking {os.path.basename(file_path)}...")

    # Try pyright first (faster)
    success, output = run_cmd(
        ["pyright", file_path],
        cwd,
        timeout=30
    )

    if success is None:
        # Try mypy
        success, output = run_cmd(
            ["mypy", "--ignore-missing-imports", file_path],
            cwd,
            timeout=30
        )

    if success is None:
        return {"skip": True, "reason": "No type checker found"}

    if success:
        return {"pass": True}
    else:
        error_count = output.count("error:")
        return {
            "pass": False,
            "errors": error_count,
            "sample": output[:200]
        }

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    cwd = data.get("cwd", os.getcwd())

    # Only run for Write/Edit operations
    if tool not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    ext = os.path.splitext(file_path)[1].lower()
    result = None

    # TypeScript/JavaScript
    if ext in [".ts", ".tsx"]:
        result = check_typescript_file(file_path, cwd)

    # Python
    elif ext == ".py":
        result = check_python_file(file_path, cwd)

    else:
        log(f"[END]️ Skipping {ext} file")
        sys.exit(0)

    # Handle result
    if result:
        if result.get("skip"):
            log(f"[END]️ Skipped: {result.get('reason', 'N/A')}")
        elif result.get("pass"):
            log(f"[OK] Type check passed")
        else:
            errors = result.get("errors", 0)
            details = result.get("details", [])
            log(f"[FAIL] Type errors: {errors}")

            # Show first few errors
            msg_parts = [f"Type errors ({errors})"]
            if details:
                msg_parts.extend(details[:2])

            output = {
                "systemMessage": f"[WARN] {os.path.basename(file_path)}: {errors} type error(s)"
            }
            print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
