#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Lint Changed Files (PostToolUse) - Run linters on modified files

Features:
- Runs ESLint on JS/TS files
- Runs Ruff on Python files
- Runs rustfmt --check on Rust files
- Fast single-file linting
- Reports issues immediately
"""

import json
import sys
import subprocess
import os
from pathlib import Path

VERBOSE = True

def log(msg: str):
    if VERBOSE:
        print(f"[Lint] {msg}", file=sys.stderr)

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

def lint_javascript(file_path: str, cwd: str) -> dict:
    """Lint JavaScript/TypeScript file with ESLint"""
    log(f"Linting {os.path.basename(file_path)} with ESLint...")

    success, output = run_cmd(
        ["npx", "eslint", "--format", "compact", file_path],
        cwd,
        timeout=30
    )

    if success is None:
        return {"skip": True, "reason": "ESLint not found"}

    if success:
        return {"pass": True}
    else:
        # Count errors and warnings
        error_count = output.count(" Error ")
        warning_count = output.count(" Warning ")
        return {
            "pass": False,
            "errors": error_count,
            "warnings": warning_count,
            "sample": output[:300]
        }

def lint_python(file_path: str, cwd: str) -> dict:
    """Lint Python file with Ruff"""
    log(f"Linting {os.path.basename(file_path)} with Ruff...")

    success, output = run_cmd(
        ["ruff", "check", file_path],
        cwd,
        timeout=30
    )

    if success is None:
        # Try with uvx
        success, output = run_cmd(
            ["uvx", "ruff", "check", file_path],
            cwd,
            timeout=30
        )
        if success is None:
            return {"skip": True, "reason": "Ruff not found"}

    if success:
        return {"pass": True}
    else:
        # Count issues
        issues = [l for l in output.split("\n") if l.strip() and ":" in l and not l.startswith("Found")]
        return {
            "pass": False,
            "errors": len(issues),
            "sample": "\n".join(issues[:3])
        }

def lint_rust(file_path: str, cwd: str) -> dict:
    """Check Rust file formatting"""
    log(f"Checking {os.path.basename(file_path)} with rustfmt...")

    success, output = run_cmd(
        ["rustfmt", "--check", file_path],
        cwd,
        timeout=30
    )

    if success is None:
        return {"skip": True, "reason": "rustfmt not found"}

    if success:
        return {"pass": True}
    else:
        return {
            "pass": False,
            "errors": 1,
            "sample": "File needs formatting"
        }

def lint_go(file_path: str, cwd: str) -> dict:
    """Lint Go file with golint or staticcheck"""
    log(f"Linting {os.path.basename(file_path)}...")

    # Try staticcheck first
    success, output = run_cmd(
        ["staticcheck", file_path],
        cwd,
        timeout=30
    )

    if success is None:
        # Try go vet
        success, output = run_cmd(
            ["go", "vet", file_path],
            cwd,
            timeout=30
        )
        if success is None:
            return {"skip": True, "reason": "No Go linter found"}

    if success:
        return {"pass": True}
    else:
        issues = [l for l in output.split("\n") if l.strip()]
        return {
            "pass": False,
            "errors": len(issues),
            "sample": "\n".join(issues[:3])
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
    filename = os.path.basename(file_path)
    result = None

    # JavaScript/TypeScript
    if ext in [".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"]:
        result = lint_javascript(file_path, cwd)

    # Python
    elif ext == ".py":
        result = lint_python(file_path, cwd)

    # Rust
    elif ext == ".rs":
        result = lint_rust(file_path, cwd)

    # Go
    elif ext == ".go":
        result = lint_go(file_path, cwd)

    else:
        log(f"⏭️ No linter for {ext}")
        sys.exit(0)

    # Handle result
    if result:
        if result.get("skip"):
            log(f"⏭️ Skipped: {result.get('reason', 'N/A')}")
        elif result.get("pass"):
            log(f"✅ Lint passed")
        else:
            errors = result.get("errors", 0)
            warnings = result.get("warnings", 0)
            log(f"❌ Lint issues: {errors} errors, {warnings} warnings")

            issue_text = f"{errors} error(s)"
            if warnings:
                issue_text += f", {warnings} warning(s)"

            output = {
                "systemMessage": f"⚠️ {filename}: {issue_text}"
            }
            print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
