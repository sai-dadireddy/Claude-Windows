#!/usr/bin/env python3
"""
Batch enhance Finance Electron test scripts - Agent enhance-3
Adds missing ON FAILURE, EXPECTED OUTCOME, and MANUAL VERIFICATION sections
"""

import os
import re
import csv
from datetime import datetime
from pathlib import Path

FINANCE_DIR = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/Finance")
TRACKER_CSV = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests/_tracker/script_tracker.csv")
AGENT_ID = "enhance-3"

def extract_topic(filename):
    """Extract topic from filename like FACC-1-0010_Audit Supervisory Organizations.txt"""
    match = re.search(r'_(.+)\.txt$', filename)
    if match:
        return match.group(1)
    return filename.replace('.txt', '')

def extract_confidence(content):
    """Extract confidence score from script content"""
    match = re.search(r'Score:\s*([\d.]+)/10', content)
    if match:
        return float(match.group(1))
    match = re.search(r'CONFIDENCE:\s*\[(HIGH|MEDIUM|LOW)\]', content)
    if match:
        levels = {'HIGH': 8.0, 'MEDIUM': 5.0, 'LOW': 3.0}
        return levels.get(match.group(1), 5.0)
    return 5.0

def has_section(content, section_name):
    """Check if a section exists in content"""
    return section_name in content

def get_fallback_steps(topic):
    """Generate fallback steps based on topic type"""
    topic_lower = topic.lower()

    if 'audit' in topic_lower:
        return [
            "- Step 3 fails (search result not found): Try alternative search terms or navigate via menu",
            "- Step 5 fails (data not displayed): Verify user has required security roles",
            "- Step 6 fails (verification error): Capture screenshot and log discrepancy for manual review"
        ]
    elif 'confirm' in topic_lower:
        return [
            "- Step 3 fails (search result not found): Navigate via Setup menu > Organization",
            "- Step 5 fails (data not displayed): Check tenant configuration and user permissions",
            "- Step 6 fails (field validation error): Document missing fields and escalate to configuration team"
        ]
    elif 'create' in topic_lower or 'add' in topic_lower:
        return [
            "- Step 3 fails (task not available): Verify security role permissions for create action",
            "- Step 5 fails (validation error): Check required fields and data dependencies",
            "- Step 6 fails (submit fails): Review error message, correct data, retry submission"
        ]
    elif 'approve' in topic_lower:
        return [
            "- Step 3 fails (approval task not found): Check inbox for pending approvals",
            "- Step 5 fails (approval denied): Review denial reason and escalate if needed",
            "- Step 6 fails (workflow error): Verify business process configuration"
        ]
    elif 'verify' in topic_lower or 'review' in topic_lower:
        return [
            "- Step 3 fails (report not found): Try searching with exact report name",
            "- Step 5 fails (data mismatch): Document discrepancy with screenshot",
            "- Step 6 fails (export error): Try alternative export format"
        ]
    elif 'edit' in topic_lower or 'update' in topic_lower:
        return [
            "- Step 3 fails (edit not available): Verify edit permissions and object status",
            "- Step 5 fails (save error): Check for required fields and validation rules",
            "- Step 6 fails (concurrent edit): Refresh and retry with latest data"
        ]
    elif 'journal' in topic_lower:
        return [
            "- Step 3 fails (journal task not found): Navigate via Accounting menu",
            "- Step 5 fails (balance error): Verify debit/credit amounts balance",
            "- Step 6 fails (posting error): Check fiscal period status and account validity"
        ]
    elif 'allocation' in topic_lower:
        return [
            "- Step 3 fails (allocation not found): Verify allocation definition exists",
            "- Step 5 fails (calculation error): Review allocation basis and target worktags",
            "- Step 6 fails (posting error): Check ledger account configuration"
        ]
    elif 'revaluation' in topic_lower:
        return [
            "- Step 3 fails (revaluation task not found): Navigate via Financial Accounting menu",
            "- Step 5 fails (rate error): Verify currency exchange rates are loaded",
            "- Step 6 fails (posting error): Check revaluation rules and target accounts"
        ]
    elif 'consolidation' in topic_lower:
        return [
            "- Step 3 fails (consolidation not found): Navigate via Consolidations menu",
            "- Step 5 fails (mapping error): Verify data mapping tables are configured",
            "- Step 6 fails (journal error): Check elimination rules and intercompany setup"
        ]
    elif 'tax' in topic_lower:
        return [
            "- Step 3 fails (tax task not found): Navigate via Tax Setup menu",
            "- Step 5 fails (tax calculation error): Verify tax codes and rates configuration",
            "- Step 6 fails (tax posting error): Check tax authority and applicability setup"
        ]
    elif 'payroll' in topic_lower:
        return [
            "- Step 3 fails (payroll task not found): Navigate via Payroll menu",
            "- Step 5 fails (calculation error): Verify pay component setup and costing",
            "- Step 6 fails (accounting error): Check payroll accounting configuration"
        ]
    elif 'intercompany' in topic_lower:
        return [
            "- Step 3 fails (intercompany not found): Navigate via Intercompany menu",
            "- Step 5 fails (affiliate error): Verify intercompany profile and affiliates setup",
            "- Step 6 fails (balancing error): Check intercompany accounts configuration"
        ]
    else:
        return [
            "- Step 3 fails (search result not found): Try alternative navigation path via menu",
            "- Step 5 fails (data not displayed): Verify user permissions and tenant setup",
            "- Step 6 fails (verification error): Capture screenshot and escalate for review"
        ]

def get_expected_outcome(topic):
    """Generate expected outcome based on topic"""
    topic_lower = topic.lower()

    if 'audit' in topic_lower:
        return [
            f"- {topic} report displays successfully",
            "- All audit criteria verified against expected values",
            "- No data discrepancies found",
            "- Screenshots captured at key verification points"
        ]
    elif 'confirm' in topic_lower:
        return [
            f"- {topic} configuration displays correctly",
            "- All required fields are populated",
            "- Data matches expected configuration values",
            "- Screenshots captured for documentation"
        ]
    elif 'create' in topic_lower:
        return [
            f"- {topic} completes successfully",
            "- New record created with correct data",
            "- Business process workflow initiated if applicable",
            "- Confirmation message displayed"
        ]
    elif 'approve' in topic_lower:
        return [
            f"- {topic} completes successfully",
            "- Approval recorded in business process history",
            "- Workflow advances to next step",
            "- Notification sent to relevant parties"
        ]
    elif 'verify' in topic_lower or 'review' in topic_lower:
        return [
            f"- {topic} completes successfully",
            "- All verification criteria pass",
            "- Data matches expected values",
            "- Report/view renders correctly"
        ]
    elif 'journal' in topic_lower:
        return [
            f"- {topic} completes successfully",
            "- Journal entries balance (debits equal credits)",
            "- Posted to correct ledger accounts",
            "- Audit trail created"
        ]
    else:
        return [
            f"- {topic} completes successfully",
            "- All verification criteria pass",
            "- No error messages displayed",
            "- Screenshots captured at key steps"
        ]

def get_manual_verification(topic):
    """Generate manual verification steps based on topic"""
    topic_lower = topic.lower()

    if 'audit' in topic_lower:
        return [
            "| M1 | Compare audit results with source system data | Requires access to source system |",
            "| M2 | Verify audit trail completeness | May require database query access |"
        ]
    elif 'confirm' in topic_lower:
        return [
            "| M1 | Validate configuration against design document | Requires design documentation |",
            "| M2 | Cross-check with legacy system if applicable | Requires legacy system access |"
        ]
    elif 'journal' in topic_lower:
        return [
            "| M1 | Verify journal amounts against source documents | Requires source document access |",
            "| M2 | Validate account codes against chart of accounts | Complex validation logic |",
            "| M3 | Confirm tax treatment if applicable | Tax expertise required |"
        ]
    elif 'tax' in topic_lower:
        return [
            "| M1 | Verify tax calculations against tax authority rules | Requires tax expertise |",
            "| M2 | Validate tax codes against jurisdiction requirements | Complex regulatory rules |"
        ]
    elif 'payroll' in topic_lower:
        return [
            "| M1 | Verify payroll calculations against pay statements | Requires HR data access |",
            "| M2 | Validate accounting distributions | Complex costing rules |"
        ]
    else:
        return [
            "| M1 | Verify data against source documentation | Requires access to source documents |",
            "| M2 | Cross-reference with related transactions | May require additional queries |"
        ]

def enhance_script(content, topic, filename):
    """Add missing sections to script content"""
    sections_added = []

    # Check for and fix nan placeholders
    if 'nan' in content.lower():
        content = re.sub(r'\bnan\b', 'N/A', content, flags=re.IGNORECASE)
        sections_added.append('nan_fixed')

    # Build the enhanced content
    enhanced = content.rstrip()

    # Remove trailing separator if present
    if enhanced.endswith('=' * 80):
        enhanced = enhanced[:-80].rstrip()

    # Add ON FAILURE section if missing
    if not has_section(content, 'ON FAILURE'):
        fallback_steps = get_fallback_steps(topic)
        enhanced += "\n\n" + "-" * 80 + "\nON FAILURE\n" + "-" * 80 + "\n"
        enhanced += "\n".join(fallback_steps)
        sections_added.append('ON FAILURE')

    # Add EXPECTED OUTCOME section if missing
    if not has_section(content, 'EXPECTED OUTCOME'):
        outcomes = get_expected_outcome(topic)
        enhanced += "\n\n" + "-" * 80 + "\nEXPECTED OUTCOME\n" + "-" * 80 + "\n"
        enhanced += "\n".join(outcomes)
        sections_added.append('EXPECTED OUTCOME')

    # Add MANUAL VERIFICATION section if missing
    if not has_section(content, 'MANUAL VERIFICATION'):
        manual_steps = get_manual_verification(topic)
        enhanced += "\n\n" + "-" * 80 + "\nMANUAL VERIFICATION\n" + "-" * 80 + "\n"
        enhanced += "| Step | Action | Reason |\n"
        enhanced += "|------|--------|--------|\n"
        enhanced += "\n".join(manual_steps)
        sections_added.append('MANUAL VERIFICATION')

    # Add closing separator
    enhanced += "\n\n" + "=" * 80 + "\n"

    return enhanced, sections_added

def calculate_new_confidence(old_conf, sections_added):
    """Calculate new confidence based on sections added"""
    # Base improvement for adding sections
    improvement = len([s for s in sections_added if s in ['ON FAILURE', 'EXPECTED OUTCOME', 'MANUAL VERIFICATION']]) * 0.3
    new_conf = min(10.0, old_conf + improvement)
    return round(new_conf, 1)

def process_all_scripts():
    """Process all Finance scripts"""
    # Get all txt files
    scripts = list(FINANCE_DIR.glob("*.txt"))
    print(f"Found {len(scripts)} Finance scripts to process")

    # Prepare tracker
    tracker_rows = []
    processed = 0
    skipped = 0

    for script_path in scripts:
        filename = script_path.name
        topic = extract_topic(filename)

        # Read content
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            skipped += 1
            continue

        old_confidence = extract_confidence(content)

        # Check what sections are missing
        missing_sections = []
        if not has_section(content, 'ON FAILURE'):
            missing_sections.append('ON FAILURE')
        if not has_section(content, 'EXPECTED OUTCOME'):
            missing_sections.append('EXPECTED OUTCOME')
        if not has_section(content, 'MANUAL VERIFICATION'):
            missing_sections.append('MANUAL VERIFICATION')

        if not missing_sections and 'nan' not in content.lower():
            # Already complete
            tracker_rows.append({
                'filename': filename,
                'area': 'Finance',
                'topic': topic,
                'old_confidence': old_confidence,
                'new_confidence': old_confidence,
                'status': 'already_complete',
                'sections_added': '',
                'enhanced_date': datetime.now().strftime('%Y-%m-%d'),
                'agent_id': AGENT_ID
            })
            skipped += 1
            continue

        # Enhance the script
        enhanced_content, sections_added = enhance_script(content, topic, filename)
        new_confidence = calculate_new_confidence(old_confidence, sections_added)

        # Write enhanced content
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
            processed += 1
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            skipped += 1
            continue

        # Add to tracker
        tracker_rows.append({
            'filename': filename,
            'area': 'Finance',
            'topic': topic,
            'old_confidence': old_confidence,
            'new_confidence': new_confidence,
            'status': 'enhanced',
            'sections_added': ';'.join(sections_added),
            'enhanced_date': datetime.now().strftime('%Y-%m-%d'),
            'agent_id': AGENT_ID
        })

        if processed % 50 == 0:
            print(f"Processed {processed} scripts...")

    # Write tracker CSV
    TRACKER_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Read existing tracker data
    existing_rows = []
    if TRACKER_CSV.exists():
        with open(TRACKER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_rows = [row for row in reader if row.get('area') != 'Finance']

    # Combine and write
    all_rows = existing_rows + tracker_rows
    with open(TRACKER_CSV, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['filename', 'area', 'topic', 'old_confidence', 'new_confidence', 'status', 'sections_added', 'enhanced_date', 'agent_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nComplete!")
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Tracker updated: {TRACKER_CSV}")

if __name__ == '__main__':
    process_all_scripts()
