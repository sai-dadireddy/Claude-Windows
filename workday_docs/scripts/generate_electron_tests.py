#!/usr/bin/env python3
"""
Generate Electron test files from Workday test scenarios Excel
"""
import pandas as pd
import os
from pathlib import Path

# Configuration
EXCEL_PATH = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests"

# Target functional areas
AREAS = {
    'Projects': 'Projects',
    'Project Billing': 'Project_Billing',
    'Grants Management': 'Grants_Management',
    'Revenue Management': 'Revenue_Management'
}

# Workday operation mapping
WD_OPERATIONS = {
    'view': 'get',
    'verify': 'get',
    'validate': 'get',
    'review': 'get',
    'create': 'submit',
    'add': 'submit',
    'update': 'put',
    'edit': 'put',
    'modify': 'put',
    'submit': 'submit',
    'delete': 'cancel',
    'cancel': 'cancel'
}

def parse_scenario_to_electron(row):
    """Convert a test scenario row to Electron commands"""
    scenario_id = str(row.get('Scenario ID', '')).strip()
    scenario_name = str(row.get('Scenario Name', '')).strip()
    task = str(row.get('Task / Step', '')).strip()
    sub_task = str(row.get('Sub Task', '')).strip()
    description = str(row.get('Scenario Description', '')).strip()
    expected = str(row.get('Customer Expected Result', '')).strip()
    role = str(row.get('Workday Role', '')).strip()

    if not scenario_name or scenario_name == 'nan':
        return None

    # Determine operation type
    operation = 'get'
    name_lower = scenario_name.lower()
    for keyword, op in WD_OPERATIONS.items():
        if keyword in name_lower:
            operation = op
            break

    # Extract entity from scenario name
    entity = extract_entity(scenario_name)

    commands = []

    # Add header comment
    commands.append(f"# {scenario_id}: {scenario_name}")
    if description and description != 'nan':
        commands.append(f"# Description: {description}")
    if role and role != 'nan':
        commands.append(f"# Role: {role}")
    commands.append("")

    # Add main command
    if operation == 'get':
        commands.append(f"electron.get('{entity}')")
        if expected and expected != 'nan':
            commands.append(f"electron.verify('{expected}')")
    elif operation == 'submit':
        commands.append(f"electron.navigate('{entity}')")
        commands.append(f"electron.create('{entity}')")
        if task and task != 'nan':
            commands.append(f"# Task: {task}")
        if sub_task and sub_task != 'nan':
            commands.append(f"# Sub-task: {sub_task}")
        commands.append(f"electron.submit()")
    elif operation == 'put':
        commands.append(f"electron.search('{entity}')")
        commands.append(f"electron.edit('{entity}')")
        if task and task != 'nan':
            commands.append(f"# Task: {task}")
        commands.append(f"electron.save()")
    elif operation == 'cancel':
        commands.append(f"electron.search('{entity}')")
        commands.append(f"electron.cancel('{entity}')")

    commands.append("")
    return "\n".join(commands)

def extract_entity(scenario_name):
    """Extract entity name from scenario"""
    # Remove common prefixes
    name = scenario_name
    for prefix in ['Verify', 'Validate', 'View', 'Create', 'Update', 'Edit', 'Submit', 'Delete', 'Cancel']:
        if name.startswith(prefix):
            name = name[len(prefix):].strip()
            break

    # Clean up
    if not name:
        name = scenario_name

    return name

def process_area(df, area_name, output_folder):
    """Process one functional area"""
    filtered = df[df['Functional Area'] == area_name].copy()

    if len(filtered) == 0:
        print(f"No data for {area_name}")
        return

    # Group by scenario
    scenarios = filtered.groupby('Scenario ID')

    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append(f"WORKDAY ELECTRON TESTS - {area_name.upper()}")
    output_lines.append("=" * 80)
    output_lines.append(f"Generated: 2025-12-30")
    output_lines.append(f"Total Scenarios: {len(scenarios)}")
    output_lines.append("=" * 80)
    output_lines.append("")

    for scenario_id, group in scenarios:
        # Use first row for main scenario info
        row = group.iloc[0]
        electron_test = parse_scenario_to_electron(row)

        if electron_test:
            output_lines.append(electron_test)

            # Add additional steps if present
            if len(group) > 1:
                output_lines.append("# Additional steps:")
                for idx, step_row in group.iloc[1:].iterrows():
                    task = str(step_row.get('Task / Step', '')).strip()
                    if task and task != 'nan':
                        output_lines.append(f"# - {task}")
                output_lines.append("")

    # Write to file
    output_path = os.path.join(output_folder, f"{area_name.replace(' ', '_').lower()}_tests.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))

    print(f"[OK] Generated {output_path} ({len(scenarios)} scenarios)")

def main():
    # Read Excel
    print(f"Reading {EXCEL_PATH}...")
    df = pd.read_excel(EXCEL_PATH)

    print(f"Total rows: {len(df)}")
    print(f"Functional areas: {df['Functional Area'].nunique()}")
    print()

    # Process each area
    for area_name, folder_name in AREAS.items():
        output_folder = os.path.join(OUTPUT_BASE, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        print(f"Processing {area_name}...")
        process_area(df, area_name, output_folder)
        print()

    print("Done!")

if __name__ == '__main__':
    main()
