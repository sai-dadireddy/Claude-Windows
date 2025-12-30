#!/usr/bin/env python3
import os
import glob

dirs = {
    'Payroll_France': 112,
    'Payroll_UK': 202,
    'Payroll_Interface': 35
}

print("=" * 70)
print("PAYROLL ELECTRON TEST GENERATION STATUS")
print("=" * 70)

total_expected = sum(dirs.values())
total_generated = 0

for dir_name, expected in dirs.items():
    if os.path.exists(dir_name):
        files = glob.glob(f"{dir_name}/*.txt")
        count = len(files)
        total_generated += count
        status = "✓ COMPLETE" if count == expected else f"⏳ IN PROGRESS ({count}/{expected})"
        print(f"{dir_name:25} {count:3}/{expected:3} files  {status}")
    else:
        print(f"{dir_name:25}   NOT STARTED")

print("=" * 70)
print(f"TOTAL: {total_generated}/{total_expected} files generated")
print(f"Progress: {(total_generated/total_expected)*100:.1f}%")
print("=" * 70)
