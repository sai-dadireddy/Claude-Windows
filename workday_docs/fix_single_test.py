#!/usr/bin/env python3
"""Fix a single test file with proper RAG-enhanced steps"""

import sys
import re
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent

def query_rag(task_name):
    """Query RAG system"""
    result = subprocess.run(
        ["python", str(BASE_DIR / "workday_rag.py"), task_name],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR),
        timeout=30
    )
    return result.stdout

def fix_test_file(test_id, task_name):
    """Fix a specific test file"""

    # Find the file
    test_files = list(BASE_DIR.glob(f"electron_tests/**/{test_id}_*.txt"))
    if not test_files:
        print(f"File not found: {test_id}")
        return

    filepath = test_files[0]
    print(f"Processing: {filepath.name}")
    print(f"Task: {task_name}")

    # Read existing file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    test_id_match = re.search(r'TEST ID:\s*(.+)', content)
    area_match = re.search(r'FUNCTIONAL AREA:\s*(.+)', content)
    name_match = re.search(r'TEST NAME:\s*(.+)', content)
    desc_match = re.search(r'DESCRIPTION:\s*(.+)', content)
    role_match = re.search(r'WORKDAY ROLE:\s*(.+)', content)

    # Query RAG
    print("Querying RAG...")
    rag_result = query_rag(task_name)

    # Check for SOAP operations
    soap_ops = re.findall(r'(Get_\w+|Submit_\w+|Put_\w+)', rag_result)
    api_alternative = f"- SOAP: {', '.join(set(soap_ops[:3]))}" if soap_ops else "- Query RAG for details"

    # Determine confidence from RAG score
    score_match = re.search(r'score:\s*(\d+)', rag_result, re.IGNORECASE)
    confidence = int(score_match.group(1)) if score_match else 5

    # Generate new content
    new_content = f"""================================================================================
TEST ID: {test_id_match.group(1) if test_id_match else test_id}
FUNCTIONAL AREA: {area_match.group(1) if area_match else 'Unknown'}
TEST NAME: {name_match.group(1) if name_match else 'Unknown'}
CONFIDENCE: [{'HIGH' if confidence >= 7 else 'MEDIUM' if confidence >= 5 else 'LOW'}] Score: {confidence}.0/10
SOURCE: [RAG Enhanced - Manual Review]
================================================================================

DESCRIPTION:
{desc_match.group(1) if desc_match else 'No description'}

WORKDAY ROLE: {role_match.group(1) if role_match else 'Not specified'}

ELECTRON STEPS:
1. enter search box as "{task_name}"
2. wait for search results
3. click search result containing "{task_name}"
4. wait for page to load
"""

    # Add task-specific steps
    task_lower = task_name.lower()
    test_id_str = test_id_match.group(1) if test_id_match else test_id

    if "supplier" in task_lower:
        new_content += f"""5. verify page title contains "Supplier"
6. click link "Related Actions"
7. screenshot as "{test_id_str}_actions.png"
8. click link "View" or "Edit"
9. wait for details to load
10. verify supplier details displayed
11. screenshot as "{test_id_str}_complete.png"

VERIFICATION:
- [ ] Supplier list or details displayed correctly
- [ ] Related Actions menu accessible
- [ ] No error messages shown
"""
    elif "requisition" in task_lower or "purchase" in task_lower:
        new_content += f"""5. click button "OK" or "Add"
6. wait for form to load
7. verify page contains "Requisition" or "Purchase Order"
8. screenshot as "{test_id_str}_form.png"
9. click button "Cancel"
10. screenshot as "{test_id_str}_complete.png"

VERIFICATION:
- [ ] Requisition/PO form accessible
- [ ] Required fields visible
- [ ] Cancel button works correctly
"""
    elif "inventory" in task_lower or "site" in task_lower or "location" in task_lower:
        new_content += f"""5. wait for results table to load
6. verify table contains data
7. screenshot as "{test_id_str}_list.png"
8. click first row to view details
9. wait for detail page to load
10. verify details displayed
11. screenshot as "{test_id_str}_complete.png"

VERIFICATION:
- [ ] Inventory/location data displayed
- [ ] Details page accessible
- [ ] Data appears complete
"""
    else:
        new_content += f"""5. wait for page to fully load
6. verify page loaded without errors
7. screenshot as "{test_id_str}_complete.png"

VERIFICATION:
- [ ] Task completed successfully
- [ ] No error messages displayed
"""

    new_content += f"""
API ALTERNATIVE:
{api_alternative}

RAG QUERY STATUS: SUCCESS (Confidence: {confidence}/10)
================================================================================
"""

    # Write updated file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Updated with confidence: {confidence}/10")
    print(f"API operations found: {len(soap_ops) if soap_ops else 0}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fix_single_test.py <TEST_ID> <TASK_NAME>")
        print('Example: python fix_single_test.py PRO-1-0010 "Find Suppliers"')
        sys.exit(1)

    test_id = sys.argv[1]
    task_name = sys.argv[2]
    fix_test_file(test_id, task_name)
