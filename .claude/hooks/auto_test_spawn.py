#!/usr/bin/env python3
"""
Auto Test Coverage Spawner Hook (PostToolUse)

Inspired by Boris's method: Auto-spawn test-writer agent during code changes.

This hook monitors code changes and automatically suggests spawning
a test-writer agent when significant new code is added without tests.

Triggers when:
- New functions/classes added without corresponding tests
- Significant code changes in files lacking test coverage
- New API endpoints without test files
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Track state
STATE_FILE = Path.home() / '.claude' / 'state' / 'auto_test_state.json'

# Patterns to detect new code needing tests
FUNCTION_PATTERNS = [
    r'(?:export\s+)?(?:async\s+)?function\s+(\w+)',  # JS/TS functions
    r'(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s*)?\(',  # Arrow functions
    r'def\s+(\w+)\s*\(',  # Python functions
    r'func\s+(\w+)\s*\(',  # Go functions
    r'fn\s+(\w+)\s*\(',  # Rust functions
]

# Files that typically need tests
NEEDS_TESTS_PATTERNS = [
    r'src/.*\.(ts|tsx|js|jsx)$',
    r'lib/.*\.py$',
    r'app/.*\.(ts|tsx|js|jsx)$',
    r'pkg/.*\.go$',
]

# Test file patterns
TEST_FILE_PATTERNS = [
    r'\.test\.(ts|tsx|js|jsx)$',
    r'\.spec\.(ts|tsx|js|jsx)$',
    r'_test\.py$',
    r'test_.*\.py$',
    r'_test\.go$',
]


def load_state():
    """Load tracking state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except:
            pass
    return {
        'files_needing_tests': {},  # path -> {functions: [], last_modified: str}
        'last_test_suggestion': None,
        'test_spawn_count': 0
    }


def save_state(state):
    """Save tracking state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def needs_tests(file_path):
    """Check if file type typically needs tests."""
    for pattern in NEEDS_TESTS_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def is_test_file(file_path):
    """Check if file is a test file."""
    for pattern in TEST_FILE_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def extract_functions(content):
    """Extract function names from code content."""
    functions = []
    for pattern in FUNCTION_PATTERNS:
        matches = re.findall(pattern, content)
        functions.extend(matches)
    # Filter out common non-test-worthy names
    skip_names = {'constructor', 'render', 'useEffect', 'useState', 'main', '__init__'}
    return [f for f in functions if f not in skip_names and not f.startswith('_')]


def find_corresponding_test(file_path):
    """Find if a test file exists for given source file."""
    path = Path(file_path)
    base_name = path.stem
    parent = path.parent

    # Common test file locations
    test_patterns = [
        parent / f'{base_name}.test{path.suffix}',
        parent / f'{base_name}.spec{path.suffix}',
        parent / '__tests__' / f'{base_name}.test{path.suffix}',
        parent.parent / 'tests' / f'test_{base_name}{path.suffix}',
        parent.parent / 'tests' / f'{base_name}_test{path.suffix}',
    ]

    for test_path in test_patterns:
        if test_path.exists():
            return str(test_path)
    return None


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        return

    tool_name = hook_input.get('tool_name', '')
    tool_input = hook_input.get('tool_input', {})
    tool_result = hook_input.get('tool_result', {})

    # Track Write and Edit operations on code files
    if tool_name not in ['Edit', 'Write']:
        return

    file_path = tool_input.get('file_path', '')
    if not file_path:
        return

    # Skip if this is a test file
    if is_test_file(file_path):
        return

    # Skip if file doesn't typically need tests
    if not needs_tests(file_path):
        return

    state = load_state()

    # Get the content that was written/edited
    content = tool_input.get('content', '') or tool_input.get('new_string', '')

    # Extract functions from the change
    new_functions = extract_functions(content)

    if new_functions:
        # Check if test file exists
        test_file = find_corresponding_test(file_path)

        if not test_file:
            # Track this file as needing tests
            if file_path not in state['files_needing_tests']:
                state['files_needing_tests'][file_path] = {
                    'functions': [],
                    'last_modified': datetime.now().isoformat()
                }

            # Add new functions
            existing = state['files_needing_tests'][file_path]['functions']
            for func in new_functions:
                if func not in existing:
                    existing.append(func)
            state['files_needing_tests'][file_path]['last_modified'] = datetime.now().isoformat()

    save_state(state)

    # Check if we should suggest test spawning
    total_untested = sum(
        len(info['functions'])
        for info in state['files_needing_tests'].values()
    )

    # Suggest after 5+ untested functions accumulated
    if total_untested >= 5:
        # Rate limit suggestions
        last_suggestion = state.get('last_test_suggestion')
        if last_suggestion:
            last_time = datetime.fromisoformat(last_suggestion)
            minutes_since = (datetime.now() - last_time).seconds / 60
            if minutes_since < 15:  # Don't suggest within 15 minutes
                return

        # Build file summary
        files_summary = []
        for path, info in list(state['files_needing_tests'].items())[:3]:
            name = Path(path).name
            funcs = ', '.join(info['functions'][:3])
            if len(info['functions']) > 3:
                funcs += f' (+{len(info["functions"]) - 3})'
            files_summary.append(f"  - {name}: {funcs}")

        summary = '\n'.join(files_summary)

        suggestion = {
            "continue": True,
            "stopReason": None,
            "message": f"""
TEST COVERAGE OPPORTUNITY

{total_untested} functions without tests detected:
{summary}

Spawn background test-writer:
```
Task(
  subagent_type="test-writer",
  prompt="Write unit tests for untested functions in: {', '.join(state['files_needing_tests'].keys())}",
  run_in_background=True,
  model="haiku"
)
```

Or run: /test generate
"""
        }

        state['last_test_suggestion'] = datetime.now().isoformat()
        state['test_spawn_count'] += 1
        save_state(state)

        print(json.dumps(suggestion))


if __name__ == '__main__':
    main()
