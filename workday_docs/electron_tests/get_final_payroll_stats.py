#!/usr/bin/env python3
"""
Check final status of Payroll test generation
"""
import os
import glob
import re

# Expected counts
EXPECTED = {
    'Payroll_France': 112,
    'Payroll_UK': 202,
    'Payroll_Interface': 35
}

def count_by_confidence(directory):
    """Count files by confidence level"""
    high = 0
    medium = 0
    manual = 0

    for filepath in glob.glob(f"{directory}/*.txt"):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Read first 500 chars
            if 'CONFIDENCE: [HIGH]' in content:
                high += 1
            elif 'CONFIDENCE: [MEDIUM]' in content or 'NEEDS SME REVIEW' in content:
                medium += 1
            elif 'MANUAL REQUIRED' in content:
                manual += 1

    return high, medium, manual

print("=" * 80)
print("PAYROLL ELECTRON TEST GENERATION - FINAL SUMMARY")
print("=" * 80)
print()

total_expected = sum(EXPECTED.values())
total_generated = 0
total_high = 0
total_medium = 0
total_manual = 0

for dir_name, expected in EXPECTED.items():
    if os.path.exists(dir_name):
        files = glob.glob(f"{dir_name}/*.txt")
        count = len(files)
        total_generated += count

        high, medium, manual = count_by_confidence(dir_name)
        total_high += high
        total_medium += medium
        total_manual += manual

        print(f"{dir_name}")
        print(f"  Total files:      {count}/{expected}")
        print(f"  High confidence:  {high}")
        print(f"  Medium (review):  {medium}")
        print(f"  Manual required:  {manual}")
        print()
    else:
        print(f"{dir_name}: NOT FOUND")
        print()

print("=" * 80)
print("OVERALL TOTALS")
print("=" * 80)
print(f"Expected:         {total_expected} scenarios")
print(f"Generated:        {total_generated} files ({(total_generated/total_expected)*100:.1f}%)")
print(f"  High confidence:   {total_high} ({(total_high/total_generated)*100:.1f}%)")
print(f"  Medium (review):   {total_medium} ({(total_medium/total_generated)*100:.1f}%)")
print(f"  Manual required:   {total_manual} ({(total_manual/total_generated)*100:.1f}%)")
print()

# Quality metrics
ready_for_automation = total_high
needs_review = total_medium
needs_sme_input = total_manual

print("=" * 80)
print("READINESS METRICS")
print("=" * 80)
print(f"✓ Ready for Electron:         {ready_for_automation} tests")
print(f"⚠ Needs SME review:           {needs_review} tests")
print(f"✗ Requires manual creation:   {needs_sme_input} tests")
print()
print(f"Automation-ready rate: {(ready_for_automation/total_generated)*100:.1f}%")
print("=" * 80)
