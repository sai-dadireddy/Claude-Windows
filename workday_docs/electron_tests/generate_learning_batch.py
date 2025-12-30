#!/usr/bin/env python3
"""
Generate Electron test files for Learning functional areas - Batch Processing
"""
import pandas as pd
import subprocess
import json
import re
import os
from pathlib import Path
import sys

# Paths
EXCEL_PATH = "WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = "."

def sanitize_filename(name):
    """Convert scenario name to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', name)
    safe = re.sub(r'[-\s]+', '_', safe)
    return safe[:100]

def generate_learning_commands(task_step, scenario_id):
    """Generate Electron commands for Learning tasks"""
    commands = []
    confidence = 5.0
    task_lower = task_step.lower()

    # Header
    commands.append(f"# Scenario ID: {scenario_id}")
    commands.append(f"# Task: {task_step}")
    commands.append("")

    # Pattern matching for Learning tasks

    # Report running
    if 'run' in task_lower and 'report' in task_lower:
        report_match = re.search(r'"([^"]+)"', task_step)
        if report_match:
            report_name = report_match.group(1)
            commands.extend([
                f'enter search box as "{report_name}"',
                'wait 2',
                f'click search result containing "{report_name}"',
                'wait for page to load'
            ])
            confidence = 8.0
        else:
            commands.extend([
                'enter search box as "View Security Group"',
                'wait 2',
                'click search result containing "View Security Group"',
                'wait for page to load'
            ])
            confidence = 6.0

    # Learning Worklet
    elif 'learning worklet' in task_lower:
        commands.extend([
            'click worklet "Learning"',
            'wait 2'
        ])
        confidence = 7.5

    # Dashboard access
    elif 'dashboard' in task_lower:
        if 'onboarding' in task_lower:
            commands.extend([
                'enter search box as "Onboarding Dashboard"',
                'wait 2',
                'click search result containing "Onboarding Dashboard"',
                'wait for page to load'
            ])
            confidence = 8.0
        elif 'learning' in task_lower:
            commands.extend([
                'enter search box as "Learning Dashboard"',
                'wait 2',
                'click search result containing "Learning Dashboard"',
                'wait for page to load'
            ])
            confidence = 8.0
        else:
            commands.extend([
                'enter search box as "Dashboard"',
                'wait 2',
                'click search result containing "Dashboard"',
                'wait for page to load'
            ])
            confidence = 6.5

    # Edit tasks
    elif 'edit' in task_lower:
        if 'learning topic' in task_lower:
            commands.extend([
                'enter search box as "Edit Learning Topic"',
                'wait 2',
                'click search result containing "Edit Learning Topic"',
                'wait for page to load'
            ])
            confidence = 7.0
        elif 'security segment' in task_lower:
            commands.extend([
                'enter search box as "Edit Learning Topic Security Segment"',
                'wait 2',
                'click search result containing "Edit Learning Topic Security Segment"',
                'wait for page to load'
            ])
            confidence = 7.5
        elif 'course' in task_lower:
            commands.extend([
                'enter search box as "Edit Course"',
                'wait 2',
                'click search result containing "Edit Course"',
                'wait for page to load'
            ])
            confidence = 7.0
        else:
            match = re.search(r'Edit\s+([^\.]+)', task_step, re.IGNORECASE)
            if match:
                task_name = match.group(1).strip()
                commands.extend([
                    f'enter search box as "Edit {task_name}"',
                    'wait 2',
                    f'click search result containing "Edit {task_name}"',
                    'wait for page to load'
                ])
                confidence = 6.5

    # Create tasks
    elif 'create' in task_lower:
        if 'course' in task_lower:
            commands.extend([
                'enter search box as "Create Course"',
                'wait 2',
                'click search result containing "Create Course"',
                'wait for page to load'
            ])
            confidence = 7.5
        elif 'lesson' in task_lower:
            commands.extend([
                'enter search box as "Create Lesson"',
                'wait 2',
                'click search result containing "Create Lesson"',
                'wait for page to load'
            ])
            confidence = 7.5
        elif 'learning' in task_lower:
            commands.extend([
                'enter search box as "Create Learning"',
                'wait 2',
                'click search result containing "Create Learning"',
                'wait for page to load'
            ])
            confidence = 7.0

    # Security Group
    elif 'security group' in task_lower:
        if 'view' in task_lower:
            commands.extend([
                'enter search box as "View Security Group"',
                'wait 2',
                'click search result containing "View Security Group"',
                'wait for page to load'
            ])
            confidence = 8.0
        else:
            commands.extend([
                'enter search box as "Maintain Security Groups"',
                'wait 2',
                'click search result containing "Maintain Security Groups"',
                'wait for page to load'
            ])
            confidence = 7.5

    # Enrollment
    elif 'enroll' in task_lower:
        if 'student' in task_lower or 'worker' in task_lower:
            commands.extend([
                'enter search box as "Enroll Student in Course"',
                'wait 2',
                'click search result containing "Enroll Student in Course"',
                'wait for page to load'
            ])
            confidence = 7.5
        else:
            commands.extend([
                'enter search box as "Enroll in Learning"',
                'wait 2',
                'click search result containing "Enroll"',
                'wait for page to load'
            ])
            confidence = 6.5

    # Assignment
    elif 'assign' in task_lower:
        if 'learning' in task_lower:
            commands.extend([
                'enter search box as "Assign Learning"',
                'wait 2',
                'click search result containing "Assign Learning"',
                'wait for page to load'
            ])
            confidence = 7.5

    # Transcript/View
    elif 'transcript' in task_lower:
        commands.extend([
            'enter search box as "View Learning Transcript"',
            'wait 2',
            'click search result containing "Learning Transcript"',
            'wait for page to load'
        ])
        confidence = 8.0

    # Navigation (Home > Menu)
    elif '>' in task_step:
        parts = [p.strip() for p in task_step.split('>')]
        for part in parts:
            if part.lower() != 'home':
                commands.extend([
                    f'click link "{part}"',
                    'wait 2'
                ])
        confidence = 6.5

    # Submit/Complete
    elif 'submit' in task_lower or 'complete' in task_lower:
        commands.extend([
            'click button "Submit"',
            'wait 2',
            'verify submission successful'
        ])
        confidence = 7.0

    # Generic fallback
    else:
        commands.extend([
            '# MANUAL IMPLEMENTATION REQUIRED',
            f'# Task: {task_step}',
            '# No automated pattern match found'
        ])
        confidence = 4.0

    # Add screenshot
    if confidence >= 5.0:
        commands.append(f'screenshot as "{scenario_id}_complete.png"')

    return commands, confidence

def generate_test_file(row, output_dir):
    """Generate a single test file"""
    scenario_id = row['Scenario ID']
    task_step = row['Task / Step']
    functional_area = row['Functional Area']
    scenario_name = row.get('Scenario Name', '')
    description = row.get('Scenario Description', '')
    expected_result = row.get('Customer Expected Result', '')

    print(f"Processing {scenario_id}: {task_step[:60]}...")

    # Generate commands
    commands, confidence = generate_learning_commands(task_step, scenario_id)

    # Determine status
    if confidence >= 7.0:
        suffix = ".txt"
        status = "AUTO-GENERATED"
    elif confidence >= 5.0:
        suffix = "_REVIEW.txt"
        status = "NEEDS SME REVIEW"
    else:
        suffix = "_MANUAL.txt"
        status = "MANUAL IMPLEMENTATION REQUIRED"

    # Create filename
    safe_name = sanitize_filename(task_step)
    filename = f"{scenario_id}_{safe_name}{suffix}"
    filepath = os.path.join(output_dir, filename)

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write(f"TEST ID: {scenario_id}\n")
        f.write(f"FUNCTIONAL AREA: {functional_area}\n")
        f.write(f"TEST NAME: {scenario_name}\n")
        f.write(f"STATUS: {status}\n")
        f.write(f"CONFIDENCE: {confidence:.1f}/10.0\n")
        f.write("="*70 + "\n\n")

        if description:
            f.write(f"DESCRIPTION:\n{description}\n\n")

        f.write("ORIGINAL TASK:\n")
        f.write(f"{task_step}\n\n")

        if expected_result:
            f.write("EXPECTED RESULT:\n")
            f.write(f"{expected_result}\n\n")

        f.write("ELECTRON STEPS:\n")
        for i, cmd in enumerate(commands, 1):
            if cmd.startswith('#'):
                f.write(f"{cmd}\n")
            else:
                f.write(f"{i}. {cmd}\n")

        if confidence < 7.0:
            f.write("\n" + "="*70 + "\n")
            f.write("NOTES:\n")
            if confidence >= 5.0:
                f.write("- This test requires SME review and validation\n")
                f.write("- Verify field names and navigation paths\n")
            else:
                f.write("- Manual implementation required\n")
                f.write("- No automated pattern match found\n")
                f.write("- Consult Workday documentation for detailed steps\n")

    return filepath, confidence

def main():
    """Main processing function"""
    print("="*70)
    print("WORKDAY LEARNING TEST GENERATION")
    print("="*70)
    print(f"\nLoading Excel file: {EXCEL_PATH}")

    df = pd.read_excel(EXCEL_PATH)

    # Filter Learning scenarios
    learning_df = df[df['Functional Area'].str.contains('Learning', case=False, na=False)].copy()

    print(f"Found {len(learning_df)} Learning scenarios\n")

    # Create output directories
    learning_dir = os.path.join(OUTPUT_BASE, 'Learning')
    extended_dir = os.path.join(OUTPUT_BASE, 'Learning_Extended')
    os.makedirs(learning_dir, exist_ok=True)
    os.makedirs(extended_dir, exist_ok=True)

    # Statistics
    stats = {
        'total': 0,
        'auto': 0,
        'review': 0,
        'manual': 0,
        'learning': 0,
        'extended': 0
    }

    # Process each scenario
    for idx, row in learning_df.iterrows():
        functional_area = row['Functional Area']

        # Determine output directory
        if 'Extended' in functional_area:
            output_dir = extended_dir
            stats['extended'] += 1
        else:
            output_dir = learning_dir
            stats['learning'] += 1

        try:
            filepath, confidence = generate_test_file(row, output_dir)

            # Update stats
            stats['total'] += 1
            if confidence >= 7.0:
                stats['auto'] += 1
            elif confidence >= 5.0:
                stats['review'] += 1
            else:
                stats['manual'] += 1

            print(f"  [OK] {os.path.basename(filepath)} (confidence: {confidence:.1f})")

        except Exception as e:
            print(f"  [ERROR] Failed to process {row['Scenario ID']}: {str(e)}")

    # Print summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)
    print(f"Total scenarios processed:     {stats['total']}")
    print(f"  - Learning:                  {stats['learning']}")
    print(f"  - Learning Extended:         {stats['extended']}")
    print(f"\nQuality Distribution:")
    print(f"  Auto-generated (>= 7.0):     {stats['auto']:3d} ({stats['auto']/stats['total']*100:.1f}%)")
    print(f"  Needs review (5.0-6.9):      {stats['review']:3d} ({stats['review']/stats['total']*100:.1f}%)")
    print(f"  Manual required (< 5.0):     {stats['manual']:3d} ({stats['manual']/stats['total']*100:.1f}%)")
    print("="*70)
    print(f"\nOutput directories:")
    print(f"  {os.path.abspath(learning_dir)}")
    print(f"  {os.path.abspath(extended_dir)}")

if __name__ == "__main__":
    main()
