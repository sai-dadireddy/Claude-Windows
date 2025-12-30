#!/usr/bin/env python3
"""
Batch runner for generating Electron tests for 4 modules
- Expenses (142)
- Tax (120)
- Revenue Management (126)
- Advanced Compensation (127)
"""

import subprocess
import sys
import os
from pathlib import Path

# Change to script directory
os.chdir(Path(__file__).parent)

MODULES = [
    {
        'name': 'Expenses',
        'script': 'generate_expenses_tests.py',
        'expected': 142
    },
    {
        'name': 'Tax',
        'script': 'generate_tax_tests.py',
        'expected': 120
    },
    {
        'name': 'Revenue Management',
        'script': 'generate_revenue_tests.py',
        'expected': 126
    },
    {
        'name': 'Advanced Compensation',
        'script': 'generate_advcomp_tests.py',
        'expected': 127
    }
]

def run_generator(module):
    """Run generator for a module"""
    print("\n" + "=" * 80)
    print(f"STARTING: {module['name']}")
    print(f"Expected scenarios: {module['expected']}")
    print("=" * 80)

    try:
        result = subprocess.run(
            [sys.executable, module['script']],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        print(result.stdout)

        if result.returncode != 0:
            print(f"\nERROR in {module['name']}:")
            print(result.stderr)
            return False

        return True

    except subprocess.TimeoutExpired:
        print(f"\nTIMEOUT: {module['name']} took longer than 1 hour")
        return False
    except Exception as e:
        print(f"\nEXCEPTION in {module['name']}: {str(e)}")
        return False

def main():
    """Main batch runner"""
    print("=" * 80)
    print("WORKDAY ELECTRON TEST BATCH GENERATOR")
    print("=" * 80)
    print(f"Modules to process: {len(MODULES)}")
    print(f"Total scenarios: {sum(m['expected'] for m in MODULES)}")
    print()

    results = []

    for module in MODULES:
        success = run_generator(module)
        results.append({
            'module': module['name'],
            'success': success
        })

    # Print summary
    print("\n" + "=" * 80)
    print("BATCH GENERATION COMPLETE")
    print("=" * 80)

    for result in results:
        status = "✓ SUCCESS" if result['success'] else "✗ FAILED"
        print(f"{status}: {result['module']}")

    print()
    successful = sum(1 for r in results if r['success'])
    print(f"Modules completed: {successful}/{len(MODULES)}")
    print("=" * 80)

    # Exit with error if any failed
    if successful < len(MODULES):
        sys.exit(1)

if __name__ == '__main__':
    main()
