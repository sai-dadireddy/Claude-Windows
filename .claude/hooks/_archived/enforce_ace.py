#!/usr/bin/env python3
"""
ACE Enforcement Hook - Makes Smart Router Visible to Claude
Purpose: Inject routing suggestions DIRECTLY into Claude's context
Priority: Run FIRST in UserPromptSubmit hook chain

Output Format: JSON with systemMessage (Claude Code v1.0.64+)
"""

import sys
import json
import os

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    try:
        # Read JSON input from stdin
        input_data = {}
        try:
            input_data = json.load(sys.stdin)
        except:
            pass
        
        prompt = input_data.get('prompt', '') or input_data.get('message', '')
        if not prompt:
            print(json.dumps({}))
            return 0

        # Check task type
        prompt_lower = prompt.lower()
        
        is_implementation = any(word in prompt_lower for word in [
            'create', 'implement', 'write', 'add', 'build', 'generate',
            'component', 'function', 'class', 'file'
        ])

        is_multi_file = any(word in prompt_lower for word in [
            'all', 'multiple', 'several', 'batch', 'many'
        ]) or prompt.count('and') > 2

        is_frontend = any(word in prompt_lower for word in [
            'ui', 'component', 'react', 'next.js', 'frontend', 'tsx', 'jsx'
        ])

        # Generate suggestions (ASCII-safe)
        suggestions = []

        if is_implementation:
            if is_frontend:
                suggestions.append("[!] FRONTEND: Delegate to GLM-4.6 (better at frontend)")
            else:
                suggestions.append("[i] IMPL: Consider GLM-4.6 (1/7th cost)")

        if is_multi_file:
            suggestions.append("[i] MULTI-FILE: Use parallel haiku agents (3-5x faster)")

        # Output as JSON with systemMessage
        if suggestions:
            print(json.dumps({
                "systemMessage": " | ".join(suggestions)
            }))
        else:
            print(json.dumps({}))

        return 0

    except Exception as e:
        # Never fail - output empty JSON
        print(json.dumps({}))
        return 0

if __name__ == "__main__":
    sys.exit(main())
