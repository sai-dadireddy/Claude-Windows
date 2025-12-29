#!/usr/bin/env python
"""
Token Guard Hook - Prevents Runaway Token Consumption
Adds deliberate friction for expensive operations

Based on industry best practice: "deliberate friction so you can understand
what Claude is doing and veto misguided approaches before it burns through
millions of tokens chasing the wrong solution"
"""

import sys
import json
import os

def should_warn(tool_name, tool_input):
    """Determine if operation should trigger warning"""

    # Read operations
    if tool_name == "Read":
        # No warning for single reads
        return False

    # Multiple file operations
    if tool_name in ["Glob", "Grep"]:
        # Check if result might be large
        tool_str = json.dumps(tool_input)
        if "**/*" in tool_str or "*.*" in tool_str:
            return True

    # Write operations to important files
    if tool_name in ["Write", "Edit"]:
        file_path = tool_input.get("file_path", "")
        sensitive_files = [
            "settings.json",
            "CLAUDE.md",
            "package.json",
            ".gitignore"
        ]
        if any(f in file_path for f in sensitive_files):
            return True

    return False

def main():
    """Main hook execution"""

    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except:
        # If no input, allow operation
        sys.exit(0)

    tool_name = hook_input.get("toolName", "")
    tool_input_data = hook_input.get("toolInput", {})

    # Check if we should warn
    if should_warn(tool_name, tool_input_data):
        # Print warning to stderr (shows to user)
        print(f"[WARN]  Token Guard: {tool_name} operation on potentially large dataset", file=sys.stderr)
        print(f"   This may consume significant tokens. Proceeding...", file=sys.stderr)

    # Always allow operation (non-blocking warning)
    sys.exit(0)

if __name__ == "__main__":
    main()
