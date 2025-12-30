#!/usr/bin/env python3
"""
Process Excel test scenarios and extract for specific modules
"""
import pandas as pd
import json
import sys

def main():
    excel_path = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"

    try:
        # Read Excel file
        print("Reading Excel file...")
        df = pd.read_excel(excel_path)

        print(f"Total scenarios: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")

        # Filter for the three modules
        modules = {
            'Grants Management': 'Grants_Management',
            'Projects': 'Projects',
            'Project Billing': 'Project_Billing'
        }

        all_scenarios = {}

        for module_name, folder_name in modules.items():
            # Case-insensitive search in Module column
            module_df = df[df['Module'].str.contains(module_name, case=False, na=False)]

            print(f"\n{module_name}: {len(module_df)} scenarios")

            # Convert to list of dicts
            scenarios = []
            for idx, row in module_df.iterrows():
                scenario = {
                    'Scenario_ID': row.get('Scenario_ID', ''),
                    'Functional_Area': row.get('Functional Area', row.get('Module', '')),
                    'Scenario_Name': row.get('Scenario_Name', ''),
                    'Scenario_Description': row.get('Scenario_Description', ''),
                    'Task': row.get('Task', row.get('Task / Step', '')),
                    'Step': row.get('Step', ''),
                    'Sub_Task': row.get('Sub_Task', row.get('Sub Task', '')),
                    'Expected_Result': row.get('Customer_Expected_Result', row.get('Customer Expected Result', '')),
                    'Est_Effort_Mins': row.get('Est_Effort_Mins', row.get('Est. Effort (mins)', '')),
                    'Workday_Role': row.get('Workday_Role', row.get('Workday Role', ''))
                }
                scenarios.append(scenario)

            all_scenarios[folder_name] = scenarios

            # Show sample
            if scenarios:
                print(f"Sample scenario: {scenarios[0]['Scenario_ID']} - {scenarios[0]['Scenario_Name']}")

        # Save to JSON
        output_path = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\filtered_scenarios.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_scenarios, f, indent=2, default=str)

        print(f"\n✅ Saved filtered scenarios to: {output_path}")

        # Print summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        for folder_name, scenarios in all_scenarios.items():
            print(f"{folder_name}: {len(scenarios)} scenarios")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
