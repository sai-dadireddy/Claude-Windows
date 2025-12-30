#!/usr/bin/env python3
"""
Batch generate Electron tests for Inventory and Asset Management.
Optimized to minimize RAG queries and process efficiently.
"""

import pandas as pd
import os
import subprocess
import re
from pathlib import Path
import json
import time

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"
OUTPUT_BASE = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"

# Functional areas to process
AREAS = {
    "Inventory": "Inventory",
    "Asset Management": "Asset_Management"
}

# Cache for RAG responses
rag_cache = {}

def query_rag_cached(query_text):
    """Query RAG with caching to avoid duplicate queries."""
    if not query_text or query_text in ['nan', '', 'None']:
        return None

    # Normalize query
    query_key = query_text.strip().lower()

    if query_key in rag_cache:
        print("(cached)", end=' ')
        return rag_cache[query_key]

    try:
        result = subprocess.run(
            ["python", RAG_SCRIPT, query_text],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8'
        )
        if result.returncode == 0:
            response = result.stdout.strip()
            rag_cache[query_key] = response
            time.sleep(0.5)  # Rate limiting
            return response
    except Exception as e:
        print(f"[RAG ERROR: {e}]", end=' ')

    rag_cache[query_key] = None
    return None

def calculate_confidence(task_step, rag_response):
    """Calculate confidence score based on RAG response quality."""
    if not rag_response or "No results found" in rag_response or len(rag_response) < 50:
        return "LOW", 2.0

    score = 5.0  # Base score
    response_lower = rag_response.lower()

    # High-value indicators (SOAP/REST operations)
    high_indicators = [
        ('get_', 1.5), ('submit_', 1.5), ('put_', 1.5), ('request', 1.0),
        ('endpoint', 1.0), ('wsdl', 1.5), ('soap', 1.0), ('rest', 1.0)
    ]

    # Medium-value indicators (UI/process terms)
    medium_indicators = [
        ('navigate', 0.8), ('click', 0.8), ('enter', 0.8), ('select', 0.8),
        ('page', 0.5), ('field', 0.5), ('button', 0.5), ('form', 0.5)
    ]

    # Apply high indicators
    for indicator, weight in high_indicators:
        if indicator in response_lower:
            score += weight

    # Apply medium indicators
    for indicator, weight in medium_indicators:
        if indicator in response_lower:
            score += weight

    # Length bonus (more detailed = better)
    if len(rag_response) > 1000:
        score += 2.0
    elif len(rag_response) > 500:
        score += 1.0
    elif len(rag_response) > 200:
        score += 0.5

    # Specific Workday terms
    workday_terms = ['workday', 'tenant', 'integration', 'business process']
    workday_count = sum(1 for term in workday_terms if term in response_lower)
    score += workday_count * 0.5

    # Cap score
    score = min(score, 10.0)

    # Determine confidence level
    if score >= 8.0:
        return "HIGH", score
    elif score >= 5.5:
        return "MEDIUM", score
    else:
        return "LOW", score

def generate_electron_steps(task_step, rag_response, scenario_id, expected_result):
    """Generate Electron test steps from RAG response."""
    steps = []

    # Always start with search
    if task_step and task_step not in ['nan', '', 'None']:
        steps.append(f'1. enter search box as "{task_step}"')
        step_num = 2
    else:
        steps.append(f'1. [MANUAL] No task specified - determine appropriate entry point')
        step_num = 2

    if not rag_response or "No results found" in rag_response:
        steps.append(f"{step_num}. [MANUAL] No RAG guidance available")
        step_num += 1
        steps.append(f"{step_num}. [MANUAL] Review expected result: {expected_result[:100]}")
        step_num += 1
        steps.append(f'{step_num}. screenshot as "{scenario_id}_complete.png"')
        return steps

    # Extract actionable information from RAG response
    response_lower = rag_response.lower()

    # Navigation steps
    if any(term in response_lower for term in ['navigate', 'go to', 'access', 'open']):
        steps.append(f"{step_num}. wait for page load (3-5 seconds)")
        step_num += 1
        steps.append(f"{step_num}. verify correct page loaded")
        step_num += 1

    # Field entries (look for specific patterns)
    field_patterns = [
        r'enter\s+([^,\.]+?)(?:\s+in|\s+into|\s+field)',
        r'fill\s+(?:in\s+)?([^,\.]+?)(?:\s+with|\s+field)',
        r'provide\s+([^,\.]+)',
        r'input\s+([^,\.]+)'
    ]

    found_fields = set()
    for pattern in field_patterns:
        matches = re.findall(pattern, rag_response, re.IGNORECASE)
        found_fields.update([m.strip() for m in matches[:5]])

    for field in list(found_fields)[:3]:
        if len(field) < 100:  # Avoid capturing long text
            steps.append(f'{step_num}. enter field "{field}" with test data')
            step_num += 1

    # Selection/dropdown actions
    if any(term in response_lower for term in ['select', 'choose', 'pick']):
        steps.append(f"{step_num}. select appropriate dropdown values")
        step_num += 1

    # Click/action buttons
    if any(term in response_lower for term in ['click', 'press', 'activate']):
        steps.append(f"{step_num}. click action button to proceed")
        step_num += 1

    # Submit/save operations
    if any(term in response_lower for term in ['submit', 'save', 'confirm', 'complete']):
        steps.append(f"{step_num}. submit form/transaction")
        step_num += 1
        steps.append(f"{step_num}. wait for confirmation message")
        step_num += 1

    # If minimal steps, add generic workflow
    if len(steps) <= 3:
        steps.append(f"{step_num}. complete required form fields")
        step_num += 1
        steps.append(f"{step_num}. validate data entry")
        step_num += 1

    # Verification step
    steps.append(f"{step_num}. verify: {expected_result[:100]}...")
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

    # Handle NaN values
    if task_step in ['nan', 'None']:
        task_step = ''
    if expected_result in ['nan', 'None']:
        expected_result = 'No expected result specified'

    # Calculate confidence
    confidence_level, confidence_score = calculate_confidence(task_step, rag_response)

    # Generate steps
    electron_steps = generate_electron_steps(task_step, rag_response, scenario_id, expected_result)

    # Create safe filename
    safe_name = re.sub(r'[^\w\s-]', '', scenario_name).strip().replace(' ', '_')[:50]
    if not safe_name:
        safe_name = "unnamed"
    filename = f"{scenario_id}_{safe_name}.txt"
    filepath = os.path.join(area_folder, filename)

    # Build file content
    content = f"""{'='*80}
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
TEST NAME: {scenario_name}
CONFIDENCE: [{confidence_level}] Score: {confidence_score:.1f}/10
{'='*80}

TASK/STEP: {task_step if task_step else '[NO TASK SPECIFIED - MANUAL TEST REQUIRED]'}

ELECTRON STEPS:
{chr(10).join(electron_steps)}

VERIFICATION: {expected_result}

{'='*80}
RAG RESPONSE SUMMARY:
"""

    if rag_response and len(rag_response) > 50:
        # Include RAG response with truncation for very long responses
        if len(rag_response) > 1500:
            rag_summary = rag_response[:1500] + "\n\n[... truncated for brevity ...]"
        else:
            rag_summary = rag_response
        content += f"{rag_summary}\n"
    else:
        content += "[NO RAG RESPONSE] - Manual test creation required\n"
        content += "REASON: "
        if not task_step:
            content += "No Task/Step provided in source data\n"
        else:
            content += "RAG query returned no results or insufficient information\n"

    content += f"{'='*80}\n"

    # Write file
    try:
        with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
        return filepath, confidence_level
    except Exception as e:
        print(f"\n[ERROR writing {filepath}: {e}]")
        return None, "LOW"

def process_functional_area(df, area_name, area_folder):
    """Process all scenarios for a functional area."""
    # Filter by functional area
    area_df = df[df['Functional Area'].str.strip() == area_name].copy()

    print(f"\n{'='*80}")
    print(f"Processing {area_name}: {len(area_df)} scenarios")
    print(f"Output: {area_folder}")
    print(f"{'='*80}\n")

    # Create output folder
    os.makedirs(area_folder, exist_ok=True)

    stats = {
        'total': len(area_df),
        'high': 0,
        'medium': 0,
        'low': 0,
        'manual': 0,
        'errors': 0
    }

    for idx, row in area_df.iterrows():
        scenario_id = str(row.get('Scenario ID', f'UNK{idx}')).strip()
        task_step = str(row.get('Task / Step', '')).strip()

        print(f"[{stats['total'] - len(area_df) + idx + 1}/{stats['total']}] {scenario_id}: ", end='')

        # Query RAG if task/step exists
        rag_response = None
        if task_step and task_step not in ['nan', '', 'None']:
            rag_response = query_rag_cached(task_step)

        # Create test file
        filepath, confidence = create_test_file(row, area_folder, rag_response)

        if filepath:
            # Update stats
            if not task_step or task_step in ['nan', '', 'None']:
                stats['manual'] += 1
                print("MANUAL")
            else:
                stats[confidence.lower()] += 1
                print(confidence)
        else:
            stats['errors'] += 1
            print("ERROR")

    return stats

def main():
    """Main execution."""
    print("="*80)
    print("Workday Electron Test Generator - Batch Mode")
    print("="*80)

    # Load Excel
    print(f"\nLoading: {EXCEL_PATH}")
    try:
        df = pd.read_excel(EXCEL_PATH)
        print(f"✓ Loaded {len(df)} total rows")
        print(f"✓ Columns: {len(df.columns)}")
    except Exception as e:
        print(f"✗ ERROR loading Excel: {e}")
        return

    # Process each functional area
    all_stats = {}

    for area_name, folder_name in AREAS.items():
        area_folder = os.path.join(OUTPUT_BASE, folder_name)
        try:
            stats = process_functional_area(df, area_name, area_folder)
            all_stats[area_name] = stats
        except Exception as e:
            print(f"\n✗ ERROR processing {area_name}: {e}")
            import traceback
            traceback.print_exc()

    # Print summary
    print("\n" + "="*80)
    print("GENERATION COMPLETE - SUMMARY")
    print("="*80)

    total_all = 0
    for area_name, stats in all_stats.items():
        total_all += stats['total']
        print(f"\n{area_name}:")
        print(f"  Total Scenarios:    {stats['total']}")
        print(f"  High Confidence:    {stats['high']:3d} ({stats['high']/stats['total']*100:5.1f}%)")
        print(f"  Medium Confidence:  {stats['medium']:3d} ({stats['medium']/stats['total']*100:5.1f}%)")
        print(f"  Low Confidence:     {stats['low']:3d} ({stats['low']/stats['total']*100:5.1f}%)")
        print(f"  Manual Required:    {stats['manual']:3d} ({stats['manual']/stats['total']*100:5.1f}%)")
        if stats['errors'] > 0:
            print(f"  Errors:             {stats['errors']:3d}")

    print(f"\n{'='*80}")
    print(f"TOTAL TESTS GENERATED: {total_all}")
    print(f"RAG Cache Size: {len(rag_cache)} unique queries")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
