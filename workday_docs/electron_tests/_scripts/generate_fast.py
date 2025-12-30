#!/usr/bin/env python3
"""
Fast Electron test generator - processes without RAG for speed
RAG can be added later for enhancement
"""

import pandas as pd
import os
from pathlib import Path

# Configuration
EXCEL_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx")
OUTPUT_BASE = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests")

# Area mappings
AREA_MAPPING = {
    'Tax': 'tax',
    'Revenue Management': 'revenue_management',
    'Asset Management': 'asset_management'
}

def assess_confidence_fast(scenario):
    """Fast confidence assessment without RAG"""
    score = 5.0
    reasons = []

    # Check if we have clear task steps
    if pd.notna(scenario.get('task_step')) and str(scenario['task_step']).strip():
        score += 1.0
        reasons.append("Clear task defined")
    else:
        return 4.0, "Missing task/step"

    # Check description
    desc = str(scenario.get('scenario_description', '')).lower()
    task = str(scenario.get('task_step', '')).lower()
    combined = desc + " " + task

    # Navigation/viewing tasks
    if any(kw in combined for kw in ['view', 'verify', 'validate', 'review', 'check']):
        score += 1.5
        reasons.append("Verification task")

    # Data entry tasks
    if any(kw in combined for kw in ['create', 'edit', 'update', 'enter', 'modify']):
        score += 1.0
        reasons.append("Data entry task")

    # Specific business terms
    if any(kw in combined for kw in ['tax', 'revenue', 'asset', 'depreciation', 'journal', 'calculation']):
        score += 0.5
        reasons.append("Domain-specific task")

    # Penalty for very short descriptions
    if len(combined.strip()) < 15:
        score -= 1.0
        reasons.append("PENALTY: Vague description")

    return min(10.0, max(0.0, score)), "; ".join(reasons)

def generate_electron_test(scenario, confidence):
    """Generate Electron test based on confidence"""

    scenario_id = scenario.get('scenario_id', 'UNKNOWN')
    scenario_name = scenario.get('scenario_name', 'Unknown Scenario')
    description = scenario.get('scenario_description', '')
    task_step = scenario.get('task_step', '')
    sub_task = scenario.get('sub_task', '')
    expected = scenario.get('expected_result', '')
    role = scenario.get('workday_role', 'Generic User')
    area = scenario.get('functional_area', '')

    # Header
    content = f"""# {scenario_id} - {scenario_name}
# Confidence Score: {confidence:.1f}/10.0
# Functional Area: {area}
# Role: {role}

"""

    if confidence >= 7.0:
        # HIGH CONFIDENCE - Full automation
        content += f"""## AUTOMATED TEST - HIGH CONFIDENCE
## Description: {description}

# Test Steps
describe "{scenario_id} - {scenario_name}" do

  before do
    login_as "{role}"
  end

  it "should complete: {scenario_name}" do
    # Step 1: Navigate to task
    enter search box as "{task_step}"
    wait for search results
    click search result containing "{task_step}"
    wait for page to load

"""

        task_lower = str(task_step).lower()

        if any(kw in task_lower for kw in ['view', 'verify', 'validate', 'review']):
            content += f"""    # Step 2: Verify page loaded
    verify page title contains "{scenario_name.split()[0]}"

    # Step 3: Validate key elements present
    verify page contains "{task_step}"

"""
            if pd.notna(expected) and str(expected).strip():
                content += f"""    # Step 4: Validate expected result
    # Expected: {expected}
    verify data accuracy

"""

            content += f"""    # Step 5: Take screenshot evidence
    screenshot as "{scenario_id}_complete.png"
"""

        elif any(kw in task_lower for kw in ['create', 'add', 'new']):
            content += f"""    # Step 2: Initiate creation
    click button "Create" or click link "New"
    wait for form to load

    # Step 3: Fill required fields
    # [NEEDS SME INPUT] - Specify exact field names and values
    enter field "field_name_1" as "value_1"
    enter field "field_name_2" as "value_2"

    # Step 4: Submit
    click button "Submit"
    wait for confirmation

    # Step 5: Verify success
    verify message contains "Success" or verify message contains "Completed"
    screenshot as "{scenario_id}_created.png"
"""

        elif any(kw in task_lower for kw in ['edit', 'update', 'modify', 'change']):
            content += f"""    # Step 2: Search for record
    enter search field as "search_criteria"
    click button "Search"
    wait for results

    # Step 3: Select record
    click first result

    # Step 4: Edit
    click button "Edit"
    wait for form to load

    # Step 5: Update fields
    # [NEEDS SME INPUT] - Specify field changes
    enter field "field_name" as "new_value"

    # Step 6: Save
    click button "Save"
    wait for confirmation
    verify message contains "Success"
    screenshot as "{scenario_id}_updated.png"
"""

        else:
            # Generic flow
            content += f"""    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: {task_step}

    # Step 3: Validation
    verify task completed successfully
    screenshot as "{scenario_id}_complete.png"
"""

        if pd.notna(sub_task) and str(sub_task).strip():
            content += f"""
    # Additional Sub-Task: {sub_task}
    # [NEEDS SME INPUT] - Define steps for sub-task
"""

        content += f"""  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: {expected if pd.notna(expected) else 'Per business requirements'}
# Sub-Task: {sub_task if pd.notna(sub_task) else 'None'}
"""

    elif confidence >= 5.0:
        # MEDIUM CONFIDENCE - Needs SME review
        content += f"""## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: {description}

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "{scenario_id} - {scenario_name}" do

  before do
    login_as "{role}"
  end

  it "should complete: {scenario_name}" do
    # Step 1: Navigate
    enter search box as "{task_step}"
    wait for search results
    click search result containing "{task_step}"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: {task_step}
    # Description: {description}
    # Sub-Task: {sub_task if pd.notna(sub_task) else 'N/A'}

    # Step 3: Validation
    # Expected Result: {expected if pd.notna(expected) else 'Define validation criteria'}

    # Step 4: Evidence
    screenshot as "{scenario_id}_complete.png"
  end

  after do
    logout
  end
end

# SME Actions Required:
# [ ] Define exact field names
# [ ] Specify test data values
# [ ] Define validation criteria
# [ ] Review business logic accuracy
"""

    else:
        # LOW CONFIDENCE - Manual only
        content += f"""## MANUAL TEST ONLY - LOW CONFIDENCE ({confidence:.1f}/10.0)

# This scenario requires manual execution due to insufficient automation detail

## Test Information
- **Scenario ID**: {scenario_id}
- **Functional Area**: {area}
- **Role**: {role}
- **Task**: {task_step}

## Manual Test Steps
1. Login as: {role}
2. Navigate to: {task_step}
3. Execute: {description}
4. Sub-Task: {sub_task if pd.notna(sub_task) else 'None'}
5. Validate: {expected if pd.notna(expected) else 'Per business requirements'}
6. Document results

## Reason for Manual Testing
- Insufficient task detail for automation
- Complex business logic requiring human judgment
- Missing field specifications

## Recommendations
1. Execute manually and document detailed steps
2. Capture field names and UI elements
3. Record business logic decisions
4. Create detailed Electron script from documentation
5. Submit for SME review
"""

    return content

def main():
    print("=" * 80)
    print("Workday Electron Test Generator (Fast Mode)")
    print("=" * 80)

    # Read Excel
    print(f"\n[1/4] Reading Excel: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Test Scenarios _ Source')

    # Filter
    print(f"[2/4] Filtering for Tax, Revenue Management, Asset Management...")
    areas = ['Tax', 'Revenue Management', 'Asset Management']
    filtered_df = df[df['Functional Area'].isin(areas)]

    print(f"  Total scenarios: {len(filtered_df)}")
    for area in areas:
        count = len(filtered_df[filtered_df['Functional Area'] == area])
        print(f"    - {area}: {count}")

    # Process
    stats = {
        'total': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0
    }

    for area_name, area_key in AREA_MAPPING.items():
        print(f"\n[3/4] Processing {area_name}...")

        area_df = filtered_df[filtered_df['Functional Area'] == area_name]
        area_output_dir = OUTPUT_BASE / area_key
        area_output_dir.mkdir(parents=True, exist_ok=True)

        for idx, row in area_df.iterrows():
            scenario = {
                'scenario_id': row['Scenario ID'],
                'scenario_name': row['Scenario Name'],
                'scenario_description': row['Scenario Description'],
                'task_step': row['Task / Step'],
                'sub_task': row['Sub Task'],
                'expected_result': row['Customer Expected Result'],
                'workday_role': row['Workday Role'],
                'test_type': row['Test Type'],
                'functional_area': area_name
            }

            if pd.isna(scenario['scenario_id']):
                continue

            stats['total'] += 1
            scenario_id = str(scenario['scenario_id']).strip()

            # Assess confidence
            confidence, reason = assess_confidence_fast(scenario)

            if confidence >= 7.0:
                stats['high_confidence'] += 1
                status = "[OK]"
            elif confidence >= 5.0:
                stats['medium_confidence'] += 1
                status = "[REVIEW]"
            else:
                stats['low_confidence'] += 1
                status = "[MANUAL]"

            print(f"  {status} {scenario_id}: {confidence:.1f}/10.0")

            # Generate
            test_content = generate_electron_test(scenario, confidence)

            # Save
            output_file = area_output_dir / f"{scenario_id.replace('/', '_')}.rb"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

    # Summary
    print("\n" + "=" * 80)
    print("[4/4] Generation Complete!")
    print("=" * 80)
    print(f"\nStatistics:")
    print(f"  Total scenarios: {stats['total']}")
    print(f"  High confidence (>=7.0): {stats['high_confidence']} ({stats['high_confidence']/stats['total']*100:.1f}%)")
    print(f"  Medium confidence (5.0-6.9): {stats['medium_confidence']} ({stats['medium_confidence']/stats['total']*100:.1f}%)")
    print(f"  Low confidence (<5.0): {stats['low_confidence']} ({stats['low_confidence']/stats['total']*100:.1f}%)")

    print(f"\nOutput directories:")
    for area_name, area_key in AREA_MAPPING.items():
        area_dir = OUTPUT_BASE / area_key
        file_count = len(list(area_dir.glob("*.rb")))
        print(f"  {area_dir}: {file_count} files")

if __name__ == "__main__":
    main()
