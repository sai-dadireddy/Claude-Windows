#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Code Quality Validator Hook (PostToolUse) - Enforces code standards"""

import json
import sys
import os
import re
from pathlib import Path

VERBOSE = False

def log(msg: str):
    if VERBOSE:
        print(f"[CodeQuality] {msg}", file=sys.stderr)

# Configuration - adjust as needed
CONFIG = {
    'max_function_length': 50,   # lines per function
    'max_file_length': 300,      # lines per file
    'max_line_length': 120,      # characters per line
    'max_nesting_depth': 4,      # indentation levels
}

def get_file_type(filepath):
    """Determine file type from extension."""
    ext = Path(filepath).suffix.lower()
    return {
        '.py': 'python',
        '.js': 'javascript', '.jsx': 'javascript',
        '.ts': 'typescript', '.tsx': 'typescript',
        '.go': 'go', '.rs': 'rust', '.rb': 'ruby',
    }.get(ext, 'unknown')

def check_file_length(lines):
    """Check if file is too long."""
    max_len = CONFIG['max_file_length']
    if len(lines) > max_len:
        return [f"File has {len(lines)} lines (max: {max_len})"]
    return []

def check_line_length(lines):
    """Check for lines that are too long."""
    violations = []
    max_len = CONFIG['max_line_length']

    for i, line in enumerate(lines, 1):
        # Skip URLs and long strings
        if 'http://' in line or 'https://' in line:
            continue

        length = len(line.rstrip())
        if length > max_len:
            violations.append(f"Line {i}: {length} chars (max: {max_len})")

    return violations[:5]  # Limit to 5 violations

def check_nesting_depth(lines, file_type):
    """Check for excessive nesting."""
    violations = []
    max_nest = CONFIG['max_nesting_depth']
    divisor = 4 if file_type == 'python' else 2

    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        nest = indent // divisor

        if nest > max_nest:
            violations.append(f"Line {i}: nesting depth {nest} (max: {max_nest})")

    return violations[:5]

def check_python_functions(lines):
    """Check Python function lengths."""
    violations = []
    max_len = CONFIG['max_function_length']
    func_pattern = re.compile(r'^\s*(?:async\s+)?def\s+(\w+)')

    in_func = False
    func_start = 0
    func_name = ""

    for i, line in enumerate(lines, 1):
        match = func_pattern.match(line)
        if match:
            # Check previous function
            if in_func and func_name:
                length = i - func_start
                if length > max_len:
                    violations.append(
                        f"Function '{func_name}' at line {func_start}: "
                        f"{length} lines (max: {max_len})"
                    )
            # Start new function
            func_name = match.group(1)
            func_start = i
            in_func = True

    # Check last function
    if in_func and func_name:
        length = len(lines) - func_start + 1
        if length > max_len:
            violations.append(
                f"Function '{func_name}' at line {func_start}: "
                f"{length} lines (max: {max_len})"
            )

    return violations[:5]

def check_js_functions(lines):
    """Check JavaScript/TypeScript function lengths."""
    violations = []
    max_len = CONFIG['max_function_length']

    func_pattern = re.compile(
        r'^\s*(function|const|let|var|export|async)\s+(\w+)\s*(\(|=.*\()'
    )

    in_func = False
    func_start = 0
    func_name = ""
    braces = 0

    for i, line in enumerate(lines, 1):
        if not in_func:
            match = func_pattern.match(line)
            if match:
                in_func = True
                func_start = i
                func_name = match.group(2)
                braces = line.count('{') - line.count('}')
        else:
            braces += line.count('{') - line.count('}')
            if braces <= 0 and '{' in ''.join(lines[func_start-1:i]):
                length = i - func_start + 1
                if length > max_len:
                    violations.append(
                        f"Function '{func_name}' at line {func_start}: "
                        f"{length} lines (max: {max_len})"
                    )
                in_func = False

    return violations[:5]

def validate_file(filepath):
    """Validate a single file."""
    if not os.path.exists(filepath):
        return []

    file_type = get_file_type(filepath)
    if file_type == 'unknown':
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return []

    violations = []
    violations.extend(check_file_length(lines))
    violations.extend(check_line_length(lines))
    violations.extend(check_nesting_depth(lines, file_type))

    if file_type == 'python':
        violations.extend(check_python_functions(lines))
    elif file_type in ['javascript', 'typescript']:
        violations.extend(check_js_functions(lines))

    return violations

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get('tool_name', '')
    log(f"Checking: {tool}")

    if tool not in ['Write', 'Edit', 'MultiEdit']:
        log("[END]️ Skipped (not a write operation)")
        sys.exit(0)

    tool_input = data.get('tool_input', {})
    filepath = tool_input.get('file_path', '')

    if not filepath:
        sys.exit(0)

    violations = validate_file(filepath)

    if violations:
        filename = os.path.basename(filepath)
        violation_list = '\n'.join(f"  - {v}" for v in violations[:5])
        msg = f"Code quality issues in {filename}:\n{violation_list}"
        log(f"[WARN] {len(violations)} issue(s) in {filename}")

        output = {"systemMessage": f"Code quality: {len(violations)} issue(s) in {filename}"}
        print(json.dumps(output))
    else:
        log(f"[OK] No issues in {os.path.basename(filepath)}")

    sys.exit(0)

if __name__ == '__main__':
    main()
