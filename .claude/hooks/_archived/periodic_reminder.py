#!/usr/bin/env python3
"""
Periodic Reminder Hook - Combats Context Drift
Injects rule reminders every N turns to prevent Claude from forgetting instructions.

Based on: https://medium.com/@peter7lee/never-remind-your-ai-again-d0ef9e58ec18
"""

import sys
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')

# Configuration
REMINDER_FREQUENCY = 10  # Remind every N turns
COUNTER_FILE = Path.home() / '.claude' / 'turn_counter.json'

def sanitize_unicode(text):
    """Remove invalid Unicode surrogates that break JSON encoding."""
    if not text:
        return ""
    try:
        return text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return ''.join(c for c in text if ord(c) < 0xD800 or (ord(c) > 0xDFFF and ord(c) < 0x10000))

# Critical rules to remind (subset of CLAUDE.md)
CRITICAL_RULES = """
## REMINDER: Critical Rules (Turn {turn})

1. **PowerShell not Bash**: Use `powershell -Command "..."` on Windows
2. **Absolute paths only**: C:\\full\\path, never relative
3. **RAG first**: `/knowledge query` before reading large docs
4. **Model selection**: haiku for search, sonnet for code, opus for architecture
5. **Files to correct folders**: reference/, docs/, tasks/, tests/
6. **Check playbook.json**: Learn from past mistakes
7. **Context at {context_pct}%**: Save at 70%, critical at 90%
"""

FULL_REMINDER = """
## FULL REMINDER: All Critical Rules (Turn {turn})

### Windows/PowerShell (CRITICAL)
- ALWAYS: `powershell -Command "your-command"`
- NEVER: Unix redirects (2>/dev/null)
- NEVER: Relative paths

### Model Selection for Agents
| Task | Model |
|------|-------|
| File search, grep | haiku |
| Code implementation | sonnet |
| Architecture | opus |

### File Locations
| Type | Location |
|------|----------|
| ROADMAP, BUGS | reference/ |
| ARCHITECTURE | docs/ |
| *.test.js | tests/ |
| Agents | .claude/agents/ |

### Multi-AI: When to Use
- Stuck >15 min -> Consult GLM-4.6/Codex
- Architecture -> Get 2-3 perspectives
- Code review -> Parallel: Codex + Qwen

### Memory Protocol
- Save at 70% context
- Update PROJECT-STATE.md
- Check playbook.json for lessons
"""


def load_counter():
    """Load turn counter"""
    try:
        if COUNTER_FILE.exists():
            raw_text = COUNTER_FILE.read_text(encoding='utf-8', errors='replace')
            data = json.loads(sanitize_unicode(raw_text))
            return data.get('turns', 0), data.get('session_id', '')
        return 0, ''
    except:
        return 0, ''


def save_counter(turns, session_id):
    """Save turn counter"""
    try:
        COUNTER_FILE.parent.mkdir(exist_ok=True)
        COUNTER_FILE.write_text(json.dumps({
            'turns': turns,
            'session_id': session_id
        }, ensure_ascii=True), encoding='utf-8')
    except:
        pass


def main():
    try:
        # Read input
        input_data = sys.stdin.read()
        input_data = sanitize_unicode(input_data)

        try:
            data = json.loads(input_data)
            session_id = data.get('sessionId', 'default')
        except:
            session_id = 'default'

        # Load counter
        turns, last_session = load_counter()

        # Reset counter for new session
        if session_id != last_session:
            turns = 0

        # Increment turn
        turns += 1
        save_counter(turns, session_id)

        # Determine if reminder needed
        reminder = None

        if turns % (REMINDER_FREQUENCY * 3) == 0:
            # Every 30 turns: Full reminder
            reminder = FULL_REMINDER.format(turn=turns)
        elif turns % REMINDER_FREQUENCY == 0:
            # Every 10 turns: Brief reminder
            # Estimate context (rough)
            context_pct = min(95, turns * 3)  # ~3% per turn estimate
            reminder = CRITICAL_RULES.format(turn=turns, context_pct=context_pct)

        if reminder:
            result = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": sanitize_unicode(reminder)
                }
            }
            print(json.dumps(result, ensure_ascii=True))
        else:
            # No reminder this turn
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))

    except Exception as e:
        # Fail gracefully
        print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))


if __name__ == '__main__':
    main()
