#!/usr/bin/env python3
"""
Quick Electron Test Generator for Accounting & Finance
Processes without RAG queries for speed
"""

import pandas as pd
import os
import re

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Finance"

def sanitize_filename(name):
    """Sanitize scenario name for filename"""
    name = re.sub(r'[<>:"/\\|?*]', '_', str(name))
    return name[:100].strip()

def calculate_confidence(scenario):
    """Calculate confidence score"""
    score = 0.0

    task = str(scenario.get('Task / Step', ''))
    expected = str(scenario.get('Customer Expected Result', ''))

    # Has Task/Step
    if task and task != 'nan':
        score += 3.0

    # Has Expected Result
    if expected and expected != 'nan':
        score += 2.0

    # Has clear action verbs
    if any(verb in task.lower() for verb in ['create', 'submit', 'approve', 'review', 'post', 'run']):
        score += 2.0

    # Has business object
    if any(obj in task.lower() for obj in ['journal', 'report', 'worktag', 'ledger', 'account']):
        score += 2.0

    # Has specific details
    if len(task) > 20:
        score += 1.0

    score = min(score, 10.0)

    if score >= 7.0:
        level = "HIGH"
    elif score >= 4.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level, score

def generate_electron_steps(scenario):
    """Generate Electron test steps"""
    task_step = str(scenario.get('Task / Step', ''))
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')

    if not task_step or task_step == 'nan':
        return None

    steps = []
    steps.append(f'1. enter search box as "{task_step}"')
    steps.append('2. wait for search results')
    steps.append('3. click search result')

    # Generate based on action type
    task_lower = task_step.lower()

    if 'create' in task_lower:
        steps.append('4. wait for page load')
        steps.append('5. fill required fields')
        steps.append('6. click "Submit" button')
    elif 'run' in task_lower or 'report' in task_lower:
        steps.append('4. wait for report page')
        steps.append('5. set report parameters')
        steps.append('6. click "OK" or "Run" button')
    elif 'review' in task_lower or 'approve' in task_lower:
        steps.append('4. wait for inbox page')
        steps.append('5. click transaction to review')
        steps.append('6. click "Approve" button')
    elif 'post' in task_lower:
        steps.append('4. wait for page load')
        steps.append('5. verify posting data')
        steps.append('6. click "Post" button')
    else:
        steps.append('4. wait for page load')
        steps.append('5. complete required actions')
        steps.append('6. click "Done" or "Submit"')

    steps.append(f'7. screenshot as "{scenario_id}_complete.png"')

    return '\n'.join(steps)

def generate_test_file(scenario, output_path):
    """Generate test file"""
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')
    scenario_name = scenario.get('Scenario Name', 'Unnamed Test')
    task_step = str(scenario.get('Task / Step', ''))
    expected = str(scenario.get('Customer Expected Result', ''))

    # Calculate confidence
    conf_level, conf_score = calculate_confidence(scenario)

    # Generate steps
    electron_steps = generate_electron_steps(scenario)
    is_manual = not electron_steps

    # Build content
    lines = []
    lines.append("=" * 80)
    lines.append(f"TEST ID: {scenario_id}")
    lines.append("FUNCTIONAL AREA: Accounting & Finance")
    lines.append(f"TEST NAME: {scenario_name}")
    lines.append(f"CONFIDENCE: [{conf_level}] Score: {conf_score}/10")
    lines.append("=" * 80)
    lines.append("")

    if is_manual:
        lines.append("STATUS: [MANUAL REQUIRED]")
        lines.append("REASON: Missing Task/Step")
        lines.append("")
        lines.append("SCENARIO DETAILS:")
        lines.append(f"Task/Step: {task_step if task_step != 'nan' else 'NOT PROVIDED'}")
        lines.append(f"Expected Result: {expected if expected != 'nan' else 'NOT PROVIDED'}")
    else:
        lines.append("ELECTRON STEPS:")
        lines.append(electron_steps)
        lines.append("")
        lines.append("VERIFICATION:")
        if expected and expected != 'nan':
            lines.append(f"- [ ] {expected}")
        else:
            lines.append("- [ ] Transaction completed successfully")
            lines.append("- [ ] No error messages displayed")

    lines.append("=" * 80)

    # Write
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return conf_level, is_manual

def main():
    print("=" * 80)
    print("WORKDAY ELECTRON TEST GENERATOR - ACCOUNTING & FINANCE")
    print("=" * 80)
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Read Excel
    print(f"Reading: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)

    # Filter
    finance_df = df[df['Functional Area'] == 'Accounting & Finance'].copy()
    print(f"Found {len(finance_df)} Accounting & Finance scenarios")
    print()

    # Process
    stats = {'total': len(finance_df), 'generated': 0, 'manual': 0,
             'high': 0, 'medium': 0, 'low': 0}

    for idx, row in finance_df.iterrows():
        scenario_id = row.get('Scenario ID', f'UNK_{idx}')
        scenario_name = row.get('Scenario Name', 'Unnamed')

        # Generate filename
        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        output_path = os.path.join(OUTPUT_DIR, filename)

        # Generate
        conf_level, is_manual = generate_test_file(row, output_path)

        # Stats
        stats['generated'] += 1
        if is_manual:
            stats['manual'] += 1
        if conf_level == 'HIGH':
            stats['high'] += 1
        elif conf_level == 'MEDIUM':
            stats['medium'] += 1
        else:
            stats['low'] += 1

        if (idx + 1) % 50 == 0:
            print(f"Progress: {idx + 1}/{len(finance_df)} scenarios processed")

    # Summary
    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print(f"Total: {stats['total']}")
    print(f"Generated: {stats['generated']}")
    print(f"Manual Required: {stats['manual']}")
    print(f"High Confidence: {stats['high']}")
    print(f"Medium Confidence: {stats['medium']}")
    print(f"Low Confidence: {stats['low']}")
    print()
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == '__main__':
    main()
