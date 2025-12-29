#!/usr/bin/env python3
"""
Build Checker Hook (Stop Event)
Runs after Claude finishes responding - checks for build errors
Execution time: <2 seconds per repo
Based on diet103's approach
"""
import json
import sys
import subprocess
from pathlib import Path

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    # Get current directory
    cwd = data.get('cwd', '')

    if not cwd:
        sys.exit(0)

    cwd_path = Path(cwd)

    # Check if package.json exists (Node.js project)
    package_json = cwd_path / 'package.json'

    if not package_json.exists():
        # Not a Node.js project, skip
        sys.exit(0)

    try:
        # Run build/typecheck
        # Try tsc first (fast type check)
        result = subprocess.run(
            ['npx', 'tsc', '--noEmit'],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            # TypeScript errors found!
            error_lines = result.stderr.split('\n')
            error_count = len([l for l in error_lines if 'error TS' in l])

            if error_count > 0:
                message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SIREN] BUILD CHECK: {error_count} TypeScript Error(s) Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{result.stderr[:1000]}

These errors need to be fixed before proceeding!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                # Send to stdout so Claude sees it
                print(message)

    except subprocess.TimeoutExpired:
        print("Build check timed out (>30s)")
    except FileNotFoundError:
        # tsc not available, skip
        pass
    except Exception as e:
        # Don't block on errors
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
