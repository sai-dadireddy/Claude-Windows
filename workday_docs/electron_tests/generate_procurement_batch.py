import pandas as pd
import subprocess
import re
from pathlib import Path
import sys

# Read scenarios
df = pd.read_excel('WD_Test_Scenarios_Master.xlsx')
proc = df[df['Functional Area'] == 'Procurement'].copy()

output_dir = Path('Procurement')
output_dir.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name):
    """Sanitize filename by removing invalid characters"""
    if pd.isna(name):
        return "Unknown"
    name = re.sub(r'[<>:"/\\|?*]', '_', str(name))
    return name[:100]

def query_rag(task_step):
    """Query the RAG system for a given task/step"""
    if pd.isna(task_step) or str(task_step).strip() == '':
        return None, "EMPTY"

    try:
        # Run RAG query
        result = subprocess.run(
            ['python', '../workday_rag.py', str(task_step)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(Path.cwd())
        )

        if result.returncode == 0 and result.stdout:
            return result.stdout, "SUCCESS"
        else:
            return result.stderr if result.stderr else None, "NO_RESULTS"

    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    except Exception as e:
        return None, f"ERROR"

def calculate_confidence(rag_result, task_step):
    """Calculate confidence score based on RAG results"""
    if rag_result is None or rag_result == "":
        return "LOW", 2.0, "INFERRED"

    rag_lower = rag_result.lower()

    # Check for API/SOAP references
    has_soap = 'soap' in rag_lower or 'wsdl' in rag_lower
    has_rest = 'rest' in rag_lower or 'api' in rag_lower
    has_steps = 'step' in rag_lower or 'click' in rag_lower or 'enter' in rag_lower
    has_task = task_step.lower() in rag_lower if task_step else False

    score = 0
    if has_soap:
        score += 3
    if has_rest:
        score += 2
    if has_steps:
        score += 2
    if has_task:
        score += 2

    if score >= 6:
        return "HIGH", 8.0 + (score - 6) * 0.5, "RAG"
    elif score >= 3:
        return "MEDIUM", 5.0 + score * 0.5, "RAG"
    else:
        return "LOW", 3.0 + score * 0.5, "KB"

def extract_soap_operations(rag_result):
    """Extract SOAP operations from RAG result"""
    if not rag_result:
        return "Query RAG for details"

    patterns = [
        r'(Get_[\w_]+)',
        r'(Create_[\w_]+)',
        r'(Update_[\w_]+)',
        r'(Submit_[\w_]+)',
        r'(Put_[\w_]+)',
        r'(Cancel_[\w_]+)',
        r'(Find_[\w_]+)'
    ]

    operations = []
    for pattern in patterns:
        matches = re.findall(pattern, rag_result, re.IGNORECASE)
        operations.extend(matches)

    if operations:
        unique_ops = list(set(operations[:5]))
        return ', '.join(unique_ops)

    return "Check WSDL index for available operations"

def generate_electron_steps(task_step, rag_result, scenario_id):
    """Generate Electron automation steps"""
    steps = [
        f'1. enter search box as "{task_step}"',
        '2. wait for search results (2 seconds)',
        f'3. click search result containing "{task_step}"',
        '4. wait for page to load (3 seconds)'
    ]

    # Add RAG-based steps if available
    if rag_result and 'click' in rag_result.lower():
        # Try to extract specific actions from RAG
        step_num = 5
        for line in rag_result.split('\n'):
            if any(keyword in line.lower() for keyword in ['click', 'enter', 'select', 'fill']):
                steps.append(f'{step_num}. {line.strip()[:100]}')
                step_num += 1
                if step_num > 8:  # Limit to reasonable number of steps
                    break

    steps.append(f'{len(steps) + 1}. screenshot as "{scenario_id}_complete.png"')

    return '\n'.join(steps)

# Get batch parameters
batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 50
start_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0

end_idx = min(start_idx + batch_size, len(proc))
batch = proc.iloc[start_idx:end_idx]

print(f"Processing batch {start_idx}-{end_idx} of {len(proc)} scenarios...")
print("="*80)

count = 0
manual_count = 0
processed_count = 0

for idx, row in batch.iterrows():
    scenario_id = row['Scenario ID']
    scenario_name = sanitize_filename(row['Scenario Name'])
    task_step = row['Task / Step']

    filename = f"{scenario_id}_{scenario_name}.txt"
    filepath = output_dir / filename

    # Check if task/step is empty
    if pd.isna(task_step) or str(task_step).strip() == '':
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
        print(f"  [{count}] {scenario_id} - MANUAL REQUIRED (no task/step)")
        continue

    # Query RAG
    print(f"  [{count + 1}] Querying RAG for: {task_step[:50]}...")
    rag_result, rag_status = query_rag(task_step)
    confidence, score, source = calculate_confidence(rag_result, task_step)

    # Extract SOAP API if available
    soap_api = extract_soap_operations(rag_result)

    # Generate Electron steps
    electron_steps = generate_electron_steps(task_step, rag_result, scenario_id)

    # Generate test file
    content = f"""================================================================================
TEST ID: {scenario_id}
FUNCTIONAL AREA: Procurement
TEST NAME: {row['Scenario Name']}
CONFIDENCE: [{confidence}] Score: {score:.1f}/10
SOURCE: [{source}]
================================================================================

DESCRIPTION:
{row['Scenario Description']}

WORKDAY ROLE: {row['Workday Role']}

ELECTRON STEPS:
{electron_steps}

VERIFICATION:
- [ ] {row['Customer Expected Result']}

API ALTERNATIVE:
- SOAP: {soap_api}

RAG QUERY STATUS: {rag_status}
================================================================================
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    processed_count += 1
    count += 1
    print(f"      ✓ Generated [{confidence}] {scenario_id}")

print("\n" + "="*80)
print(f"Batch {start_idx}-{end_idx} COMPLETE")
print(f"Processed with RAG: {processed_count}")
print(f"Manual required: {manual_count}")
print(f"="*80)
