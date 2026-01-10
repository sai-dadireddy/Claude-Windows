#!/usr/bin/env python3
"""
CallMe Integration for Ralph
Enables phone calls when Ralph completes tasks or hits blockers.

Setup required:
1. Telnyx or Twilio account with phone number
2. OpenAI API key (for speech)
3. ngrok account (free tier works)

See ~/.claude/docs/callme-setup.md for full instructions.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration from environment
CALLME_ENABLED = os.environ.get("CALLME_ENABLED", "false").lower() == "true"
CALLME_PHONE_PROVIDER = os.environ.get("CALLME_PHONE_PROVIDER", "")
CALLME_USER_PHONE_NUMBER = os.environ.get("CALLME_USER_PHONE_NUMBER", "")

def is_configured() -> bool:
    """Check if CallMe is properly configured"""
    required = [
        "CALLME_PHONE_PROVIDER",
        "CALLME_PHONE_ACCOUNT_SID",
        "CALLME_PHONE_AUTH_TOKEN",
        "CALLME_PHONE_NUMBER",
        "CALLME_USER_PHONE_NUMBER",
        "CALLME_OPENAI_API_KEY",
        "CALLME_NGROK_AUTHTOKEN"
    ]

    missing = [var for var in required if not os.environ.get(var)]

    if missing:
        return False
    return True

def get_status() -> dict:
    """Get CallMe configuration status"""
    required = {
        "CALLME_ENABLED": os.environ.get("CALLME_ENABLED", "false"),
        "CALLME_PHONE_PROVIDER": os.environ.get("CALLME_PHONE_PROVIDER", ""),
        "CALLME_USER_PHONE_NUMBER": os.environ.get("CALLME_USER_PHONE_NUMBER", ""),
        "CALLME_PHONE_NUMBER": os.environ.get("CALLME_PHONE_NUMBER", ""),
        "CALLME_OPENAI_API_KEY": "set" if os.environ.get("CALLME_OPENAI_API_KEY") else "missing",
        "CALLME_NGROK_AUTHTOKEN": "set" if os.environ.get("CALLME_NGROK_AUTHTOKEN") else "missing"
    }

    return {
        "configured": is_configured(),
        "enabled": CALLME_ENABLED,
        "provider": CALLME_PHONE_PROVIDER or "not set",
        "user_phone": CALLME_USER_PHONE_NUMBER or "not set",
        "variables": required
    }

def log_call_attempt(event_type: str, message: str, success: bool):
    """Log call attempts for debugging"""
    log_dir = Path.home() / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "callme.log"

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "message": message[:100],  # Truncate for log
        "success": success
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")

def notify_completion(task_summary: str, tasks_completed: int, total_tasks: int) -> bool:
    """
    Call user when Ralph loop completes.
    Returns True if call was made, False otherwise.
    """
    if not CALLME_ENABLED:
        print("[CALLME] Disabled - skipping notification call")
        log_call_attempt("completion", task_summary, False)
        return False

    if not is_configured():
        print("[CALLME] Not configured - run 'python callme_integration.py setup'")
        log_call_attempt("completion", "not configured", False)
        return False

    message = f"Hey! Ralph just finished. {tasks_completed} of {total_tasks} tasks completed. {task_summary}"

    # This would call the MCP tool - for now we output the intent
    print(f"[CALLME] Would call with: {message}")
    print(f"[CALLME] Tools: initiate_call(message='{message}')")

    log_call_attempt("completion", message, True)
    return True

def notify_blocker(task_name: str, blocker_description: str, attempts: int) -> bool:
    """
    Call user when Ralph hits a blocker.
    Returns True if call was made, False otherwise.
    """
    if not CALLME_ENABLED:
        print("[CALLME] Disabled - skipping blocker call")
        log_call_attempt("blocker", blocker_description, False)
        return False

    if not is_configured():
        print("[CALLME] Not configured")
        log_call_attempt("blocker", "not configured", False)
        return False

    message = f"Hey, I'm stuck on '{task_name}'. I've tried {attempts} times. The issue is: {blocker_description}. What should I do?"

    print(f"[CALLME] Would call with: {message}")
    print(f"[CALLME] Tools: initiate_call(message='{message}')")

    log_call_attempt("blocker", message, True)
    return True

def notify_decision_needed(task_name: str, options: list) -> bool:
    """
    Call user when Ralph needs a decision.
    Returns True if call was made, False otherwise.
    """
    if not CALLME_ENABLED or not is_configured():
        return False

    options_text = ", ".join([f"option {i+1}: {opt}" for i, opt in enumerate(options)])
    message = f"Hey, I need your input on '{task_name}'. I have a few options: {options_text}. Which should I go with?"

    print(f"[CALLME] Would call with: {message}")
    log_call_attempt("decision", message, True)
    return True

def print_setup_guide():
    """Print setup instructions"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    CallMe Setup Guide                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 1: Phone Provider (Telnyx recommended - cheaper)           ║
║  ─────────────────────────────────────────────────────           ║
║  1. Go to https://portal.telnyx.com                              ║
║  2. Create account, verify identity                              ║
║  3. Purchase phone number (~$1/month)                            ║
║  4. Create Voice API application                                 ║
║  5. Note: Connection ID + API Key                                ║
║                                                                  ║
║  STEP 2: ngrok (free tier works)                                 ║
║  ─────────────────────────────────────────────────────           ║
║  1. Go to https://ngrok.com                                      ║
║  2. Create free account                                          ║
║  3. Copy authtoken from dashboard                                ║
║                                                                  ║
║  STEP 3: OpenAI API Key                                          ║
║  ─────────────────────────────────────────────────────           ║
║  1. Go to https://platform.openai.com                            ║
║  2. Create API key with speech permissions                       ║
║                                                                  ║
║  STEP 4: Configure Environment                                   ║
║  ─────────────────────────────────────────────────────           ║
║  Add to ~/.claude/settings.json in "env" section:                ║
║                                                                  ║
║    "CALLME_ENABLED": "true",                                     ║
║    "CALLME_PHONE_PROVIDER": "telnyx",                            ║
║    "CALLME_PHONE_ACCOUNT_SID": "your-connection-id",             ║
║    "CALLME_PHONE_AUTH_TOKEN": "your-api-key",                    ║
║    "CALLME_PHONE_NUMBER": "+15551234567",                        ║
║    "CALLME_USER_PHONE_NUMBER": "+15559876543",                   ║
║    "CALLME_OPENAI_API_KEY": "sk-...",                            ║
║    "CALLME_NGROK_AUTHTOKEN": "your-ngrok-token"                  ║
║                                                                  ║
║  STEP 5: Restart Claude Code                                     ║
║  ─────────────────────────────────────────────────────           ║
║  The environment variables will be loaded on next start.         ║
║                                                                  ║
║  COSTS                                                           ║
║  ─────────────────────────────────────────────────────           ║
║  - Telnyx calls: ~$0.007/min                                     ║
║  - Phone number: ~$1/month                                       ║
║  - OpenAI STT: ~$0.006/min                                       ║
║  - OpenAI TTS: ~$0.02/min                                        ║
║  - Total: ~$0.03-0.04/min of conversation                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

def print_status():
    """Print current configuration status"""
    status = get_status()

    print("\n=== CallMe Status ===")
    print(f"Configured: {'Yes' if status['configured'] else 'No'}")
    print(f"Enabled: {status['enabled']}")
    print(f"Provider: {status['provider']}")
    print(f"User Phone: {status['user_phone']}")
    print("\nEnvironment Variables:")
    for var, value in status['variables'].items():
        if 'KEY' in var or 'TOKEN' in var or 'SID' in var:
            display = "***" if value and value not in ['missing', 'set'] else value
        else:
            display = value
        print(f"  {var}: {display}")

    if not status['configured']:
        print("\n[!] Run 'python callme_integration.py setup' for instructions")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_status()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "setup":
        print_setup_guide()

    elif cmd == "status":
        print_status()

    elif cmd == "test":
        if is_configured():
            print("[CALLME] Configuration valid - would make test call")
            notify_completion("Test call from Ralph integration", 1, 1)
        else:
            print("[CALLME] Not configured yet")
            print_status()

    elif cmd == "completion":
        summary = sys.argv[2] if len(sys.argv) > 2 else "Tasks completed"
        completed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        total = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        notify_completion(summary, completed, total)

    elif cmd == "blocker":
        task = sys.argv[2] if len(sys.argv) > 2 else "Unknown task"
        desc = sys.argv[3] if len(sys.argv) > 3 else "Unknown blocker"
        attempts = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        notify_blocker(task, desc, attempts)

    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python callme_integration.py [status|setup|test|completion|blocker]")
