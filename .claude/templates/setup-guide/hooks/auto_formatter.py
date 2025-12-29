#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Auto-Formatter Hook (PostToolUse) - Runs formatters on edited files"""

import json
import sys
import subprocess
import os
from pathlib import Path

VERBOSE = True

def log(msg: str):
    if VERBOSE:
        print(f"[AutoFormatter] {msg}", file=sys.stderr)

def format_python(file_path):
    """Format Python files using ruff (fast) or black (fallback)."""
    formatters = [
        ['ruff', 'format', file_path],
        ['black', '-q', file_path],
    ]
    for cmd in formatters:
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=10)
            return cmd[0]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None

def format_javascript(file_path):
    """Format JS/TS files using prettier or eslint."""
    formatters = [
        ['prettier', '--write', '--log-level=silent', file_path],
        ['eslint', '--fix', '--quiet', file_path],
    ]
    for cmd in formatters:
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=10)
            return cmd[0]
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None

def format_rust(file_path):
    """Format Rust files using rustfmt."""
    try:
        subprocess.run(['rustfmt', file_path], check=True, capture_output=True, timeout=10)
        return 'rustfmt'
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None

def format_go(file_path):
    """Format Go files using gofmt."""
    try:
        subprocess.run(['gofmt', '-w', file_path], check=True, capture_output=True, timeout=10)
        return 'gofmt'
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None

def format_file(file_path):
    """Format file based on extension."""
    ext = Path(file_path).suffix.lower()

    formatters = {
        '.py': format_python,
        '.js': format_javascript,
        '.jsx': format_javascript,
        '.ts': format_javascript,
        '.tsx': format_javascript,
        '.rs': format_rust,
        '.go': format_go,
    }

    formatter_fn = formatters.get(ext)
    if formatter_fn and os.path.exists(file_path):
        return formatter_fn(file_path)
    return None

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get('tool_name', '')
    log(f"Checking: {tool}")

    if tool not in ['Write', 'Edit', 'MultiEdit']:
        log("⏭️ Skipped (not a write operation)")
        sys.exit(0)

    tool_input = data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if not file_path:
        sys.exit(0)

    formatter = format_file(file_path)

    if formatter:
        filename = os.path.basename(file_path)
        log(f"✨ Formatted {filename} with {formatter}")
        output = {"systemMessage": f"formatted {filename} with {formatter}"}
        print(json.dumps(output))
    else:
        log(f"⏭️ No formatter for {os.path.basename(file_path)}")

    sys.exit(0)

if __name__ == '__main__':
    main()
