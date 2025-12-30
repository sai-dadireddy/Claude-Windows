#!/usr/bin/env python3
"""
Generate Electron tests for 10 remaining Workday functional areas:
Mobile, Prism, Peakon, Messaging, User_Experience, Candidate_Engagement,
Journey_Paths, Labor_Optimization, Scheduling, Other
"""

import pandas as pd
import os
import json
import re
from datetime import datetime

# Folder mapping (Excel name -> Output folder)
AREA_MAPPING = {
    'Mobile': 'Mobile',
    'Prism': 'Prism',
    'Peakon': 'Peakon',
    'Messaging': 'Messaging',
    'User Experience': 'User_Experience',
    'Candidate Engagement': 'Candidate_Engagement',
    'Journey Paths': 'Journey_Paths',
    'Labor Optimization': 'Labor_Optimization',
    'Scheduling': 'Scheduling',
    'Other': 'Other'
}

def sanitize_filename(text):
    """Convert text to safe filename"""
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    return text[:100]

def calculate_confidence(scenario_data):
    """
    Calculate confidence score (0-10) for test automation

    Criteria:
    - Has clear task/step description: +3
    - Has expected result: +2
    - Has workday role: +1
    - Has business process: +1
    - Clear action verbs (create, submit, approve, view): +2
    - Complex multi-step: -1
    """
    score = 5.0  # Base score

    task = str(scenario_data.get('Task / Step', '')).lower()
    expected = str(scenario_data.get('Customer Expected Result', '')).lower()
    role = str(scenario_data.get('Workday Role', '')).lower()
    bp = str(scenario_data.get('Business Process Alignment (Level 3)', '')).lower()

    # Has clear task
    if task and task != 'nan' and len(task) > 10:
        score += 2.0

    # Has expected result
    if expected and expected != 'nan' and len(expected) > 10:
        score += 1.5

    # Has role
    if role and role != 'nan':
        score += 0.5

    # Has business process
    if bp and bp != 'nan':
        score += 0.5

    # Action verbs present
    action_verbs = ['create', 'submit', 'approve', 'view', 'update', 'delete', 'search', 'run', 'generate']
    if any(verb in task for verb in action_verbs):
        score += 1.0

    # Complex indicators (reduce score)
    complex_indicators = ['multiple', 'various', 'all', 'bulk', 'mass', 'integration']
    if any(ind in task for ind in complex_indicators):
        score -= 0.5

    return min(10.0, max(0.0, score))

def extract_electron_actions(scenario_data):
    """Extract Electron commands from scenario data"""
    task = str(scenario_data.get('Task / Step', ''))
    expected = str(scenario_data.get('Customer Expected Result', ''))
    role = str(scenario_data.get('Workday Role', ''))

    actions = []

    # Common patterns for different areas
    task_lower = task.lower()

    # Mobile-specific
    if 'mobile' in task_lower:
        if 'login' in task_lower or 'access' in task_lower:
            actions.append('// Access mobile application')
            actions.append('await page.goto("https://wd5-impl.workday.com");')
        if 'view' in task_lower or 'display' in task_lower:
            actions.append('// View mobile interface')
            actions.append('await page.waitForSelector("[data-automation-id=\\"mobileView\\"]");')

    # Prism-specific
    elif 'prism' in task_lower or 'analytics' in task_lower:
        if 'create' in task_lower or 'build' in task_lower:
            actions.append('// Navigate to Prism Analytics')
            actions.append('await page.fill("input[role=\\"search\\"]", "Prism Analytics");')
            actions.append('await page.keyboard.press("Enter");')
        if 'report' in task_lower or 'dashboard' in task_lower:
            actions.append('// Open report/dashboard')
            actions.append('await page.click("[data-automation-id=\\"prismReport\\"]");')

    # Peakon-specific
    elif 'peakon' in task_lower or 'engagement' in task_lower:
        if 'survey' in task_lower:
            actions.append('// Access Peakon survey')
            actions.append('await page.fill("input[role=\\"search\\"]", "Employee Engagement");')
            actions.append('await page.keyboard.press("Enter");')
        if 'feedback' in task_lower or 'response' in task_lower:
            actions.append('// View feedback/responses')
            actions.append('await page.click("[data-automation-id=\\"peakonFeedback\\"]");')

    # Messaging-specific
    elif 'message' in task_lower or 'notification' in task_lower:
        if 'send' in task_lower or 'create' in task_lower:
            actions.append('// Navigate to Messaging')
            actions.append('await page.click("[data-automation-id=\\"messaging\\"]");')
            actions.append('await page.click("button:has-text(\\"New Message\\")");')
        if 'view' in task_lower or 'read' in task_lower:
            actions.append('// View messages')
            actions.append('await page.click("[data-automation-id=\\"inbox\\"]");')

    # Journey Paths-specific
    elif 'journey' in task_lower or 'path' in task_lower:
        if 'create' in task_lower or 'configure' in task_lower:
            actions.append('// Navigate to Journey configuration')
            actions.append('await page.fill("input[role=\\"search\\"]", "Configure Journey");')
            actions.append('await page.keyboard.press("Enter");')
        if 'assign' in task_lower or 'employee' in task_lower:
            actions.append('// Assign journey to employee')
            actions.append('await page.click("[data-automation-id=\\"assignJourney\\"]");')

    # Labor Optimization-specific
    elif 'labor' in task_lower or 'optimization' in task_lower:
        if 'schedule' in task_lower or 'shift' in task_lower:
            actions.append('// Navigate to Labor Optimization')
            actions.append('await page.fill("input[role=\\"search\\"]", "Labor Optimization");')
            actions.append('await page.keyboard.press("Enter");')
        if 'workload' in task_lower or 'demand' in task_lower:
            actions.append('// Configure workload/demand')
            actions.append('await page.click("[data-automation-id=\\"laborWorkload\\"]");')

    # Scheduling-specific
    elif 'schedule' in task_lower or 'shift' in task_lower:
        if 'create' in task_lower or 'build' in task_lower:
            actions.append('// Navigate to Scheduling')
            actions.append('await page.fill("input[role=\\"search\\"]", "Create Schedule");')
            actions.append('await page.keyboard.press("Enter");')
        if 'assign' in task_lower or 'worker' in task_lower:
            actions.append('// Assign schedule to worker')
            actions.append('await page.click("[data-automation-id=\\"assignSchedule\\"]");')
        if 'pattern' in task_lower or 'template' in task_lower:
            actions.append('// Configure schedule pattern')
            actions.append('await page.click("[data-automation-id=\\"schedulePattern\\"]");')

    # Generic actions if nothing specific matched
    if not actions:
        if 'search' in task_lower:
            actions.append(f'await page.fill("input[role=\\"search\\"]", "{task[:50]}");')
            actions.append('await page.keyboard.press("Enter");')
        elif 'view' in task_lower or 'open' in task_lower:
            actions.append('await page.waitForLoadState("networkidle");')
            actions.append(f'// View: {task[:80]}')
        elif 'create' in task_lower or 'submit' in task_lower:
            actions.append('await page.click("button:has-text(\\"Submit\\")");')
            actions.append('await page.waitForSelector("text=Success");')

    return actions

def generate_electron_test(scenario_data, confidence):
    """Generate Electron test file content"""

    scenario_id = scenario_data.get('Scenario ID', 'UNKNOWN')
    scenario_name = scenario_data.get('Scenario Name', 'Unnamed Scenario')
    task = scenario_data.get('Task / Step', '')
    expected = scenario_data.get('Customer Expected Result', '')
    role = scenario_data.get('Workday Role', 'Employee')

    actions = extract_electron_actions(scenario_data)

    test_content = f'''const {{ test, expect }} = require('@playwright/test');

/**
 * Test: {scenario_name}
 * Scenario ID: {scenario_id}
 * Confidence: {confidence:.1f}/10
 *
 * Task: {task}
 * Expected: {expected}
 * Role: {role}
 */

test.describe('{scenario_name}', () => {{
    test.beforeEach(async ({{ page }}) => {{
        // Login as {role}
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    }});

    test('should complete: {task[:80]}', async ({{ page }}) => {{
'''

    if confidence >= 7.0:
        # High confidence - full implementation
        for action in actions:
            test_content += f'        {action}\n'

        if expected and str(expected) != 'nan':
            test_content += f'\n        // Verify expected result\n'
            test_content += f'        // Expected: {expected[:100]}\n'
            test_content += f'        await page.waitForLoadState("networkidle");\n'

    elif confidence >= 5.0:
        # Medium confidence - needs review
        test_content += f'        // [NEEDS SME REVIEW] - Confidence: {confidence:.1f}/10\n'
        test_content += f'        // Task: {task}\n'
        test_content += f'        // Expected: {expected}\n\n'
        for action in actions:
            test_content += f'        {action}\n'

    else:
        # Low confidence - manual implementation needed
        test_content += f'        // [MANUAL IMPLEMENTATION REQUIRED] - Confidence: {confidence:.1f}/10\n'
        test_content += f'        // This test requires manual implementation\n'
        test_content += f'        // Task: {task}\n'
        test_content += f'        // Expected: {expected}\n'
        test_content += f'        test.skip();\n'

    test_content += '''    });
});
'''

    return test_content

def process_area(df, area_name, output_folder):
    """Process all scenarios for a specific area"""

    area_df = df[df['Functional Area'] == area_name]

    if len(area_df) == 0:
        print(f"⚠️  No scenarios found for {area_name}")
        return {
            'total': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0,
            'files_generated': 0
        }

    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    stats = {
        'total': len(area_df),
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0,
        'files_generated': 0
    }

    # Group by scenario
    for idx, row in area_df.iterrows():
        scenario_id = row.get('Scenario ID', f'UNKNOWN_{idx}')
        scenario_name = row.get('Scenario Name', 'Unnamed')

        # Calculate confidence
        confidence = calculate_confidence(row)

        if confidence >= 7.0:
            stats['high_confidence'] += 1
        elif confidence >= 5.0:
            stats['medium_confidence'] += 1
        else:
            stats['low_confidence'] += 1

        # Generate test file
        test_content = generate_electron_test(row, confidence)

        # Create filename
        safe_name = sanitize_filename(f"{scenario_id}_{scenario_name}")
        filename = f"{safe_name}.spec.js"
        filepath = os.path.join(output_folder, filename)

        # Write test file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(test_content)

        stats['files_generated'] += 1

    # Generate summary
    summary_file = os.path.join(output_folder, 'GENERATION_SUMMARY.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Generation Summary for {area_name}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(f"Total Scenarios: {stats['total']}\n")
        f.write(f"Files Generated: {stats['files_generated']}\n\n")
        f.write(f"Confidence Breakdown:\n")
        f.write(f"  High (7.0-10.0):   {stats['high_confidence']:3d} scenarios\n")
        f.write(f"  Medium (5.0-6.9):  {stats['medium_confidence']:3d} scenarios [NEEDS SME REVIEW]\n")
        f.write(f"  Low (0.0-4.9):     {stats['low_confidence']:3d} scenarios [MANUAL]\n\n")
        f.write(f"Success Rate: {(stats['high_confidence']/stats['total']*100):.1f}%\n")

    return stats

def main():
    """Main execution"""

    excel_path = 'WD_Test_Scenarios_Master.xlsx'

    print("=" * 70)
    print("Workday Electron Test Generator - 10 Remaining Areas")
    print("=" * 70)
    print()

    # Load Excel
    print("📊 Loading Excel file...")
    df = pd.read_excel(excel_path)
    print(f"✓ Loaded {len(df)} total scenarios\n")

    # Process each area
    all_stats = {}

    for excel_area, folder_name in AREA_MAPPING.items():
        print(f"\n{'=' * 70}")
        print(f"Processing: {excel_area} -> {folder_name}/")
        print(f"{'=' * 70}")

        stats = process_area(df, excel_area, folder_name)
        all_stats[folder_name] = stats

        if stats['total'] > 0:
            print(f"✓ Generated {stats['files_generated']} test files")
            print(f"  High Confidence: {stats['high_confidence']}")
            print(f"  Medium (Review): {stats['medium_confidence']}")
            print(f"  Low (Manual):    {stats['low_confidence']}")

    # Overall summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)

    total_scenarios = sum(s['total'] for s in all_stats.values())
    total_high = sum(s['high_confidence'] for s in all_stats.values())
    total_medium = sum(s['medium_confidence'] for s in all_stats.values())
    total_low = sum(s['low_confidence'] for s in all_stats.values())
    total_files = sum(s['files_generated'] for s in all_stats.values())

    print(f"\nTotal Scenarios Processed: {total_scenarios}")
    print(f"Total Files Generated:     {total_files}")
    print()
    print(f"Confidence Distribution:")
    print(f"  High (7.0-10):    {total_high:4d} ({total_high/total_scenarios*100:.1f}%)")
    print(f"  Medium (5.0-6.9): {total_medium:4d} ({total_medium/total_scenarios*100:.1f}%) [NEEDS REVIEW]")
    print(f"  Low (0.0-4.9):    {total_low:4d} ({total_low/total_scenarios*100:.1f}%) [MANUAL]")
    print()

    # Save overall summary
    with open('GENERATION_SUMMARY_10_AREAS.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("Workday Electron Tests - 10 Remaining Areas\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        for folder_name, stats in all_stats.items():
            if stats['total'] > 0:
                f.write(f"\n{folder_name}:\n")
                f.write(f"  Scenarios: {stats['total']}\n")
                f.write(f"  High:      {stats['high_confidence']}\n")
                f.write(f"  Medium:    {stats['medium_confidence']}\n")
                f.write(f"  Low:       {stats['low_confidence']}\n")

        f.write(f"\n{'=' * 70}\n")
        f.write(f"Total: {total_scenarios} scenarios, {total_files} files\n")
        f.write(f"Success Rate: {total_high/total_scenarios*100:.1f}%\n")

    print("\n✓ Generation complete!")
    print(f"📄 Summary saved to: GENERATION_SUMMARY_10_AREAS.txt\n")

if __name__ == '__main__':
    main()
