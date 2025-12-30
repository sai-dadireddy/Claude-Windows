#!/usr/bin/env python3
"""Summarize Benefits test generation results"""
import os
import re
from pathlib import Path

BENEFITS_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Benefits"

def main():
    files = list(Path(BENEFITS_DIR).glob("*.txt"))

    stats = {
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0,
        'MANUAL': 0
    }

    for f in files:
        content = f.read_text(encoding='utf-8')

        if 'STATUS: [MANUAL REQUIRED]' in content:
            stats['MANUAL'] += 1
        elif match := re.search(r'CONFIDENCE: \[(HIGH|MEDIUM|LOW)\]', content):
            stats[match.group(1)] += 1

    print("="*80)
    print("BENEFITS TEST GENERATION - FINAL SUMMARY")
    print("="*80)
    print(f"Total Scenarios Processed: {len(files)}")
    print()
    print("Confidence Distribution:")
    print(f"  [HIGH] Confidence (>= 7.5):    {stats['HIGH']}")
    print(f"  [MEDIUM] Confidence (5-7.4):   {stats['MEDIUM']}")
    print(f"  [LOW] Confidence (< 5.0):      {stats['LOW']}")
    print(f"  [MANUAL] Required:             {stats['MANUAL']}")
    print()
    print(f"Output Directory: {BENEFITS_DIR}")
    print("="*80)

if __name__ == "__main__":
    main()
