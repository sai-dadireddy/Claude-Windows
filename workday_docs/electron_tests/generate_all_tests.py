#!/usr/bin/env python3
"""
Generate Electron test files for Tax, Revenue_Management, and Asset_Management
from WD_Test_Scenarios_Master.xlsx
"""

import pandas as pd
import json
import os
import sys
import subprocess
from pathlib import Path

# Configuration
EXCEL_PATH = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/WD_Test_Scenarios_Master.xlsx")
OUTPUT_BASE = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests")
RAG_SCRIPT = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/workday_rag.py")

# Functional area mappings
AREA_MAPPING = {
    'Tax': 'tax',
    'Revenue Management': 'revenue_management',
    'Asset Management': 'asset_management'
}

def query_rag(query):
    """Query Workday RAG for relevant documentation"""
    try:
        result = subprocess.run(
            ['python', str(RAG_SCRIPT), query],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception as e:
        print(f"RAG query failed: {e}")
        return ""

def assess_confidence(scenario, rag_result):
    """
    Assess confidence level for generating Electron test
    Returns: (confidence_score, reason)
    - 7.0-10.0: Full automation possible
    - 5.0-6.9: Needs SME review
    - < 5.0: Manual only
    """
    score = 5.0  # Base score
    reasons = []

    # Check if we have clear task steps
    if pd.notna(scenario.get('task_step')) and scenario['task_step'].strip():
        score += 1.0
        reasons.append("Clear task/step defined")

    # Check if RAG found relevant info
    if rag_result and len(rag_result) > 100:
        score += 1.5
        reasons.append("RAG found relevant documentation")

    # Check for specific Electron-friendly keywords
    task = str(scenario.get('task_step', '')).lower()
    desc = str(scenario.get('scenario_description', '')).lower()
    combined = task + " " + desc

    # Navigation keywords
    if any(kw in combined for kw in ['view', 'navigate', 'open', 'access', 'search']):
        score += 0.5
        reasons.append("Contains navigation keywords")

    # Action keywords
    if any(kw in combined for kw in ['create', 'edit', 'update', 'submit', 'approve', 'verify']):
        score += 0.5
        reasons.append("Contains action keywords")

    # Validation keywords
    if any(kw in combined for kw in ['validate', 'verify', 'check', 'confirm']):
        score += 0.5
        reasons.append("Contains validation keywords")

    # Penalty for vague descriptions
    if len(combined.strip()) < 20:
        score -= 1.0
        reasons.append("PENALTY: Description too vague")

    # Bonus for specific business process names
    if any(kw in combined for kw in ['tax applicability', 'revenue', 'asset', 'depreciation', 'journal']):
        score += 0.5
        reasons.append("Specific business process mentioned")

    return min(10.0, max(0.0, score)), "; ".join(reasons)

def generate_electron_test(scenario, confidence, rag_result):
    """Generate Electron test content based on confidence level"""

    scenario_id = scenario.get('scenario_id', 'UNKNOWN')
    scenario_name = scenario.get('scenario_name', 'Unknown Scenario')
    description = scenario.get('scenario_description', '')
    task_step = scenario.get('task_step', '')
    role = scenario.get('workday_role', 'Generic User')

    # Header
    content = f"""# {scenario_id} - {scenario_name}
# Confidence Score: {confidence:.1f}/10.0
# Role: {role}

"""

    if confidence >= 7.0:
        # Full automation - generate Electron commands
        content += f"""## AUTOMATED TEST
## Description: {description}

# Test Steps
describe "{scenario_id} - {scenario_name}" do

  # Setup
  before do
    login_as "{role}"
  end

  it "should complete: {scenario_name}" do
    # Step 1: Navigate to task
    navigate_to_task "{task_step}"
    wait_for_page_load

"""

        # Add specific steps based on task type
        task_lower = str(task_step).lower()

        if 'view' in task_lower or 'verify' in task_lower:
            content += f"""    # Step 2: Verify page loaded
    expect(page).to have_content "{scenario_name.split()[0]}"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#{scenario_id}_verification"
"""
        elif 'create' in task_lower or 'submit' in task_lower:
            content += f"""    # Step 2: Click Create/New
    click_button "Create" || click_link "New"

    # Step 3: Fill required fields
    # [NEEDS SME REVIEW] - Specify exact field names
    fill_in "field_name_1", with: "test_value"

    # Step 4: Submit
    click_button "Submit"
    wait_for_success_message

    # Step 5: Verify creation
    expect(page).to have_content "Successfully"
"""
        elif 'edit' in task_lower or 'update' in task_lower:
            content += f"""    # Step 2: Search for record
    search_for "record_identifier"

    # Step 3: Open record
    click_first_result

    # Step 4: Click Edit
    click_button "Edit"

    # Step 5: Update fields
    # [NEEDS SME REVIEW] - Specify exact field changes
    fill_in "field_name", with: "updated_value"

    # Step 6: Save changes
    click_button "Save"
    wait_for_success_message
"""

        content += f"""  end

  # Cleanup
  after do
    logout
  end
end

# RAG Context:
# {rag_result[:500] if rag_result else 'No RAG data available'}
"""

    elif confidence >= 5.0:
        # Needs SME review - partial automation
        content += f"""## [NEEDS SME REVIEW] - PARTIAL AUTOMATION
## Description: {description}

# Test Steps (requires SME input for specific field names and values)
describe "{scenario_id} - {scenario_name}" do

  before do
    login_as "{role}"
  end

  it "should complete: {scenario_name}" do
    # Step 1: Navigate to task
    # [SME REVIEW NEEDED] - Verify exact task name
    navigate_to_task "{task_step}"
    wait_for_page_load

    # Step 2: Perform main action
    # [SME REVIEW NEEDED] - Specify exact steps and field names
    # Task: {task_step}
    # Description: {description}

    # Step 3: Validation
    # [SME REVIEW NEEDED] - Define expected results

    # Step 4: Screenshot evidence
    screenshot "#{scenario_id}_completion"
  end

  after do
    logout
  end
end

# RAG Context:
# {rag_result[:500] if rag_result else 'No RAG data available'}

# SME Actions Required:
# 1. Verify task navigation path
# 2. Specify exact field names and values
# 3. Define validation criteria
# 4. Review business logic accuracy
"""

    else:
        # Manual only - too low confidence
        content += f"""## MANUAL TEST ONLY - Insufficient automation confidence
## Description: {description}

# This scenario requires manual testing due to:
# - Insufficient detail in scenario description
# - Complex business logic requiring human judgment
# - Limited RAG documentation available

## Manual Test Steps:
1. Login as: {role}
2. Navigate to: {task_step}
3. Execute: {description}
4. Validate: {scenario.get('expected_result', 'As per business requirements')}

## Additional Information:
- Scenario ID: {scenario_id}
- Test Type: {scenario.get('test_type', 'N/A')}

# RAG Context:
# {rag_result[:300] if rag_result else 'No RAG data available'}

# Recommended Approach:
# 1. Perform manual test execution
# 2. Document detailed steps taken
# 3. Create Electron script based on documented steps
# 4. Submit for SME review before automation
"""

    return content

def main():
    print("=" * 80)
    print("Workday Electron Test Generator")
    print("=" * 80)

    # Read Excel file
    print(f"\n[1/5] Reading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Test Scenarios _ Source')

    # Filter for target areas
    print(f"[2/5] Filtering for Tax, Revenue Management, Asset Management...")
    areas = ['Tax', 'Revenue Management', 'Asset Management']
    filtered_df = df[df['Functional Area'].isin(areas)]

    print(f"  Total scenarios: {len(filtered_df)}")
    for area in areas:
        count = len(filtered_df[filtered_df['Functional Area'] == area])
        print(f"    - {area}: {count}")

    # Process each area
    stats = {
        'total': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0
    }

    for area_name, area_key in AREA_MAPPING.items():
        print(f"\n[3/5] Processing {area_name}...")

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
                'test_type': row['Test Type']
            }

            # Skip if no scenario ID
            if pd.isna(scenario['scenario_id']):
                continue

            stats['total'] += 1
            scenario_id = str(scenario['scenario_id']).strip()

            # Query RAG
            rag_query = f"{area_name} {scenario['scenario_name']} {scenario['task_step']}"
            print(f"  Processing {scenario_id}: {scenario['scenario_name'][:50]}...")
            rag_result = query_rag(rag_query)

            # Assess confidence
            confidence, reason = assess_confidence(scenario, rag_result)

            if confidence >= 7.0:
                stats['high_confidence'] += 1
                print(f"    ✓ High confidence ({confidence:.1f})")
            elif confidence >= 5.0:
                stats['medium_confidence'] += 1
                print(f"    ⚠ Medium confidence ({confidence:.1f}) - Needs SME review")
            else:
                stats['low_confidence'] += 1
                print(f"    ✗ Low confidence ({confidence:.1f}) - Manual only")

            # Generate test file
            test_content = generate_electron_test(scenario, confidence, rag_result)

            # Save to file
            output_file = area_output_dir / f"{scenario_id.replace('/', '_')}.rb"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

    # Print summary
    print("\n" + "=" * 80)
    print("[5/5] Generation Complete!")
    print("=" * 80)
    print(f"\nStatistics:")
    print(f"  Total scenarios processed: {stats['total']}")
    print(f"  High confidence (>=7.0): {stats['high_confidence']} ({stats['high_confidence']/stats['total']*100:.1f}%)")
    print(f"  Medium confidence (5.0-6.9): {stats['medium_confidence']} ({stats['medium_confidence']/stats['total']*100:.1f}%)")
    print(f"  Low confidence (<5.0): {stats['low_confidence']} ({stats['low_confidence']/stats['total']*100:.1f}%)")

    print(f"\nOutput directories:")
    for area_name, area_key in AREA_MAPPING.items():
        area_dir = OUTPUT_BASE / area_key
        file_count = len(list(area_dir.glob("*.rb")))
        print(f"  {area_dir}: {file_count} test files")

    print("\nNext Steps:")
    print("  1. Review all [NEEDS SME REVIEW] files")
    print("  2. Enhance Manual test files with specific steps")
    print("  3. Validate high-confidence tests with SMEs")
    print("  4. Execute tests in Electron framework")

if __name__ == "__main__":
    main()
