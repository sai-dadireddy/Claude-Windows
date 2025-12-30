#!/usr/bin/env python3
"""
Generate Electron tests for Absence and Time_Tracking functional areas from Excel master file.
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
    "Absence": "Absence",
    "Time Tracking": "Time_Tracking"
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
        "step", "navigate", "click", "enter",  # Procedural steps
        "absence", "time", "entry", "request"  # Domain-specific
    ]

    medium_indicators = [
        "page", "field", "button", "form",
        "record", "document", "transaction",
        "submit", "save", "approve"
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
    if score >= 7.0:
        return "HIGH", min(score, 10.0)
    elif score >= 5.0:
        return "MEDIUM", score
    else:
        return "LOW", score

def generate_electron_steps(task_step, rag_response, scenario_id, confidence_score):
    """Generate Electron test steps from RAG response."""
    steps = []

    # Always start with search
    steps.append(f'enter search box as "{task_step}"')

    # If low confidence, mark as MANUAL
    if confidence_score < 5.0:
        return steps, "MANUAL"

    if not rag_response or "No results found" in rag_response:
        return steps, "MANUAL"

    # Parse RAG response for actionable steps
    step_num = 2

    # Look for common patterns
    if "navigate" in rag_response.lower() or "go to" in rag_response.lower():
        steps.append(f"wait for search results")
        steps.append(f'click search result containing "{task_step}"')
        steps.append("wait for page to load")
    else:
        steps.append("wait for search results")
        steps.append('click first search result')
        steps.append("wait for page to load")

    # Look for specific field names in RAG response
    field_patterns = re.findall(r'(?:enter|input|fill|select)\s+["\']?([A-Za-z\s]+)["\']?', rag_response, re.IGNORECASE)
    field_patterns = [f.strip() for f in field_patterns if len(f.strip()) > 2 and len(f.strip()) < 50]

    for field in field_patterns[:3]:  # Limit to 3 fields
        if any(word in field.lower() for word in ['date', 'time', 'worker', 'reason', 'type', 'hours']):
            steps.append(f'enter field "{field}" with appropriate value')

    # Look for button/action mentions
    button_patterns = re.findall(r'(?:click|select|press)\s+["\']?([A-Za-z\s]+)["\']?\s*button', rag_response, re.IGNORECASE)
    for button in button_patterns[:2]:
        steps.append(f'click button "{button.strip()}"')

    # Look for submit/save
    if "submit" in rag_response.lower():
        steps.append('click button "Submit"')
    elif "save" in rag_response.lower():
        steps.append('click button "Save"')

    # If medium confidence but no specific steps found
    if confidence_score >= 5.0 and confidence_score < 7.0 and len(steps) < 5:
        steps.append("[NEEDS SME REVIEW] - Complete required fields based on business process")
        steps.append("[NEEDS SME REVIEW] - Submit form")

    # Always end with screenshot
    steps.append(f'screenshot as "{scenario_id}_complete.png"')

    # Determine if valid or needs review
    if confidence_score >= 7.0:
        return steps, "VALID"
    elif confidence_score >= 5.0:
        return steps, "NEEDS_REVIEW"
    else:
        return steps[:1], "MANUAL"  # Only search step

def create_test_file(row, area_folder, rag_response=None):
    """Create individual test file for a scenario."""
    scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
    scenario_name = str(row.get('Scenario Name', 'Unnamed')).strip()
    task_step = str(row.get('Task / Step', '')).strip()
    expected_result = str(row.get('Customer Expected Result', 'No expected result specified')).strip()
    functional_area = str(row.get('Functional Area', '')).strip()
    workday_role = str(row.get('Workday Role', 'Not specified')).strip()
    est_effort = str(row.get('Est. Effort (mins)', '')).strip()

    # Calculate confidence
    confidence_level, confidence_score = calculate_confidence(task_step, rag_response)

    # Generate steps
    electron_steps, test_status = generate_electron_steps(task_step, rag_response, scenario_id, confidence_score)

    # Create filename
    safe_name = re.sub(r'[^\w\s-]', '', scenario_name).strip().replace(' ', '_')[:50]

    if test_status == "MANUAL":
        filename = f"{scenario_id}_{safe_name}_MANUAL.txt"
    elif test_status == "NEEDS_REVIEW":
        filename = f"{scenario_id}_{safe_name}_REVIEW.txt"
    else:
        filename = f"{scenario_id}_{safe_name}.txt"

    filepath = os.path.join(area_folder, filename)

    # Build file content
    if test_status == "MANUAL":
        content = f"""{'='*80}
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
TEST NAME: {scenario_name}
STATUS: ❌ MANUAL REQUIRED
CONFIDENCE: [{confidence_level}] Score: {confidence_score:.1f}/10
{'='*80}

TASK/STEP: {task_step if task_step else '[NO TASK SPECIFIED]'}

REASON FOR MANUAL:
Insufficient knowledge base coverage for this task. RAG confidence score < 5.0.

RECOMMENDED ACTIONS:
1. Search Workday Knowledge Base for "{task_step}"
2. Consult SME for detailed steps
3. Update KB article: kb_{functional_area.lower().replace(' ', '_')}_{safe_name[:30]}.txt

EXPECTED RESULT: {expected_result}
WORKDAY ROLE: {workday_role}
EST. EFFORT: {est_effort} minutes

{'='*80}
RAG RESPONSE SUMMARY:
"""
        if rag_response:
            rag_summary = rag_response[:300] + "..." if len(rag_response) > 300 else rag_response
            content += f"{rag_summary}\n"
        else:
            content += "[NO RAG RESPONSE]\n"
        content += f"{'='*80}\n"

    else:
        status_marker = "⚠️ NEEDS SME REVIEW" if test_status == "NEEDS_REVIEW" else "✅ ACCEPTED"
        content = f"""{'='*80}
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
TEST NAME: {scenario_name}
STATUS: {status_marker}
CONFIDENCE: [{confidence_level}] Score: {confidence_score:.1f}/10
{'='*80}

DESCRIPTION:
Task/Step: {task_step if task_step else '[NO TASK SPECIFIED]'}

PREREQUISITES:
- User logged in with {workday_role} permissions
- Required permissions for {functional_area} tasks

ELECTRON STEPS:
"""
        for i, step in enumerate(electron_steps, 1):
            content += f"{i}. {step}\n"

        content += f"""
VERIFICATION:
- [ ] {expected_result}
- [ ] No error messages displayed
- [ ] Task completed successfully

WORKDAY ROLE: {workday_role}
EST. EFFORT: {est_effort} minutes

{'='*80}
RAG RESPONSE SUMMARY:
"""
        if rag_response:
            rag_summary = rag_response[:500] + "..." if len(rag_response) > 500 else rag_response
            content += f"{rag_summary}\n"
        else:
            content += "[NO RAG RESPONSE]\n"
        content += f"{'='*80}\n"

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath, test_status

def process_functional_area(df, area_name, area_folder):
    """Process all scenarios for a functional area."""
    # Filter by functional area (partial match for "Time Tracking")
    area_df = df[df['Functional Area'].str.contains(area_name, case=False, na=False)].copy()

    print(f"\n{'='*80}")
    print(f"Processing {area_name}: {len(area_df)} scenarios")
    print(f"{'='*80}\n")

    # Create output folder
    os.makedirs(area_folder, exist_ok=True)

    stats = {
        'total': len(area_df),
        'valid': 0,
        'needs_review': 0,
        'manual': 0
    }

    for idx, row in area_df.iterrows():
        scenario_id = str(row.get('Scenario ID', 'UNKNOWN')).strip()
        task_step = str(row.get('Task / Step', '')).strip()

        print(f"[{stats['total'] - len(area_df) + idx + 1}/{stats['total']}] Processing {scenario_id}...", end=' ')

        # Query RAG if task/step exists
        rag_response = None
        if task_step and task_step not in ['nan', '', 'None']:
            print(f"Querying RAG...", end=' ')
            rag_response = query_rag(task_step)

        # Create test file
        filepath, test_status = create_test_file(row, area_folder, rag_response)

        # Update stats
        if test_status == "VALID":
            stats['valid'] += 1
            print(f"ACCEPTED")
        elif test_status == "NEEDS_REVIEW":
            stats['needs_review'] += 1
            print(f"NEEDS REVIEW")
        else:
            stats['manual'] += 1
            print(f"MANUAL")

    return stats

def main():
    """Main execution."""
    print("="*80)
    print("Workday Electron Test Generator - Absence & Time_Tracking")
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

    total_all = 0
    valid_all = 0
    review_all = 0
    manual_all = 0

    for area_name, stats in all_stats.items():
        total_all += stats['total']
        valid_all += stats['valid']
        review_all += stats['needs_review']
        manual_all += stats['manual']

        print(f"\n{area_name}:")
        print(f"  Total Scenarios: {stats['total']}")
        print(f"  ✅ Accepted (>= 7.0): {stats['valid']} ({stats['valid']/stats['total']*100:.1f}%)")
        print(f"  ⚠️ Needs Review (5.0-6.9): {stats['needs_review']} ({stats['needs_review']/stats['total']*100:.1f}%)")
        print(f"  ❌ Manual Required (< 5.0): {stats['manual']} ({stats['manual']/stats['total']*100:.1f}%)")

    print(f"\n{'='*80}")
    print("OVERALL TOTALS:")
    print(f"  Total Scenarios: {total_all}")
    print(f"  ✅ Accepted: {valid_all} ({valid_all/total_all*100:.1f}%)")
    print(f"  ⚠️ Needs Review: {review_all} ({review_all/total_all*100:.1f}%)")
    print(f"  ❌ Manual: {manual_all} ({manual_all/total_all*100:.1f}%)")
    print("="*80)

if __name__ == "__main__":
    main()
