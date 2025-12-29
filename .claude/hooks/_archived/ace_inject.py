#!/usr/bin/env python3
"""
ACE (Agentic Context Engineering) - Inject Learnings
Injects accumulated learnings from playbook.json at session start
"""

import sys
import json
import os
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')

PLAYBOOK_PATH = Path.home() / '.claude' / 'playbook.json'
SESSION_PATH = Path.home() / '.claude' / 'last-session-id.txt'

def sanitize_unicode(text):
    """Remove invalid Unicode surrogates that break JSON encoding."""
    if not text:
        return ""
    try:
        return text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return ''.join(c for c in text if ord(c) < 0xD800 or (ord(c) > 0xDFFF and ord(c) < 0x10000))

def is_first_message(session_id):
    """Check if this is first message of new session"""
    try:
        if SESSION_PATH.exists():
            last_session = SESSION_PATH.read_text(encoding='utf-8', errors='replace').strip()
            if last_session == session_id:
                return False  # Same session, already injected

        # New session - save ID
        SESSION_PATH.write_text(session_id, encoding='utf-8')
        return True
    except:
        return True  # Default to inject on error

def load_playbook():
    """Load playbook with accumulated learnings"""
    try:
        if not PLAYBOOK_PATH.exists():
            return []

        raw_text = PLAYBOOK_PATH.read_text(encoding='utf-8', errors='replace')
        safe_text = sanitize_unicode(raw_text)
        data = json.loads(safe_text)
        return data.get('learnings', [])
    except:
        return []

def format_learnings(learnings):
    """Format top learnings for injection"""
    if not learnings:
        return None

    # Sort by score (highest first)
    sorted_learnings = sorted(
        learnings,
        key=lambda x: x.get('score', 0),
        reverse=True
    )

    # Top 10 learnings with positive scores
    top_learnings = [
        l for l in sorted_learnings
        if l.get('score', 0) > 0
    ][:10]

    if not top_learnings:
        return None

    # Format as context
    context = "## Knowledge from Previous Sessions\n\n"
    context += "Apply these proven patterns:\n\n"

    for learning in top_learnings:
        score = learning.get('score', 0)
        text = sanitize_unicode(learning.get('text', ''))
        sessions = learning.get('sessions_applied', 0)

        context += f"- {text} [Score: +{score}, Used: {sessions}x]\n"

    return context

def main():
    try:
        # Read input
        if len(sys.argv) < 2:
            input_data = sys.stdin.read()
        else:
            input_data = ' '.join(sys.argv[1:])

        # Sanitize input
        input_data = sanitize_unicode(input_data)

        # Parse session ID
        try:
            data = json.loads(input_data)
            session_id = data.get('sessionId', 'default')
        except:
            session_id = 'default'

        # Check if first message
        if not is_first_message(session_id):
            # Not first message - return empty
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        # Load and format learnings
        learnings = load_playbook()
        context = format_learnings(learnings)

        if not context:
            # No learnings yet
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        # Sanitize final context
        context = sanitize_unicode(context)

        # Return injection
        result = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context
            }
        }

        print(json.dumps(result, ensure_ascii=True))

    except Exception as e:
        # Fail gracefully - don't block Claude
        print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))

if __name__ == '__main__':
    main()
