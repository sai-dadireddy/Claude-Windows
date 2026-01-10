#!/usr/bin/env python3
"""
Ralph Loop State Management (Based on official Anthropic implementation)

This script manages the ralph-loop state file and provides utilities for:
- Starting a ralph loop
- Checking loop status
- Incrementing iterations
- Canceling loops
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_state_file(cwd: str = None) -> Path:
    """Get the ralph loop state file path"""
    if cwd:
        return Path(cwd) / ".claude" / "ralph-loop.local.md"
    return Path.cwd() / ".claude" / "ralph-loop.local.md"

def start_loop(prompt: str, max_iterations: int = 50, completion_promise: str = "DONE", cwd: str = None):
    """Initialize a new ralph loop"""
    state_file = get_state_file(cwd)
    state_file.parent.mkdir(parents=True, exist_ok=True)

    content = f"""---
active: true
iteration: 1
max_iterations: {max_iterations}
completion_promise: "{completion_promise}"
started: "{datetime.now().isoformat()}"
---

# Ralph Loop Task

{prompt}

---

## Progress Log

- Iteration 1 started at {datetime.now().strftime("%H:%M:%S")}
"""

    state_file.write_text(content)
    print(json.dumps({
        "status": "started",
        "state_file": str(state_file),
        "max_iterations": max_iterations,
        "completion_promise": completion_promise
    }))

def check_status(cwd: str = None) -> dict:
    """Check current ralph loop status"""
    state_file = get_state_file(cwd)

    if not state_file.exists():
        return {"active": False, "message": "No active ralph loop"}

    content = state_file.read_text()

    # Parse frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            status = {}
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    if key == "active":
                        status["active"] = value.lower() == "true"
                    elif key == "iteration":
                        status["iteration"] = int(value)
                    elif key == "max_iterations":
                        status["max_iterations"] = int(value)
                    elif key == "completion_promise":
                        status["completion_promise"] = value
            return status

    return {"active": False, "message": "Could not parse state file"}

def increment_iteration(cwd: str = None) -> dict:
    """Increment the iteration counter"""
    state_file = get_state_file(cwd)

    if not state_file.exists():
        return {"error": "No active ralph loop"}

    content = state_file.read_text()
    status = check_status(cwd)

    if not status.get("active"):
        return {"error": "Ralph loop not active"}

    new_iteration = status.get("iteration", 0) + 1
    max_iter = status.get("max_iterations", 50)

    if new_iteration > max_iter:
        cancel_loop(cwd)
        return {"stopped": True, "reason": f"Max iterations ({max_iter}) reached"}

    # Update iteration in frontmatter
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("iteration:"):
            lines[i] = f"iteration: {new_iteration}"
            break

    # Add progress entry
    progress_line = f"- Iteration {new_iteration} started at {datetime.now().strftime('%H:%M:%S')}"
    lines.append(progress_line)

    state_file.write_text("\n".join(lines))

    return {
        "iteration": new_iteration,
        "max_iterations": max_iter,
        "remaining": max_iter - new_iteration
    }

def cancel_loop(cwd: str = None):
    """Cancel the current ralph loop"""
    state_file = get_state_file(cwd)

    if state_file.exists():
        content = state_file.read_text()
        # Mark as inactive
        content = content.replace("active: true", "active: false")
        content += f"\n- Loop cancelled at {datetime.now().strftime('%H:%M:%S')}\n"
        state_file.write_text(content)
        print(json.dumps({"status": "cancelled", "state_file": str(state_file)}))
    else:
        print(json.dumps({"status": "no_loop", "message": "No active ralph loop to cancel"}))

def get_prompt(cwd: str = None) -> str:
    """Extract the original prompt from state file"""
    state_file = get_state_file(cwd)

    if not state_file.exists():
        return ""

    content = state_file.read_text()

    # Extract content after frontmatter, before Progress Log
    if "---" in content:
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body = parts[2]
            if "## Progress Log" in body:
                body = body.split("## Progress Log")[0]
            return body.strip()

    return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: ralph_loop.py <command> [args]")
        print("Commands: start, status, increment, cancel, prompt")
        sys.exit(1)

    cmd = sys.argv[1]
    cwd = os.environ.get("CLAUDE_CWD", os.getcwd())

    if cmd == "start":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "Complete the tasks"
        max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        promise = sys.argv[4] if len(sys.argv) > 4 else "DONE"
        start_loop(prompt, max_iter, promise, cwd)

    elif cmd == "status":
        status = check_status(cwd)
        print(json.dumps(status))

    elif cmd == "increment":
        result = increment_iteration(cwd)
        print(json.dumps(result))

    elif cmd == "cancel":
        cancel_loop(cwd)

    elif cmd == "prompt":
        prompt = get_prompt(cwd)
        print(prompt)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
