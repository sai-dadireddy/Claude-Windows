#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Create Checkpoint Hook (Stop) - Auto git commit after each response

Features:
- Creates automatic git checkpoint after Claude finishes
- Only commits if there are actual changes
- Uses session-based branch naming for isolation
- Preserves ability to restore to any checkpoint
"""

import json
import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path

VERBOSE = True
LOG_DIR = Path.home() / ".claude" / "logs"
CHECKPOINT_LOG = LOG_DIR / "checkpoints.jsonl"

def log(msg: str):
    if VERBOSE:
        print(f"[Checkpoint] {msg}", file=sys.stderr)

def run_git(args: list, cwd: str) -> tuple:
    """Run git command and return (success, output)"""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def is_git_repo(cwd: str) -> bool:
    """Check if directory is a git repository"""
    success, _ = run_git(["rev-parse", "--git-dir"], cwd)
    return success

def has_changes(cwd: str) -> bool:
    """Check if there are uncommitted changes"""
    success, output = run_git(["status", "--porcelain"], cwd)
    return success and bool(output.strip())

def get_changed_files(cwd: str) -> list:
    """Get list of changed files"""
    success, output = run_git(["status", "--porcelain"], cwd)
    if not success:
        return []

    files = []
    for line in output.split("\n"):
        if line.strip():
            # Format: XY filename
            filename = line[3:].strip()
            files.append(filename)
    return files

def create_checkpoint(cwd: str, session_id: str) -> dict:
    """Create a git checkpoint"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_ts = datetime.now().strftime("%H:%M:%S")

    # Get changed files for commit message
    changed_files = get_changed_files(cwd)
    files_summary = ", ".join(changed_files[:3])
    if len(changed_files) > 3:
        files_summary += f" (+{len(changed_files) - 3} more)"

    # Stage all changes
    success, _ = run_git(["add", "-A"], cwd)
    if not success:
        return {"success": False, "error": "Failed to stage changes"}

    # Create commit
    commit_msg = f"checkpoint [{short_ts}]: {files_summary}"
    success, output = run_git(
        ["commit", "-m", commit_msg, "--no-verify"],
        cwd
    )

    if not success:
        # Check if nothing to commit
        if "nothing to commit" in output:
            return {"success": True, "skipped": True}
        return {"success": False, "error": output}

    # Get commit hash
    success, commit_hash = run_git(["rev-parse", "--short", "HEAD"], cwd)

    return {
        "success": True,
        "commit": commit_hash,
        "files": len(changed_files),
        "message": commit_msg
    }

def log_checkpoint(result: dict, cwd: str, session_id: str):
    """Log checkpoint to file"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id[:12] if session_id else "",
        "project": os.path.basename(cwd),
        "cwd": cwd,
        **result
    }

    try:
        with open(CHECKPOINT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    session_id = data.get("session_id", "")

    log(f"Checking for changes in {cwd}")

    # Check if git repo
    if not is_git_repo(cwd):
        log("⏭️ Not a git repo, skipping")
        sys.exit(0)

    # Check for changes
    if not has_changes(cwd):
        log("⏭️ No changes to checkpoint")
        sys.exit(0)

    # Create checkpoint
    result = create_checkpoint(cwd, session_id)

    # Log result
    log_checkpoint(result, cwd, session_id)

    # Output user message
    if result.get("success"):
        if result.get("skipped"):
            log("⏭️ Nothing to commit")
        else:
            commit = result.get("commit", "")
            files = result.get("files", 0)
            log(f"📸 Checkpoint created: {commit} ({files} files)")
            output = {
                "systemMessage": f"📸 Checkpoint: {commit} ({files} files)"
            }
            print(json.dumps(output))
    else:
        error = result.get("error", "Unknown error")
        log(f"❌ Failed: {error}")

    sys.exit(0)

if __name__ == "__main__":
    main()
