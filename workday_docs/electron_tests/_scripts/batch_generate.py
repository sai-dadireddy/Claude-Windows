#!/usr/bin/env python3
"""
Batch generate Electron test files for Talent scenarios
"""

import json
import re
from pathlib import Path

# Paths
BASE_DIR = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests")
SCENARIOS_FILE = BASE_DIR / "talent_scenarios.json"

# Output directories
OUTPUT_DIRS = {
    "Talent Acquisition": BASE_DIR / "Talent_Acquisition",
    "Talent Optimization": BASE_DIR / "Talent_Optimization"
}

# Create output directories
for dir_path in OUTPUT_DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)

def sanitize_filename(text, max_length=50):
    """Sanitize text for use in filename"""
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '_', text)
    if len(text) > max_length:
        text = text[:max_length]
    return text.strip('_')

def generate_test_file(scenario):
    """Generate Electron test file for a scenario"""
    lines = []

    # Header
    lines.append(f"# {scenario['scenario_id']}: {scenario['scenario_name']}")
    lines.append(f"# Functional Area: {scenario['functional_area']}")
    lines.append(f"# Test Type: {scenario['test_type']}")
    lines.append(f"# Role: {scenario['workday_role']}")
    lines.append("")

    task = scenario['task_step'].lower() if scenario['task_step'] != 'nan' else ''
    functional_area = scenario['functional_area']

    # Determine confidence based on task clarity
    needs_review = len(task) < 20 or task == '' or 'nan' in task

    if needs_review:
        lines.append("# [NEEDS SME REVIEW - Insufficient task details]")
        lines.append("")

    # Login
    lines.append("# Step 1: Login")
    role = scenario['workday_role'] if scenario['workday_role'] != 'nan' else 'Default User'
    lines.append(f"login|{role}")
    lines.append("")

    # Generate steps based on functional area and task
    if functional_area == "Talent Acquisition":
        lines.extend(generate_talent_acquisition_steps(scenario, task))
    else:  # Talent Optimization
        lines.extend(generate_talent_optimization_steps(scenario, task))

    # Logout
    lines.append("")
    lines.append("# Final Step: Logout")
    lines.append("logout")

    return "\n".join(lines)

def generate_talent_acquisition_steps(scenario, task):
    """Generate Talent Acquisition specific steps"""
    steps = []

    # Security tasks
    if 'security' in task and 'group' in task:
        steps.append("# Step 2: Navigate to Security Administration")
        steps.append("search|View Domain")
        steps.append("click|View Domain")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Security Group Assignments")
        steps.append("filter|User-Based Security Groups")
        steps.append("verify|Security groups display correctly")
        steps.append("")
        steps.append("# Step 4: Export Security Assignments")
        steps.append("click|Export to Excel")
        steps.append("verify|Export completes successfully")

    # Setup/Configuration tasks
    elif 'setup' in task or 'configuration' in task:
        steps.append("# Step 2: Navigate to Setup")
        steps.append("search|Setup")
        steps.append("click|Recruiting Setup")
        steps.append("wait|2")
        steps.append("")
        steps.append(f"# Step 3: Configure {scenario['scenario_name']}")
        steps.append("verify|Configuration options are available")
        steps.append("# [MANUAL: Complete configuration based on requirements]")

    # Job Requisition tasks
    elif 'job' in task or 'requisition' in task:
        steps.append("# Step 2: Navigate to Job Requisitions")
        steps.append("search|Create Job Requisition")
        steps.append("click|Create Job Requisition")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Create/Review Job Requisition")
        steps.append("input|Job Title|Test Position")
        steps.append("verify|Job requisition form displays")

    # Candidate tasks
    elif 'candidate' in task:
        steps.append("# Step 2: Navigate to Candidates")
        steps.append("search|Find Candidates")
        steps.append("click|Find Candidates")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Candidate Information")
        steps.append("filter|Active Candidates")
        steps.append("verify|Candidate list displays")

    # Offer tasks
    elif 'offer' in task:
        steps.append("# Step 2: Navigate to Offers")
        steps.append("search|Create Offer")
        steps.append("click|Create Offer")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Process Offer")
        steps.append("verify|Offer creation form displays")

    # Interview tasks
    elif 'interview' in task:
        steps.append("# Step 2: Navigate to Interviews")
        steps.append("search|Schedule Interview")
        steps.append("click|Schedule Interview")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Schedule Interview")
        steps.append("verify|Interview scheduling form displays")

    # Agency/Source tasks
    elif 'agency' in task or 'source' in task:
        steps.append("# Step 2: Navigate to Recruiting Sources")
        steps.append("search|Recruiting Sources")
        steps.append("click|Manage Recruiting Sources")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Recruiting Sources")
        steps.append("verify|Recruiting sources display")

    # Generic recruiting task
    else:
        steps.append("# Step 2: Navigate to Recruiting")
        steps.append("search|Recruiting")
        steps.append("click|Recruiting")
        steps.append("wait|2")
        steps.append("")
        steps.append(f"# Step 3: {scenario['scenario_name']}")
        if task:
            steps.append(f"# Task: {scenario['task_step'][:100]}")
        steps.append("# [MANUAL: Complete specific recruiting actions]")

    return steps

def generate_talent_optimization_steps(scenario, task):
    """Generate Talent Optimization specific steps"""
    steps = []

    # Performance Review tasks
    if 'performance' in task or 'review' in task:
        steps.append("# Step 2: Navigate to Performance Management")
        steps.append("search|My Performance")
        steps.append("click|My Performance")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Access Performance Review")
        steps.append("click|Performance Review")
        steps.append("verify|Performance review displays")
        steps.append("")
        steps.append("# Step 4: Review Performance Data")
        steps.append("verify|Performance ratings are visible")

    # Goal Management tasks
    elif 'goal' in task:
        steps.append("# Step 2: Navigate to Goals")
        steps.append("search|Goals")
        steps.append("click|My Goals")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Goals")
        steps.append("verify|Goal list displays")
        steps.append("")
        steps.append("# Step 4: Manage Goals")
        steps.append("click|Add Goal")
        steps.append("verify|Goal creation form displays")

    # Career Development tasks
    elif 'career' in task or 'development' in task:
        steps.append("# Step 2: Navigate to Career Development")
        steps.append("search|Career")
        steps.append("click|Career")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Development Plans")
        steps.append("click|Development")
        steps.append("verify|Development items display")

    # Succession Planning tasks
    elif 'succession' in task:
        steps.append("# Step 2: Navigate to Succession Planning")
        steps.append("search|Succession Planning")
        steps.append("click|Succession Planning")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Succession Plans")
        steps.append("verify|Succession plan data displays")

    # Talent Review/Calibration tasks
    elif 'talent review' in task or 'calibration' in task:
        steps.append("# Step 2: Navigate to Talent Review")
        steps.append("search|Talent Review")
        steps.append("click|Talent Review")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Access Talent Review Session")
        steps.append("verify|Talent review interface displays")

    # Feedback tasks
    elif 'feedback' in task:
        steps.append("# Step 2: Navigate to Feedback")
        steps.append("search|Give Feedback")
        steps.append("click|Give Feedback")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Provide Feedback")
        steps.append("verify|Feedback form displays")

    # Competency tasks
    elif 'competenc' in task:
        steps.append("# Step 2: Navigate to Competencies")
        steps.append("search|Competencies")
        steps.append("click|View Competencies")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Competency Profile")
        steps.append("verify|Competency data displays")

    # Generic talent optimization task
    else:
        steps.append("# Step 2: Navigate to Talent")
        steps.append("search|Talent")
        steps.append("click|Talent")
        steps.append("wait|2")
        steps.append("")
        steps.append(f"# Step 3: {scenario['scenario_name']}")
        if task:
            steps.append(f"# Task: {scenario['task_step'][:100]}")
        steps.append("# [MANUAL: Complete specific talent optimization actions]")

    return steps

def main():
    """Main processing function"""
    # Load scenarios
    with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    print(f"Processing {len(scenarios)} scenarios...")

    stats = {
        'total': 0,
        'needs_review': 0,
        'by_area': {}
    }

    for idx, scenario in enumerate(scenarios, 1):
        functional_area = scenario['functional_area']
        scenario_id = scenario['scenario_id']
        scenario_name = scenario['scenario_name']

        print(f"[{idx}/{len(scenarios)}] {scenario_id}: {scenario_name[:50]}...")

        # Generate test content
        test_content = generate_test_file(scenario)

        # Determine output path
        output_dir = OUTPUT_DIRS.get(functional_area)
        if not output_dir:
            print(f"  WARNING: Unknown functional area: {functional_area}")
            continue

        # Create filename
        safe_name = sanitize_filename(scenario_name)
        filename = f"{scenario_id}_{safe_name}.txt"
        output_path = output_dir / filename

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(test_content)

        # Update stats
        stats['total'] += 1
        stats['by_area'][functional_area] = stats['by_area'].get(functional_area, 0) + 1

        if '[NEEDS SME REVIEW' in test_content:
            stats['needs_review'] += 1

    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    print(f"Total scenarios processed: {stats['total']}")
    print(f"Tests needing SME review: {stats['needs_review']}")
    print("\nBy Functional Area:")
    for area, count in sorted(stats['by_area'].items()):
        print(f"  {area}: {count}")
        output_dir = OUTPUT_DIRS[area]
        print(f"    Output: {output_dir}")
    print("="*60)

if __name__ == "__main__":
    main()
