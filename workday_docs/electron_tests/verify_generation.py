#!/usr/bin/env python3
"""
Verify Electron test generation results.
Provides detailed statistics and identifies issues.
"""

import os
from pathlib import Path
import re

OUTPUT_BASE = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"

AREAS = {
    "Inventory": {"folder": "Inventory", "expected": 313},
    "Asset Management": {"folder": "Asset_Management", "expected": 285}
}

def analyze_test_file(filepath):
    """Extract metadata from a test file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Extract key fields
        test_id = re.search(r'TEST ID:\s*(.+)', content)
        confidence = re.search(r'CONFIDENCE:\s*\[(\w+)\]\s*Score:\s*([\d.]+)', content)
        has_rag = '[NO RAG RESPONSE]' not in content
        is_manual = '[MANUAL]' in content or '[NO TASK SPECIFIED' in content

        return {
            'test_id': test_id.group(1).strip() if test_id else 'Unknown',
            'confidence': confidence.group(1) if confidence else 'Unknown',
            'score': float(confidence.group(2)) if confidence else 0.0,
            'has_rag': has_rag,
            'is_manual': is_manual,
            'size': len(content)
        }
    except Exception as e:
        return {
            'test_id': 'ERROR',
            'confidence': 'ERROR',
            'score': 0.0,
            'has_rag': False,
            'is_manual': True,
            'size': 0,
            'error': str(e)
        }

def verify_area(area_name, area_info):
    """Verify generation for a functional area."""
    folder_path = os.path.join(OUTPUT_BASE, area_info['folder'])

    print(f"\n{'='*80}")
    print(f"Verifying: {area_name}")
    print(f"Expected: {area_info['expected']} scenarios")
    print(f"Folder: {folder_path}")
    print(f"{'='*80}")

    if not os.path.exists(folder_path):
        print(f"✗ ERROR: Folder does not exist!")
        return None

    # Get all test files
    test_files = list(Path(folder_path).glob('*.txt'))
    actual_count = len(test_files)

    print(f"✓ Found {actual_count} test files")

    if actual_count == 0:
        print(f"✗ ERROR: No test files found!")
        return None

    # Analyze each file
    stats = {
        'total': actual_count,
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0,
        'manual': 0,
        'with_rag': 0,
        'errors': 0,
        'total_size': 0,
        'scores': []
    }

    issues = []

    for filepath in test_files:
        analysis = analyze_test_file(filepath)

        if 'error' in analysis:
            stats['errors'] += 1
            issues.append(f"ERROR reading {filepath.name}: {analysis['error']}")
            continue

        # Update stats
        conf = analysis['confidence']
        if conf in ['HIGH', 'MEDIUM', 'LOW']:
            stats[conf] += 1
        else:
            stats['errors'] += 1
            issues.append(f"Invalid confidence in {filepath.name}: {conf}")

        if analysis['is_manual']:
            stats['manual'] += 1

        if analysis['has_rag']:
            stats['with_rag'] += 1

        stats['total_size'] += analysis['size']
        stats['scores'].append(analysis['score'])

        # Check for issues
        if analysis['size'] < 200:
            issues.append(f"File too small: {filepath.name} ({analysis['size']} bytes)")

    # Calculate statistics
    avg_score = sum(stats['scores']) / len(stats['scores']) if stats['scores'] else 0
    avg_size = stats['total_size'] / stats['total'] if stats['total'] > 0 else 0

    # Print detailed stats
    print(f"\nConfidence Distribution:")
    print(f"  HIGH:     {stats['HIGH']:4d} ({stats['HIGH']/actual_count*100:5.1f}%)")
    print(f"  MEDIUM:   {stats['MEDIUM']:4d} ({stats['MEDIUM']/actual_count*100:5.1f}%)")
    print(f"  LOW:      {stats['LOW']:4d} ({stats['LOW']/actual_count*100:5.1f}%)")

    print(f"\nContent Analysis:")
    print(f"  With RAG Response:  {stats['with_rag']:4d} ({stats['with_rag']/actual_count*100:5.1f}%)")
    print(f"  Manual Required:    {stats['manual']:4d} ({stats['manual']/actual_count*100:5.1f}%)")
    print(f"  Average Score:      {avg_score:4.1f}/10")
    print(f"  Average File Size:  {avg_size:,.0f} bytes")

    if stats['errors'] > 0:
        print(f"\n✗ Errors Found: {stats['errors']}")

    # Coverage check
    coverage = (actual_count / area_info['expected']) * 100
    print(f"\nCoverage: {actual_count}/{area_info['expected']} ({coverage:.1f}%)")

    if coverage < 100:
        print(f"⚠ WARNING: Missing {area_info['expected'] - actual_count} test files")
    else:
        print(f"✓ Full coverage achieved!")

    # Print issues
    if issues:
        print(f"\nIssues Found ({len(issues)}):")
        for issue in issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")

    return stats

def main():
    """Main verification."""
    print("="*80)
    print("Electron Test Generation Verification")
    print("="*80)

    all_stats = {}
    total_files = 0
    total_expected = 0

    # Verify each area
    for area_name, area_info in AREAS.items():
        stats = verify_area(area_name, area_info)
        if stats:
            all_stats[area_name] = stats
            total_files += stats['total']
            total_expected += area_info['expected']

    # Overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)

    if not all_stats:
        print("✗ No valid results found!")
        return

    # Aggregate stats
    agg = {
        'total': total_files,
        'expected': total_expected,
        'HIGH': sum(s['HIGH'] for s in all_stats.values()),
        'MEDIUM': sum(s['MEDIUM'] for s in all_stats.values()),
        'LOW': sum(s['LOW'] for s in all_stats.values()),
        'manual': sum(s['manual'] for s in all_stats.values()),
        'with_rag': sum(s['with_rag'] for s in all_stats.values()),
        'errors': sum(s['errors'] for s in all_stats.values())
    }

    print(f"\nTotal Test Files: {agg['total']}/{agg['expected']} ({agg['total']/agg['expected']*100:.1f}%)")
    print(f"\nConfidence Distribution:")
    print(f"  HIGH:     {agg['HIGH']:4d} ({agg['HIGH']/agg['total']*100:5.1f}%)")
    print(f"  MEDIUM:   {agg['MEDIUM']:4d} ({agg['MEDIUM']/agg['total']*100:5.1f}%)")
    print(f"  LOW:      {agg['LOW']:4d} ({agg['LOW']/agg['total']*100:5.1f}%)")
    print(f"\nAutomation Readiness:")
    print(f"  Ready (HIGH):       {agg['HIGH']:4d}")
    print(f"  Needs Review (MED): {agg['MEDIUM']:4d}")
    print(f"  Manual (LOW):       {agg['LOW']:4d}")
    print(f"  No Task (MANUAL):   {agg['manual']:4d}")

    if agg['errors'] > 0:
        print(f"\n✗ Total Errors: {agg['errors']}")

    print(f"\n{'='*80}")

    # Quality assessment
    quality_score = (agg['HIGH'] * 1.0 + agg['MEDIUM'] * 0.6 + agg['LOW'] * 0.3) / agg['total'] * 100
    print(f"Quality Score: {quality_score:.1f}%")

    if quality_score >= 70:
        print("✓ EXCELLENT - High automation potential")
    elif quality_score >= 50:
        print("✓ GOOD - Moderate automation potential")
    else:
        print("⚠ FAIR - Requires significant manual enhancement")

    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
