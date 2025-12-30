#!/usr/bin/env python3
"""Check test generation status"""
import os
from pathlib import Path

base_dir = Path(__file__).parent

target_areas = {
    'Scheduling': 221,
    'Absence': 178,
    'Time_Tracking': 152
}

print("Test Generation Status\n" + "="*60)

total_expected = sum(target_areas.values())
total_found = 0

for area, expected in target_areas.items():
    area_dir = base_dir / area
    if area_dir.exists():
        files = list(area_dir.glob('*.spec.js'))
        count = len(files)
        total_found += count
        status = "OK" if count == expected else "..."
        print(f"{status} {area:20s}: {count:3d} / {expected:3d} files ({count/expected*100:5.1f}%)")

        # Show sample files
        if files:
            print(f"   Sample: {files[0].name}")
    else:
        print(f"X {area:20s}: Directory not found")

print(f"\n{'='*60}")
print(f"Total: {total_found} / {total_expected} files ({total_found/total_expected*100:5.1f}%)")

# Check for confidence distribution in generated files
if total_found > 0:
    print(f"\nChecking confidence levels in sample files...")
    confidence_stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'MANUAL': 0}

    for area in target_areas.keys():
        area_dir = base_dir / area
        if area_dir.exists():
            for test_file in list(area_dir.glob('*.spec.js'))[:5]:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'CONFIDENCE: HIGH' in content:
                        confidence_stats['HIGH'] += 1
                    elif 'CONFIDENCE: MEDIUM' in content:
                        confidence_stats['MEDIUM'] += 1
                    elif 'CONFIDENCE: LOW' in content:
                        confidence_stats['LOW'] += 1
                    elif 'CONFIDENCE: MANUAL' in content:
                        confidence_stats['MANUAL'] += 1

    print("\nSample Confidence Distribution (first 5 files per area):")
    for level, count in confidence_stats.items():
        if count > 0:
            print(f"  {level:8s}: {count:2d}")
