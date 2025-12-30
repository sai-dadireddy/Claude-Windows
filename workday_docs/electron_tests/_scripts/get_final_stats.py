#!/usr/bin/env python3
"""Get final statistics from generated HCM test files"""

import re
from pathlib import Path
from collections import Counter

OUTPUT_DIR = Path("HCM")

def parse_file(filepath):
    """Extract metadata from a test file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {
        'file': filepath.name,
        'type': None,
        'confidence': None,
        'score': None
    }

    # Check if MANUAL
    if 'STATUS: [MANUAL REQUIRED]' in content:
        metadata['type'] = 'MANUAL'
        return metadata

    # Extract confidence
    conf_match = re.search(r'CONFIDENCE: \[(HIGH|MEDIUM|LOW)\] Score: ([\d.]+)/10', content)
    if conf_match:
        metadata['type'] = 'GENERATED'
        metadata['confidence'] = conf_match.group(1)
        metadata['score'] = float(conf_match.group(2))

    return metadata

def main():
    print("=" * 80)
    print("HCM ELECTRON TEST GENERATION - FINAL STATISTICS")
    print("=" * 80)
    print()

    # Get all files
    files = list(OUTPUT_DIR.glob("*.txt"))
    total = len(files)

    print(f"Total files generated: {total}")
    print()

    # Parse all files
    stats = {
        'total': total,
        'generated': 0,
        'manual': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
        'scores': []
    }

    for filepath in files:
        meta = parse_file(filepath)

        if meta['type'] == 'MANUAL':
            stats['manual'] += 1
        elif meta['type'] == 'GENERATED':
            stats['generated'] += 1
            if meta['confidence'] == 'HIGH':
                stats['high'] += 1
            elif meta['confidence'] == 'MEDIUM':
                stats['medium'] += 1
            elif meta['confidence'] == 'LOW':
                stats['low'] += 1

            if meta['score']:
                stats['scores'].append(meta['score'])

    # Print summary
    print("BREAKDOWN:")
    print(f"  Generated tests:     {stats['generated']}")
    print(f"    - High confidence: {stats['high']}")
    print(f"    - Medium confidence: {stats['medium']}")
    print(f"    - Low confidence:  {stats['low']}")
    print(f"  Manual required:     {stats['manual']}")
    print()

    if stats['scores']:
        avg_score = sum(stats['scores']) / len(stats['scores'])
        print(f"Average confidence score: {avg_score:.2f}/10")
        print()

    # Success rate
    if total > 0:
        success_rate = (stats['generated'] / total) * 100
        high_quality_rate = (stats['high'] / total) * 100
        print(f"Generation success rate: {success_rate:.1f}%")
        print(f"High quality rate (>= 7.0): {high_quality_rate:.1f}%")
        print()

    print("=" * 80)
    print("SAMPLE FILES:")
    print("=" * 80)

    # Show samples
    for filepath in sorted(files)[:5]:
        print(f"  {filepath.name}")
    print(f"  ... ({total - 5} more)")
    print()

    print("=" * 80)
    print(f"Output location: {OUTPUT_DIR.resolve()}")
    print("=" * 80)

if __name__ == "__main__":
    main()
