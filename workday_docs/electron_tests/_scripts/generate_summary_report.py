#!/usr/bin/env python3
"""
Generate comprehensive summary report for Electron test generation
"""
import os
import json
from pathlib import Path
from collections import defaultdict
import re

def analyze_test_file(test_file: Path) -> dict:
    """Extract metadata from a test file"""
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract confidence
    confidence_match = re.search(r'CONFIDENCE: (\w+)', content)
    confidence = confidence_match.group(1) if confidence_match else 'UNKNOWN'

    # Extract reasoning
    reasoning_match = re.search(r'REASONING: (.+)', content)
    reasoning = reasoning_match.group(1) if reasoning_match else 'N/A'

    # Extract scenario info
    scenario_id_match = re.search(r'Electron Test: (\S+) -', content)
    scenario_id = scenario_id_match.group(1) if scenario_id_match else test_file.stem

    task_match = re.search(r'Task/Step: (.+)', content)
    task = task_match.group(1) if task_match else 'N/A'

    return {
        'scenario_id': scenario_id,
        'confidence': confidence,
        'reasoning': reasoning,
        'task': task,
        'file': test_file.name
    }

def generate_report():
    """Generate summary report"""
    base_dir = Path(__file__).parent

    target_areas = {
        'Scheduling': 221,
        'Absence': 178,
        'Time_Tracking': 152
    }

    report_lines = []
    report_lines.append("="*80)
    report_lines.append("ELECTRON TEST GENERATION SUMMARY REPORT")
    report_lines.append(f"Generated: {Path(__file__).parent.name}")
    report_lines.append("="*80)
    report_lines.append("")

    all_stats = defaultdict(lambda: defaultdict(int))
    all_tests = []

    for area, expected_count in target_areas.items():
        area_dir = base_dir / area
        if not area_dir.exists():
            report_lines.append(f"❌ {area}: Directory not found")
            continue

        test_files = list(area_dir.glob('*.spec.js'))
        actual_count = len(test_files)

        report_lines.append(f"\n{'='*80}")
        report_lines.append(f"FUNCTIONAL AREA: {area}")
        report_lines.append(f"{'='*80}")
        report_lines.append(f"Expected: {expected_count} scenarios")
        report_lines.append(f"Generated: {actual_count} tests ({actual_count/expected_count*100:.1f}%)")

        if actual_count == 0:
            report_lines.append("⚠️  No tests generated")
            continue

        # Analyze all tests in this area
        confidence_stats = defaultdict(list)

        for test_file in sorted(test_files):
            try:
                test_info = analyze_test_file(test_file)
                confidence_stats[test_info['confidence']].append(test_info)
                all_stats[area][test_info['confidence']] += 1
                all_tests.append({**test_info, 'area': area})
            except Exception as e:
                report_lines.append(f"⚠️  Error analyzing {test_file.name}: {e}")

        # Confidence distribution for this area
        report_lines.append(f"\nConfidence Distribution:")
        for level in ['HIGH', 'MEDIUM', 'LOW', 'MANUAL', 'UNKNOWN']:
            count = len(confidence_stats.get(level, []))
            if count > 0:
                pct = count / actual_count * 100
                report_lines.append(f"  {level:8s}: {count:3d} ({pct:5.1f}%)")

        # Sample tests by confidence
        for level in ['HIGH', 'MEDIUM', 'LOW']:
            samples = confidence_stats.get(level, [])[:3]
            if samples:
                report_lines.append(f"\n  Sample {level} Confidence Tests:")
                for sample in samples:
                    report_lines.append(f"    • {sample['scenario_id']}: {sample['task']}")

        # Manual tests
        manual_tests = confidence_stats.get('MANUAL', [])
        if manual_tests:
            report_lines.append(f"\n  ⚠️  {len(manual_tests)} MANUAL tests require SME review:")
            for test in manual_tests[:5]:
                report_lines.append(f"    • {test['scenario_id']}: {test['task']}")
            if len(manual_tests) > 5:
                report_lines.append(f"    ... and {len(manual_tests) - 5} more")

    # Overall summary
    report_lines.append(f"\n\n{'='*80}")
    report_lines.append("OVERALL SUMMARY")
    report_lines.append(f"{'='*80}")

    total_expected = sum(target_areas.values())
    total_generated = len(all_tests)
    report_lines.append(f"\nTotal Expected: {total_expected} scenarios")
    report_lines.append(f"Total Generated: {total_generated} tests ({total_generated/total_expected*100:.1f}%)")

    # Overall confidence distribution
    overall_confidence = defaultdict(int)
    for test in all_tests:
        overall_confidence[test['confidence']] += 1

    report_lines.append(f"\nOverall Confidence Distribution:")
    for level in ['HIGH', 'MEDIUM', 'LOW', 'MANUAL', 'UNKNOWN']:
        count = overall_confidence.get(level, 0)
        if count > 0:
            pct = count / total_generated * 100 if total_generated > 0 else 0
            report_lines.append(f"  {level:8s}: {count:3d} ({pct:5.1f}%)")

    # Recommendations
    report_lines.append(f"\n{'='*80}")
    report_lines.append("RECOMMENDATIONS")
    report_lines.append(f"{'='*80}")

    manual_count = overall_confidence.get('MANUAL', 0)
    low_count = overall_confidence.get('LOW', 0)

    if manual_count > 0:
        report_lines.append(f"\n⚠️  {manual_count} scenarios marked MANUAL:")
        report_lines.append("   → Review task/step definitions")
        report_lines.append("   → Enhance RAG knowledge base")
        report_lines.append("   → Add KB articles for common tasks")

    if low_count > 0:
        report_lines.append(f"\n⚠️  {low_count} scenarios with LOW confidence:")
        report_lines.append("   → RAG found limited guidance")
        report_lines.append("   → May need SME verification")
        report_lines.append("   → Consider adding detailed KB articles")

    high_count = overall_confidence.get('HIGH', 0)
    if high_count > 0:
        report_lines.append(f"\n✅ {high_count} scenarios with HIGH confidence:")
        report_lines.append("   → These tests can proceed to implementation")

    # Output files
    report_lines.append(f"\n{'='*80}")
    report_lines.append("OUTPUT LOCATIONS")
    report_lines.append(f"{'='*80}")

    for area in target_areas.keys():
        area_dir = base_dir / area
        if area_dir.exists():
            report_lines.append(f"\n{area}:")
            report_lines.append(f"  {area_dir.absolute()}")
            count = len(list(area_dir.glob('*.spec.js')))
            report_lines.append(f"  {count} test files")

    # Save report
    report_content = "\n".join(report_lines)
    report_file = base_dir / 'GENERATION_REPORT.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(report_content)
    print(f"\n\nReport saved to: {report_file}")

    # Save detailed JSON
    json_file = base_dir / 'test_generation_details.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_expected': total_expected,
                'total_generated': total_generated,
                'completion_pct': round(total_generated/total_expected*100, 2) if total_expected > 0 else 0
            },
            'by_area': dict(all_stats),
            'tests': all_tests
        }, f, indent=2)

    print(f"Details saved to: {json_file}")

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    generate_report()
