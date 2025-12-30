#!/usr/bin/env python3
"""Generate Electron tests for Advanced_Compensation, Data_Management_FIN, Data_Management_HCM"""

import json
import os
import sys
import re
import subprocess
from pathlib import Path

def query_rag(task):
    """Query RAG system"""
    try:
        rag_script = Path(__file__).parent.parent / 'workday_rag.py'
        result = subprocess.run(
            [sys.executable, str(rag_script), task],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout

        # Extract confidence score
        score_match = re.search(r'score:\s*(\d+)', output, re.IGNORECASE)
        if score_match:
            confidence = float(score_match.group(1))
        elif len(output) > 100:
            confidence = 6.0
        else:
            confidence = 3.0

        return output, confidence
    except Exception as e:
        return f"Error: {e}", 0.0

def extract_task_name(task_step):
    """Extract clean task name from Task/Step column"""
    if not task_step or str(task_step) == 'nan':
        return ""

    task = str(task_step).strip()

    # Extract from "Search bar: 'term'"
    if "Search bar:" in task:
        match = re.search(r"['\"]([^'\"]+)['\"]", task)
        if match:
            return match.group(1)

    # Get first line
    lines = task.split('\n')
    if lines:
        first = lines[0].strip()
        first = re.sub(r'^-\s*', '', first)
        first = re.sub(r'^Go to\s+', '', first, flags=re.IGNORECASE)
        return first[:100]

    return task[:100]

def generate_electron_steps(scenario, task, task_full, rag_result, confidence):
    """Generate Electron test steps"""
    steps = []

    if confidence >= 7.0:
        # HIGH CONFIDENCE - Valid Electron commands only
        if "Search bar:" in task_full:
            match = re.search(r"['\"]([^'\"]+)['\"]", task_full)
            if match:
                search_term = match.group(1)
                steps.append(f'enter search box as "{search_term}"')
                steps.append('wait for search results')

                # Look for what to click
                click_match = re.search(r'Click (?:on )?(?:the )?([^.]+)', task_full)
                if click_match:
                    click_text = click_match.group(1).strip()
                    steps.append(f'click "{click_text}"')
                else:
                    steps.append(f'click search result containing "{search_term}"')
            else:
                steps.append(f'enter search box as "{task}"')
                steps.append('wait for search results')
                steps.append('click search result')
        elif "Go to" in task_full or "Navigate to" in task_full:
            nav_match = re.search(r'(?:Go to|Navigate to)\s+([^\n]+)', task_full)
            if nav_match:
                nav_path = nav_match.group(1).strip()
                steps.append(f'navigate to "{nav_path}"')
            else:
                steps.append(f'enter search box as "{task}"')
                steps.append('wait for search results')
                steps.append('click search result')
        else:
            steps.append(f'enter search box as "{task}"')
            steps.append('wait for search results')
            steps.append(f'click search result containing "{task}"')

        steps.append('wait for page to load')

        # Verification
        expected = scenario.get('Customer Expected Result', '')
        if expected and str(expected) != 'nan':
            steps.append(f'verify {expected}')

        # Screenshot
        scenario_id = scenario.get('Scenario ID', 'test')
        steps.append(f'screenshot as "{scenario_id}_complete.png"')

    elif confidence >= 5.0:
        # MEDIUM CONFIDENCE - Needs SME review
        steps.append(f'[NEEDS SME REVIEW - Confidence: {confidence:.1f}/10]')
        steps.append('')
        steps.append(f'# Task: {task}')
        steps.append('')

        if "Search bar:" in task_full:
            match = re.search(r"['\"]([^'\"]+)['\"]", task_full)
            if match:
                steps.append(f'enter search box as "{match.group(1)}"')
                steps.append('wait for search results')
                steps.append('# [SME: Verify exact element to click]')
        else:
            steps.append(f'enter search box as "{task}"')
            steps.append('wait for search results')
            steps.append('# [SME: Verify exact search result text]')

        steps.append('')
        steps.append('# SME ACTION REQUIRED:')
        steps.append('# 1. Verify field names and interactions')
        steps.append('# 2. Add missing validation steps')
        steps.append('# 3. Update confidence score when complete')

    else:
        # LOW CONFIDENCE - Manual required
        steps.append('[MANUAL REQUIRED - Insufficient KB coverage]')
        steps.append(f'Confidence Score: {confidence:.1f}/10')
        steps.append('')
        steps.append('RAG Results:')
        steps.append(rag_result[:500] if rag_result else 'No relevant documentation found')

    return steps

def generate_test_file(scenario, output_dir):
    """Generate complete test file"""
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')
    functional_area = scenario.get('Functional Area', '')
    scenario_name = scenario.get('Scenario Name', '')
    task_step = scenario.get('Task / Step', '')
    description = scenario.get('Scenario Description', '')
    expected_result = scenario.get('Customer Expected Result', '')
    effort_mins = scenario.get('Est. Effort (mins)', '')
    role = scenario.get('Workday Role', '')

    # Extract task
    task = extract_task_name(task_step)
    if not task:
        print(f"  ⚠️  {scenario_id}: INCOMPLETE - Missing Task/Step")
        return None

    # Query RAG
    print(f"  {scenario_id}: {task[:60]}...")
    rag_result, confidence = query_rag(task)

    # Determine status
    if confidence >= 7.0:
        status = "✅ ACCEPTED"
        status_code = 'accepted'
    elif confidence >= 5.0:
        status = "⚠️ NEEDS REVIEW"
        status_code = 'review'
    else:
        status = "❌ MANUAL"
        status_code = 'manual'

    print(f"    {status} (Confidence: {confidence:.1f}/10)")

    # Generate steps
    steps = generate_electron_steps(scenario, task, task_step, rag_result, confidence)

    # Create filename
    filename = f"{scenario_id}.txt"
    filepath = output_dir / filename

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"TEST ID: {scenario_id}\n")
        f.write(f"FUNCTIONAL AREA: {functional_area}\n")
        f.write(f"TEST NAME: {scenario_name}\n")
        f.write(f"WORKDAY ROLE: {role}\n")
        f.write(f"EST. DURATION: {effort_mins} minutes\n")
        f.write(f"CONFIDENCE SCORE: {confidence:.1f}/10\n")
        f.write(f"STATUS: {status}\n")
        f.write("=" * 80 + "\n\n")

        f.write("DESCRIPTION:\n")
        f.write(f"{description}\n\n")

        f.write("TASK/STEP:\n")
        f.write(f"{task_step}\n\n")

        f.write("PREREQUISITES:\n")
        f.write(f"- User logged in with {role} permissions\n")
        f.write(f"- Required data: [Based on scenario requirements]\n\n")

        f.write("ELECTRON STEPS:\n")
        for i, step in enumerate(steps, 1):
            f.write(f"{i}. {step}\n")
        f.write("\n")

        f.write("VERIFICATION:\n")
        if expected_result and str(expected_result) != 'nan':
            f.write(f"- [ ] {expected_result}\n")
        f.write("- [ ] No error messages displayed\n")
        f.write("- [ ] Task completed successfully\n\n")

        if confidence < 7.0:
            f.write("RAG ANALYSIS:\n")
            f.write("-" * 80 + "\n")
            f.write(rag_result[:1000])
            f.write("\n" + "-" * 80 + "\n\n")

        f.write("=" * 80 + "\n")

    return status_code

def process_area(area_name, json_file):
    """Process all scenarios for a functional area"""
    print(f"\n{'='*80}")
    print(f"Processing: {area_name}")
    print(f"{'='*80}")

    # Load scenarios
    with open(json_file, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    print(f"Found {len(scenarios)} scenarios\n")

    # Create output directory
    output_dir = Path(area_name)
    output_dir.mkdir(exist_ok=True)

    # Process each scenario
    stats = {'accepted': 0, 'review': 0, 'manual': 0, 'incomplete': 0}

    for scenario in scenarios:
        try:
            result = generate_test_file(scenario, output_dir)
            if result:
                stats[result] += 1
            else:
                stats['incomplete'] += 1
        except Exception as e:
            print(f"  ❌ Error: {scenario.get('Scenario ID', 'UNKNOWN')}: {e}")
            stats['incomplete'] += 1

    # Summary
    print(f"\n{'-'*80}")
    print(f"Summary for {area_name}:")
    print(f"  ✅ Accepted (>= 7.0):     {stats['accepted']}")
    print(f"  ⚠️  Needs Review (5-6.9):  {stats['review']}")
    print(f"  ❌ Manual (< 5.0):        {stats['manual']}")
    print(f"  ⚠️  Incomplete:            {stats['incomplete']}")
    print(f"  Total:                    {len(scenarios)}")
    print(f"{'-'*80}")

    return stats

def main():
    """Main execution"""
    base_dir = Path(__file__).parent
    os.chdir(base_dir)

    print(f"\nWorkday Electron Test Generator - Three Areas")
    print(f"{'='*80}\n")

    areas = {
        'Advanced_Compensation': 'Advanced_Compensation_scenarios.json',
        'Data_Management_FIN': 'Data_Management_FIN_scenarios.json',
        'Data_Management_HCM': 'Data_Management_HCM_scenarios.json'
    }

    total_stats = {'accepted': 0, 'review': 0, 'manual': 0, 'incomplete': 0}

    for area_name, json_file in areas.items():
        json_path = base_dir / json_file
        if json_path.exists():
            area_stats = process_area(area_name, json_file)
            for key in total_stats:
                total_stats[key] += area_stats[key]
        else:
            print(f"⚠️  Warning: {json_file} not found")

    # Grand total
    print(f"\n{'='*80}")
    print(f"GRAND TOTAL:")
    print(f"  ✅ Accepted (>= 7.0):     {total_stats['accepted']}")
    print(f"  ⚠️  Needs Review (5-6.9):  {total_stats['review']}")
    print(f"  ❌ Manual (< 5.0):        {total_stats['manual']}")
    print(f"  ⚠️  Incomplete:            {total_stats['incomplete']}")
    print(f"  Total Scenarios:          {sum(total_stats.values())}")
    print(f"{'='*80}\n")
    print(f"Output location: {base_dir}")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
