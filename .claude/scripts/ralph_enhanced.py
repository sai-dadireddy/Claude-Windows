#!/usr/bin/env python3
"""
Ralph Enhanced - Autonomous loop with negative memory
Manages state, negative memory, and loop control
Integrates with CallMe for phone notifications
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# CallMe integration (optional)
try:
    from callme_integration import notify_completion, notify_blocker, is_configured as callme_configured
    CALLME_AVAILABLE = True
except ImportError:
    CALLME_AVAILABLE = False
    def notify_completion(*args, **kwargs): return False
    def notify_blocker(*args, **kwargs): return False
    def callme_configured(): return False

RALPH_DIR = ".ralph"
STATE_FILE = f"{RALPH_DIR}/state.json"
NEG_MEM_FILE = f"{RALPH_DIR}/negative-memory.json"
PLAN_FILE = f"{RALPH_DIR}/plan.md"
LOG_FILE = f"{RALPH_DIR}/log.md"
SCREENSHOTS_DIR = f"{RALPH_DIR}/screenshots"
VERIFIED_PREFIX = "verified_"

def ensure_ralph_dir():
    """Create .ralph directory if it doesn't exist"""
    Path(RALPH_DIR).mkdir(exist_ok=True)
    Path(SCREENSHOTS_DIR).mkdir(exist_ok=True)

# =============================================================================
# SCREENSHOT VERIFICATION PROTOCOL
# Based on TDD + Ralph workflow: https://youtube.com/watch?v=...
# Prevents premature promise output by requiring visual verification
# =============================================================================

def verify_screenshots(screenshot_dir: str = None) -> dict:
    """
    Check screenshot verification status.
    Screenshots must be renamed with 'verified_' prefix after review.

    Returns dict with:
    - verified: count of verified screenshots
    - unverified: count of unverified screenshots
    - unverified_files: list of files needing review
    - can_complete: True if all verified
    """
    dir_path = Path(screenshot_dir) if screenshot_dir else Path(SCREENSHOTS_DIR)

    if not dir_path.exists():
        return {"verified": 0, "unverified": 0, "unverified_files": [], "can_complete": True, "message": "No screenshots directory"}

    screenshots = list(dir_path.glob("*.png")) + list(dir_path.glob("*.jpg")) + list(dir_path.glob("*.jpeg"))

    verified = []
    unverified = []

    for img in screenshots:
        if img.name.startswith(VERIFIED_PREFIX):
            verified.append(img.name)
        else:
            unverified.append(img.name)

    return {
        "verified": len(verified),
        "unverified": len(unverified),
        "unverified_files": unverified,
        "verified_files": verified,
        "can_complete": len(unverified) == 0,
        "total": len(screenshots)
    }

def mark_screenshot_verified(filepath: str) -> bool:
    """
    Mark a screenshot as verified by adding 'verified_' prefix.
    Call this AFTER visually reviewing the screenshot.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"[RALPH] Screenshot not found: {filepath}")
        return False

    if path.name.startswith(VERIFIED_PREFIX):
        print(f"[RALPH] Already verified: {path.name}")
        return True

    new_name = path.parent / f"{VERIFIED_PREFIX}{path.name}"
    path.rename(new_name)
    print(f"[RALPH] Marked verified: {path.name} -> {new_name.name}")
    return True

def mark_all_screenshots_verified(screenshot_dir: str = None) -> int:
    """Mark all screenshots in directory as verified. Returns count marked."""
    dir_path = Path(screenshot_dir) if screenshot_dir else Path(SCREENSHOTS_DIR)

    if not dir_path.exists():
        return 0

    count = 0
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for img in dir_path.glob(ext):
            if not img.name.startswith(VERIFIED_PREFIX):
                new_name = img.parent / f"{VERIFIED_PREFIX}{img.name}"
                img.rename(new_name)
                count += 1

    print(f"[RALPH] Marked {count} screenshots as verified")
    return count

def reset_screenshot_verification(screenshot_dir: str = None) -> int:
    """Remove verified_ prefix from all screenshots. Returns count reset."""
    dir_path = Path(screenshot_dir) if screenshot_dir else Path(SCREENSHOTS_DIR)

    if not dir_path.exists():
        return 0

    count = 0
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        for img in dir_path.glob(ext):
            if img.name.startswith(VERIFIED_PREFIX):
                new_name = img.parent / img.name[len(VERIFIED_PREFIX):]
                img.rename(new_name)
                count += 1

    print(f"[RALPH] Reset {count} screenshots")
    return count

def can_output_promise(min_iterations: int = 2) -> dict:
    """
    Check if it's safe to output the completion promise.

    Rules (from TDD + Ralph workflow):
    1. Must have completed at least min_iterations loops
    2. All screenshots must be verified
    3. All tasks must be complete

    Returns dict with can_complete and reasons.
    """
    state = get_state()
    if not state:
        return {"can_complete": False, "reason": "No active loop"}

    reasons = []
    can_complete = True

    # Check minimum iterations
    min_iter = state.get("min_iterations", min_iterations)
    if state["iteration"] < min_iter:
        can_complete = False
        reasons.append(f"Need {min_iter} iterations, only at {state['iteration']}")

    # Check screenshots
    screenshot_status = verify_screenshots(state.get("screenshots_dir"))
    if screenshot_status["unverified"] > 0:
        can_complete = False
        reasons.append(f"{screenshot_status['unverified']} unverified screenshots")

    # Check tasks
    incomplete = [t for t in state["tasks"] if t["status"] != "complete"]
    if incomplete:
        can_complete = False
        reasons.append(f"{len(incomplete)} tasks incomplete")

    return {
        "can_complete": can_complete,
        "reasons": reasons if not can_complete else ["All checks passed"],
        "iteration": state["iteration"],
        "min_iterations": min_iter,
        "screenshots": screenshot_status,
        "tasks_complete": len(state["tasks"]) - len(incomplete),
        "tasks_total": len(state["tasks"])
    }

# =============================================================================
# END SCREENSHOT VERIFICATION PROTOCOL
# =============================================================================

def init_state(tasks_str: str, max_iterations: int = 50, completion_promise: str = "ALL_TASKS_VERIFIED", min_iterations: int = 2, screenshots_dir: str = ""):
    """Initialize a new Ralph loop with screenshot verification protocol"""
    ensure_ralph_dir()

    # Parse tasks from string (format: "1. task one 2. task two")
    import re
    task_matches = re.findall(r'\d+\.\s*\[?\s*[xX ]?\s*\]?\s*([^\d]+?)(?=\d+\.|$)', tasks_str + " 999.")
    tasks = [{"id": i+1, "task": t.strip(), "status": "pending", "verified": False, "attempts": 0}
             for i, t in enumerate(task_matches) if t.strip()]

    if not tasks:
        # Fallback: split by newlines
        lines = [l.strip() for l in tasks_str.split('\n') if l.strip()]
        tasks = [{"id": i+1, "task": l, "status": "pending", "verified": False, "attempts": 0}
                 for i, l in enumerate(lines)]

    state = {
        "phase": "build",
        "iteration": 0,
        "max_iterations": max_iterations,
        "min_iterations": min_iterations,  # Minimum loops before promise allowed
        "screenshots_dir": screenshots_dir or SCREENSHOTS_DIR,  # For UI verification
        "started": datetime.now().isoformat(),
        "completion_promise": completion_promise,
        "current_task": 0,
        "tasks": tasks
    }

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    # Initialize negative memory if not exists
    if not os.path.exists(NEG_MEM_FILE):
        neg_mem = {
            "failed_approaches": [],
            "blockers": [],
            "anti_patterns": []
        }
        with open(NEG_MEM_FILE, 'w') as f:
            json.dump(neg_mem, f, indent=2)

    # Initialize log
    with open(LOG_FILE, 'w') as f:
        f.write(f"# Ralph Loop Log\n\nStarted: {datetime.now().isoformat()}\n\n## Tasks\n\n")
        for t in tasks:
            f.write(f"- [ ] {t['task']}\n")
        f.write("\n## Iterations\n\n")

    print(f"[RALPH] Initialized with {len(tasks)} tasks, max {max_iterations} iterations")
    print(f"[RALPH] Completion promise: {completion_promise}")
    return state

def get_state():
    """Get current state"""
    if not os.path.exists(STATE_FILE):
        print("[RALPH] No active loop. Use 'start' to begin.")
        return None
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def get_negative_memory():
    """Get negative memory"""
    if not os.path.exists(NEG_MEM_FILE):
        return {"failed_approaches": [], "blockers": [], "anti_patterns": []}
    with open(NEG_MEM_FILE, 'r') as f:
        return json.load(f)

def status():
    """Print current status"""
    state = get_state()
    if not state:
        return

    neg_mem = get_negative_memory()

    complete = sum(1 for t in state["tasks"] if t["status"] == "complete")
    total = len(state["tasks"])

    print(f"\n=== RALPH STATUS ===")
    print(f"Phase: {state['phase']}")
    print(f"Iteration: {state['iteration']}/{state['max_iterations']} (min: {state.get('min_iterations', 2)})")
    print(f"Progress: {complete}/{total} tasks complete")
    print(f"Current task: {state['current_task'] + 1 if state['current_task'] < total else 'Done'}")
    print(f"\nTasks:")
    for t in state["tasks"]:
        status_icon = "[x]" if t["status"] == "complete" else "[ ]"
        verified = " (verified)" if t.get("verified") else ""
        attempts = f" (attempts: {t.get('attempts', 0)})" if t.get('attempts', 0) > 0 else ""
        print(f"  {status_icon} {t['id']}. {t['task']}{verified}{attempts}")

    # Screenshot verification status
    screenshots_dir = state.get("screenshots_dir", SCREENSHOTS_DIR)
    ss_status = verify_screenshots(screenshots_dir)
    if ss_status["total"] > 0:
        print(f"\nScreenshots: {ss_status['verified']}/{ss_status['total']} verified")
        if ss_status["unverified_files"]:
            print(f"  Unverified: {', '.join(ss_status['unverified_files'][:3])}{'...' if len(ss_status['unverified_files']) > 3 else ''}")

    # Can output promise check
    promise_check = can_output_promise()
    if promise_check["can_complete"]:
        print(f"\nPromise output: ALLOWED")
    else:
        print(f"\nPromise output: BLOCKED")
        for r in promise_check.get("reasons", []):
            print(f"  - {r}")

    if neg_mem["failed_approaches"]:
        print(f"\nNegative Memory: {len(neg_mem['failed_approaches'])} failed approaches")
    if neg_mem["blockers"]:
        print(f"Blockers: {len(neg_mem['blockers'])}")
    if neg_mem["anti_patterns"]:
        print(f"Anti-patterns: {len(neg_mem['anti_patterns'])}")

def check_negative_memory(task_name: str):
    """Check if there are failed approaches for a task"""
    neg_mem = get_negative_memory()
    relevant = [f for f in neg_mem["failed_approaches"] if task_name.lower() in f["task"].lower()]

    if relevant:
        print(f"\n[WARNING] Previous failed approaches for '{task_name}':")
        for f in relevant:
            print(f"  Approach: {f['approach']}")
            print(f"  Failure: {f['failure']}")
            print(f"  Lesson: {f['lesson']}")
            print()
        print("[RALPH] Use a DIFFERENT approach!\n")

    # Also print anti-patterns
    if neg_mem["anti_patterns"]:
        print("[ANTI-PATTERNS] Remember:")
        for ap in neg_mem["anti_patterns"]:
            print(f"  - {ap}")
        print()

    return relevant

def log_failure(task_name: str, approach: str, failure: str, lesson: str):
    """Log a failed approach to negative memory"""
    neg_mem = get_negative_memory()
    neg_mem["failed_approaches"].append({
        "task": task_name,
        "approach": approach,
        "failure": failure,
        "lesson": lesson,
        "timestamp": datetime.now().isoformat()
    })
    with open(NEG_MEM_FILE, 'w') as f:
        json.dump(neg_mem, f, indent=2)
    print(f"[RALPH] Logged failure to negative memory: {approach}")

def add_blocker(description: str, workaround: str = ""):
    """Add a blocker to negative memory"""
    neg_mem = get_negative_memory()
    neg_mem["blockers"].append({
        "description": description,
        "workaround": workaround,
        "discovered": datetime.now().isoformat()
    })
    with open(NEG_MEM_FILE, 'w') as f:
        json.dump(neg_mem, f, indent=2)
    print(f"[RALPH] Added blocker: {description}")

def add_anti_pattern(pattern: str):
    """Add an anti-pattern to remember"""
    neg_mem = get_negative_memory()
    if pattern not in neg_mem["anti_patterns"]:
        neg_mem["anti_patterns"].append(pattern)
        with open(NEG_MEM_FILE, 'w') as f:
            json.dump(neg_mem, f, indent=2)
    print(f"[RALPH] Added anti-pattern: {pattern}")

def complete_task(task_id: int, verified: bool = True):
    """Mark a task as complete"""
    state = get_state()
    if not state:
        return

    for t in state["tasks"]:
        if t["id"] == task_id:
            t["status"] = "complete"
            t["verified"] = verified
            break

    # Move to next incomplete task
    for i, t in enumerate(state["tasks"]):
        if t["status"] != "complete":
            state["current_task"] = i
            break
    else:
        state["current_task"] = len(state["tasks"])  # All done

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    # Log to file
    with open(LOG_FILE, 'a') as f:
        f.write(f"- [{datetime.now().strftime('%H:%M')}] Completed task {task_id}\n")

    print(f"[RALPH] Task {task_id} marked complete (verified: {verified})")

def increment_attempt(task_id: int):
    """Increment attempt count for a task"""
    state = get_state()
    if not state:
        return

    for t in state["tasks"]:
        if t["id"] == task_id:
            t["attempts"] = t.get("attempts", 0) + 1
            break

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def next_iteration():
    """Increment iteration count"""
    state = get_state()
    if not state:
        return None

    state["iteration"] += 1

    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    # Check if max reached
    if state["iteration"] >= state["max_iterations"]:
        print(f"[RALPH] Max iterations ({state['max_iterations']}) reached!")
        return None

    return state

def is_complete():
    """Check if all tasks are complete"""
    state = get_state()
    if not state:
        return False

    return all(t["status"] == "complete" and t.get("verified", False) for t in state["tasks"])

def cancel():
    """Cancel the loop"""
    if os.path.exists(STATE_FILE):
        _ = get_state()  # Validate state exists
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n## Cancelled\n\n{datetime.now().isoformat()}\n")
        print("[RALPH] Loop cancelled. State preserved in .ralph/")
    else:
        print("[RALPH] No active loop to cancel")

def call_on_completion():
    """Call user when Ralph completes all tasks"""
    state = get_state()
    if not state:
        print("[RALPH] No active loop")
        return False

    completed = sum(1 for t in state["tasks"] if t["status"] == "complete")
    total = len(state["tasks"])
    task_names = ", ".join(t["task"][:30] for t in state["tasks"] if t["status"] == "complete")

    if CALLME_AVAILABLE and callme_configured():
        notify_completion(f"Completed: {task_names}", completed, total)
        return True
    else:
        print(f"[RALPH] CallMe not configured. Would notify: {completed}/{total} tasks done")
        return False

def call_on_blocker(task_name: str, description: str):
    """Call user when Ralph hits a blocker"""
    state = get_state()
    attempts = 0
    if state:
        for t in state["tasks"]:
            if task_name.lower() in t["task"].lower():
                attempts = t.get("attempts", 0)
                break

    if CALLME_AVAILABLE and callme_configured():
        notify_blocker(task_name, description, attempts)
        return True
    else:
        print(f"[RALPH] CallMe not configured. Would call about blocker: {task_name}")
        return False

def print_help():
    print("""
Ralph Enhanced - Autonomous loop with negative memory, screenshot verification, CallMe

Usage:
    python ralph_enhanced.py start "TASKS" [MAX_ITER] [PROMISE] [MIN_ITER] [SCREENSHOTS_DIR]
    python ralph_enhanced.py status
    python ralph_enhanced.py check "TASK_NAME"     # Check negative memory
    python ralph_enhanced.py fail "TASK" "APPROACH" "FAILURE" "LESSON"
    python ralph_enhanced.py blocker "DESC" ["WORKAROUND"]
    python ralph_enhanced.py antipattern "PATTERN"
    python ralph_enhanced.py complete TASK_ID [--verified/--unverified]
    python ralph_enhanced.py next                  # Next iteration
    python ralph_enhanced.py done                  # Check if complete
    python ralph_enhanced.py cancel

Screenshot Verification Protocol (TDD workflow):
    python ralph_enhanced.py screenshots           # Check screenshot status
    python ralph_enhanced.py verify-screenshot FILE  # Mark single screenshot verified
    python ralph_enhanced.py verify-all            # Mark ALL screenshots verified
    python ralph_enhanced.py reset-screenshots     # Reset all (remove verified_ prefix)
    python ralph_enhanced.py can-complete          # Check if promise can be output

CallMe Integration (phone notifications):
    python ralph_enhanced.py call-complete         # Call user on completion
    python ralph_enhanced.py call-blocker "TASK" "DESC"  # Call about blocker
    python ralph_enhanced.py callme-status         # Check CallMe config

Screenshot Verification Rules:
    1. Review each screenshot visually
    2. Run: verify-screenshot FILE for each reviewed image
    3. DO NOT output promise after verifying - let next iteration confirm
    4. Next iteration checks all have verified_ prefix
    5. Only THEN output completion promise

Examples:
    python ralph_enhanced.py start "1. Implement UI 2. Pass tests" 30 "COMPLETE" 2
    python ralph_enhanced.py screenshots           # See unverified files
    python ralph_enhanced.py verify-screenshot .ralph/screenshots/button.png
    python ralph_enhanced.py can-complete          # Check if safe to output promise
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "start":
        tasks = sys.argv[2] if len(sys.argv) > 2 else ""
        max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 50
        promise = sys.argv[4] if len(sys.argv) > 4 else "ALL_TASKS_VERIFIED"
        min_iter = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        screenshots_dir = sys.argv[6] if len(sys.argv) > 6 else ""
        init_state(tasks, max_iter, promise, min_iter, screenshots_dir)

    elif cmd == "status":
        status()

    elif cmd == "check":
        task = sys.argv[2] if len(sys.argv) > 2 else ""
        check_negative_memory(task)

    elif cmd == "fail":
        if len(sys.argv) >= 6:
            log_failure(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Usage: fail TASK APPROACH FAILURE LESSON")

    elif cmd == "blocker":
        desc = sys.argv[2] if len(sys.argv) > 2 else ""
        workaround = sys.argv[3] if len(sys.argv) > 3 else ""
        add_blocker(desc, workaround)

    elif cmd == "antipattern":
        pattern = sys.argv[2] if len(sys.argv) > 2 else ""
        add_anti_pattern(pattern)

    elif cmd == "complete":
        task_id = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        verified = "--unverified" not in sys.argv
        complete_task(task_id, verified)

    elif cmd == "next":
        state = next_iteration()
        if state:
            print(f"[RALPH] Iteration {state['iteration']}/{state['max_iterations']}")

    elif cmd == "done":
        if is_complete():
            state = get_state()
            if state:
                print(state["completion_promise"])
        else:
            print("[RALPH] Not complete yet")

    elif cmd == "cancel":
        cancel()

    elif cmd == "call-complete":
        call_on_completion()

    elif cmd == "call-blocker":
        task = sys.argv[2] if len(sys.argv) > 2 else "Unknown task"
        desc = sys.argv[3] if len(sys.argv) > 3 else "Hit a blocker"
        call_on_blocker(task, desc)

    elif cmd == "callme-status":
        print(f"[CALLME] Available: {CALLME_AVAILABLE}")
        print(f"[CALLME] Configured: {callme_configured()}")
        if not CALLME_AVAILABLE:
            print("[CALLME] Run: python ~/.claude/scripts/callme_integration.py setup")

    # Screenshot verification commands
    elif cmd == "screenshots":
        state = get_state()
        screenshots_dir = state.get("screenshots_dir", SCREENSHOTS_DIR) if state else SCREENSHOTS_DIR
        result = verify_screenshots(screenshots_dir)
        print(f"\n=== SCREENSHOT STATUS ===")
        print(f"Directory: {screenshots_dir}")
        print(f"Total: {result['total']}")
        print(f"Verified: {result['verified']}")
        print(f"Unverified: {result['unverified']}")
        if result['unverified_files']:
            print(f"\nUnverified files:")
            for f in result['unverified_files']:
                print(f"  - {f}")
        print(f"\nCan complete: {result['can_complete']}")

    elif cmd == "verify-screenshot":
        filepath = sys.argv[2] if len(sys.argv) > 2 else ""
        if filepath:
            mark_screenshot_verified(filepath)
        else:
            print("Usage: verify-screenshot FILE")

    elif cmd == "verify-all":
        state = get_state()
        screenshots_dir = state.get("screenshots_dir", SCREENSHOTS_DIR) if state else SCREENSHOTS_DIR
        count = mark_all_screenshots_verified(screenshots_dir)
        print(f"[RALPH] Marked {count} screenshots as verified")

    elif cmd == "reset-screenshots":
        state = get_state()
        screenshots_dir = state.get("screenshots_dir", SCREENSHOTS_DIR) if state else SCREENSHOTS_DIR
        count = reset_screenshot_verification(screenshots_dir)
        print(f"[RALPH] Reset {count} screenshots")

    elif cmd == "can-complete":
        result = can_output_promise()
        print(f"\n=== CAN OUTPUT PROMISE? ===")
        print(f"Can complete: {'YES' if result['can_complete'] else 'NO'}")
        print(f"Iteration: {result.get('iteration', 0)}/{result.get('min_iterations', 2)}")
        print(f"Tasks: {result.get('tasks_complete', 0)}/{result.get('tasks_total', 0)}")
        if result.get('screenshots'):
            ss = result['screenshots']
            print(f"Screenshots: {ss.get('verified', 0)} verified, {ss.get('unverified', 0)} unverified")
        if not result['can_complete']:
            print(f"\nReasons:")
            for r in result.get('reasons', []):
                print(f"  - {r}")

    else:
        print_help()
