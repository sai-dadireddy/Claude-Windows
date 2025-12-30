import pandas as pd
import json
import subprocess
import re
import os
from pathlib import Path

# Read scenarios
df = pd.read_excel('WD_Test_Scenarios_Master.xlsx')
proc = df[df['Functional Area'] == 'Procurement'].copy()

output_dir = Path('Procurement')
output_dir.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    """Sanitize filename by removing invalid characters"""
    if pd.isna(name):
        return "Unknown"
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '_', str(name))
    # Limit length
    return name[:100]

def query_rag(task_step):
    """Query the RAG system for a given task/step"""
    if pd.isna(task_step) or str(task_step).strip() == '':
        return None, "EMPTY"

    try:
        result = subprocess.run(
            ['python', '../workday_rag.py', str(task_step)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(Path.cwd())
        )
        return result.stdout, "SUCCESS"
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    except Exception as e:
        return None, f"ERROR: {str(e)}"

def calculate_confidence(rag_result, task_step):
    """Calculate confidence score based on RAG results"""
    if rag_result is None:
        return "LOW", 2.0, "INFERRED"

    # Check for API/SOAP references
    has_soap = 'SOAP' in rag_result or 'wsdl' in rag_result.lower()
    has_api = 'API' in rag_result or 'REST' in rag_result
    has_steps = 'step' in rag_result.lower() or 'click' in rag_result.lower()

    if has_soap and has_steps:
        return "HIGH", 8.5, "RAG"
    elif has_soap or has_api:
        return "MEDIUM", 6.5, "RAG"
    elif has_steps:
        return "MEDIUM", 6.0, "RAG"
    else:
        return "LOW", 4.0, "KB"

def extract_soap_operations(rag_result):
    """Extract SOAP operations from RAG result"""
    if not rag_result:
        return "Not found in RAG"

    # Look for common SOAP operation patterns
    patterns = [
        r'(Get_\w+)',
        r'(Create_\w+)',
        r'(Update_\w+)',
        r'(Submit_\w+)',
        r'(Put_\w+)',
        r'(Cancel_\w+)'
    ]

    operations = []
    for pattern in patterns:
        matches = re.findall(pattern, rag_result)
        operations.extend(matches)

    if operations:
        return ', '.join(set(operations[:3]))  # Return up to 3 unique operations

    return "Not found in RAG"

# Process all scenarios
count = 0
manual_count = 0
processed_count = 0

print(f"Processing {len(proc)} Procurement scenarios...")

for idx, row in proc.iterrows():
    scenario_id = row['Scenario ID']
    scenario_name = sanitize_filename(row['Scenario Name'])
    task_step = row['Task / Step']

    filename = f"{scenario_id}_{scenario_name}.txt"
    filepath = output_dir / filename

    if (count % 10) == 0:
        print(f"Progress: {count}/{len(proc)} scenarios processed...")

    # Check if task/step is empty
    if pd.isna(task_step) or str(task_step).strip() == '':
        # Generate MANUAL file
        content = f"""TEST ID: {scenario_id}
STATUS: [MANUAL REQUIRED]
REASON: Missing Task/Step - need SME input

SCENARIO NAME: {row['Scenario Name']}
DESCRIPTION: {row['Scenario Description']}
EXPECTED RESULT: {row['Customer Expected Result']}
WORKDAY ROLE: {row['Workday Role']}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        manual_count += 1
        count += 1
        continue

    # Query RAG
    rag_result, rag_status = query_rag(task_step)
    confidence, score, source = calculate_confidence(rag_result, task_step)

    # Extract SOAP API if available
    soap_api = extract_soap_operations(rag_result)

    # Generate RAG-based steps if available
    rag_steps = ""
    if rag_result and confidence in ["HIGH", "MEDIUM"]:
        rag_steps = f"""
RAG INSIGHTS:
{rag_result[:500]}...
"""

    # Generate test file
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: Procurement
TEST NAME: {row['Scenario Name']}
CONFIDENCE: [{confidence}] Score: {score}/10
SOURCE: [{source}]
================================================================================

DESCRIPTION:
{row['Scenario Description']}

WORKDAY ROLE: {row['Workday Role']}

ELECTRON STEPS:
1. enter search box as "{task_step}"
2. wait for search results
3. click search result containing "{task_step}"
4. wait for page to load
5. screenshot as "{scenario_id}_complete.png"

VERIFICATION:
- [ ] {row['Customer Expected Result']}

API ALTERNATIVE:
- SOAP: {soap_api}
{rag_steps}
RAG QUERY STATUS: {rag_status}
================================================================================
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    processed_count += 1
    count += 1

print(f"\n" + "="*80)
print(f"GENERATION COMPLETE")
print(f"="*80)
print(f"Total scenarios: {len(proc)}")
print(f"Processed with RAG: {processed_count}")
print(f"Manual required: {manual_count}")
print(f"Output directory: {output_dir.absolute()}")
print(f"="*80)
