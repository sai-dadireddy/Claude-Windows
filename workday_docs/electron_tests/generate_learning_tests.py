#!/usr/bin/env python3
"""
Generate Electron test files for Learning functional areas
"""
import pandas as pd
import subprocess
import json
import re
import os
from pathlib import Path

# Paths
EXCEL_PATH = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/workday_rag.py"
OUTPUT_BASE = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests"

def sanitize_filename(name):
    """Convert scenario name to safe filename"""
    # Remove special characters, replace spaces with underscores
    safe = re.sub(r'[^\w\s-]', '', name)
    safe = re.sub(r'[-\s]+', '_', safe)
    return safe[:100]  # Limit length

def query_rag(task_description):
    """Query Workday RAG for task information"""
    try:
        result = subprocess.run(
            ['python', RAG_SCRIPT, task_description],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"RAG Query Error: {str(e)}"

def extract_electron_commands(task_step, rag_response):
    """Generate Electron commands based on task and RAG context"""
    commands = []
    confidence = 5.0

    task_lower = task_step.lower()

    # Header
    commands.append(f"# Task: {task_step}")
    commands.append(f"# RAG Context Summary:")
    commands.append(f"# {rag_response[:200]}...")
    commands.append("")

    # Pattern matching for common Learning tasks

    # Report running
    if 'run' in task_lower and 'report' in task_lower:
        report_match = re.search(r'"([^"]+)"', task_step)
        if report_match:
            report_name = report_match.group(1)
            commands.append(f'search "{report_name}"')
            commands.append('wait 2')
            commands.append(f'click "link:{report_name}"')
            commands.append('wait 3')
            confidence = 8.0
        else:
            commands.append('search "View Security Group"')
            commands.append('wait 2')
            commands.append('click "link:View Security Group"')
            commands.append('wait 3')
            confidence = 6.0

    # Learning Worklet access
    elif 'learning worklet' in task_lower:
        commands.append('click "button:Learning"')
        commands.append('wait 2')
        confidence = 7.5

    # Dashboard access
    elif 'dashboard' in task_lower:
        if 'onboarding' in task_lower:
            commands.append('search "Onboarding Dashboard"')
            commands.append('wait 2')
            commands.append('click "link:Onboarding Dashboard"')
            commands.append('wait 3')
            confidence = 8.0
        elif 'learning' in task_lower:
            commands.append('search "Learning Dashboard"')
            commands.append('wait 2')
            commands.append('click "link:Learning Dashboard"')
            commands.append('wait 3')
            confidence = 8.0

    # Edit/Create tasks
    elif 'edit' in task_lower or 'create' in task_lower:
        if 'learning topic' in task_lower:
            commands.append('search "Edit Learning Topic"')
            commands.append('wait 2')
            commands.append('click "link:Edit Learning Topic"')
            commands.append('wait 3')
            confidence = 7.0
        elif 'course' in task_lower:
            commands.append('search "Create Course"')
            commands.append('wait 2')
            commands.append('click "link:Create Course"')
            commands.append('wait 3')
            confidence = 7.0
        elif 'lesson' in task_lower:
            commands.append('search "Create Lesson"')
            commands.append('wait 2')
            commands.append('click "link:Create Lesson"')
            commands.append('wait 3')
            confidence = 7.0

    # Security Group tasks
    elif 'security group' in task_lower:
        commands.append('search "Maintain Security Groups"')
        commands.append('wait 2')
        commands.append('click "link:Maintain Security Groups"')
        commands.append('wait 3')
        confidence = 7.5

    # Enrollment tasks
    elif 'enroll' in task_lower:
        if 'student' in task_lower:
            commands.append('search "Enroll Student in Course"')
            commands.append('wait 2')
            commands.append('click "link:Enroll Student in Course"')
            commands.append('wait 3')
            confidence = 7.5
        else:
            commands.append('search "Enrollment"')
            commands.append('wait 2')
            confidence = 6.0

    # Assignment tasks
    elif 'assign' in task_lower:
        if 'learning' in task_lower:
            commands.append('search "Assign Learning"')
            commands.append('wait 2')
            commands.append('click "link:Assign Learning"')
            commands.append('wait 3')
            confidence = 7.5

    # Submit/Complete tasks
    elif 'submit' in task_lower or 'complete' in task_lower:
        commands.append('click "button:Submit"')
        commands.append('wait 2')
        confidence = 7.0

    # View/Review tasks
    elif 'view' in task_lower or 'review' in task_lower:
        if 'transcript' in task_lower:
            commands.append('search "View Learning Transcript"')
            commands.append('wait 2')
            commands.append('click "link:View Learning Transcript"')
            commands.append('wait 3')
            confidence = 8.0
        else:
            commands.append('# View task - context specific')
            confidence = 5.0

    # Navigation tasks (Home > Menu)
    elif '>' in task_step:
        parts = [p.strip() for p in task_step.split('>')]
        for i, part in enumerate(parts):
            if part.lower() != 'home':
                commands.append(f'click "link:{part}"')
                commands.append('wait 2')
        confidence = 6.5

    # Generic fallback
    else:
        commands.append('# Task requires manual implementation')
        commands.append(f'# Context: {task_step}')
        confidence = 4.0

    return commands, confidence

def generate_test_file(row, output_dir):
    """Generate a single test file"""
    scenario_id = row['Scenario ID']
    task_step = row['Task / Step']
    functional_area = row['Functional Area']

    # Query RAG
    print(f"Processing {scenario_id}: {task_step[:60]}...")
    rag_response = query_rag(task_step)

    # Generate Electron commands
    commands, confidence = extract_electron_commands(task_step, rag_response)

    # Determine file suffix
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
        f.write(f"# Scenario ID: {scenario_id}\n")
        f.write(f"# Functional Area: {functional_area}\n")
        f.write(f"# Status: {status}\n")
        f.write(f"# Confidence: {confidence:.1f}/10.0\n")
        f.write(f"# Original Task: {task_step}\n")
        f.write("#" + "="*70 + "\n\n")

        for cmd in commands:
            f.write(cmd + "\n")

        if confidence < 7.0:
            f.write("\n# NOTES:\n")
            f.write("# This test requires manual review and enhancement\n")
            f.write("# RAG context may provide additional implementation details\n")

    return filepath, confidence

def main():
    """Main processing function"""
    print("Loading Excel file...")
    df = pd.read_excel(EXCEL_PATH)

    # Filter Learning scenarios
    learning_df = df[df['Functional Area'].str.contains('Learning', case=False, na=False)].copy()

    print(f"Found {len(learning_df)} Learning scenarios")

    # Process each scenario
    stats = {
        'total': 0,
        'auto': 0,
        'review': 0,
        'manual': 0
    }

    for idx, row in learning_df.iterrows():
        functional_area = row['Functional Area']

        # Determine output directory
        if 'Extended' in functional_area:
            output_dir = os.path.join(OUTPUT_BASE, 'Learning_Extended')
        else:
            output_dir = os.path.join(OUTPUT_BASE, 'Learning')

        # Generate test file
        filepath, confidence = generate_test_file(row, output_dir)

        # Update stats
        stats['total'] += 1
        if confidence >= 7.0:
            stats['auto'] += 1
        elif confidence >= 5.0:
            stats['review'] += 1
        else:
            stats['manual'] += 1

        print(f"  ✓ Generated: {os.path.basename(filepath)} (confidence: {confidence:.1f})")

    # Print summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)
    print(f"Total scenarios processed: {stats['total']}")
    print(f"Auto-generated (≥7.0):     {stats['auto']} ({stats['auto']/stats['total']*100:.1f}%)")
    print(f"Needs review (5.0-6.9):    {stats['review']} ({stats['review']/stats['total']*100:.1f}%)")
    print(f"Manual required (<5.0):    {stats['manual']} ({stats['manual']/stats['total']*100:.1f}%)")
    print("="*70)

if __name__ == "__main__":
    main()
