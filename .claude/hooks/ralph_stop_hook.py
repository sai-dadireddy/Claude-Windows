#!/usr/bin/env python3
"""
Ralph Wiggum Stop Hook Integration

This hook intercepts Claude's stop event and checks if a ralph loop is active.
If active and not complete, it blocks the stop and continues the loop.

Based on official Anthropic ralph-wiggum plugin pattern.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

def get_state_file(cwd: str) -> Path:
    """Get the ralph loop state file path"""
    return Path(cwd) / ".claude" / "ralph-loop.local.md"

def parse_state(state_file: Path) -> dict:
    """Parse the ralph state file"""
    if not state_file.exists():
        return {"active": False}

    content = state_file.read_text()

    # Parse frontmatter
    if not content.startswith("---"):
        return {"active": False}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"active": False}

    frontmatter = parts[1].strip()
    body = parts[2] if len(parts) > 2 else ""

    status = {"active": False, "body": body}

    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"')

            if key == "active":
                status["active"] = value.lower() == "true"
            elif key == "iteration":
                try:
                    status["iteration"] = int(value)
                except:
                    status["iteration"] = 1
            elif key == "max_iterations":
                try:
                    status["max_iterations"] = int(value)
                except:
                    status["max_iterations"] = 50
            elif key == "completion_promise":
                status["completion_promise"] = value

    return status

def check_completion_promise(transcript: str, promise: str) -> bool:
    """Check if the completion promise appears in the transcript"""
    if not promise:
        return False

    # Check for explicit promise tag or just the promise text
    if f"<promise>{promise}</promise>" in transcript:
        return True
    if f"COMPLETION: {promise}" in transcript:
        return True
    if promise in transcript:
        # Only count if it's in the last assistant message
        return True

    return False

def increment_state(state_file: Path, status: dict) -> dict:
    """Increment the iteration counter in state file"""
    content = state_file.read_text()

    new_iteration = status.get("iteration", 0) + 1
    max_iter = status.get("max_iterations", 50)

    if new_iteration > max_iter:
        # Max iterations reached, deactivate
        content = content.replace("active: true", "active: false")
        content += f"\n- Loop stopped: max iterations ({max_iter}) reached at {datetime.now().strftime('%H:%M:%S')}\n"
        state_file.write_text(content)
        return {"stopped": True, "reason": "max_iterations"}

    # Update iteration
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("iteration:"):
            lines[i] = f"iteration: {new_iteration}"
            break

    # Add progress entry
    lines.append(f"- Iteration {new_iteration} started at {datetime.now().strftime('%H:%M:%S')}")

    state_file.write_text("\n".join(lines))

    return {
        "iteration": new_iteration,
        "max_iterations": max_iter,
        "continued": True
    }

def get_original_prompt(status: dict) -> str:
    """Extract the original prompt from state body"""
    body = status.get("body", "")

    # Remove progress log section
    if "## Progress Log" in body:
        body = body.split("## Progress Log")[0]

    # Remove header if present
    if "# Ralph Loop Task" in body:
        body = body.replace("# Ralph Loop Task", "").strip()

    return body.strip()

def main():
    try:
        data = json.load(sys.stdin)
    except:
        # No input, just exit normally
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    transcript = data.get("transcript_summary", "")
    session_id = data.get("session_id", "")[:8]

    state_file = get_state_file(cwd)
    status = parse_state(state_file)

    # If no active ralph loop, let the normal stop proceed
    if not status.get("active"):
        sys.exit(0)

    # Check if completion promise was met
    promise = status.get("completion_promise", "DONE")
    if check_completion_promise(transcript, promise):
        # Promise met, deactivate loop and allow stop
        content = state_file.read_text()
        content = content.replace("active: true", "active: false")
        content += f"\n- Loop completed successfully at {datetime.now().strftime('%H:%M:%S')} (promise: {promise})\n"
        state_file.write_text(content)

        output = {
            "systemMessage": f"[RALPH] Loop complete! Promise '{promise}' fulfilled after {status.get('iteration', 1)} iterations."
        }
        print(json.dumps(output))
        sys.exit(0)

    # Promise not met, continue the loop
    result = increment_state(state_file, status)

    if result.get("stopped"):
        # Max iterations reached
        output = {
            "systemMessage": f"[RALPH] Loop stopped: {result.get('reason')}. Review progress in .claude/ralph-loop.local.md"
        }
        print(json.dumps(output))
        sys.exit(0)

    # Continue the loop - block the stop and reinject prompt
    original_prompt = get_original_prompt(status)
    iteration = result.get("iteration", 2)
    max_iter = result.get("max_iterations", 50)

    continue_message = f"""[RALPH LOOP - Iteration {iteration}/{max_iter}]

The previous iteration did not complete all tasks. Continue working.

Original task:
{original_prompt}

Check your progress:
- Review git log for what's been committed
- Check file contents for what's been implemented
- Look at .claude/ralph-loop.local.md for progress log

Continue until ALL tasks are verified complete, then output: {promise}"""

    output = {
        "decision": "block",
        "reason": f"Ralph loop iteration {iteration}/{max_iter} - continuing work",
        "systemMessage": continue_message
    }

    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
