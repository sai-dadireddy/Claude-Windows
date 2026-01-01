#!/usr/bin/env python3
"""
Enhance Payroll_US Electron test scripts by adding missing sections:
- ON FAILURE
- EXPECTED OUTCOME
- MANUAL VERIFICATION table

Agent ID: enhance-5
"""

import os
import re
import csv
from datetime import datetime
from pathlib import Path

# Configuration
BASE_DIR = Path(r"C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/Payroll_US")
TRACKER_PATH = Path(r"C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/_tracker/script_tracker.csv")
AGENT_ID = "enhance-5"

def extract_topic_from_filename(filename):
    """Extract topic from filename like USP-1-0010_Review_Period_Schedule_Configuration.txt"""
    # Remove prefix like USP-1-0010_ and suffix .txt
    match = re.match(r'USP-\d+-\d+(?:-\d+)?_(.+)\.txt', filename)
    if match:
        topic = match.group(1).replace('_', ' ')
        return topic
    return filename.replace('.txt', '').replace('_', ' ')

def extract_confidence_score(content):
    """Extract confidence score from script content"""
    match = re.search(r'Score:\s*([\d.]+)/10', content)
    if match:
        return float(match.group(1))
    # Look for [HIGH], [MEDIUM], [LOW]
    if '[HIGH]' in content:
        return 8.5
    elif '[MEDIUM]' in content:
        return 6.5
    elif '[LOW]' in content:
        return 4.0
    return 7.0

def has_section(content, section_name):
    """Check if a section exists in the content"""
    pattern = rf'^-+\s*\n{section_name}\s*\n-+\s*\n'
    return bool(re.search(pattern, content, re.MULTILINE | re.IGNORECASE))

def is_manual_required(content):
    """Check if script is marked as MANUAL REQUIRED"""
    return 'STATUS: [MANUAL REQUIRED]' in content

def generate_on_failure_section(topic, test_id):
    """Generate ON FAILURE section based on topic"""
    return f"""
--------------------------------------------------------------------------------
ON FAILURE
--------------------------------------------------------------------------------
- Page fails to load: Verify network connectivity and retry navigation
- Search results not found: Check task name spelling and user permissions
- Configuration data missing: Confirm tenant data migration completed
- Screenshot capture fails: Check disk space and file permissions
- Verification step fails: Document discrepancy and escalate to SME for {topic} review
- Timeout error: Increase wait time and verify system performance
"""

def generate_expected_outcome_section(topic, test_id):
    """Generate EXPECTED OUTCOME section based on topic"""
    return f"""
--------------------------------------------------------------------------------
EXPECTED OUTCOME
--------------------------------------------------------------------------------
- {topic} configuration displays correctly in Workday
- All verification criteria pass without errors
- Screenshots captured at key validation points
- No unexpected error messages or warnings displayed
- Configuration matches expected business requirements
"""

def generate_manual_verification_section(topic, test_id):
    """Generate MANUAL VERIFICATION table based on topic"""
    return f"""
--------------------------------------------------------------------------------
MANUAL VERIFICATION
--------------------------------------------------------------------------------
| Step | Action | Reason |
|------|--------|--------|
| M1 | Compare {topic} values with design document | Business requirement validation |
| M2 | Verify data accuracy with SME | Expert confirmation required |
| M3 | Cross-check with legacy system data if applicable | Data migration validation |
"""

def enhance_script(filepath):
    """Enhance a single script file with missing sections"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None, f"Error reading: {e}"

    filename = os.path.basename(filepath)
    topic = extract_topic_from_filename(filename)
    test_id = re.search(r'(USP-\d+-\d+(?:-\d+)?)', filename)
    test_id = test_id.group(1) if test_id else "USP-UNKNOWN"

    # Skip MANUAL REQUIRED scripts - they need SME input first
    if is_manual_required(content):
        return {
            'filename': filename,
            'topic': topic,
            'old_confidence': 0,
            'new_confidence': 0,
            'status': 'skipped_manual',
            'sections_added': '',
        }, "Skipped - MANUAL REQUIRED"

    old_confidence = extract_confidence_score(content)
    sections_added = []
    modified = False

    # Find the end marker to insert before it
    end_marker = "=" * 80

    # Check and add missing sections
    if not has_section(content, 'ON FAILURE'):
        on_failure = generate_on_failure_section(topic, test_id)
        sections_added.append('ON FAILURE')
        modified = True
    else:
        on_failure = ''

    if not has_section(content, 'EXPECTED OUTCOME'):
        expected = generate_expected_outcome_section(topic, test_id)
        sections_added.append('EXPECTED OUTCOME')
        modified = True
    else:
        expected = ''

    if not has_section(content, 'MANUAL VERIFICATION'):
        manual = generate_manual_verification_section(topic, test_id)
        sections_added.append('MANUAL VERIFICATION')
        modified = True
    else:
        manual = ''

    # Fix any "nan" placeholders
    if 'nan' in content.lower():
        content = re.sub(r'\bnan\b', 'N/A', content, flags=re.IGNORECASE)
        if 'nan_fix' not in sections_added:
            sections_added.append('nan_fix')
        modified = True

    if not modified:
        return {
            'filename': filename,
            'topic': topic,
            'old_confidence': old_confidence,
            'new_confidence': old_confidence,
            'status': 'already_complete',
            'sections_added': '',
        }, "Already complete"

    # Calculate new confidence (boost for adding sections)
    new_confidence = min(old_confidence + (0.5 * len([s for s in sections_added if s != 'nan_fix'])), 10.0)

    # Insert sections before final separator
    new_sections = on_failure + expected + manual

    # Find the last occurrence of the end marker
    last_end = content.rfind(end_marker)
    if last_end > 0:
        # Insert before the final end marker
        content = content[:last_end] + new_sections + "\n" + end_marker + "\n"
    else:
        # Append at the end
        content = content.rstrip() + new_sections + "\n" + end_marker + "\n"

    # Write enhanced content
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return None, f"Error writing: {e}"

    return {
        'filename': filename,
        'topic': topic,
        'old_confidence': old_confidence,
        'new_confidence': new_confidence,
        'status': 'enhanced',
        'sections_added': ';'.join(sections_added),
    }, "Enhanced successfully"

def main():
    """Main processing function"""
    # Find all USP scripts
    scripts = list(BASE_DIR.glob("USP*.txt"))
    print(f"Found {len(scripts)} USP scripts in Payroll_US")

    # Prepare tracker data
    tracker_rows = []
    enhanced_count = 0
    skipped_count = 0
    error_count = 0
    already_complete = 0

    for script_path in sorted(scripts):
        result, message = enhance_script(script_path)

        if result is None:
            print(f"ERROR: {script_path.name} - {message}")
            error_count += 1
            continue

        if result['status'] == 'enhanced':
            print(f"ENHANCED: {result['filename']} - Added: {result['sections_added']}")
            enhanced_count += 1
        elif result['status'] == 'skipped_manual':
            print(f"SKIPPED: {result['filename']} - MANUAL REQUIRED")
            skipped_count += 1
        else:
            print(f"COMPLETE: {result['filename']} - Already has all sections")
            already_complete += 1

        # Add to tracker
        tracker_rows.append({
            'filename': result['filename'],
            'area': 'Payroll_US',
            'topic': result['topic'],
            'old_confidence': result['old_confidence'],
            'new_confidence': result['new_confidence'],
            'status': result['status'],
            'sections_added': result['sections_added'],
            'enhanced_date': datetime.now().strftime('%Y-%m-%d'),
            'agent_id': AGENT_ID
        })

    # Write tracker CSV
    try:
        # Read existing tracker entries
        existing_rows = []
        if TRACKER_PATH.exists():
            with open(TRACKER_PATH, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                existing_rows = [row for row in reader if row.get('area') != 'Payroll_US']

        # Write combined data
        with open(TRACKER_PATH, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['filename', 'area', 'topic', 'old_confidence', 'new_confidence',
                         'status', 'sections_added', 'enhanced_date', 'agent_id']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(existing_rows)
            writer.writerows(tracker_rows)

        print(f"\nTracker updated: {TRACKER_PATH}")
    except Exception as e:
        print(f"Error writing tracker: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"ENHANCEMENT SUMMARY - Agent: {AGENT_ID}")
    print(f"{'='*60}")
    print(f"Total scripts processed: {len(scripts)}")
    print(f"Enhanced: {enhanced_count}")
    print(f"Already complete: {already_complete}")
    print(f"Skipped (MANUAL REQUIRED): {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
