import os
from pathlib import Path
import re

output_dir = Path('Procurement')

# Count all files
all_files = list(output_dir.glob('*.txt'))
total_files = len(all_files)

# Analyze files
high_conf = 0
medium_conf = 0
low_conf = 0
manual_required = 0

for filepath in all_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '[MANUAL REQUIRED]' in content:
        manual_required += 1
    elif '[HIGH]' in content:
        high_conf += 1
    elif '[MEDIUM]' in content:
        medium_conf += 1
    elif '[LOW]' in content:
        low_conf += 1

print("="*80)
print("PROCUREMENT ELECTRON TEST GENERATION - SUMMARY REPORT")
print("="*80)
print(f"\nTotal Test Files Generated: {total_files}")
print(f"\nConfidence Distribution:")
print(f"  HIGH Confidence:    {high_conf:3d} ({high_conf/total_files*100:.1f}%)")
print(f"  MEDIUM Confidence:  {medium_conf:3d} ({medium_conf/total_files*100:.1f}%)")
print(f"  LOW Confidence:     {low_conf:3d} ({low_conf/total_files*100:.1f}%)")
print(f"  MANUAL Required:    {manual_required:3d} ({manual_required/total_files*100:.1f}%)")
print(f"\nOutput Directory: {output_dir.absolute()}")
print("="*80)

# Show sample files
print("\nSample Generated Files:")
print("-"*80)
for f in sorted(all_files)[:10]:
    print(f"  {f.name}")

print("\n" + "="*80)
print("GENERATION COMPLETE - Ready for Electron automation")
print("="*80)
