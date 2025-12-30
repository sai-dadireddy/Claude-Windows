#!/usr/bin/env python3
"""
Workday Electron Test Generator for International Payroll
Generates individual test files for Payroll Canada, UK, France, and Interface scenarios
"""

import pandas as pd
import subprocess
import re
import os
from pathlib import Path

# Paths
EXCEL_PATH = "WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = "../workday_rag.py"

# Functional areas to process with their output directories
PAYROLL_AREAS = {
    'Payroll for Canada': 'Payroll_Canada',
    'Payroll for UK': 'Payroll_UK',
    'Payroll for France': 'Payroll_France',
    'Payroll Interface': 'Payroll_Interface'
}

def sanitize_filename(name):
    """Convert scenario name to safe filename"""
    # Remove special characters, keep alphanumeric, spaces, hyphens
    safe = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    # Limit length
    return safe[:80]

def query_rag(task_step):
    """Query the RAG system for Workday documentation"""
    if pd.isna(task_step) or not task_step.strip():
        return None, 0.0, "NO_TASK"

    try:
        # Run RAG query
        result = subprocess.run(
            ["python", RAG_SCRIPT, task_step],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        if result.returncode != 0:
            return None, 0.0, "RAG_ERROR"

        output = result.stdout

        # Extract confidence score (looking for patterns like "Score: 8.5" or "Confidence: 8.5/10")
        confidence = 5.0  # Default medium confidence
        score_match = re.search(r'(?:Score|Confidence):\s*(\d+\.?\d*)', output, re.IGNORECASE)
        if score_match:
            confidence = float(score_match.group(1))

        return output, confidence, "RAG"

    except subprocess.TimeoutExpired:
        return None, 0.0, "TIMEOUT"
    except Exception as e:
        return None, 0.0, f"ERROR: {str(e)}"

def get_confidence_level(score):
    """Convert numeric score to confidence level"""
    if score >= 7.0:
        return "HIGH"
    elif score >= 4.0:
        return "MEDIUM"
    else:
        return "LOW"

def extract_api_info(rag_output):
    """Extract API information from RAG output"""
    if not rag_output:
        return "Not available", "Not available"

    soap_ops = []
    rest_endpoints = []

    # Look for SOAP operations (payroll specific)
    soap_matches = re.findall(r'(Get_\w+|Put_\w+|Submit_\w+|Import_\w+|Process_\w+)', rag_output)
    if soap_matches:
        soap_ops = list(set(soap_matches[:3]))  # Top 3 unique

    # Look for REST endpoints (payroll specific)
    rest_matches = re.findall(r'/payroll|/workers|/api/v\d+/\w+', rag_output)
    if rest_matches:
        rest_endpoints = list(set(rest_matches[:3]))

    soap_str = ", ".join(soap_ops) if soap_ops else "Not available in RAG results"
    rest_str = ", ".join(rest_endpoints) if rest_endpoints else "Not available in RAG results"

    return soap_str, rest_str

def generate_test_file(row, functional_area, output_dir, rag_output, confidence, source):
    """Generate test scenario file"""
    scenario_id = row['Scenario ID']
    scenario_name = row['Scenario Name']
    scenario_desc = row['Scenario Description'] if pd.notna(row['Scenario Description']) else "No description provided"
    task_step = row['Task / Step']
    workday_role = row['Workday Role'] if pd.notna(row['Workday Role']) else "Payroll Administrator"
    effort = row['Est. Effort (mins)'] if pd.notna(row['Est. Effort (mins)']) else 10
    expected_result = row['Customer Expected Result'] if pd.notna(row['Customer Expected Result']) else "Task completed successfully"
    country_code = row['Country Code (Scope)'] if pd.notna(row['Country Code (Scope)']) else "N/A"

    # Sanitize filename
    filename = f"{scenario_id}_{sanitize_filename(scenario_name)}.txt"
    filepath = Path(output_dir) / filename

    # Check if task/step is missing
    if pd.isna(task_step) or not task_step.strip():
        content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
COUNTRY: {country_code}
TEST NAME: {scenario_name}
STATUS: [MANUAL REQUIRED]
================================================================================

REASON FOR MANUAL:
- Missing "Task / Step" column value
- Cannot determine which Workday task to execute
- SME input required to identify the specific Workday task

AVAILABLE DATA:
- Scenario Description: {scenario_desc}
- Expected Result: {expected_result}
- Workday Role: {workday_role}
- Country Code: {country_code}

ACTION NEEDED:
Payroll SME must provide the specific task name to search in Workday.
================================================================================
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath, "MANUAL"

    # Generate full test file
    confidence_level = get_confidence_level(confidence)
    soap_api, rest_api = extract_api_info(rag_output)

    # Extract steps from RAG if available
    rag_steps = ""
    if rag_output and confidence >= 4.0:
        # Try to extract procedural information
        lines = rag_output.split('\n')
        step_lines = [l for l in lines if re.search(r'^\d+\.|^-\s|^•\s|step|click|enter|select', l, re.IGNORECASE)]
        if step_lines:
            rag_steps = "\n".join(f"   {line.strip()}" for line in step_lines[:10])

    if not rag_steps:
        rag_steps = "   [RAG data available but no specific steps found - follow standard task flow]"

    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
COUNTRY: {country_code}
TEST NAME: {scenario_name}
CONFIDENCE: [{confidence_level}] Score: {confidence:.1f}/10
SOURCE: [{source}]
================================================================================

DESCRIPTION:
{scenario_desc}

WORKDAY ROLE: {workday_role}
EST. DURATION: {effort} minutes
COUNTRY SCOPE: {country_code}

PREREQUISITES:
- User logged in with {workday_role} permissions
- Required data available in tenant
- Access to {country_code} payroll data

ELECTRON STEPS:
1. enter search box as "{task_step}"
2. wait for search results
3. click search result containing "{task_step}"
4. wait for page to load
5. RAG-extracted steps:
{rag_steps}
6. screenshot as "{scenario_id}_complete.png"

VERIFICATION:
- [ ] {expected_result}
- [ ] Task completed successfully
- [ ] No error messages displayed
- [ ] Country-specific data validates correctly

API ALTERNATIVE:
- SOAP: {soap_api}
- REST: {rest_api}

RAG NOTES:
{rag_output[:500] + '...' if rag_output and len(rag_output) > 500 else (rag_output or 'No RAG data available')}
================================================================================
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath, confidence_level

def process_functional_area(df, functional_area, output_dir):
    """Process all scenarios for a specific functional area"""
    print(f"\n{'=' * 80}")
    print(f"PROCESSING: {functional_area}")
    print(f"Output Directory: {output_dir}")
    print(f"{'=' * 80}\n")

    # Filter scenarios for this area
    area_df = df[df['Functional Area'] == functional_area].copy()

    if len(area_df) == 0:
        print(f"⚠️  No scenarios found for {functional_area}\n")
        return None

    print(f"Found {len(area_df)} scenarios")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process each scenario
    stats = {
        'total': len(area_df),
        'generated': 0,
        'manual': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0,
        'errors': 0
    }

    for idx, row in area_df.iterrows():
        scenario_id = row['Scenario ID']
        task_step = row['Task / Step']

        print(f"[{stats['generated'] + stats['manual'] + 1}/{stats['total']}] Processing {scenario_id}...", end=" ")

        # Query RAG
        rag_output, confidence, source = query_rag(task_step)

        try:
            # Generate file
            filepath, result = generate_test_file(row, functional_area, output_dir, rag_output, confidence, source)

            if result == "MANUAL":
                stats['manual'] += 1
                print("MANUAL REQUIRED")
            else:
                stats['generated'] += 1
                if result == "HIGH":
                    stats['high_confidence'] += 1
                elif result == "MEDIUM":
                    stats['medium_confidence'] += 1
                else:
                    stats['low_confidence'] += 1
                print(f"OK [{result}]")

        except Exception as e:
            stats['errors'] += 1
            print(f"ERROR: {str(e)}")

    return stats

def main():
    """Main processing function"""
    print("=" * 80)
    print("WORKDAY ELECTRON TEST GENERATOR - INTERNATIONAL PAYROLL")
    print("=" * 80)
    print()

    # Read Excel
    print(f"Reading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)
    print(f"Total rows in Excel: {len(df)}")
    print()

    # Overall statistics
    overall_stats = {
        'total': 0,
        'generated': 0,
        'manual': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0,
        'errors': 0
    }

    # Process each functional area
    for functional_area, output_dir in PAYROLL_AREAS.items():
        area_stats = process_functional_area(df, functional_area, output_dir)

        if area_stats:
            # Add to overall stats
            for key in overall_stats:
                overall_stats[key] += area_stats[key]

            # Print area summary
            print(f"\n{functional_area} Summary:")
            print(f"  Generated:           {area_stats['generated']}")
            print(f"    - High confidence: {area_stats['high_confidence']}")
            print(f"    - Med confidence:  {area_stats['medium_confidence']}")
            print(f"    - Low confidence:  {area_stats['low_confidence']}")
            print(f"  Manual required:     {area_stats['manual']}")
            print(f"  Errors:              {area_stats['errors']}")

    # Final summary
    print()
    print("=" * 80)
    print("OVERALL GENERATION SUMMARY")
    print("=" * 80)
    print(f"Total scenarios:       {overall_stats['total']}")
    print(f"Generated:             {overall_stats['generated']}")
    print(f"  - High confidence:   {overall_stats['high_confidence']}")
    print(f"  - Medium confidence: {overall_stats['medium_confidence']}")
    print(f"  - Low confidence:    {overall_stats['low_confidence']}")
    print(f"Manual required:       {overall_stats['manual']}")
    print(f"Errors:                {overall_stats['errors']}")
    print()
    print(f"Output locations:")
    for functional_area, output_dir in PAYROLL_AREAS.items():
        full_path = os.path.abspath(output_dir)
        if os.path.exists(full_path):
            print(f"  {functional_area}: {full_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
