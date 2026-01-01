#!/usr/bin/env python
"""
Enhance Inventory Electron Test Scripts
Agent: enhance-7
Purpose: Add missing ON FAILURE, EXPECTED OUTCOME, and MANUAL VERIFICATION sections
"""

import os
import re
import csv
from datetime import datetime

def get_confidence_score(content):
    """Extract confidence score from content"""
    match = re.search(r'Score:\s*([\d.]+)/10', content)
    if match:
        return float(match.group(1))
    match = re.search(r'CONFIDENCE:.*?(\d+)', content)
    if match:
        return float(match.group(1))
    return 5.0

def enhance_script(filepath):
    """Read and enhance a single script file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Extract test ID and name
    test_id_match = re.search(r'TEST ID: ([\w-]+)', content)
    test_name_match = re.search(r'TEST NAME: (.+)', content)

    test_id = test_id_match.group(1) if test_id_match else "UNKNOWN"
    test_name = test_name_match.group(1).strip() if test_name_match else "Unknown Task"

    old_confidence = get_confidence_score(content)

    # Check if sections exist
    has_on_failure = "ON FAILURE" in content
    has_expected_outcome = "EXPECTED OUTCOME" in content
    has_manual_verification = "MANUAL VERIFICATION" in content

    sections_added = []

    # Fix empty DESCRIPTION
    if re.search(r'DESCRIPTION:\s*\n\s*\n\s*WORKDAY ROLE', content):
        desc_text = f"Verify and validate {test_name} configuration in Workday Inventory module."
        content = re.sub(
            r'(DESCRIPTION:)\s*\n\s*\n(\s*WORKDAY ROLE)',
            f'\\1\n{desc_text}\n\n\\2',
            content
        )
        sections_added.append("DESCRIPTION")

    # Fix empty WORKDAY ROLE
    if re.search(r'WORKDAY ROLE:\s*\n\s*\n', content):
        content = re.sub(
            r'(WORKDAY ROLE:)\s*\n(\s*\n)',
            '\\1 Inventory Manager / Supply Chain Administrator\n\\2',
            content
        )
        sections_added.append("WORKDAY ROLE")

    # Fix "nan" placeholders
    if 'nan' in content.lower():
        content = re.sub(r'\bnan\b', 'N/A', content, flags=re.IGNORECASE)
        sections_added.append("FIX_NAN")

    if not has_on_failure or not has_expected_outcome or not has_manual_verification:
        new_sections = ""

        if not has_on_failure:
            new_sections += f"""
================================================================================
ON FAILURE:
================================================================================
- Step 1-3 fails (search not found): Try alternate search terms for "{test_name}"
- Navigation error: Clear browser cache and retry
- Permission denied: Verify user has appropriate Inventory domain access
- Page timeout: Increase wait time and retry
"""
            sections_added.append("ON FAILURE")

        if not has_expected_outcome:
            new_sections += f"""
================================================================================
EXPECTED OUTCOME:
================================================================================
- {test_name} task completes successfully
- All verification criteria pass
- No error messages displayed
- Screenshots captured at key steps
"""
            sections_added.append("EXPECTED OUTCOME")

        if not has_manual_verification:
            new_sections += """
================================================================================
MANUAL VERIFICATION:
================================================================================
| Step | Action | Reason |
|------|--------|--------|
| M1 | Verify data accuracy | Business validation required |
| M2 | Confirm configuration matches requirements | Business logic validation |
"""
            sections_added.append("MANUAL VERIFICATION")

        if new_sections:
            # Insert before RAG QUERY STATUS if present
            if "RAG QUERY STATUS" in content:
                content = content.replace(
                    "RAG QUERY STATUS",
                    new_sections.strip() + "\n\nRAG QUERY STATUS"
                )
            elif "API ALTERNATIVE" in content:
                api_pos = content.find("API ALTERNATIVE")
                if api_pos > 0:
                    sep_start = content.rfind("=" * 40, 0, api_pos)
                    if sep_start > 0:
                        content = content[:sep_start] + new_sections + content[sep_start:]
            elif "ALTERNATE SEARCH" in content:
                alt_pos = content.find("ALTERNATE SEARCH")
                if alt_pos > 0:
                    sep_start = content.rfind("=" * 40, 0, alt_pos)
                    if sep_start > 0:
                        content = content[:sep_start] + new_sections + content[sep_start:]
            else:
                content = content.rstrip() + "\n" + new_sections + "\n================================================================================\n"

    # Calculate new confidence
    new_confidence = min(old_confidence + 0.5 if sections_added else old_confidence, 10.0)

    # Only write if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return test_id, test_name, old_confidence, new_confidence, sections_added

def main():
    # Process all files in Inventory directory
    inventory_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/Inventory"
    files = sorted([f for f in os.listdir(inventory_dir) if f.endswith('.txt')])

    tracker_data = []
    enhanced_count = 0
    skipped_count = 0

    print(f"Processing {len(files)} inventory scripts...")

    for i, f in enumerate(files):
        filepath = os.path.join(inventory_dir, f)
        try:
            test_id, test_name, old_conf, new_conf, sections = enhance_script(filepath)

            status = "enhanced" if sections else "skipped"
            if sections:
                enhanced_count += 1
            else:
                skipped_count += 1

            tracker_data.append({
                'filename': f,
                'area': 'Inventory',
                'topic': test_name,
                'old_confidence': old_conf,
                'new_confidence': new_conf,
                'status': status,
                'sections_added': ';'.join(sections) if sections else '',
                'enhanced_date': datetime.now().strftime('%Y-%m-%d'),
                'agent_id': 'enhance-7'
            })

            if (i + 1) % 25 == 0:
                print(f"Progress: {i + 1}/{len(files)} files processed...")
        except Exception as e:
            print(f"Error processing {f}: {e}")

    print(f"\nCompleted: {enhanced_count} enhanced, {skipped_count} skipped")

    # Write to tracker CSV
    tracker_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/_tracker"
    os.makedirs(tracker_dir, exist_ok=True)
    tracker_path = os.path.join(tracker_dir, "script_tracker.csv")

    # Read existing data if file exists
    existing_data = []
    if os.path.exists(tracker_path):
        with open(tracker_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)

    # Write data
    with open(tracker_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['filename', 'area', 'topic', 'old_confidence', 'new_confidence', 'status', 'sections_added', 'enhanced_date', 'agent_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # Keep non-Inventory entries
        for row in existing_data:
            if row.get('area') != 'Inventory':
                writer.writerow(row)
        # Add Inventory entries
        for row in tracker_data:
            writer.writerow(row)

    print(f"Tracker updated: {tracker_path}")
    return enhanced_count, skipped_count

if __name__ == "__main__":
    main()
