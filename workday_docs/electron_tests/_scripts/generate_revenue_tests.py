#!/usr/bin/env python3
"""
Electron Test Generator for Revenue Management
Generates test scenarios from Excel with RAG-based enrichment
"""

import pandas as pd
import os
import re
import subprocess
import sys

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Revenue_Management"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

def sanitize_filename(name):
    """Sanitize scenario name for filename"""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name[:100]
    return name.strip()

def query_rag(task_step):
    """Query Workday RAG for task/step information"""
    if not task_step or pd.isna(task_step):
        return None, "No Task/Step provided"

    try:
        result = subprocess.run(
            [sys.executable, RAG_SCRIPT, str(task_step)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(RAG_SCRIPT)
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip(), None
        else:
            return None, f"RAG query failed: {result.stderr}"
    except Exception as e:
        return None, f"RAG error: {str(e)}"

def calculate_confidence(scenario, rag_result):
    """Calculate confidence score based on available data"""
    score = 0.0

    # Has Task/Step (3 points)
    if scenario.get('Task / Step') and not pd.isna(scenario.get('Task / Step')):
        score += 3.0

    # Has Expected Result (2 points)
    if scenario.get('Customer Expected Result') and not pd.isna(scenario.get('Customer Expected Result')):
        score += 2.0

    # RAG found results (3 points)
    if rag_result and len(rag_result) > 100:
        score += 3.0
    elif rag_result:
        score += 1.5

    # Has clear action verbs (1 point)
    task = str(scenario.get('Task / Step', ''))
    if any(verb in task.lower() for verb in ['create', 'submit', 'recognize', 'review', 'post', 'calculate']):
        score += 1.0

    # Has business object reference (1 point)
    if any(obj in task.lower() for obj in ['revenue', 'recognition', 'category', 'contract', 'allocation', 'schedule']):
        score += 1.0

    # Normalize to 10
    score = min(score, 10.0)

    if score >= 7.0:
        level = "HIGH"
    elif score >= 4.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level, score

def generate_electron_steps(scenario, rag_result):
    """Generate Electron-specific test steps"""
    task_step = scenario.get('Task / Step', '')

    if not task_step or pd.isna(task_step):
        return None

    steps = []
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')

    # Step 1: Enter search
    steps.append(f'1. enter search box as "{task_step}"')
    steps.append('2. wait for search results')
    steps.append('3. click search result')

    # Extract RAG-based actions
    if rag_result:
        if 'create' in task_step.lower() or 'contract' in task_step.lower():
            steps.append('4. wait for page load')
            steps.append('5. enter revenue contract details')
            steps.append('6. configure revenue categories')
            steps.append('7. click "Submit" button')
        elif 'recognize' in task_step.lower() or 'recognition' in task_step.lower():
            steps.append('4. wait for recognition page')
            steps.append('5. select recognition period')
            steps.append('6. verify revenue allocation')
            steps.append('7. click "Process" or "Submit" button')
        elif 'schedule' in task_step.lower() or 'allocation' in task_step.lower():
            steps.append('4. wait for page load')
            steps.append('5. configure schedule parameters')
            steps.append('6. verify allocation amounts')
            steps.append('7. click "Submit" button')
        else:
            steps.append('4. wait for page load')
            steps.append('5. complete required actions')
            steps.append('6. click "Done" or "Submit" button')
    else:
        steps.append('4. wait for page load')
        steps.append('5. complete transaction')
        steps.append('6. submit')

    # Final screenshot
    steps.append(f'8. screenshot as "{scenario_id}_complete.png"')

    return '\n'.join(steps)

def generate_verification(scenario):
    """Generate verification checklist"""
    expected = scenario.get('Customer Expected Result', '')

    if expected and not pd.isna(expected):
        return f"- [ ] {expected}"
    else:
        return "- [ ] Transaction completed successfully\n- [ ] No error messages displayed"

def generate_test_file(scenario, rag_result, output_path):
    """Generate complete test file"""
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')
    scenario_name = scenario.get('Scenario Name', 'Unnamed Test')
    task_step = scenario.get('Task / Step', '')

    # Calculate confidence
    conf_level, conf_score = calculate_confidence(scenario, rag_result)

    # Generate steps
    electron_steps = generate_electron_steps(scenario, rag_result)

    # Check if manual
    is_manual = not task_step or pd.isna(task_step) or not electron_steps

    # Build file content
    content = []
    content.append("=" * 80)
    content.append(f"TEST ID: {scenario_id}")
    content.append("FUNCTIONAL AREA: Revenue Management")
    content.append(f"TEST NAME: {scenario_name}")
    content.append(f"CONFIDENCE: [{conf_level}] Score: {conf_score}/10")
    content.append("=" * 80)
    content.append("")

    if is_manual:
        content.append("STATUS: [MANUAL REQUIRED]")
        content.append("REASON: Missing Task/Step or insufficient information")
        content.append("")
        content.append(f"SCENARIO DETAILS:")
        content.append(f"Task/Step: {task_step if task_step else 'NOT PROVIDED'}")
        content.append(f"Expected Result: {scenario.get('Customer Expected Result', 'NOT PROVIDED')}")
    else:
        content.append("ELECTRON STEPS:")
        content.append(electron_steps)
        content.append("")
        content.append("VERIFICATION:")
        content.append(generate_verification(scenario))

        # Add RAG insights if available
        if rag_result and len(rag_result) > 50:
            content.append("")
            content.append("RAG INSIGHTS:")
            content.append("-" * 80)
            # Truncate RAG result to first 500 chars
            content.append(rag_result[:500])
            if len(rag_result) > 500:
                content.append("...")

    content.append("=" * 80)

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    return conf_level, conf_score, is_manual

def main():
    """Main processing function"""
    print("=" * 80)
    print("WORKDAY ELECTRON TEST GENERATOR - REVENUE MANAGEMENT")
    print("=" * 80)
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

    # Read Excel
    print(f"Reading Excel: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Revenue_Management')
    print(f"Total Revenue Management scenarios: {len(df)}")
    print()

    # Process each scenario
    stats = {
        'total': len(df),
        'generated': 0,
        'manual': 0,
        'high_conf': 0,
        'medium_conf': 0,
        'low_conf': 0
    }

    for idx, row in df.iterrows():
        scenario_id = row.get('Scenario ID', f'UNKNOWN_{idx}')
        scenario_name = row.get('Scenario Name', 'Unnamed')
        task_step = row.get('Task / Step', '')

        print(f"Processing [{idx+1}/{len(df)}]: {scenario_id} - {scenario_name[:50]}...")

        # Query RAG
        rag_result = None
        if task_step and not pd.isna(task_step):
            print(f"  Querying RAG for: {task_step[:60]}...")
            rag_result, error = query_rag(task_step)
            if error:
                print(f"  WARNING: {error}")

        # Generate filename
        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        output_path = os.path.join(OUTPUT_DIR, filename)

        # Generate test file
        conf_level, conf_score, is_manual = generate_test_file(row, rag_result, output_path)

        # Update stats
        stats['generated'] += 1
        if is_manual:
            stats['manual'] += 1
        if conf_level == 'HIGH':
            stats['high_conf'] += 1
        elif conf_level == 'MEDIUM':
            stats['medium_conf'] += 1
        else:
            stats['low_conf'] += 1

        print(f"  [OK] Generated: {filename} [Confidence: {conf_level} - {conf_score}/10]")
        print()

    # Print summary
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print(f"Total scenarios processed: {stats['total']}")
    print(f"Files generated: {stats['generated']}")
    print(f"Manual scenarios: {stats['manual']}")
    print(f"High confidence: {stats['high_conf']}")
    print(f"Medium confidence: {stats['medium_conf']}")
    print(f"Low confidence: {stats['low_conf']}")
    print()
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == '__main__':
    main()
