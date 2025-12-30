#!/usr/bin/env python3
"""Check status of test generation"""

import os
from pathlib import Path

BASE = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests'

TARGET_MODULES = {
    'Talent_Optimization': 203,
    'Talent_Acquisition': 114,
    'Learning': 146,
    'Learning_Extended': 59
}

print("=" * 80)
print("Test Generation Status Check")
print("=" * 80)

for folder, expected in TARGET_MODULES.items():
    path = Path(BASE) / folder
    if path.exists():
        files = list(path.glob("*.txt"))
        count = len(files)
        pct = (count / expected * 100) if expected > 0 else 0
        status = "✓" if count == expected else "⚠" if count > 0 else "✗"
        print(f"{status} {folder:25s}: {count:3d}/{expected:3d} files ({pct:.1f}%)")
    else:
        print(f"✗ {folder:25s}: Directory not found")

print("=" * 80)
