#!/usr/bin/env python3
"""
RAG Reminder Hook
Suggests using /knowledge query when reading documentation
Execution time: <5ms (minimal overhead)
"""
import json
import sys

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool_name = data.get('tool_name', '')

    if tool_name != 'Read':
        sys.exit(0)

    file_path = data.get('tool_input', {}).get('file_path', '').lower()

    # Documentation patterns
    doc_patterns = [
        'readme', 'documentation', '/docs/', 'api-reference',
        'guide', 'tutorial', 'manual', '.md'
    ]

    # Check if reading documentation
    if any(pattern in file_path for pattern in doc_patterns):
        # Non-blocking reminder (allow with suggestion)
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "[TIP] RAG Reminder: Consider /knowledge query first (97% token savings). Allowing Read..."
            }
        }))

    sys.exit(0)

if __name__ == "__main__":
    main()
