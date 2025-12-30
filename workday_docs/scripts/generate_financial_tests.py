#!/usr/bin/env python3
"""
Generate Electron test files for Workday financial areas
Based on Excel scenarios with RAG enhancement
"""

import pandas as pd
import json
import os
import subprocess
from pathlib import Path

# Configuration
EXCEL_PATH = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests"
RAG_SCRIPT = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/workday_rag.py"

# Financial areas to process
FINANCIAL_AREAS = [
    'Accounts Payable',
    'Accounts Receivable',
    'Cash Management',
    'Asset Management'
]

# Electron command templates
ELECTRON_TEMPLATES = {
    'extract': [
        'enter search box as "{task}"',
        'wait for search results',
        'click search result containing "{task}"',
        'wait for page to load',
        'verify report parameters page displays',
        'click "OK" to run report with default parameters',
        'wait for report to generate',
        'verify report displays data',
        'click "Export to Excel" button',
        'wait for export confirmation',
        'screenshot as "{test_id}_{step}.png"'
    ],
    'find': [
        'enter search box as "{task}"',
        'wait for search results',
        'click search result containing "{task}"',
        'wait for page to load',
        'verify search page displays',
        'click "OK" to search with default criteria',
        'wait for results to load',
        'verify results display',
        'screenshot as "{test_id}_{step}.png"'
    ],
    'maintain': [
        'enter search box as "{task}"',
        'wait for search results',
        'click search result containing "{task}"',
        'wait for page to load',
        'verify configuration page displays',
        'review configuration settings',
        'verify settings are correct',
        'screenshot as "{test_id}_{step}.png"'
    ],
    'view': [
        'enter search box as "{task}"',
        'wait for search results',
        'click search result containing "{task}"',
        'wait for page to load',
        'verify data displays',
        'screenshot as "{test_id}_{step}.png"'
    ],
    'default': [
        'enter search box as "{task}"',
        'wait for search results',
        'click search result containing "{task}"',
        'wait for page to load',
        'complete required fields',
        'click "Submit" button',
        'wait for confirmation',
        'verify success message displays',
        'screenshot as "{test_id}_complete.png"'
    ]
}


def query_rag(task_name):
    """Query RAG for task guidance"""
    try:
        result = subprocess.run(
            ['python', RAG_SCRIPT, task_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        print(f"RAG query failed for '{task_name}': {e}")
        return None


def extract_confidence_score(rag_output):
    """Extract confidence score from RAG output"""
    if not rag_output:
        return 0.0

    # Look for "score: X" pattern
    import re
    scores = re.findall(r'score:\s*(\d+)', rag_output, re.IGNORECASE)
    if scores:
        return float(scores[0])
    return 0.0


def determine_template(task_name):
    """Determine which Electron template to use based on task name"""
    task_lower = task_name.lower()

    if 'extract' in task_lower or 'export' in task_lower:
        return 'extract'
    elif 'find' in task_lower or 'search' in task_lower:
        return 'find'
    elif 'maintain' in task_lower or 'create' in task_lower or 'edit' in task_lower:
        return 'maintain'
    elif 'view' in task_lower or 'review' in task_lower:
        return 'view'
    else:
        return 'default'


def generate_electron_steps(test_id, task_name, template_type='default'):
    """Generate Electron steps from template"""
    template = ELECTRON_TEMPLATES.get(template_type, ELECTRON_TEMPLATES['default'])

    steps = []
    for i, step_template in enumerate(template, 1):
        step = step_template.format(
            task=task_name,
            test_id=test_id,
            step=f"step{i}"
        )
        steps.append(f"{i}. {step}")

    return steps


def generate_test_file(row, area_safe, rag_score=0.0):
    """Generate a single Electron test file"""

    # Extract fields
    scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
    scenario_name = str(row.get('Scenario Name', 'Unnamed Test')).strip()
    task_step = str(row.get('Task / Step', '')).strip()
    description = str(row.get('Scenario Description', '')).strip()
    expected_result = str(row.get('Customer Expected Result', '')).strip()
    est_effort = row.get('Est. Effort (mins)', 5)
    workday_role = str(row.get('Workday Role', 'System User')).strip()
    sub_task = str(row.get('Sub Task', '')).strip()

    # Skip if no task/step
    if not task_step or task_step == 'nan':
        return None, 'INCOMPLETE'

    # Determine template
    template_type = determine_template(task_step)

    # Generate steps
    electron_steps = generate_electron_steps(scenario_id, task_step, template_type)

    # Determine status based on RAG score
    if rag_score >= 7.0:
        status = 'ACCEPTED'
        confidence_label = '✅ HIGH CONFIDENCE'
    elif rag_score >= 5.0:
        status = 'NEEDS_REVIEW'
        confidence_label = '⚠️ NEEDS SME REVIEW'
    else:
        status = 'MANUAL'
        confidence_label = '❌ MANUAL REQUIRED'

    # Build test content
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: {row.get('Functional Area', area_safe)}
TEST NAME: {scenario_name}
WORKDAY ROLE: {workday_role}
EST. DURATION: {est_effort} minutes
RAG CONFIDENCE: {rag_score:.1f}/10.0 {confidence_label}
================================================================================

DESCRIPTION:
{description if description != 'nan' else 'No description provided'}

PREREQUISITES:
- User logged in with {workday_role} permissions
- Required access to {row.get('Functional Area', area_safe)} domain
- Test data prepared and available

ELECTRON STEPS:
"""

    for step in electron_steps:
        content += f"{step}\n"

    content += f"""
VERIFICATION:
- [ ] {expected_result if expected_result != 'nan' else 'Task completed successfully'}
- [ ] No error messages displayed
- [ ] Data accuracy verified
- [ ] Screenshots captured with test ID prefix

"""

    if sub_task and sub_task != 'nan':
        content += f"""SUB-TASKS:
{sub_task}

"""

    content += f"""RELATED INFORMATION:
- Scenario Name: {scenario_name}
- Template Used: {template_type}
- RAG Query: "{task_step}"

NOTES:
"""

    if status == 'NEEDS_REVIEW':
        content += "- ⚠️ This test requires SME review before execution\n"
        content += "- Verify field names and values match actual Workday UI\n"
    elif status == 'MANUAL':
        content += "- ❌ Insufficient knowledge base coverage for automation\n"
        content += "- Manual testing required - SME must create detailed steps\n"

    content += f"""
================================================================================
"""

    return content, status


def process_area(area_name):
    """Process all scenarios for a financial area"""

    print(f"\n{'='*80}")
    print(f"Processing: {area_name}")
    print(f"{'='*80}")

    # Read Excel
    df = pd.read_excel(EXCEL_PATH)

    # Filter by area
    area_df = df[df['Functional Area'] == area_name].copy()

    print(f"Total scenarios: {len(area_df)}")

    # Create output directory
    area_safe = area_name.replace(' ', '_').lower()
    output_dir = Path(OUTPUT_BASE) / area_safe
    output_dir.mkdir(parents=True, exist_ok=True)

    # Statistics
    stats = {
        'total': len(area_df),
        'accepted': 0,
        'needs_review': 0,
        'manual': 0,
        'incomplete': 0
    }

    # Process each scenario
    for idx, row in area_df.iterrows():
        task_step = str(row.get('Task / Step', '')).strip()
        scenario_id = str(row.get('Scenario ID', f'{area_safe}_{idx}')).strip()

        # Skip empty tasks
        if not task_step or task_step == 'nan':
            stats['incomplete'] += 1
            continue

        # Query RAG
        print(f"  Processing: {scenario_id} - {task_step[:50]}...")
        rag_output = query_rag(task_step)
        rag_score = extract_confidence_score(rag_output)

        # Generate test
        content, status = generate_test_file(row, area_safe, rag_score)

        if content:
            # Save to file
            filename = f"{scenario_id.replace('/', '_')}_{status}.txt"
            output_path = output_dir / filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Update stats
            if status == 'ACCEPTED':
                stats['accepted'] += 1
            elif status == 'NEEDS_REVIEW':
                stats['needs_review'] += 1
            elif status == 'MANUAL':
                stats['manual'] += 1

    # Print summary
    print(f"\n{area_name} - Summary:")
    print(f"  ✅ Accepted:      {stats['accepted']:4d} ({stats['accepted']/stats['total']*100:5.1f}%)")
    print(f"  ⚠️  Needs Review:  {stats['needs_review']:4d} ({stats['needs_review']/stats['total']*100:5.1f}%)")
    print(f"  ❌ Manual:        {stats['manual']:4d} ({stats['manual']/stats['total']*100:5.1f}%)")
    print(f"  ⚫ Incomplete:    {stats['incomplete']:4d} ({stats['incomplete']/stats['total']*100:5.1f}%)")
    print(f"  📁 Output: {output_dir}")

    return stats


def main():
    """Main execution"""
    print("="*80)
    print("Workday Electron Test Generator - Financial Areas")
    print("="*80)

    all_stats = {
        'total': 0,
        'accepted': 0,
        'needs_review': 0,
        'manual': 0,
        'incomplete': 0
    }

    for area in FINANCIAL_AREAS:
        stats = process_area(area)

        # Aggregate stats
        for key in all_stats:
            all_stats[key] += stats[key]

    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY - All Financial Areas")
    print(f"{'='*80}")
    print(f"  Total Scenarios:  {all_stats['total']:4d}")
    print(f"  ✅ Accepted:      {all_stats['accepted']:4d} ({all_stats['accepted']/all_stats['total']*100:5.1f}%)")
    print(f"  ⚠️  Needs Review:  {all_stats['needs_review']:4d} ({all_stats['needs_review']/all_stats['total']*100:5.1f}%)")
    print(f"  ❌ Manual:        {all_stats['manual']:4d} ({all_stats['manual']/all_stats['total']*100:5.1f}%)")
    print(f"  ⚫ Incomplete:    {all_stats['incomplete']:4d} ({all_stats['incomplete']/all_stats['total']*100:5.1f}%)")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
