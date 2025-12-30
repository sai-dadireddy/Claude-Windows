#!/usr/bin/env python3
"""
Electron Test Generator for AP, AR, Cash Management
Generates test scenarios from Excel with RAG-based enrichment
"""

import pandas as pd
import os
import re
import subprocess
import sys
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
BASE_OUTPUT_DIR = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

# Module configurations
MODULES = {
    "Accounts Payable": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "Accounts_Payable"),
        "expected_count": 244
    },
    "Accounts Receivable": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "Accounts_Receivable"),
        "expected_count": 221
    },
    "Cash Management": {
        "output_dir": os.path.join(BASE_OUTPUT_DIR, "Cash_Management"),
        "expected_count": 168
    }
}

def sanitize_filename(name):
    """Sanitize scenario name for filename"""
    name = re.sub(r'[<>:"/\\|?*]', '_', str(name))
    name = name[:100]  # Limit length
    return name.strip()

def query_rag(task_step):
    """Query Workday RAG for task/step information"""
    if not task_step or pd.isna(task_step):
        return None, "No Task/Step provided"

    try:
        result = subprocess.run(
            [sys.executable, RAG_SCRIPT, str(task_step)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(RAG_SCRIPT)
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip(), None
        else:
            return None, f"RAG query failed: {result.stderr}"
    except Exception as e:
        return None, f"RAG error: {str(e)}"

def calculate_confidence(scenario, rag_result):
    """Calculate confidence score based on available data"""
    score = 0.0

    # Has Task/Step (3 points)
    task_col = scenario.get('Task / Step') or scenario.get('Task')
    if task_col and not pd.isna(task_col):
        score += 3.0

    # Has Expected Result (2 points)
    exp_col = scenario.get('Customer Expected Result') or scenario.get('Expected_Result')
    if exp_col and not pd.isna(exp_col):
        score += 2.0

    # RAG found results (3 points)
    if rag_result:
        if len(rag_result) > 200:
            score += 3.0
        elif len(rag_result) > 50:
            score += 1.5

    # Has clear action verbs (1 point)
    task = str(task_col if task_col else '')
    action_verbs = ['create', 'submit', 'approve', 'review', 'post', 'run', 'generate',
                    'process', 'reconcile', 'enter', 'add', 'update']
    if any(verb in task.lower() for verb in action_verbs):
        score += 1.0

    # Has business object reference (1 point)
    business_objects = ['invoice', 'payment', 'customer', 'supplier', 'cash', 'receipt',
                       'adjustment', 'journal', 'settlement', 'deposit', 'bank']
    if any(obj in task.lower() for obj in business_objects):
        score += 1.0

    # Normalize to 10
    score = min(score, 10.0)

    if score >= 7.0:
        level = "HIGH"
    elif score >= 4.0:
        level = "MEDIUM"
    else:
        level = "LOW"

    return level, score

def extract_rag_steps(rag_result, task_step):
    """Extract actionable steps from RAG results"""
    steps = []

    # Look for SOAP operations
    soap_ops = re.findall(r'(Get_\w+|Submit_\w+|Create_\w+|Update_\w+)', rag_result or '')
    if soap_ops:
        steps.append(f"   API ALTERNATIVE: Use SOAP operation: {soap_ops[0]}")

    # Look for REST endpoints
    rest_eps = re.findall(r'/api/v\d+/[\w/]+', rag_result or '')
    if rest_eps:
        steps.append(f"   API ALTERNATIVE: Call REST endpoint: {rest_eps[0]}")

    return steps

def generate_electron_steps(scenario, rag_result):
    """Generate Electron-specific test steps"""
    task_step = scenario.get('Task / Step') or scenario.get('Task', '')

    if not task_step or pd.isna(task_step):
        return None

    steps = []
    scenario_id = scenario.get('Scenario ID') or scenario.get('Scenario_ID', 'UNKNOWN')
    task_lower = str(task_step).lower()

    # Step 1-3: Search and navigate
    steps.append(f'1. enter search box as "{task_step}"')
    steps.append('2. wait for search results')
    steps.append('3. click search result')

    # Steps 4-6: Based on task type
    if any(word in task_lower for word in ['create', 'enter', 'add', 'submit']):
        steps.append('4. wait for page load')
        steps.append('5. fill required fields')
        steps.append('   - Enter all mandatory data')
        steps.append('   - Validate field formats')
        steps.append('6. click "Submit" button')

    elif any(word in task_lower for word in ['run', 'generate', 'report']):
        steps.append('4. wait for report page')
        steps.append('5. set report parameters')
        steps.append('   - Select date range')
        steps.append('   - Choose output format')
        steps.append('6. click "OK" or "Run" button')

    elif any(word in task_lower for word in ['review', 'approve', 'process']):
        steps.append('4. wait for inbox/task page')
        steps.append('5. click transaction to review')
        steps.append('   - Verify details are correct')
        steps.append('   - Check for validation errors')
        steps.append('6. click "Approve" or "Submit" button')

    elif any(word in task_lower for word in ['reconcile', 'settle', 'match']):
        steps.append('4. wait for reconciliation page')
        steps.append('5. select items to reconcile')
        steps.append('   - Match transactions')
        steps.append('   - Resolve discrepancies')
        steps.append('6. click "Complete" or "Settle" button')

    else:
        steps.append('4. wait for page load')
        steps.append('5. complete required actions')
        steps.append('   - Follow on-screen instructions')
        steps.append('   - Enter required data')
        steps.append('6. click "Done" or "Submit" button')

    # Step 7: Screenshot
    steps.append(f'7. screenshot as "{scenario_id}_complete.png"')

    # Add RAG-based insights
    rag_steps = extract_rag_steps(rag_result, task_step)
    if rag_steps:
        steps.append('')
        steps.extend(rag_steps)

    return '\n'.join(steps)

def generate_verification(scenario):
    """Generate verification checklist"""
    expected = scenario.get('Customer Expected Result') or scenario.get('Expected_Result', '')

    verifications = []

    if expected and not pd.isna(expected):
        verifications.append(f"- [ ] {expected}")

    # Add standard verifications
    verifications.append("- [ ] Transaction completed successfully")
    verifications.append("- [ ] No error messages displayed")
    verifications.append("- [ ] All required fields populated")
    verifications.append("- [ ] Confirmation message received")

    return '\n'.join(verifications)

def generate_test_file(scenario, rag_result, output_path, module_name):
    """Generate complete test file"""
    scenario_id = scenario.get('Scenario ID') or scenario.get('Scenario_ID', 'UNKNOWN')
    scenario_name = scenario.get('Scenario Name') or scenario.get('Scenario_Name', 'Unnamed Test')
    task_step = scenario.get('Task / Step') or scenario.get('Task', '')

    # Calculate confidence
    conf_level, conf_score = calculate_confidence(scenario, rag_result)

    # Generate steps
    electron_steps = generate_electron_steps(scenario, rag_result)

    # Check if manual
    is_manual = not task_step or pd.isna(task_step) or not electron_steps

    # Build file content
    content = []
    content.append("=" * 80)
    content.append(f"TEST ID: {scenario_id} | CONFIDENCE: {conf_level} Score: {int(conf_score)}/10")
    content.append("=" * 80)
    content.append("")
    content.append(f"MODULE: {module_name}")
    content.append(f"TEST NAME: {scenario_name}")
    content.append(f"TASK/STEP: {task_step if task_step and not pd.isna(task_step) else 'N/A'}")
    content.append("")

    if is_manual:
        content.append("=" * 80)
        content.append("STATUS: [MANUAL REQUIRED]")
        content.append("=" * 80)
        content.append("REASON: Missing Task/Step or insufficient information for automation")
        content.append("")
        content.append(f"SCENARIO DETAILS:")
        content.append(f"  Name: {scenario_name}")
        desc = scenario.get('Scenario Description') or scenario.get('Scenario_Description', '')
        if desc and not pd.isna(desc):
            content.append(f"  Description: {desc}")
        expected = scenario.get('Customer Expected Result') or scenario.get('Expected_Result', '')
        if expected and not pd.isna(expected):
            content.append(f"  Expected Result: {expected}")
        content.append("")
        content.append("MANUAL TEST STEPS:")
        content.append("1. Review scenario requirements")
        content.append("2. Navigate to appropriate Workday page")
        content.append("3. Complete transaction manually")
        content.append("4. Verify expected results")
        content.append(f"5. screenshot as \"{scenario_id}_manual_complete.png\"")
    else:
        content.append("=" * 80)
        content.append("ELECTRON STEPS:")
        content.append("=" * 80)
        content.append(electron_steps)
        content.append("")
        content.append("=" * 80)
        content.append("VERIFICATION:")
        content.append("=" * 80)
        content.append(generate_verification(scenario))

        # Add RAG insights if available
        if rag_result and len(rag_result) > 50:
            content.append("")
            content.append("=" * 80)
            content.append("RAG RESULTS:")
            content.append("=" * 80)
            # Truncate RAG result to first 1000 chars
            content.append(rag_result[:1000])
            if len(rag_result) > 1000:
                content.append("...")

    content.append("")
    content.append("=" * 80)

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

    return conf_level, conf_score, is_manual

def process_module(module_name, config):
    """Process all scenarios for a module"""
    print("=" * 80)
    print(f"Processing: {module_name}")
    print("=" * 80)

    # Create output directory
    output_dir = config['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Read Excel - try to find the right sheet
    try:
        xl = pd.ExcelFile(EXCEL_PATH)

        # Try exact match first
        if module_name in xl.sheet_names:
            df = pd.read_excel(EXCEL_PATH, sheet_name=module_name)
        # Try finding by Module column
        else:
            df_all = pd.read_excel(EXCEL_PATH)
            # Check if there's a Module column
            if 'Module' in df_all.columns:
                df = df_all[df_all['Module'] == module_name].copy()
            elif 'Functional Area' in df_all.columns:
                df = df_all[df_all['Functional Area'] == module_name].copy()
            else:
                print(f"ERROR: Cannot find {module_name} in Excel")
                print(f"Available sheets: {xl.sheet_names[:10]}")
                return None

        print(f"Found {len(df)} scenarios")

        if len(df) == 0:
            print(f"WARNING: No scenarios found for {module_name}")
            return None

    except Exception as e:
        print(f"ERROR reading Excel: {e}")
        return None

    # Process each scenario
    stats = {
        'total': len(df),
        'generated': 0,
        'manual': 0,
        'high_conf': 0,
        'medium_conf': 0,
        'low_conf': 0
    }

    for idx, row in df.iterrows():
        scenario_id = row.get('Scenario ID') or row.get('Scenario_ID', f'UNKNOWN_{idx}')
        scenario_name = row.get('Scenario Name') or row.get('Scenario_Name', 'Unnamed')
        task_step = row.get('Task / Step') or row.get('Task', '')

        print(f"\n[{idx+1}/{len(df)}] {scenario_id} - {str(scenario_name)[:50]}...")

        # Query RAG
        rag_result = None
        if task_step and not pd.isna(task_step):
            print(f"  Querying RAG: {str(task_step)[:60]}...")
            rag_result, error = query_rag(task_step)
            if error:
                print(f"  WARNING: {error}")

        # Generate filename
        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        output_path = os.path.join(output_dir, filename)

        # Generate test file
        try:
            conf_level, conf_score, is_manual = generate_test_file(row, rag_result, output_path, module_name)

            # Update stats
            stats['generated'] += 1
            if is_manual:
                stats['manual'] += 1
            if conf_level == 'HIGH':
                stats['high_conf'] += 1
            elif conf_level == 'MEDIUM':
                stats['medium_conf'] += 1
            else:
                stats['low_conf'] += 1

            print(f"  ✓ Generated: {filename}")
            print(f"    Confidence: {conf_level} ({int(conf_score)}/10)")

        except Exception as e:
            print(f"  ERROR generating test: {e}")

    # Print module summary
    print("\n" + "=" * 80)
    print(f"{module_name} - COMPLETE")
    print("=" * 80)
    print(f"Total scenarios: {stats['total']}")
    print(f"Files generated: {stats['generated']}")
    print(f"Manual scenarios: {stats['manual']}")
    print(f"HIGH confidence: {stats['high_conf']} ({stats['high_conf']/stats['total']*100:.1f}%)")
    print(f"MEDIUM confidence: {stats['medium_conf']} ({stats['medium_conf']/stats['total']*100:.1f}%)")
    print(f"LOW confidence: {stats['low_conf']} ({stats['low_conf']/stats['total']*100:.1f}%)")
    print()

    return stats

def main():
    """Main processing function"""
    print("=" * 80)
    print("WORKDAY ELECTRON TEST GENERATOR")
    print("AP / AR / CASH MANAGEMENT")
    print("=" * 80)
    print()

    all_stats = {}

    # Process each module
    for module_name, config in MODULES.items():
        stats = process_module(module_name, config)
        if stats:
            all_stats[module_name] = stats

    # Print final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)

    total_all = 0
    total_generated = 0
    total_high = 0
    total_medium = 0
    total_low = 0
    total_manual = 0

    for module_name, stats in all_stats.items():
        print(f"\n{module_name}:")
        print(f"  Expected: {MODULES[module_name]['expected_count']}")
        print(f"  Found: {stats['total']}")
        print(f"  Generated: {stats['generated']}")
        print(f"  HIGH: {stats['high_conf']}")
        print(f"  MEDIUM: {stats['medium_conf']}")
        print(f"  LOW: {stats['low_conf']}")
        print(f"  MANUAL: {stats['manual']}")

        total_all += stats['total']
        total_generated += stats['generated']
        total_high += stats['high_conf']
        total_medium += stats['medium_conf']
        total_low += stats['low_conf']
        total_manual += stats['manual']

    print("\n" + "=" * 80)
    print("OVERALL TOTALS:")
    print(f"  Scenarios processed: {total_all}")
    print(f"  Files generated: {total_generated}")
    print(f"  HIGH confidence: {total_high} ({total_high/total_all*100:.1f}%)")
    print(f"  MEDIUM confidence: {total_medium} ({total_medium/total_all*100:.1f}%)")
    print(f"  LOW confidence: {total_low} ({total_low/total_all*100:.1f}%)")
    print(f"  MANUAL required: {total_manual} ({total_manual/total_all*100:.1f}%)")
    print("=" * 80)

if __name__ == '__main__':
    main()
