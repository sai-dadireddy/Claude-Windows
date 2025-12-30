#!/usr/bin/env python3
"""
Generate Electron tests for Endowments, Case Management, and Lease Accounting from Excel master file.
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
    "Endowments": "Endowments",
    "Case Management": "Case_Management",
    "Lease Accounting": "Lease_Accounting"
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
    """Calculate confidence score based on RAG response quality.

    Returns:
        tuple: (confidence_level, confidence_score)
        - HIGH (>= 7.0): Valid Electron steps can be generated
        - MEDIUM (5.0-6.9): Needs SME review
        - LOW (< 5.0): Manual creation required
    """
    if not rag_response or "No results found" in rag_response:
        return "LOW", 2.0

    # Check for specific Electron-actionable indicators
    high_indicators = [
        "Get_", "Submit_", "Put_", "Request",  # SOAP operations
        "endpoint", "API", "service",  # REST/SOAP terms
    ]

    # Specific field/UI element indicators (needed for actual steps)
    specific_indicators = [
        "field", "button", "dropdown", "checkbox", "radio",
        "tab", "link", "menu", "panel", "section"
    ]

    # Procedural indicators
    procedural_indicators = [
        "step", "navigate", "click", "enter", "select",
        "choose", "fill", "type", "search"
    ]

    score = 3.0  # Base score (starts lower - must earn points)
    response_lower = rag_response.lower()

    # Check for SOAP/REST operations (strong signal)
    high_count = sum(1 for ind in high_indicators if ind.lower() in response_lower)
    if high_count >= 2:
        score += 3.0
    elif high_count >= 1:
        score += 1.5

    # Check for specific UI elements (critical for Electron steps)
    specific_count = sum(1 for ind in specific_indicators if ind.lower() in response_lower)
    if specific_count >= 3:
        score += 2.5
    elif specific_count >= 1:
        score += 1.0

    # Check for procedural language
    proc_count = sum(1 for ind in procedural_indicators if ind.lower() in response_lower)
    if proc_count >= 3:
        score += 2.0
    elif proc_count >= 1:
        score += 0.5

    # Length check (longer responses often more detailed)
    if len(rag_response) > 500:
        score += 1.0
    elif len(rag_response) > 200:
        score += 0.5

    # Determine confidence level (stricter thresholds)
    if score >= 7.0:
        return "HIGH", min(score, 10.0)
    elif score >= 5.0:
        return "MEDIUM", score
    else:
        return "LOW", score

def generate_electron_steps(task_step, rag_response, scenario_id, confidence_score):
    """Generate Electron test steps from RAG response.

    Only generates actual Electron commands for HIGH confidence (>= 7.0).
    For MEDIUM/LOW, marks as needing review or manual creation.
    """
    steps = []

    # For LOW confidence (< 5.0), mark as MANUAL
    if confidence_score < 5.0:
        steps.append("[MANUAL TEST REQUIRED]")
        steps.append(f"Reason: Insufficient RAG data (confidence: {confidence_score:.1f}/10)")
        steps.append(f"Task: {task_step}")
        steps.append("")
        steps.append("SME Action: Create test steps manually based on Workday knowledge.")
        return steps

    # For MEDIUM confidence (5.0-6.9), mark for SME review
    if confidence_score < 7.0:
        steps.append("[NEEDS SME REVIEW]")
        steps.append(f"Confidence: {confidence_score:.1f}/10 - Below acceptance threshold")
        steps.append("")
        steps.append("Preliminary steps (MUST be reviewed and enhanced):")
        steps.append(f'1. enter search box as "{task_step}"')
        steps.append("2. wait for search results")
        steps.append(f'3. screenshot as "{scenario_id}_initial.png"')
        steps.append("")
        steps.append("SME Action: Validate task name and add remaining steps.")
        return steps

    # HIGH confidence (>= 7.0) - Generate actual steps
    step_num = 1

    # Always start with search
    steps.append(f'{step_num}. enter search box as "{task_step}"')
    step_num += 1

    steps.append(f"{step_num}. wait for search results")
    step_num += 1

    # Parse RAG response for specific fields/actions
    response_lower = rag_response.lower()

    # Look for specific field names (extract from RAG)
    field_patterns = re.findall(r'(?:enter|input|fill|type)\s+(?:the\s+)?(["\']?[\w\s]+["\']?)\s+(?:field|box|into)', rag_response, re.IGNORECASE)
    for field in field_patterns[:3]:  # Limit to 3 specific fields
        clean_field = field.strip().strip('"\'')
        steps.append(f'{step_num}. enter field "{clean_field}" with [VALUE]')
        step_num += 1

    # Look for specific buttons/links
    button_patterns = re.findall(r'(?:click|select|choose)\s+(?:the\s+)?(["\']?[\w\s]+["\']?)\s+(?:button|link)', rag_response, re.IGNORECASE)
    for button in button_patterns[:2]:  # Limit to 2 buttons
        clean_button = button.strip().strip('"\'')
        steps.append(f'{step_num}. click button "{clean_button}"')
        step_num += 1

    # Look for dropdown selections
    dropdown_patterns = re.findall(r'(?:select|choose)\s+(?:the\s+)?(["\']?[\w\s]+["\']?)\s+(?:from|in)\s+(?:the\s+)?dropdown', rag_response, re.IGNORECASE)
    for dropdown in dropdown_patterns[:2]:
        clean_dropdown = dropdown.strip().strip('"\'')
        steps.append(f'{step_num}. select dropdown "{clean_dropdown}" as [VALUE]')
        step_num += 1

    # Only add generic steps if we found NO specific fields/buttons/dropdowns
    if len(steps) == 2:  # Only search + wait
        # Check if RAG mentions any specific UI elements
        if any(term in response_lower for term in ['field', 'button', 'form', 'page']):
            steps.append(f"{step_num}. [VERIFY] RAG mentions UI elements but no specific names found")
            steps.append(f"{step_num+1}. [SME] Add specific field/button interactions")
            step_num += 2

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
    electron_steps = generate_electron_steps(task_step, rag_response, scenario_id, confidence_score)

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
        'accepted': 0,      # >= 7.0
        'needs_review': 0,  # 5.0-6.9
        'manual': 0,        # < 5.0 or no task
        'high': 0,
        'medium': 0,
        'low': 0
    }

    for idx, row in area_df.iterrows():
        scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
        task_step = str(row.get('Task / Step', '')).strip()

        print(f"[{idx+1}/{len(area_df)}] Processing {scenario_id}...", end=' ')

        # Query RAG if task/step exists
        rag_response = None
        confidence_score = 0.0

        if task_step and task_step not in ['nan', '', 'None']:
            print(f"Querying RAG...", end=' ')
            rag_response = query_rag(task_step)

            # Calculate confidence to categorize
            from subprocess import run
            _, confidence_score = calculate_confidence(task_step, rag_response)

        # Create test file
        filepath, confidence = create_test_file(row, area_folder, rag_response)

        # Update stats
        if not task_step or task_step in ['nan', '', 'None']:
            stats['manual'] += 1
            print("MANUAL (no task/step)")
        else:
            # Legacy stats
            stats[confidence.lower()] += 1

            # New categorization
            if confidence_score >= 7.0:
                stats['accepted'] += 1
                print(f"✅ ACCEPTED ({confidence_score:.1f})")
            elif confidence_score >= 5.0:
                stats['needs_review'] += 1
                print(f"⚠️ NEEDS REVIEW ({confidence_score:.1f})")
            else:
                stats['manual'] += 1
                print(f"❌ MANUAL ({confidence_score:.1f})")

    return stats

def main():
    """Main execution."""
    print("="*80)
    print("Workday Electron Test Generator - Endowments/Case/Lease")
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

    total_accepted = 0
    total_needs_review = 0
    total_manual = 0
    grand_total = 0

    for area_name, stats in all_stats.items():
        print(f"\n{area_name}:")
        print(f"  Total Scenarios: {stats['total']}")
        if stats['total'] > 0:
            print(f"  ✅ ACCEPTED (>= 7.0):     {stats['accepted']:3d} ({stats['accepted']/stats['total']*100:5.1f}%)")
            print(f"  ⚠️  NEEDS REVIEW (5-6.9): {stats['needs_review']:3d} ({stats['needs_review']/stats['total']*100:5.1f}%)")
            print(f"  ❌ MANUAL (< 5.0):        {stats['manual']:3d} ({stats['manual']/stats['total']*100:5.1f}%)")

            total_accepted += stats['accepted']
            total_needs_review += stats['needs_review']
            total_manual += stats['manual']
            grand_total += stats['total']

    print("\n" + "="*80)
    print("OVERALL TOTALS:")
    print(f"  Grand Total:        {grand_total}")
    print(f"  ✅ ACCEPTED:        {total_accepted:3d} ({total_accepted/grand_total*100:5.1f}%)")
    print(f"  ⚠️  NEEDS REVIEW:   {total_needs_review:3d} ({total_needs_review/grand_total*100:5.1f}%)")
    print(f"  ❌ MANUAL:          {total_manual:3d} ({total_manual/grand_total*100:5.1f}%)")
    print("="*80)

if __name__ == "__main__":
    main()
