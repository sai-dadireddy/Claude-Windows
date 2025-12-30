#!/usr/bin/env python3
"""
Generate Electron Test Scenarios in batches
"""

import pandas as pd
import os
import re
import subprocess
import sys
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Payroll_US"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

def sanitize_filename(text):
    """Convert text to safe filename"""
    if pd.isna(text):
        return "Unknown"
    text = re.sub(r'[^\w\s-]', '', str(text))
    text = re.sub(r'\s+', '_', text)
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

    if "Operation:" in rag_output or "WSDL:" in rag_output:
        return "HIGH", 9.0

    if "REST" in rag_output or "endpoint" in rag_output.lower():
        return "HIGH", 8.5

    if task_step.lower() in rag_output.lower():
        return "MEDIUM", 7.0

    return "MEDIUM", 6.0

def extract_api_info(rag_output):
    """Extract SOAP/REST API information from RAG output"""
    soap_ops = []
    rest_endpoints = []

    if not rag_output:
        return "No API information available", "N/A"

    for line in rag_output.split('\n'):
        if 'Operation:' in line or 'WSDL:' in line:
            soap_ops.append(line.strip())

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

    confidence_level, confidence_score = calculate_confidence(rag_output, str(task_step))
    soap_info, rest_info = extract_api_info(rag_output)
    source = "RAG" if rag_output else "KB"

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
    """Generate manual test file"""
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
    # Get batch parameters
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    start_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading Excel from: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH)

    payroll = df[df['Functional Area'] == 'Payroll for the United States'].copy()
    total = len(payroll)

    print(f"Total scenarios: {total}")
    print(f"Processing batch: {start_idx} to {start_idx + batch_size}")

    generated = 0
    manual = 0

    # Process batch
    batch = payroll.iloc[start_idx:start_idx + batch_size]

    for idx, row in batch.iterrows():
        scenario_id = row['Scenario ID']
        scenario_name = row['Scenario Name']
        task_step = row['Task / Step']

        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        print(f"\nProcessing {generated + manual + 1}/{len(batch)}: {scenario_id}")

        if pd.isna(task_step) or str(task_step).strip() == '':
            print(f"  [!] No Task/Step - MANUAL required")
            content = generate_manual_file(row, 'Missing "Task / Step" - SME must provide Workday task name')
            manual += 1
        else:
            print(f"  Task: {task_step}")
            rag_output = query_rag(str(task_step))
            content = generate_test_file(row, rag_output)
            generated += 1

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  [OK] {filename}")

    print(f"\n{'='*80}")
    print(f"BATCH SUMMARY:")
    print(f"  Generated automated: {generated}")
    print(f"  Manual required: {manual}")
    print(f"  Next batch start: {start_idx + batch_size}")
    print(f"  Remaining: {total - (start_idx + batch_size)}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
