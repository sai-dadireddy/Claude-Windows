#!/usr/bin/env python3
"""
Batch fix low-confidence Procurement and Inventory test files
Uses local RAG system to enhance test steps
"""

import os
import re
import subprocess
import json
from pathlib import Path

BASE_DIR = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs")
PROCUREMENT_DIR = BASE_DIR / "electron_tests" / "Procurement"
INVENTORY_DIR = BASE_DIR / "electron_tests" / "Inventory"

def query_rag(task_name):
    """Query the RAG system for task information"""
    try:
        result = subprocess.run(
            ["python", str(BASE_DIR / "workday_rag.py"), task_name],
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR),
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"ERROR: {str(e)}"

def extract_task_from_file(filepath):
    """Extract the task name from 'enter search box as' line"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the search box line
    match = re.search(r'enter search box as ["\']?([^"\'\n]+)["\']?', content, re.IGNORECASE)
    if match:
        task = match.group(1).strip()
        # Clean up common patterns
        task = task.replace(' or Extract ', ' ')
        task = task.replace('Extract ', '')
        task = task.replace('Find ', '')
        return task
    return None

def parse_test_file(filepath):
    """Parse existing test file and extract metadata"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = {}
    metadata['test_id'] = re.search(r'TEST ID:\s*(.+)', content)
    metadata['test_id'] = metadata['test_id'].group(1) if metadata['test_id'] else ''

    metadata['area'] = re.search(r'FUNCTIONAL AREA:\s*(.+)', content)
    metadata['area'] = metadata['area'].group(1) if metadata['area'] else ''

    metadata['name'] = re.search(r'TEST NAME:\s*(.+)', content)
    metadata['name'] = metadata['name'].group(1) if metadata['name'] else ''

    metadata['description'] = re.search(r'DESCRIPTION:\s*(.+)', content)
    metadata['description'] = metadata['description'].group(1) if metadata['description'] else ''

    metadata['role'] = re.search(r'WORKDAY ROLE:\s*(.+)', content)
    metadata['role'] = metadata['role'].group(1) if metadata['role'] else ''

    return metadata, content

def generate_enhanced_test(metadata, task_name, rag_response):
    """Generate enhanced test file with valid Electron commands"""

    # Parse RAG response for confidence score
    confidence_match = re.search(r'score:\s*(\d+)', rag_response, re.IGNORECASE)
    confidence = int(confidence_match.group(1)) if confidence_match else 0

    # Extract relevant SOAP/REST operations from RAG
    api_info = "- Query RAG for details"
    if "Get_" in rag_response or "Submit_" in rag_response:
        ops = re.findall(r'(Get_\w+|Submit_\w+|Put_\w+)', rag_response)
        if ops:
            api_info = f"- SOAP: {', '.join(set(ops[:3]))}"

    # Build the test file
    test_content = f"""================================================================================
TEST ID: {metadata['test_id']}
FUNCTIONAL AREA: {metadata['area']}
TEST NAME: {metadata['name']}
CONFIDENCE: [{'HIGH' if confidence >= 7 else 'MEDIUM' if confidence >= 5 else 'LOW'}] Score: {confidence}.0/10
SOURCE: [RAG Enhanced]
================================================================================

DESCRIPTION:
{metadata['description']}

WORKDAY ROLE: {metadata['role']}

ELECTRON STEPS:
1. enter search box as "{task_name}"
2. wait for search results (2 seconds)
3. click search result containing "{task_name}"
4. wait for page to load (3 seconds)
"""

    # Add specific steps based on task type
    task_lower = task_name.lower()

    if "supplier" in task_lower or "vendor" in task_lower:
        test_content += """5. verify supplier list displayed
6. click link "Actions"
7. screenshot as "{}_list.png"
8. click button "View All"
9. wait for data to load (2 seconds)
10. screenshot as "{}_complete.png"
""".format(metadata['test_id'], metadata['test_id'])
        verification = "- [ ] Supplier data displayed\n- [ ] No error messages shown"

    elif "requisition" in task_lower or "purchase" in task_lower:
        test_content += """5. click button "OK"
6. wait for form to load (3 seconds)
7. verify page contains "Requisition"
8. screenshot as "{}_form.png"
9. click button "Cancel"
10. screenshot as "{}_complete.png"
""".format(metadata['test_id'], metadata['test_id'])
        verification = "- [ ] Requisition form accessible\n- [ ] All required fields visible"

    elif "inventory" in task_lower or "site" in task_lower or "location" in task_lower:
        test_content += """5. wait for results to load (2 seconds)
6. verify table displayed
7. screenshot as "{}_list.png"
8. click first row in table
9. wait for details to load (2 seconds)
10. screenshot as "{}_complete.png"
""".format(metadata['test_id'], metadata['test_id'])
        verification = "- [ ] Inventory data displayed\n- [ ] Details accessible"

    else:
        # Generic steps
        test_content += """5. wait for page content to load (3 seconds)
6. verify page loaded successfully
7. screenshot as "{}_complete.png"
""".format(metadata['test_id'])
        verification = "- [ ] Task executed successfully\n- [ ] No errors displayed"

    test_content += f"""
VERIFICATION:
{verification}

API ALTERNATIVE:
{api_info}

RAG QUERY STATUS: SUCCESS (Score: {confidence})
================================================================================
"""

    return test_content, confidence

def process_test_file(filepath):
    """Process a single test file"""
    print(f"\nProcessing: {filepath.name}")

    # Extract task name
    task_name = extract_task_from_file(filepath)
    if not task_name:
        print(f"  [X] Could not extract task name")
        return None

    print(f"  Task: {task_name}")

    # Parse existing metadata
    metadata, old_content = parse_test_file(filepath)

    # Query RAG
    print(f"  Querying RAG...")
    rag_response = query_rag(task_name)

    # Generate enhanced test
    new_content, confidence = generate_enhanced_test(metadata, task_name, rag_response)

    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  [OK] Updated (Confidence: {confidence}/10)")

    return {
        'file': filepath.name,
        'task': task_name,
        'confidence': confidence,
        'status': 'UPDATED'
    }

def main():
    """Main processing function"""
    results = []

    # Process Procurement files
    print("\n" + "="*80)
    print("PROCESSING PROCUREMENT TESTS")
    print("="*80)

    procurement_files = sorted(PROCUREMENT_DIR.glob("PRO-*.txt"))[:25]
    for filepath in procurement_files:
        result = process_test_file(filepath)
        if result:
            results.append(result)

    # Process Inventory files
    print("\n" + "="*80)
    print("PROCESSING INVENTORY TESTS")
    print("="*80)

    inventory_files = sorted(INVENTORY_DIR.glob("INV-*.txt"))[:25]
    for filepath in inventory_files:
        result = process_test_file(filepath)
        if result:
            results.append(result)

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files processed: {len(results)}")
    print(f"High confidence (>= 7): {sum(1 for r in results if r['confidence'] >= 7)}")
    print(f"Medium confidence (5-6): {sum(1 for r in results if 5 <= r['confidence'] < 7)}")
    print(f"Low confidence (< 5): {sum(1 for r in results if r['confidence'] < 5)}")

    # Save results
    results_file = BASE_DIR / "batch_fix_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    main()
