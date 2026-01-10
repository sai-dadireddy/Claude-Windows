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
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

VERBOSE = False
LOG_DIR = Path.home() / ".claude" / "logs"

def log(msg: str):
    if VERBOSE:
        print(f"[Stop] {msg}", file=sys.stderr)

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
    session_id = data.get("session_id", "")[:8]
    cwd = data.get("cwd", os.getcwd())

    log(f"Response complete at {stop_ts}")

    # Log completion
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_DIR / "events.jsonl", "a") as f:
            f.write(json.dumps({
                "e": "stop",
                "t": stop_ts,
                "session": session_id,
                "cwd": cwd
            }) + "\n")
    except:
        pass

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

    output = {"systemMessage": system_msg}
    print(json.dumps(output))

    # Emit terminal bell - propagates through SSH/SSM
    sys.stderr.write("\a")
    sys.stderr.flush()

    sys.exit(0)

if __name__ == "__main__":
    main()
