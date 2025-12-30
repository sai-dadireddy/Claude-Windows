#!/usr/bin/env python3
"""
Generate Electron test files for Workday financial areas (Fast version)
Uses template-based generation without RAG queries
"""

import pandas as pd
from pathlib import Path

# Configuration
EXCEL_PATH = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests"

# Financial areas to process
FINANCIAL_AREAS = [
    'Accounts Payable',
    'Accounts Receivable',
    'Cash Management',
    'Asset Management'
]


def determine_template(task_name):
    """Determine which Electron template to use based on task name"""
    task_lower = task_name.lower()

    if 'extract' in task_lower or 'export' in task_lower:
        return 'extract'
    elif 'find' in task_lower or 'search' in task_lower:
        return 'find'
    elif 'maintain' in task_lower or 'create' in task_lower or 'edit' in task_lower:
        return 'maintain'
    elif 'view' in task_lower or 'review' in task_lower or 'verify' in task_lower:
        return 'view'
    else:
        return 'default'


def generate_electron_steps(test_id, task_name, template_type='default'):
    """Generate Electron steps from template"""

    steps = []

    if template_type == 'extract':
        steps = [
            f'enter search box as "{task_name}"',
            'wait for search results',
            f'click search result containing "{task_name}"',
            'wait for page to load',
            'verify report parameters page displays',
            'click "OK" to run report with default parameters',
            'wait for report to generate',
            'verify report displays data',
            'verify column headers are correct',
            'scroll down to review data',
            'click "Export to Excel" button',
            'wait for export confirmation',
            f'screenshot as "{test_id}_complete.png"'
        ]
    elif template_type == 'find':
        steps = [
            f'enter search box as "{task_name}"',
            'wait for search results',
            f'click search result containing "{task_name}"',
            'wait for page to load',
            'verify search page displays',
            'click "OK" to search with default criteria',
            'wait for results to load',
            'verify results display',
            'verify data accuracy',
            f'screenshot as "{test_id}_complete.png"'
        ]
    elif template_type == 'maintain':
        steps = [
            f'enter search box as "{task_name}"',
            'wait for search results',
            f'click search result containing "{task_name}"',
            'wait for page to load',
            'verify configuration page displays',
            'review configuration settings',
            'verify all required fields are populated',
            'verify settings are correct',
            f'screenshot as "{test_id}_complete.png"'
        ]
    elif template_type == 'view':
        steps = [
            f'enter search box as "{task_name}"',
            'wait for search results',
            f'click search result containing "{task_name}"',
            'wait for page to load',
            'verify data displays',
            'verify information is accurate',
            f'screenshot as "{test_id}_complete.png"'
        ]
    else:  # default
        steps = [
            f'enter search box as "{task_name}"',
            'wait for search results',
            f'click search result containing "{task_name}"',
            'wait for page to load',
            'verify page displays correctly',
            'complete required fields',
            'click "Submit" button',
            'wait for confirmation',
            'verify success message displays',
            f'screenshot as "{test_id}_complete.png"'
        ]

    return [f"{i}. {step}" for i, step in enumerate(steps, 1)]


def generate_test_file(row, area_name):
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

    # Build test content
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: {area_name}
TEST NAME: {scenario_name}
WORKDAY ROLE: {workday_role}
EST. DURATION: {est_effort} minutes
TEMPLATE: {template_type.upper()}
================================================================================

DESCRIPTION:
{description if description != 'nan' else 'No description provided'}

PREREQUISITES:
- User logged in with {workday_role} permissions
- Required access to {area_name} domain
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
- Task/Step: {task_step}

NOTES:
- This test was generated using template-based automation
- Verify field names match actual Workday UI before execution
- Adjust wait times based on system performance

================================================================================
"""

    return content, 'GENERATED'


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
        'generated': 0,
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

        # Generate test
        content, status = generate_test_file(row, area_name)

        if content:
            # Save to file
            filename = f"{scenario_id.replace('/', '_').replace(' ', '_')}.txt"
            output_path = output_dir / filename

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            stats['generated'] += 1

            if stats['generated'] % 20 == 0:
                print(f"  Progress: {stats['generated']}/{len(area_df)} files generated...")

    # Print summary
    print(f"\n{area_name} - Summary:")
    print(f"  Generated:     {stats['generated']:4d} ({stats['generated']/stats['total']*100:5.1f}%)")
    print(f"  Incomplete:    {stats['incomplete']:4d} ({stats['incomplete']/stats['total']*100:5.1f}%)")
    print(f"  Output: {output_dir}")

    return stats


def main():
    """Main execution"""
    print("="*80)
    print("Workday Electron Test Generator - Financial Areas (Fast Mode)")
    print("="*80)

    all_stats = {
        'total': 0,
        'generated': 0,
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
    print(f"  Generated:     {all_stats['generated']:4d} ({all_stats['generated']/all_stats['total']*100:5.1f}%)")
    print(f"  Incomplete:    {all_stats['incomplete']:4d} ({all_stats['incomplete']/all_stats['total']*100:5.1f}%)")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    main()
