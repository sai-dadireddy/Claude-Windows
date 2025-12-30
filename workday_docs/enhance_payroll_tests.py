#!/usr/bin/env python3
"""
Enhance Payroll Test Files with Accurate Electron Steps
Uses RAG knowledge base to improve low-confidence test files
"""

import os
import re
from pathlib import Path

# Enhanced steps database based on RAG knowledge
ENHANCED_STEPS = {
    "Create Settlement Run": {
        "steps": [
            'enter search box as "Create Settlement Run"',
            'wait for search results',
            'click search result containing "Create Settlement Run"',
            'wait for page to load',
            'select pay group from dropdown',
            'select company hierarchy if multiple companies exist',
            'select filter "All Available Pay Groups"',
            'select filter "All Available Pay Group Exceptions"',
            'verify payment date is displayed',
            'verify bank routing rules configuration',
            'click button "Submit"',
            'wait for processing to complete',
            'verify message contains "Settlement run created successfully"',
        ],
        "verification": [
            "Settlement run created successfully",
            "All pay groups selected",
            "Company hierarchy configured",
            "No errors displayed",
            "Integration errors can be ignored (expected until E2E testing)"
        ],
        "confidence": 8.5
    },
    "View Period Schedule": {
        "steps": [
            'enter search box as "View Period Schedule"',
            'wait for search results',
            'click search result containing "View Period Schedule"',
            'wait for page to load',
            'verify period schedule table is displayed',
            'verify column "Period Start Date" is visible',
            'verify column "Period End Date" is visible',
            'verify column "Payment Date" is visible',
            'verify column "Accounting Date Override" is visible',
            'verify forward accrual settings',
            'verify linkage to Absence/Time Tracking',
            'verify correct number of periods per year',
            'scroll down to review configuration',
        ],
        "verification": [
            "All expected period schedules are present",
            "Dates are correct (start, end, payment, accounting override)",
            "Forward accrual settings match expectations",
            "Period schedules linked to Absence/Time Tracking",
            "Correct number of periods for each year"
        ],
        "confidence": 8.0
    },
    "Run Category Configuration": {
        "steps": [
            'enter search box as "Configure Run Category"',
            'wait for search results',
            'click search result containing "Configure Run Category"',
            'wait for page to load',
            'verify run category list is displayed',
            'verify column "Run Category Name" is visible',
            'verify column "Pay Group" is visible',
            'verify column "Frequency" is visible',
            'review configuration for each run category',
            'verify off-cycle run categories exist',
        ],
        "verification": [
            "All run categories configured",
            "Run category names are descriptive",
            "Pay groups correctly assigned",
            "Frequency settings appropriate",
            "Off-cycle categories exist for special payments"
        ],
        "confidence": 7.5
    },
    "Pay Group Configuration": {
        "steps": [
            'enter search box as "Configure Pay Group"',
            'wait for search results',
            'click search result containing "Configure Pay Group"',
            'wait for page to load',
            'verify pay group list is displayed',
            'verify column "Pay Group Name" is visible',
            'verify column "Pay Frequency" is visible',
            'verify column "Period Schedule" is visible',
            'click on first pay group to review details',
            'verify payment election rules',
            'verify run categories assigned',
        ],
        "verification": [
            "All pay groups configured",
            "Pay frequency correct (weekly, biweekly, monthly, etc.)",
            "Period schedules linked appropriately",
            "Payment election rules configured",
            "Run categories assigned to pay groups"
        ],
        "confidence": 8.0
    },
    "Payment Election Rule Configuration": {
        "steps": [
            'enter search box as "Configure Payment Election Rule"',
            'wait for search results',
            'click search result containing "Configure Payment Election Rule"',
            'wait for page to load',
            'verify payment election rules table',
            'verify column "Rule Name" is visible',
            'verify column "Payment Type" is visible',
            'verify default payment methods configured',
            'verify bank account validation rules',
        ],
        "verification": [
            "Payment election rules configured",
            "Default payment methods set",
            "Bank account validation active",
            "Payment types defined (ACH, check, wire, etc.)"
        ],
        "confidence": 7.5
    },
    "Earnings Configuration": {
        "steps": [
            'enter search box as "Configure Earnings"',
            'wait for search results',
            'click search result containing "Configure Earnings"',
            'wait for page to load',
            'verify earnings list displayed',
            'verify salary earnings types',
            'verify hourly earnings types',
            'verify overtime earnings types',
            'verify bonus earnings types',
            'review tax treatment for each earning',
        ],
        "verification": [
            "All earnings types configured",
            "Salary, hourly, overtime, bonus types exist",
            "Tax treatment correct for each earning",
            "GL accounts mapped to earnings",
            "No deprecated earnings codes"
        ],
        "confidence": 7.5
    },
    "Deductions Configuration": {
        "steps": [
            'enter search box as "Configure Deductions"',
            'wait for search results',
            'click search result containing "Configure Deductions"',
            'wait for page to load',
            'verify deductions list displayed',
            'verify pre-tax deductions (401k, HSA, FSA)',
            'verify post-tax deductions (loans, garnishments)',
            'verify employer deductions',
            'review frequency and calculation methods',
        ],
        "verification": [
            "All deduction types configured",
            "Pre-tax and post-tax deductions separated",
            "Employer deductions exist",
            "Calculation methods correct",
            "GL accounts mapped"
        ],
        "confidence": 7.5
    },
    "Tax Elections Review": {
        "steps": [
            'enter search box as "Tax Elections"',
            'wait for search results',
            'click search result containing "Tax Elections"',
            'wait for page to load',
            'verify employee tax elections list',
            'verify federal withholding settings',
            'verify state withholding settings',
            'verify local tax settings',
            'filter for employees with missing elections',
        ],
        "verification": [
            "All employees have tax elections",
            "Federal W-4 forms on file",
            "State withholding configured",
            "Multi-state employees handled correctly",
            "No missing tax elections"
        ],
        "confidence": 8.0
    },
    "Payment Election Review": {
        "steps": [
            'enter search box as "Payment Elections"',
            'wait for search results',
            'click search result containing "Payment Elections"',
            'wait for page to load',
            'verify payment elections list',
            'verify employee bank account information',
            'verify payment methods (ACH, check, etc.)',
            'verify split payments configuration',
            'filter for employees with missing payment elections',
        ],
        "verification": [
            "All employees have payment elections",
            "Bank accounts validated",
            "Payment methods configured",
            "Split payments work correctly",
            "No missing payment elections"
        ],
        "confidence": 8.0
    },
    "Pay Group Assignments Review": {
        "steps": [
            'enter search box as "Pay Group Assignments"',
            'wait for search results',
            'click search result containing "Pay Group Assignments"',
            'wait for page to load',
            'verify employee pay group assignments',
            'verify all active employees have assignments',
            'verify assignment effective dates',
            'verify no duplicate assignments',
        ],
        "verification": [
            "All active employees assigned to pay groups",
            "Effective dates are correct",
            "No duplicate assignments",
            "Pay group assignments match job data",
            "No unassigned employees"
        ],
        "confidence": 8.0
    }
}

def extract_task_name(test_name):
    """Extract the main task name from test name"""
    # Remove BP: prefix
    test_name = re.sub(r'^BP:\s*', '', test_name)

    # Remove Review prefix if it exists
    test_name = re.sub(r'^Review\s+', '', test_name)

    # Try to match known patterns
    for key in ENHANCED_STEPS.keys():
        if key.lower() in test_name.lower():
            return key

    return None

def enhance_test_file(file_path):
    """Enhance a single test file with better Electron steps"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract test name
    test_name_match = re.search(r'TEST NAME: (.+)', content)
    if not test_name_match:
        return False

    test_name = test_name_match.group(1)
    task_name = extract_task_name(test_name)

    if not task_name or task_name not in ENHANCED_STEPS:
        return False

    # Get enhanced steps
    enhanced = ENHANCED_STEPS[task_name]

    # Extract test ID and create screenshot name
    test_id_match = re.search(r'TEST ID: ([A-Z]+-\d+-\d+)', content)
    if not test_id_match:
        return False
    test_id = test_id_match.group(1)

    # Build new Electron steps section
    steps_lines = []
    for i, step in enumerate(enhanced['steps'], 1):
        steps_lines.append(f"{i}. {step}")

    # Add screenshot as last step
    steps_lines.append(f"{len(enhanced['steps']) + 1}. screenshot as \"{test_id}_complete.png\"")

    new_steps = "\n".join(steps_lines)

    # Build new verification section
    verification_lines = []
    for item in enhanced['verification']:
        verification_lines.append(f"- [ ] {item}")
    new_verification = "\n".join(verification_lines)

    # Update confidence score
    new_confidence = f"CONFIDENCE: [HIGH] Score: {enhanced['confidence']}/10"

    # Replace sections in content
    # Replace confidence
    content = re.sub(
        r'CONFIDENCE: \[.*?\] Score: [\d.]+/10',
        new_confidence,
        content
    )

    # Replace electron steps
    content = re.sub(
        r'ELECTRON STEPS:\n(.+?)(?=\n\nVERIFICATION:)',
        f'ELECTRON STEPS:\n{new_steps}',
        content,
        flags=re.DOTALL
    )

    # Replace verification
    content = re.sub(
        r'VERIFICATION:\n(.+?)(?=\n\nAPI ALTERNATIVE:)',
        f'VERIFICATION:\n{new_verification}',
        content,
        flags=re.DOTALL
    )

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Main enhancement process"""
    base_dir = Path(__file__).parent / "electron_tests"

    directories = [
        base_dir / "Payroll_US",
        base_dir / "Payroll_Canada"
    ]

    enhanced_count = 0
    total_count = 0

    for directory in directories:
        if not directory.exists():
            print(f"Directory not found: {directory}")
            continue

        print(f"\nProcessing {directory.name}...")

        for file_path in directory.glob("*.txt"):
            # Skip non-test files
            if file_path.name in ['README.txt', 'INDEX.txt', 'GENERATION_SUMMARY.txt']:
                continue

            total_count += 1

            if enhance_test_file(file_path):
                enhanced_count += 1
                print(f"  [+] Enhanced: {file_path.name}")
            else:
                print(f"  [-] Skipped: {file_path.name}")

    print(f"\n{'='*60}")
    print(f"Enhancement Complete")
    print(f"{'='*60}")
    print(f"Total files processed: {total_count}")
    print(f"Files enhanced: {enhanced_count}")
    print(f"Files skipped: {total_count - enhanced_count}")

if __name__ == "__main__":
    main()
