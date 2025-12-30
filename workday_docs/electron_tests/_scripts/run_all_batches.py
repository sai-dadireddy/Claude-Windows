#!/usr/bin/env python3
"""
Run all batches to generate all 312 Payroll US test scenarios
"""

import subprocess
import sys

BATCH_SIZE = 20
TOTAL_SCENARIOS = 312

def main():
    print("=" * 80)
    print("PAYROLL US ELECTRON TEST GENERATION")
    print("=" * 80)
    print(f"Total scenarios: {TOTAL_SCENARIOS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Total batches: {(TOTAL_SCENARIOS + BATCH_SIZE - 1) // BATCH_SIZE}")
    print("=" * 80)

    batch_num = 1
    start_idx = 0

    while start_idx < TOTAL_SCENARIOS:
        print(f"\n\n{'#' * 80}")
        print(f"BATCH {batch_num} - Starting at index {start_idx}")
        print(f"{'#' * 80}")

        result = subprocess.run(
            ['python', 'generate_batch.py', str(BATCH_SIZE), str(start_idx)],
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print(f"ERROR in batch {batch_num}!")
            sys.exit(1)

        start_idx += BATCH_SIZE
        batch_num += 1

    print(f"\n\n{'=' * 80}")
    print("ALL BATCHES COMPLETED!")
    print(f"{'=' * 80}")

if __name__ == '__main__':
    main()
