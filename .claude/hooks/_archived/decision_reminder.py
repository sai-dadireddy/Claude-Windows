#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Decision/Preference Reminder Hook (UserPromptSubmit)

Detects when user makes decisions or states preferences,
reminds Claude to save them to memory.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

def log(msg: str):
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [DecisionReminder] {msg}\n")
    except:
        pass

# Patterns for decisions
DECISION_PATTERNS = re.compile(
    r"\b(let'?s|we should|i want to|go with|choose|pick|select|use|prefer|switch to|install|set up|configure|enable|disable)\s+"
    r"|\b(yes|ok|okay|sure|do it|go ahead|sounds good|let'?s do)\b"
    r"|\b(i like|i prefer|i want|i need|i'?d rather)\b"
    r"|\b(decision|decided|choosing|picked|selected)\b",
    re.I
)

# Patterns for preferences
PREFERENCE_PATTERNS = re.compile(
    r"\b(i (always|usually|prefer|like|want|need|hate|don'?t like))\b"
    r"|\b(my (preference|style|way|approach))\b"
    r"|\b(prefer.+over|rather.+than|instead of)\b"
    r"|\b(don'?t|never|always|usually)\s+(use|want|like|do)\b",
    re.I
)

# Patterns for setup/config decisions
SETUP_PATTERNS = re.compile(
    r"\b(install|set ?up|configure|enable|add|create|init)\s+(it|this|that|\w+)\b"
    r"|\b(yes.*(install|set ?up|add|create))\b"
    r"|\b(do it|go ahead|proceed|implement)\b",
    re.I
)

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    prompt = data.get("prompt", "")

    if len(prompt) < 5:
        sys.exit(0)

    reminders = []

    # Check for decision patterns
    if DECISION_PATTERNS.search(prompt):
        reminders.append("decision")
        log(f"Decision detected: {prompt[:50]}...")

    # Check for preference patterns
    if PREFERENCE_PATTERNS.search(prompt):
        reminders.append("preference")
        log(f"Preference detected: {prompt[:50]}...")

    # Check for setup/config decisions
    if SETUP_PATTERNS.search(prompt):
        reminders.append("setup")
        log(f"Setup decision detected: {prompt[:50]}...")

    if not reminders:
        sys.exit(0)

    # Build reminder context
    reminder_type = reminders[0]

    if reminder_type == "decision":
        context = """<memory-reminder>
[!] USER MADE A DECISION - Save it NOW!
Command: ~/.claude/scripts/memory_manager.py save-memory PROJECT decision "WHAT_WAS_DECIDED"
</memory-reminder>"""
        user_msg = "[SAVE] Decision detected -> Save to memory!"

    elif reminder_type == "preference":
        context = """<memory-reminder>
[!] USER STATED A PREFERENCE - Save it NOW!
Command: ~/.claude/scripts/memory_manager.py save-memory global preference "WHAT_USER_PREFERS"
</memory-reminder>"""
        user_msg = "[SAVE] Preference detected -> Save to memory!"

    else:  # setup
        context = """<memory-reminder>
[!] USER APPROVED SETUP/CONFIG - Save after completing!
Command: ~/.claude/scripts/memory_manager.py save-memory PROJECT decision "WHAT_WAS_SET_UP"
</memory-reminder>"""
        user_msg = "[SAVE] Setup decision -> Save after done!"

    log(f"Writing hint for: {reminder_type}")

    # Write to signal file (workaround for broken context injection)
    hint_file = Path.home() / ".claude" / "hints" / "current.txt"
    hint_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%H:%M:%S")
    hint_text = f"SAVE TO MEMORY: {reminder_type} detected - use memory_manager.py"
    with open(hint_file, "a") as f:
        f.write(f"[{timestamp}] [memory] {hint_text}\n")

    print("[MEMORY] Hint written to ~/.claude/hints/current.txt")
    sys.exit(0)

if __name__ == "__main__":
    main()
