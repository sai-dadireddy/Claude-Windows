#!/usr/bin/env python3
"""
Batch update Finance test files with RAG-enhanced Electron steps
"""
import os
import re
import sys
from pathlib import Path
from workday_rag import WorkdayRAG

def extract_task_name(file_path):
    """Extract task name from filename"""
    # Example: FACC-1-0130_Edit Tenant Setup Financials.txt
    # Extract: Edit Tenant Setup Financials
    filename = Path(file_path).name
    match = re.match(r'FACC-\d+-\d+_(.+)\.txt', filename)
    if match:
        return match.group(1)
    return None

def read_test_file(file_path):
    """Read existing test file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_test_file(content):
    """Parse test file to extract metadata"""
    data = {}

    # Extract TEST ID
    match = re.search(r'TEST ID: (FACC-\d+-\d+)', content)
    if match:
        data['test_id'] = match.group(1)

    # Extract TEST NAME
    match = re.search(r'TEST NAME: (.+)', content)
    if match:
        data['test_name'] = match.group(1)

    # Extract CONFIDENCE
    match = re.search(r'CONFIDENCE: \[(\w+)\] Score: ([\d.]+)/10', content)
    if match:
        data['confidence_level'] = match.group(1)
        data['confidence_score'] = float(match.group(2))

    return data

def generate_electron_steps(task_name, rag_results, test_id):
    """Generate Electron steps from RAG results"""

    if not rag_results or len(rag_results) == 0:
        return None, 2.0  # No results, very low confidence

    # Calculate confidence from RAG score
    top_score = rag_results[0]['score']

    if top_score < 5.0:
        # MANUAL - insufficient knowledge
        return None, top_score

    # Extract relevant content
    steps = []
    steps.append(f'enter search box as "{task_name}"')
    steps.append('wait for search results')
    steps.append(f'click search result containing "{task_name}"')
    steps.append('wait for page to load')

    # Add specific steps based on task type
    if 'confirm' in task_name.lower() or 'verify' in task_name.lower():
        steps.append('verify data displayed correctly')
        steps.append('check required fields are populated')
    elif 'edit' in task_name.lower():
        steps.append('modify required fields')
        steps.append('click button "OK"')
    elif 'audit' in task_name.lower():
        steps.append('review displayed information')
        steps.append('verify against expected values')

    steps.append(f'screenshot as "{test_id}_complete.png"')

    return steps, min(top_score, 10.0)

def format_test_file(test_data, task_name, steps, confidence_score):
    """Format updated test file"""

    # Determine confidence level
    if confidence_score >= 7.0:
        conf_level = "HIGH"
    elif confidence_score >= 5.0:
        conf_level = "MEDIUM"
    else:
        conf_level = "LOW"

    content = f"""================================================================================
TEST ID: {test_data['test_id']}
FUNCTIONAL AREA: Accounting & Finance
TEST NAME: {test_data['test_name']}
CONFIDENCE: [{conf_level}] Score: {confidence_score:.1f}/10
================================================================================

"""

    if steps:
        content += "ELECTRON STEPS:\n"
        for i, step in enumerate(steps, 1):
            content += f"{i}. {step}\n"
    else:
        content += """ELECTRON STEPS:
[MANUAL TEST - INSUFFICIENT KB COVERAGE]
This test requires SME input to generate valid Electron automation steps.
RAG confidence score was too low (< 5.0).

"""

    content += """
VERIFICATION:
- [ ] Transaction completed successfully
- [ ] No error messages displayed
================================================================================
"""

    return content

def process_file(file_path, rag, dry_run=True):
    """Process a single test file"""
    print(f"\n{'='*80}")
    print(f"Processing: {Path(file_path).name}")

    # Extract task name from filename
    task_name = extract_task_name(file_path)
    if not task_name:
        print(f"  ❌ Could not extract task name from filename")
        return False

    print(f"  Task: {task_name}")

    # Read existing file
    content = read_test_file(file_path)
    test_data = parse_test_file(content)

    # Check if it has placeholder text
    if 'complete required actions' not in content:
        print(f"  ⏭️  SKIP - Already has detailed steps")
        return False

    # Query RAG
    print(f"  🔍 Querying RAG...")
    results = rag.search(task_name, top_k=3)

    if results:
        print(f"  📊 Top RAG score: {results[0]['score']:.1f}")

    # Generate steps
    steps, confidence = generate_electron_steps(task_name, results, test_data['test_id'])

    # Format updated content
    updated_content = format_test_file(test_data, task_name, steps, confidence)

    # Write or preview
    if dry_run:
        print(f"  📝 PREVIEW (confidence: {confidence:.1f}):")
        print("\n" + updated_content[:400] + "..." if len(updated_content) > 400 else updated_content)
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  ✅ Updated (confidence: {confidence:.1f})")

    return True

def main():
    """Main processing function"""
    import argparse

    parser = argparse.ArgumentParser(description='Update Finance test files with RAG-enhanced steps')
    parser.add_argument('--limit', type=int, default=50, help='Max files to process')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--write', action='store_true', help='Actually write files')

    args = parser.parse_args()

    # Initialize RAG
    print("Loading Workday RAG system...")
    rag = WorkdayRAG()

    # Get Finance directory
    finance_dir = Path(__file__).parent / 'electron_tests' / 'Finance'

    # Get all test files
    test_files = sorted(finance_dir.glob('FACC-*.txt'))

    print(f"Found {len(test_files)} Finance test files")
    print(f"Processing limit: {args.limit}")
    print(f"Mode: {'DRY RUN' if args.dry_run or not args.write else 'WRITE'}")

    processed = 0
    updated = 0

    for file_path in test_files[:args.limit]:
        if process_file(file_path, rag, dry_run=(args.dry_run or not args.write)):
            processed += 1
            if not (args.dry_run or not args.write):
                updated += 1

    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  Files processed: {processed}")
    if not (args.dry_run or not args.write):
        print(f"  Files updated: {updated}")
    else:
        print(f"  Mode was DRY RUN - no files written")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
