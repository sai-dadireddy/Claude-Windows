#!/usr/bin/env python3
"""
Generate Electron tests for Inventory and Asset Management from Excel master file.
"""

import pandas as pd
import os
import subprocess
import re
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"
OUTPUT_BASE = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"

# Functional areas to process
AREAS = {
    "Inventory": "Inventory",
    "Asset Management": "Asset_Management"
}

def query_rag(query_text):
    """Query the Workday RAG system."""
    try:
        result = subprocess.run(
            ["python", RAG_SCRIPT, query_text],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"RAG query failed: {e}")
        return None

def calculate_confidence(task_step, rag_response):
    """Calculate confidence score based on RAG response quality."""
    if not rag_response or "No results found" in rag_response:
        return "LOW", 2.0

    # Check for indicators of high quality response
    high_indicators = [
        "Get_", "Submit_", "Put_", "Request",  # SOAP operations
        "endpoint", "API", "service",  # REST/SOAP terms
        "step", "navigate", "click", "enter"  # Procedural steps
    ]

    medium_indicators = [
        "page", "field", "button", "form",
        "record", "document", "transaction"
    ]

    score = 5.0  # Base score
    response_lower = rag_response.lower()

    # Check high indicators
    high_count = sum(1 for ind in high_indicators if ind.lower() in response_lower)
    if high_count >= 3:
        score += 3.0
    elif high_count >= 1:
        score += 1.5

    # Check medium indicators
    medium_count = sum(1 for ind in medium_indicators if ind.lower() in response_lower)
    if medium_count >= 2:
        score += 1.0

    # Length check (longer responses often more detailed)
    if len(rag_response) > 500:
        score += 1.0
    elif len(rag_response) > 200:
        score += 0.5

    # Determine confidence level
    if score >= 8.0:
        return "HIGH", min(score, 10.0)
    elif score >= 5.5:
        return "MEDIUM", score
    else:
        return "LOW", score

def generate_electron_steps(task_step, rag_response, scenario_id):
    """Generate Electron test steps from RAG response."""
    steps = []

    # Always start with search
    steps.append(f'1. enter search box as "{task_step}"')

    if not rag_response or "No results found" in rag_response:
        steps.append("2. [MANUAL] No RAG guidance available - manual test required")
        steps.append(f'3. screenshot as "{scenario_id}_complete.png"')
        return steps

    # Parse RAG response for actionable steps
    step_num = 2

    # Look for common patterns
    if "navigate" in rag_response.lower() or "go to" in rag_response.lower():
        steps.append(f"{step_num}. wait for page load")
        step_num += 1

    # Look for field entries
    field_patterns = re.findall(r'enter\s+([^,\.]+)', rag_response, re.IGNORECASE)
    for field in field_patterns[:3]:  # Limit to 3 fields
        steps.append(f'{step_num}. enter field "{field.strip()}" with appropriate value')
        step_num += 1

    # Look for clicks/actions
    if "click" in rag_response.lower() or "select" in rag_response.lower():
        steps.append(f"{step_num}. click appropriate action button")
        step_num += 1

    # Look for submit/save
    if "submit" in rag_response.lower() or "save" in rag_response.lower():
        steps.append(f"{step_num}. submit form")
        step_num += 1

    # If no specific steps found, add generic navigation
    if len(steps) == 1:
        steps.append(f"{step_num}. navigate to appropriate page")
        step_num += 1
        steps.append(f"{step_num}. complete required fields")
        step_num += 1

    # Always end with screenshot
    steps.append(f'{step_num}. screenshot as "{scenario_id}_complete.png"')

    return steps

def create_test_file(row, area_folder, rag_response=None):
    """Create individual test file for a scenario."""
    scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
    scenario_name = str(row.get('Scenario Name', 'Unnamed')).strip()
    task_step = str(row.get('Task / Step', '')).strip()
    expected_result = str(row.get('Customer Expected Result', 'No expected result specified')).strip()
    functional_area = str(row.get('Functional Area', '')).strip()

    # Calculate confidence
    confidence_level, confidence_score = calculate_confidence(task_step, rag_response)

    # Generate steps
    electron_steps = generate_electron_steps(task_step, rag_response, scenario_id)

    # Create filename
    safe_name = re.sub(r'[^\w\s-]', '', scenario_name).strip().replace(' ', '_')[:50]
    filename = f"{scenario_id}_{safe_name}.txt"
    filepath = os.path.join(area_folder, filename)

    # Build file content
    content = f"""{'='*80}
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
TEST NAME: {scenario_name}
CONFIDENCE: [{confidence_level}] Score: {confidence_score:.1f}/10
{'='*80}

TASK/STEP: {task_step if task_step else '[NO TASK SPECIFIED]'}

ELECTRON STEPS:
{chr(10).join(electron_steps)}

VERIFICATION: {expected_result}

{'='*80}
RAG RESPONSE SUMMARY:
"""

    if rag_response:
        # Truncate RAG response for file
        rag_summary = rag_response[:500] + "..." if len(rag_response) > 500 else rag_response
        content += f"{rag_summary}\n"
    else:
        content += "[NO RAG RESPONSE] - Manual test creation required\n"

    content += f"{'='*80}\n"

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath, confidence_level

def process_functional_area(df, area_name, area_folder):
    """Process all scenarios for a functional area."""
    # Filter by functional area
    area_df = df[df['Functional Area'].str.strip() == area_name].copy()

    print(f"\n{'='*80}")
    print(f"Processing {area_name}: {len(area_df)} scenarios")
    print(f"{'='*80}\n")

    # Create output folder
    os.makedirs(area_folder, exist_ok=True)

    stats = {
        'total': len(area_df),
        'high': 0,
        'medium': 0,
        'low': 0,
        'manual': 0
    }

    for idx, row in area_df.iterrows():
        scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
        task_step = str(row.get('Task / Step', '')).strip()

        print(f"[{idx+1}/{len(area_df)}] Processing {scenario_id}...", end=' ')

        # Query RAG if task/step exists
        rag_response = None
        if task_step and task_step not in ['nan', '', 'None']:
            print(f"Querying RAG...", end=' ')
            rag_response = query_rag(task_step)

        # Create test file
        filepath, confidence = create_test_file(row, area_folder, rag_response)

        # Update stats
        if not task_step or task_step in ['nan', '', 'None']:
            stats['manual'] += 1
            print("MANUAL (no task/step)")
        else:
            stats[confidence.lower()] += 1
            print(f"{confidence}")

    return stats

def main():
    """Main execution."""
    print("="*80)
    print("Workday Electron Test Generator")
    print("="*80)

    # Load Excel
    print(f"\nLoading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)

    print(f"Total rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns.tolist())}")

    # Process each functional area
    all_stats = {}

    for area_name, folder_name in AREAS.items():
        area_folder = os.path.join(OUTPUT_BASE, folder_name)
        stats = process_functional_area(df, area_name, area_folder)
        all_stats[area_name] = stats

    # Print summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE - SUMMARY")
    print("="*80)

    for area_name, stats in all_stats.items():
        print(f"\n{area_name}:")
        print(f"  Total Scenarios: {stats['total']}")
        print(f"  High Confidence: {stats['high']} ({stats['high']/stats['total']*100:.1f}%)")
        print(f"  Medium Confidence: {stats['medium']} ({stats['medium']/stats['total']*100:.1f}%)")
        print(f"  Low Confidence: {stats['low']} ({stats['low']/stats['total']*100:.1f}%)")
        print(f"  Manual Required: {stats['manual']} ({stats['manual']/stats['total']*100:.1f}%)")

    print("\n" + "="*80)

if __name__ == "__main__":
    main()
