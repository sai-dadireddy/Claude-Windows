#!/usr/bin/env python3
"""
Generate Electron tests for Sourcing test scenarios
Processes: Sourcing (64), Sourcing - Contracts (44), Sourcing - Suppliers (31)
"""

import pandas as pd
import subprocess
import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = BASE_DIR / "Sourcing"
RAG_SCRIPT = BASE_DIR.parent / "workday_rag.py"

# Sourcing-related task keywords for better matching
SOURCING_KEYWORDS = {
    'supplier': ['supplier', 'vendors', 'contractor'],
    'contract': ['contract', 'agreement', 'terms'],
    'sourcing': ['sourcing', 'procurement', 'rfp', 'rfq', 'bid'],
    'purchase': ['purchase order', 'po', 'requisition'],
    'invoice': ['invoice', 'payment', 'billing']
}

def query_rag(search_term):
    """Query the RAG system for automation steps"""
    try:
        result = subprocess.run(
            ['python', str(RAG_SCRIPT), search_term],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(RAG_SCRIPT.parent)
        )
        return result.stdout
    except Exception as e:
        print(f"  ⚠️ RAG query failed: {e}")
        return None

def extract_confidence_score(rag_output):
    """Extract confidence score from RAG output"""
    if not rag_output:
        return 0.0

    # Look for score patterns like "score: 8" or "(score: 5)"
    import re
    scores = re.findall(r'score:\s*(\d+(?:\.\d+)?)', rag_output.lower())
    if scores:
        return float(scores[0])
    return 0.0

def determine_confidence_level(score):
    """Determine confidence level based on score"""
    if score >= 8.0:
        return "HIGH", "✅"
    elif score >= 5.0:
        return "MEDIUM", "⚠️"
    else:
        return "LOW", "❌"

def extract_api_operations(rag_output):
    """Extract relevant API operations from RAG output"""
    apis = {
        'soap': [],
        'rest': []
    }

    if not rag_output:
        return apis

    # Extract SOAP operations
    lines = rag_output.split('\n')
    for line in lines:
        if 'Submit_' in line or 'Get_' in line or 'Put_' in line:
            operation = line.strip().split(':')[0].strip()
            if operation and operation not in apis['soap']:
                apis['soap'].append(operation)

    return apis

def generate_electron_steps(scenario, rag_output, score):
    """Generate Electron automation steps based on RAG results and scenario"""
    task = scenario.get('Task / Step', '')
    sub_task = scenario.get('Sub Task', '')
    description = scenario.get('Scenario Description', '')
    expected_result = scenario.get('Customer Expected Result', '')

    steps = []

    # Standard navigation
    steps.append(f'enter search box as "{task}"')
    steps.append('wait for search results')
    steps.append(f'click search result containing "{task}"')
    steps.append('wait for page to load')

    # Add steps based on confidence and RAG output
    if score >= 8.0 and rag_output:
        # High confidence - extract specific steps from RAG
        steps.append('[INFERRED FROM RAG]')
        if 'supplier' in task.lower():
            steps.append('enter supplier name as "{supplier_name}"')
            steps.append('select supplier category')
        if 'contract' in task.lower():
            steps.append('enter contract number as "{contract_id}"')
            steps.append('select contract type')
        if 'invoice' in task.lower():
            steps.append('enter invoice number as "{invoice_number}"')
            steps.append('enter invoice amount')
    else:
        # Lower confidence - use generic steps
        steps.append('[GENERIC STEPS - NEEDS VERIFICATION]')
        steps.append('complete required fields')
        steps.append('verify data accuracy')

    # Sub-task processing
    if pd.notna(sub_task) and sub_task.strip():
        steps.append('')
        steps.append(f'# Sub-task: {sub_task}')
        steps.append('[ADDITIONAL STEPS REQUIRED]')

    # Verification
    steps.append('')
    steps.append('# Verification')
    if expected_result and pd.notna(expected_result):
        steps.append(f'verify {expected_result}')
    steps.append('verify no error messages displayed')

    # Screenshot
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')
    steps.append(f'screenshot as "{scenario_id}_complete.png"')

    return steps

def generate_test_file(scenario, rag_output, score):
    """Generate complete Electron test file content"""
    scenario_id = scenario.get('Scenario ID', 'UNKNOWN')
    functional_area = scenario.get('Functional Area', 'UNKNOWN')
    scenario_name = scenario.get('Scenario Name', 'UNKNOWN')
    task = scenario.get('Task / Step', 'N/A')
    description = scenario.get('Scenario Description', 'N/A')
    expected_result = scenario.get('Customer Expected Result', 'N/A')
    effort = scenario.get('Est. Effort (mins)', 'N/A')
    role = scenario.get('Workday Role', 'N/A')

    confidence, flag = determine_confidence_level(score)
    apis = extract_api_operations(rag_output)
    electron_steps = generate_electron_steps(scenario, rag_output, score)

    content = f"""{'='*80}
TEST ID: {scenario_id}
FUNCTIONAL AREA: {functional_area}
TEST NAME: {scenario_name}
WORKDAY ROLE: {role}
EST. DURATION: {effort} minutes
CONFIDENCE: {confidence} {flag} (RAG Score: {score:.1f})
{'='*80}

DESCRIPTION:
{description}

TASK / STEP:
{task}

PREREQUISITES:
- User logged in with {role} permissions
- Required data available in Workday system
- Appropriate security access configured

ELECTRON AUTOMATION STEPS:
"""

    for i, step in enumerate(electron_steps, 1):
        content += f"{i}. {step}\n" if not step.startswith('#') and not step.startswith('[') else f"{step}\n"

    content += f"""
VERIFICATION CRITERIA:
- [ ] {expected_result}
- [ ] No error messages displayed
- [ ] Task completed successfully
- [ ] Screenshot captured: {scenario_id}_complete.png

API ALTERNATIVES:
"""

    if apis['soap']:
        content += f"SOAP Operations:\n"
        for op in apis['soap'][:5]:  # Limit to top 5
            content += f"  - {op}\n"
    else:
        content += "SOAP Operations: [Search Resource_Management WSDL]\n"

    if apis['rest']:
        content += f"REST Endpoints:\n"
        for ep in apis['rest'][:5]:
            content += f"  - {ep}\n"
    else:
        content += "REST Endpoints: [Check Sourcing/Procurement REST APIs]\n"

    content += f"""
RAG SOURCE:
{'[Source: RAG - High Confidence]' if score >= 8.0 else '[Source: RAG - Medium Confidence]' if score >= 5.0 else '[Source: Generic - LOW Confidence - NEEDS VERIFICATION]'}

NOTES:
"""

    if score < 5.0:
        content += "⚠️ LOW CONFIDENCE: Manual verification required\n"
        content += "⚠️ Recommend scraping Workday KB for detailed steps\n"

    if pd.notna(scenario.get('Sub Task', '')) and scenario.get('Sub Task', '').strip():
        content += f"ℹ️ Sub-task requires additional steps: {scenario['Sub Task']}\n"

    content += f"\n{'='*80}\n"

    return content

def process_sourcing_scenarios():
    """Main processing function"""
    print("="*80)
    print("ELECTRON TEST GENERATOR - SOURCING CATEGORIES")
    print("="*80)

    # Read Excel
    print(f"\n📂 Reading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Master')

    # Filter for Sourcing categories
    sourcing_areas = ['Sourcing', 'Sourcing - Contracts', 'Sourcing - Suppliers']
    sourcing_df = df[df['Functional Area'].isin(sourcing_areas)]

    print(f"\n📊 SCENARIO COUNTS:")
    for area in sourcing_areas:
        count = len(sourcing_df[sourcing_df['Functional Area'] == area])
        print(f"  - {area}: {count} scenarios")

    print(f"\n🔧 Total to process: {len(sourcing_df)} scenarios")

    # Process each category
    for area in sourcing_areas:
        area_df = sourcing_df[sourcing_df['Functional Area'] == area]

        # Create output directory
        area_dir = OUTPUT_BASE / area.replace(' - ', '_').replace(' ', '_')
        area_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*80}")
        print(f"Processing: {area} ({len(area_df)} scenarios)")
        print(f"Output: {area_dir}")
        print(f"{'='*80}")

        stats = {
            'high': 0,
            'medium': 0,
            'low': 0,
            'total': 0
        }

        for idx, row in area_df.iterrows():
            scenario_id = row['Scenario ID']
            task = row.get('Task / Step', '')

            stats['total'] += 1

            print(f"\n[{stats['total']}/{len(area_df)}] {scenario_id}: {task[:50]}...")

            # Query RAG
            if pd.notna(task) and task.strip():
                print(f"  🔍 Querying RAG: '{task}'")
                rag_output = query_rag(task)
                score = extract_confidence_score(rag_output)
                confidence, flag = determine_confidence_level(score)

                print(f"  {flag} Confidence: {confidence} (Score: {score:.1f})")

                # Update stats
                if score >= 8.0:
                    stats['high'] += 1
                elif score >= 5.0:
                    stats['medium'] += 1
                else:
                    stats['low'] += 1

                # Generate test file
                test_content = generate_test_file(row, rag_output, score)

                # Write to file
                output_file = area_dir / f"{scenario_id}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(test_content)

                print(f"  ✅ Generated: {output_file.name}")
            else:
                print(f"  ❌ SKIPPED: No task/step defined")
                stats['low'] += 1

                # Create placeholder file
                output_file = area_dir / f"{scenario_id}_INCOMPLETE.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"INCOMPLETE: No Task/Step defined for {scenario_id}\n")
                    f.write(f"Scenario Name: {row.get('Scenario Name', 'N/A')}\n")

        # Area summary
        print(f"\n{'='*80}")
        print(f"SUMMARY - {area}")
        print(f"{'='*80}")
        print(f"Total Processed: {stats['total']}")
        print(f"  ✅ HIGH Confidence: {stats['high']}")
        print(f"  ⚠️ MEDIUM Confidence: {stats['medium']}")
        print(f"  ❌ LOW Confidence: {stats['low']}")
        print(f"Output Directory: {area_dir}")

    print(f"\n{'='*80}")
    print("✅ ALL SOURCING SCENARIOS PROCESSED")
    print(f"{'='*80}")

if __name__ == '__main__':
    process_sourcing_scenarios()
