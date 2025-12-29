#!/usr/bin/env python3
"""
Pilot - Autonomous Beads Task Executor

Watches for beads tasks labeled 'pilot' across all projects and
spawns Claude Code instances to complete them.

Usage:
    python pilot.py              # Run once
    python pilot.py --watch      # Continuous polling mode
    python pilot.py --list       # List all pilot tasks

Features:
- Discovers .beads/ directories across configured project roots
- Polls for tasks with 'pilot' label
- Claims and executes tasks via Claude Code
- Updates beads status on completion
"""

import subprocess
import sys
import json
import os
import time
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
BD_PATH = Path.home() / ".local" / "bin" / "bd.exe"
POLL_INTERVAL = 30  # seconds
LOG_FILE = Path.home() / ".claude" / "logs" / "pilot.log"

# Project roots to scan for .beads directories
PROJECT_ROOTS = [
    Path.home() / "OneDrive - ERPA" / "Claude" / "projects",
    Path.home() / "OneDrive - ERPA" / "Claude",
    Path.home() / "projects",
    Path(os.getcwd()),
]


def log(msg: str, level: str = "INFO"):
    """Log message to file and stderr."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {msg}"
    print(line, file=sys.stderr)
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass


def find_beads_dirs() -> list[Path]:
    """Find all .beads directories in project roots."""
    beads_dirs = []
    seen = set()

    for root in PROJECT_ROOTS:
        if not root.exists():
            continue

        # Check root itself
        beads_dir = root / ".beads"
        if beads_dir.exists() and str(beads_dir) not in seen:
            beads_dirs.append(beads_dir)
            seen.add(str(beads_dir))

        # Check immediate subdirectories (1 level deep for performance)
        try:
            for subdir in root.iterdir():
                if subdir.is_dir():
                    beads_dir = subdir / ".beads"
                    if beads_dir.exists() and str(beads_dir) not in seen:
                        beads_dirs.append(beads_dir)
                        seen.add(str(beads_dir))
        except PermissionError:
            continue

    return beads_dirs


def run_bd(beads_dir: Path, *args) -> tuple[bool, str]:
    """Run bd command with specified beads directory."""
    env = os.environ.copy()
    env["BEADS_DIR"] = str(beads_dir)

    cmd = [str(BD_PATH)] + list(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=beads_dir.parent  # Project root
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)


def get_pilot_tasks(beads_dir: Path) -> list[dict]:
    """Get all ready tasks with 'pilot' label from a beads directory."""
    success, output = run_bd(beads_dir, "list", "--json", "-l", "pilot", "-s", "open")

    if not success:
        return []

    try:
        # Parse JSON output (array format)
        data = json.loads(output.strip())
        if isinstance(data, list):
            for task in data:
                task["_beads_dir"] = str(beads_dir)
                task["_project_dir"] = str(beads_dir.parent)
            return data
        elif isinstance(data, dict):
            data["_beads_dir"] = str(beads_dir)
            data["_project_dir"] = str(beads_dir.parent)
            return [data]
        return []
    except json.JSONDecodeError:
        return []


def claim_task(beads_dir: Path, task_id: str) -> bool:
    """Mark task as in_progress."""
    success, output = run_bd(beads_dir, "update", task_id, "--status", "in_progress")
    if success:
        log(f"Claimed task {task_id}")
    else:
        log(f"Failed to claim {task_id}: {output}", "ERROR")
    return success


def complete_task(beads_dir: Path, task_id: str, reason: str) -> bool:
    """Mark task as closed."""
    success, output = run_bd(beads_dir, "close", task_id, "--reason", reason)
    if success:
        log(f"Completed task {task_id}")
    else:
        log(f"Failed to complete {task_id}: {output}", "ERROR")
    return success


def execute_task(task: dict) -> tuple[bool, str]:
    """Execute a task using Claude Code."""
    task_id = task.get("id", "unknown")
    title = task.get("title", "")
    description = task.get("description", title)
    project_dir = task.get("_project_dir", os.getcwd())

    # Build prompt for Claude
    prompt = f"""You are executing a Pilot task from Beads.

Task ID: {task_id}
Title: {title}
Description: {description}

Instructions:
1. Complete the task described above
2. Make necessary code changes
3. Run tests if applicable
4. Summarize what you did

Begin working on this task now.
"""

    log(f"Executing task {task_id}: {title}")

    # Run Claude Code with the task
    try:
        # Use --print mode for non-interactive execution
        result = subprocess.run(
            ["claude", "--print", "--dangerously-skip-permissions", prompt],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=project_dir,
            env={**os.environ, "CLAUDE_CODE_ENTRYPOINT": "pilot"}
        )

        if result.returncode == 0:
            return True, result.stdout[:500] if result.stdout else "Completed"
        else:
            return False, result.stderr[:500] if result.stderr else "Failed"
    except subprocess.TimeoutExpired:
        return False, "Task execution timed out (10 min)"
    except FileNotFoundError:
        return False, "Claude Code not found in PATH"
    except Exception as e:
        return False, str(e)


def list_all_pilot_tasks():
    """List all pilot tasks across all projects."""
    beads_dirs = find_beads_dirs()

    print(f"Scanning {len(beads_dirs)} beads directories...")
    print()

    all_tasks = []
    for beads_dir in beads_dirs:
        tasks = get_pilot_tasks(beads_dir)
        for task in tasks:
            task["_project"] = beads_dir.parent.name
            all_tasks.append(task)

    if not all_tasks:
        print("No pilot tasks found.")
        return

    print(f"Found {len(all_tasks)} pilot task(s):\n")
    for task in all_tasks:
        project = task.get("_project", "?")
        task_id = task.get("id", "?")
        title = task.get("title", "?")
        priority = task.get("priority", "?")
        print(f"  [{project}] {task_id} [P{priority}] - {title}")


def run_once() -> int:
    """Run pilot once, execute one task if available."""
    beads_dirs = find_beads_dirs()
    log(f"Found {len(beads_dirs)} beads directories")

    for beads_dir in beads_dirs:
        tasks = get_pilot_tasks(beads_dir)

        for task in tasks:
            task_id = task.get("id")
            if not task_id:
                continue

            # Claim the task
            if not claim_task(beads_dir, task_id):
                continue

            # Execute the task
            success, result = execute_task(task)

            # Complete the task
            reason = f"Pilot: {'Success' if success else 'Failed'} - {result[:100]}"
            complete_task(beads_dir, task_id, reason)

            return 0 if success else 1

    log("No pilot tasks found")
    return 0


def watch_mode():
    """Continuously poll for pilot tasks."""
    log("Pilot starting in watch mode...")
    log(f"Polling every {POLL_INTERVAL} seconds")
    log("Press Ctrl+C to stop")

    try:
        while True:
            run_once()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        log("Pilot stopped by user")


def main():
    parser = argparse.ArgumentParser(description="Pilot - Autonomous Beads Task Executor")
    parser.add_argument("--watch", "-w", action="store_true", help="Continuous polling mode")
    parser.add_argument("--list", "-l", action="store_true", help="List all pilot tasks")
    parser.add_argument("--interval", "-i", type=int, default=30, help="Poll interval in seconds")

    args = parser.parse_args()

    global POLL_INTERVAL
    POLL_INTERVAL = args.interval

    if not BD_PATH.exists():
        print(f"Error: bd not found at {BD_PATH}", file=sys.stderr)
        print("Install beads first: https://github.com/anthropics/beads", file=sys.stderr)
        sys.exit(1)

    if args.list:
        list_all_pilot_tasks()
    elif args.watch:
        watch_mode()
    else:
        sys.exit(run_once())


if __name__ == "__main__":
    main()
