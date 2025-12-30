#!/usr/bin/env python3
"""
Extract Time/Absence/Scheduling scenarios from master Excel file
"""
import pandas as pd
import json
import os
from pathlib import Path

def extract_scenarios():
    excel_file = 'WD_Test_Scenarios_Master.xlsx'
    output_json = 'time_absence_scheduling_scenarios.json'

    # Read Excel
    df = pd.read_excel(excel_file, sheet_name='Test Scenarios _ Source')

    # Filter for target functional areas
    target_areas = ['Scheduling', 'Absence', 'Time Tracking']
    filtered_df = df[df['Functional Area'].isin(target_areas)].copy()

    print(f"Total scenarios found: {len(filtered_df)}")
    print(f"\nBreakdown:")
    for area in target_areas:
        count = len(filtered_df[filtered_df['Functional Area'] == area])
        print(f"  {area}: {count}")

    # Show sample scenarios
    print(f"\n=== Sample Scheduling Scenarios ===")
    scheduling = filtered_df[filtered_df['Functional Area'] == 'Scheduling'].head(3)
    for idx, row in scheduling.iterrows():
        print(f"\nScenario ID: {row['Scenario ID']}")
        print(f"Name: {row['Scenario Name']}")
        desc = row['Scenario Description']
        if pd.notna(desc):
            print(f"Description: {str(desc)[:100]}...")
        else:
            print("Description: N/A")
        print(f"Task/Step: {row['Task / Step']}")

    # Export to JSON for processing
    output = []
    for idx, row in filtered_df.iterrows():
        output.append({
            'row_id': int(row['Row ID']) if pd.notna(row['Row ID']) else None,
            'functional_area': str(row['Functional Area']) if pd.notna(row['Functional Area']) else None,
            'scenario_id': str(row['Scenario ID']) if pd.notna(row['Scenario ID']) else None,
            'scenario_name': str(row['Scenario Name']) if pd.notna(row['Scenario Name']) else None,
            'scenario_description': str(row['Scenario Description']) if pd.notna(row['Scenario Description']) else None,
            'task_step': str(row['Task / Step']) if pd.notna(row['Task / Step']) else None,
            'sub_task': str(row['Sub Task']) if pd.notna(row['Sub Task']) else None,
            'expected_result': str(row['Customer Expected Result']) if pd.notna(row['Customer Expected Result']) else None,
            'effort_mins': float(row['Est. Effort (mins)']) if pd.notna(row['Est. Effort (mins)']) else None,
            'workday_role': str(row['Workday Role']) if pd.notna(row['Workday Role']) else None
        })

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Exported {len(output)} scenarios to {output_json}")
    return output

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    scenarios = extract_scenarios()
