#!/usr/bin/env python3
"""
Idle Documentation Generator Hook (PostToolUse)

Inspired by Boris's method: Use "downtime" for documentation and tests.
This hook tracks significant code changes and suggests doc generation
when there's a natural pause in development.

Triggers when:
- Multiple files have been edited without doc updates
- A significant feature has been implemented
- Tests have been added without documentation
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Thresholds for suggesting doc generation
CODE_CHANGES_THRESHOLD = 5  # Files edited before suggesting docs
FEATURE_KEYWORDS = ['feat', 'feature', 'add', 'implement', 'create', 'new']
TEST_KEYWORDS = ['test', 'spec', '.test.', '.spec.']

# Track state in temp file
STATE_FILE = Path.home() / '.claude' / 'state' / 'idle_doc_state.json'


def load_state():
    """Load tracking state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {
        'edited_files': [],
        'tests_added': [],
        'last_doc_suggestion': None,
        'session_start': datetime.now().isoformat()
    }


def save_state(state):
    """Save tracking state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def is_code_file(path):
    """Check if file is a code file (not docs/config)."""
    code_extensions = {'.py', '.ts', '.tsx', '.js', '.jsx', '.go', '.rs', '.java', '.cpp', '.c'}
    return Path(path).suffix.lower() in code_extensions


def is_doc_file(path):
    """Check if file is documentation."""
    path_lower = path.lower()
    return (
        path_lower.endswith('.md') or
        '/docs/' in path_lower or
        'readme' in path_lower or
        'changelog' in path_lower
    )


def is_test_file(path):
    """Check if file is a test file."""
    path_lower = path.lower()
    return any(kw in path_lower for kw in TEST_KEYWORDS)


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})

    # Only track Edit and Write operations
    if tool_name not in ['Edit', 'Write']:
        return

    file_path = tool_input.get('file_path', '')
    if not file_path:
        return

    state = load_state()

    # Track the file
    if is_code_file(file_path):
        if file_path not in state['edited_files']:
            state['edited_files'].append(file_path)

    if is_test_file(file_path):
        if file_path not in state['tests_added']:
            state['tests_added'].append(file_path)

    # Reset if doc was updated
    if is_doc_file(file_path):
        state['edited_files'] = []
        state['tests_added'] = []
        state['last_doc_suggestion'] = datetime.now().isoformat()
        save_state(state)
        return

    save_state(state)

    # Check if we should suggest documentation
    code_changes = len(state['edited_files'])
    tests_added = len(state['tests_added'])

    # Suggest docs if threshold reached
    if code_changes >= CODE_CHANGES_THRESHOLD:
        # Don't suggest too frequently
        last_suggestion = state.get('last_doc_suggestion')
        if last_suggestion:
            last_time = datetime.fromisoformat(last_suggestion)
            minutes_since = (datetime.now() - last_time).seconds / 60
            if minutes_since < 10:  # Don't suggest within 10 minutes
                return

        # Build suggestion
        files_summary = ', '.join(Path(f).name for f in state['edited_files'][:3])
        if len(state['edited_files']) > 3:
            files_summary += f' (+{len(state["edited_files"]) - 3} more)'

        suggestion = {
            "continue": True,
            "stopReason": None,
            "message": f"""
DOC GENERATION OPPORTUNITY

{code_changes} code files edited since last doc update:
{files_summary}

Consider spawning @scribe agent for documentation:
- README updates
- API documentation
- Code comments for complex logic

Quick command: Task(subagent_type="scribe", prompt="Update docs for recent changes", run_in_background=True)
"""
        }

        # Update last suggestion time
        state['last_doc_suggestion'] = datetime.now().isoformat()
        save_state(state)

        print(json.dumps(suggestion))
        return

    # Suggest test docs if tests added without documentation
    if tests_added >= 3 and code_changes < CODE_CHANGES_THRESHOLD:
        suggestion = {
            "continue": True,
            "stopReason": None,
            "message": f"""
TEST DOCUMENTATION OPPORTUNITY

{tests_added} test files added. Consider documenting:
- Test scenarios covered
- How to run tests
- Test fixtures/mocks used

Quick: Task(subagent_type="scribe", prompt="Document test coverage", run_in_background=True, model="haiku")
"""
        }
        state['tests_added'] = []  # Reset
        save_state(state)
        print(json.dumps(suggestion))


if __name__ == '__main__':
    main()
