#!/usr/bin/env python3
import pandas as pd
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
EXCEL_PATH = BASE_DIR / "WD_Test_Scenarios_Master.xlsx"
OUTPUT_BASE = BASE_DIR / "Sourcing"
RAG_SCRIPT = BASE_DIR.parent / "workday_rag.py"

def query_rag(search_term):
    try:
        result = subprocess.run(['python', str(RAG_SCRIPT), search_term], capture_output=True, text=True, timeout=30, cwd=str(RAG_SCRIPT.parent))
        return result.stdout
    except Exception as e:
        print(f"  WARNING RAG query failed: {e}", file=sys.stderr)
        return None

def extract_score(rag_output):
    if not rag_output:
        return 0.0
    import re
    scores = re.findall(r'score:\s*(\d+(?:\.\d+)?)', rag_output.lower())
    return float(scores[0]) if scores else 0.0

def get_confidence(score):
    if score >= 7.0:
        return "HIGH", "[OK]"
    elif score >= 5.0:
        return "MEDIUM", "[!]"
    else:
        return "LOW", "[X]"

def extract_apis(rag_output):
    apis = {'soap': []}
    if not rag_output:
        return apis
    for line in rag_output.split('\n'):
        if 'Submit_' in line or 'Get_' in line or 'Put_' in line:
            op = line.strip().split(':')[0].strip()
            if op and op not in apis['soap']:
                apis['soap'].append(op)
    return apis

def gen_steps(scenario, rag_output, score):
    task = scenario.get('Task / Step', '')
    sub_task = scenario.get('Sub Task', '')
    result = scenario.get('Customer Expected Result', '')
    steps = []

    steps.append(f'enter search box as "{task}"')
    steps.append('wait for search results')
    steps.append(f'click search result containing "{task}"')
    steps.append('wait for page to load')

    if score >= 7.0 and rag_output:
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
    elif score >= 5.0:
        steps.append('[NEEDS SME REVIEW]')
        steps.append('complete required fields')
    else:
        steps.append('[MANUAL - RAG score < 5.0]')
        return steps

    if pd.notna(sub_task) and sub_task.strip():
        steps.append('')
        steps.append(f'# Sub-task: {sub_task}')

    steps.append('')
    steps.append('# Verification')
    if result and pd.notna(result):
        steps.append(f'verify {result}')
    steps.append('verify no error messages displayed')

    sid = scenario.get('Scenario ID', 'UNKNOWN')
    steps.append(f'screenshot as "{sid}_complete.png"')

    return steps

def gen_file(scenario, rag_output, score):
    sid = scenario.get('Scenario ID', 'UNKNOWN')
    area = scenario.get('Functional Area', 'UNKNOWN')
    name = scenario.get('Scenario Name', 'UNKNOWN')
    task = scenario.get('Task / Step', 'N/A')
    desc = scenario.get('Scenario Description', 'N/A')
    result = scenario.get('Customer Expected Result', 'N/A')
    effort = scenario.get('Est. Effort (mins)', 'N/A')
    role = scenario.get('Workday Role', 'N/A')

    conf, flag = get_confidence(score)
    apis = extract_apis(rag_output)
    steps = gen_steps(scenario, rag_output, score)

    content = f"""{'='*80}
TEST ID: {sid}
FUNCTIONAL AREA: {area}
TEST NAME: {name}
WORKDAY ROLE: {role}
EST. DURATION: {effort} minutes
CONFIDENCE: {conf} {flag} (RAG Score: {score:.1f})
{'='*80}

DESCRIPTION:
{desc}

TASK / STEP:
{task}

PREREQUISITES:
- User logged in with {role} permissions
- Required data available in Workday system

ELECTRON AUTOMATION STEPS:
"""

    for i, step in enumerate(steps, 1):
        content += f"{i}. {step}\n" if not step.startswith('#') and not step.startswith('[') else f"{step}\n"

    content += f"""
VERIFICATION CRITERIA:
- [ ] {result}
- [ ] No error messages displayed
- [ ] Task completed successfully

API ALTERNATIVES:
"""

    if apis['soap']:
        content += "SOAP Operations:\n"
        for op in apis['soap'][:5]:
            content += f"  - {op}\n"
    else:
        content += "SOAP Operations: [Search Resource_Management WSDL]\n"

    content += f"""
RAG SOURCE:
{'[Source: RAG - High Confidence]' if score >= 7.0 else '[Source: RAG - Medium Confidence]' if score >= 5.0 else '[Source: MANUAL REQUIRED - LOW Confidence]'}

NOTES:
"""

    if score < 5.0:
        content += "[!] LOW CONFIDENCE: Manual steps required - RAG cannot provide guidance\n"
    elif score < 7.0:
        content += "[!] MEDIUM CONFIDENCE: SME review required before use\n"

    if pd.notna(scenario.get('Sub Task', '')) and scenario.get('Sub Task', '').strip():
        content += f"[i] Sub-task requires additional steps: {scenario['Sub Task']}\n"

    content += f"\n{'='*80}\n"

    return content

def main():
    print("="*80)
    print("ELECTRON TEST GENERATOR - SOURCING CATEGORIES")
    print("="*80)

    print(f"\nReading Excel: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Master')

    areas = ['Sourcing', 'Sourcing - Contracts', 'Sourcing - Suppliers']
    sourcing_df = df[df['Functional Area'].isin(areas)]

    print(f"\nSCENARIO COUNTS:")
    for area in areas:
        count = len(sourcing_df[sourcing_df['Functional Area'] == area])
        print(f"  - {area}: {count}")

    print(f"\nTotal: {len(sourcing_df)}")

    for area in areas:
        area_df = sourcing_df[sourcing_df['Functional Area'] == area]
        area_dir = OUTPUT_BASE / area.replace(' - ', '_').replace(' ', '_')
        area_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*80}")
        print(f"Processing: {area} ({len(area_df)})")
        print(f"Output: {area_dir}")
        print(f"{'='*80}")

        stats = {'high': 0, 'medium': 0, 'low': 0, 'manual': 0, 'total': 0}

        for idx, row in area_df.iterrows():
            sid = row['Scenario ID']
            task = row.get('Task / Step', '')
            stats['total'] += 1

            print(f"\n[{stats['total']}/{len(area_df)}] {sid}: {task[:50]}...")

            if pd.notna(task) and task.strip():
                print(f"  Querying RAG: {task}")
                rag_out = query_rag(task)
                score = extract_score(rag_out)
                conf, flag = get_confidence(score)

                print(f"  {flag} {conf} (Score: {score:.1f})")

                if score >= 7.0:
                    stats['high'] += 1
                elif score >= 5.0:
                    stats['medium'] += 1
                else:
                    stats['manual'] += 1
                    stats['low'] += 1

                content = gen_file(row, rag_out, score)
                suffix = '_MANUAL.txt' if score < 5.0 else '.txt'
                out_file = area_dir / f"{sid}{suffix}"
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"  [OK] Generated: {out_file.name}")
            else:
                print(f"  [X] SKIPPED: No task defined")
                stats['low'] += 1
                out_file = area_dir / f"{sid}_INCOMPLETE.txt"
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(f"INCOMPLETE: No Task/Step for {sid}\n")
                    f.write(f"Name: {row.get('Scenario Name', 'N/A')}\n")

        print(f"\n{'='*80}")
        print(f"SUMMARY - {area}")
        print(f"{'='*80}")
        print(f"Total: {stats['total']}")
        print(f"  HIGH (>= 7.0): {stats['high']}")
        print(f"  MEDIUM (5.0-6.9): {stats['medium']}")
        print(f"  MANUAL (< 5.0): {stats['manual']}")
        print(f"  Skipped: {stats['low'] - stats['manual']}")
        print(f"Output: {area_dir}")

    print(f"\n{'='*80}")
    print("COMPLETED")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
