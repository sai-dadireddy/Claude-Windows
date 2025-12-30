#!/usr/bin/env python3
"""
Generate Electron Test Scenarios for Benefits Functional Area
Queries Workday RAG for each scenario to generate accurate test steps
"""

import pandas as pd
import subprocess
import os
import re
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Benefits"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

def sanitize_filename(name):
    """Sanitize scenario name for filename"""
    # Remove special characters, replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', name)
    sanitized = re.sub(r'[\s]+', '_', sanitized)
    return sanitized[:100]  # Limit length

def query_rag(task_step):
    """Query Workday RAG for task/step information"""
    try:
        result = subprocess.run(
            ['python', RAG_SCRIPT, task_step],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"RAG_ERROR: {str(e)}"

def calculate_confidence(task_step, rag_result, expected_result):
    """Calculate confidence score for test generation"""
    score = 5.0  # Base score

    # Check if task/step is provided
    if not task_step or pd.isna(task_step):
        return "LOW", 1.0

    # Check RAG result quality
    if "RAG_ERROR" in rag_result:
        score -= 3.0
    elif len(rag_result) < 50:
        score -= 2.0
    elif "operation" in rag_result.lower() or "request" in rag_result.lower():
        score += 2.0

    # Check expected result clarity
    if expected_result and not pd.isna(expected_result):
        score += 2.0

    # Determine confidence level
    if score >= 7.5:
        level = "HIGH"
    elif score >= 5.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level, min(10.0, max(1.0, score))

def extract_electron_steps(task_step, rag_result):
    """Extract Electron automation steps from RAG result"""
    steps = []

    # Start with search
    steps.append(f'1. enter search box as "{task_step}"')
    steps.append('2. wait for search results')
    steps.append(f'3. click search result containing "{task_step}"')

    # Parse RAG result for additional steps
    if "operation" in rag_result.lower():
        # Try to extract operation name
        lines = rag_result.split('\n')
        for line in lines:
            if 'operation' in line.lower() or 'request' in line.lower():
                steps.append(f'4. wait for page load')
                steps.append(f'5. fill required fields based on RAG guidance')
                break

    return steps

def generate_test_file(row, output_dir):
    """Generate individual test scenario file"""
    scenario_id = row.get('Scenario ID', 'UNKNOWN')
    scenario_name = row.get('Scenario Name', 'UNKNOWN')
    task_step = row.get('Task / Step', '')
    expected_result = row.get('Customer Expected Result', '')

    # Sanitize filename
    safe_name = sanitize_filename(scenario_name)
    filename = f"{scenario_id}_{safe_name}.txt"
    filepath = os.path.join(output_dir, filename)

    # Check if manual required
    if not task_step or pd.isna(task_step):
        content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: Benefits
TEST NAME: {scenario_name}
STATUS: [MANUAL REQUIRED]
================================================================================

REASON: Missing Task/Step field - cannot generate automated steps
EXPECTED RESULT: {expected_result}

MANUAL ACTIONS REQUIRED:
Please manually define test steps for this scenario.
================================================================================
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return 'MANUAL'

    # Query RAG
    print(f"Querying RAG for: {task_step}")
    rag_result = query_rag(task_step)

    # Calculate confidence
    confidence_level, confidence_score = calculate_confidence(task_step, rag_result, expected_result)

    # Extract steps
    electron_steps = extract_electron_steps(task_step, rag_result)

    # Add screenshot step
    electron_steps.append(f'{len(electron_steps) + 1}. screenshot as "{scenario_id}_complete.png"')

    # Generate file content
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: Benefits
TEST NAME: {scenario_name}
CONFIDENCE: [{confidence_level}] Score: {confidence_score:.1f}/10
================================================================================

TASK/STEP: {task_step}

RAG QUERY RESULT:
{rag_result[:500]}
{'' if len(rag_result) <= 500 else '... (truncated)'}

ELECTRON STEPS:
{chr(10).join(electron_steps)}

VERIFICATION:
- [ ] {expected_result}

NOTES:
- Confidence score based on RAG result quality and expected result clarity
- Review and enhance steps as needed based on actual Workday UI
================================================================================
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return confidence_level

def main():
    """Main processing function"""
    # Load Excel
    print(f"Loading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)

    # Filter for Benefits
    benefits_df = df[df['Functional Area'] == 'Benefits'].copy()
    print(f"Found {len(benefits_df)} Benefits scenarios")

    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Process each scenario
    stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'MANUAL': 0}

    for idx, row in benefits_df.iterrows():
        scenario_id = row.get('Scenario ID', f'UNK_{idx}')
        print(f"\nProcessing {scenario_id}...")

        result = generate_test_file(row, OUTPUT_DIR)
        stats[result] = stats.get(result, 0) + 1

    # Print summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE")
    print("="*80)
    print(f"Total Scenarios: {len(benefits_df)}")
    print(f"High Confidence: {stats['HIGH']}")
    print(f"Medium Confidence: {stats['MEDIUM']}")
    print(f"Low Confidence: {stats['LOW']}")
    print(f"Manual Required: {stats['MANUAL']}")
    print(f"\nOutput Directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
