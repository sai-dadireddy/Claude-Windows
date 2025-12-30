#!/usr/bin/env python3
"""
Generate Electron Test Scenarios for Payroll US
"""

import pandas as pd
import os
import re
import subprocess
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Payroll_US"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

def sanitize_filename(text):
    """Convert text to safe filename"""
    if pd.isna(text):
        return "Unknown"
    # Remove special characters
    text = re.sub(r'[^\w\s-]', '', str(text))
    # Replace spaces with underscores
    text = re.sub(r'\s+', '_', text)
    # Limit length
    return text[:100]

def query_rag(task_step):
    """Query workday_rag.py for task information"""
    try:
        result = subprocess.run(
            ['python', RAG_SCRIPT, task_step],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(RAG_SCRIPT)
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception as e:
        return f"RAG query failed: {str(e)}"

def calculate_confidence(rag_output, task_step):
    """Calculate confidence score based on RAG results"""
    if not rag_output or "No relevant" in rag_output:
        return "LOW", 3.0

    # Check for WSDL operations
    if "Operation:" in rag_output or "WSDL:" in rag_output:
        return "HIGH", 9.0

    # Check for REST endpoints
    if "REST" in rag_output or "endpoint" in rag_output.lower():
        return "HIGH", 8.5

    # Check for specific task matches
    if task_step.lower() in rag_output.lower():
        return "MEDIUM", 7.0

    return "MEDIUM", 6.0

def extract_api_info(rag_output):
    """Extract SOAP/REST API information from RAG output"""
    soap_ops = []
    rest_endpoints = []

    if not rag_output:
        return "No API information available", "N/A"

    # Look for SOAP operations
    for line in rag_output.split('\n'):
        if 'Operation:' in line or 'WSDL:' in line:
            soap_ops.append(line.strip())

    # Look for REST mentions
    if 'REST' in rag_output or 'endpoint' in rag_output.lower():
        rest_endpoints.append("REST API available (see RAG output)")

    soap_info = '\n  '.join(soap_ops) if soap_ops else "No SOAP operation found"
    rest_info = '\n  '.join(rest_endpoints) if rest_endpoints else "N/A"

    return soap_info, rest_info

def generate_test_file(row, rag_output):
    """Generate test scenario file"""
    scenario_id = row['Scenario ID']
    scenario_name = row['Scenario Name']
    scenario_desc = row['Scenario Description']
    task_step = row['Task / Step']
    workday_role = row['Workday Role']
    effort = row['Est. Effort (mins)']
    expected_result = row['Customer Expected Result']

    # Calculate confidence
    confidence_level, confidence_score = calculate_confidence(rag_output, str(task_step))

    # Extract API info
    soap_info, rest_info = extract_api_info(rag_output)

    # Determine source
    source = "RAG" if rag_output else "KB"

    # Generate content
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: Payroll for the United States
TEST NAME: {scenario_name}
CONFIDENCE: [{confidence_level}] Score: {confidence_score}/10
SOURCE: [{source}]
================================================================================

DESCRIPTION:
{scenario_desc if not pd.isna(scenario_desc) else 'No description provided'}

WORKDAY ROLE: {workday_role if not pd.isna(workday_role) else 'Not specified'}
EST. DURATION: {effort if not pd.isna(effort) else 'N/A'} minutes

PREREQUISITES:
- User logged in with {workday_role if not pd.isna(workday_role) else 'appropriate'} permissions
- System is in proper state for payroll operations

ELECTRON STEPS:
1. enter search box as "{task_step}"
2. wait for search results
3. click search result containing "{task_step}"
4. wait for page to load
5. verify page title contains expected content
6. review configuration/data as described in test description
7. screenshot as "{scenario_id}_complete.png"

VERIFICATION:
- [ ] Page loads successfully
- [ ] {expected_result if not pd.isna(expected_result) else 'Configuration/data matches expected values'}
- [ ] No error messages displayed
- [ ] All required fields/sections are visible

API ALTERNATIVE:
SOAP:
  {soap_info}

REST:
  {rest_info}

RAG QUERY RESULTS:
{rag_output[:500] if rag_output else 'No RAG results available'}

================================================================================
"""
    return content

def generate_manual_file(row, reason):
    """Generate manual test file for scenarios without Task/Step"""
    scenario_id = row['Scenario ID']
    scenario_name = row['Scenario Name']

    content = f"""================================================================================
TEST ID: {scenario_id}
STATUS: [MANUAL REQUIRED]
REASON: {reason}
================================================================================

SCENARIO NAME: {scenario_name}
DESCRIPTION: {row['Scenario Description'] if not pd.isna(row['Scenario Description']) else 'N/A'}

ACTION REQUIRED:
Subject Matter Expert must provide:
1. Specific Workday task name or menu path
2. Step-by-step navigation instructions
3. Expected system behavior

Once SME input is received, this test can be automated using Electron.

================================================================================
"""
    return content

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load Excel
    print(f"Loading Excel from: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)

    # Filter for Payroll US
    payroll = df[df['Functional Area'] == 'Payroll for the United States'].copy()
    print(f"Found {len(payroll)} Payroll US scenarios")

    # Process each scenario
    generated = 0
    manual = 0

    for idx, row in payroll.iterrows():
        scenario_id = row['Scenario ID']
        scenario_name = row['Scenario Name']
        task_step = row['Task / Step']

        # Sanitize filename
        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        print(f"\nProcessing: {scenario_id} - {scenario_name}")

        # Check if Task/Step exists
        if pd.isna(task_step) or str(task_step).strip() == '':
            print(f"  [!] No Task/Step - generating MANUAL file")
            content = generate_manual_file(row, 'Missing "Task / Step" - SME must provide Workday task name')
            manual += 1
        else:
            print(f"  Task: {task_step}")
            print(f"  Querying RAG...")

            # Query RAG
            rag_output = query_rag(str(task_step))

            # Generate test file
            content = generate_test_file(row, rag_output)
            generated += 1

        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] Created: {filename}")

    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"  Total scenarios: {len(payroll)}")
    print(f"  Generated automated tests: {generated}")
    print(f"  Manual required: {manual}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
