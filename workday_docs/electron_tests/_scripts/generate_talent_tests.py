#!/usr/bin/env python3
"""
Generate Electron test files for Talent Acquisition and Talent Optimization scenarios
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Paths
BASE_DIR = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests")
RAG_SCRIPT = Path("C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/workday_rag.py")
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
    # Remove special characters
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces with underscores
    text = re.sub(r'\s+', '_', text)
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    return text.strip('_')

def query_rag(query_text):
    """Query Workday RAG for information"""
    try:
        result = subprocess.run(
            ['python', str(RAG_SCRIPT), query_text],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout
    except Exception as e:
        return f"ERROR: {str(e)}"

def calculate_confidence(rag_response, scenario):
    """Calculate confidence score based on RAG response quality"""
    score = 5.0  # Base score

    response_lower = rag_response.lower()

    # High confidence indicators
    if 'business process' in response_lower:
        score += 1.5
    if 'report' in response_lower or 'task' in response_lower:
        score += 1.0
    if 'security' in response_lower and 'security' in scenario['task_step'].lower():
        score += 1.0
    if 'recruitment' in response_lower or 'candidate' in response_lower:
        score += 0.5
    if 'performance' in response_lower or 'goal' in response_lower:
        score += 0.5

    # Low confidence indicators
    if 'error' in response_lower:
        score -= 3.0
    if len(rag_response) < 100:
        score -= 2.0
    if 'no results' in response_lower:
        score -= 2.0

    return min(10.0, max(0.0, score))

def generate_electron_steps(scenario, rag_response, confidence):
    """Generate Electron test steps based on scenario and RAG data"""
    steps = []

    task = scenario['task_step']
    functional_area = scenario['functional_area']

    # Header
    steps.append(f"# {scenario['scenario_id']}: {scenario['scenario_name']}")
    steps.append(f"# Functional Area: {functional_area}")
    steps.append(f"# Confidence: {confidence:.1f}/10.0")
    steps.append("")

    if confidence < 5.0:
        steps.append("# [MANUAL TEST - LOW CONFIDENCE]")
        steps.append(f"# Reason: Insufficient RAG data for automated generation")
        steps.append(f"# Task: {task}")
        steps.append("")
        steps.append("# Please create manual test steps based on:")
        steps.append(f"# - Scenario: {scenario['scenario_name']}")
        steps.append(f"# - Role: {scenario['workday_role']}")
        steps.append(f"# - Expected: {scenario['expected_result']}")
        return "\n".join(steps)

    if confidence < 7.0:
        steps.append("# [NEEDS SME REVIEW]")
        steps.append("# This test was generated with medium confidence and requires validation")
        steps.append("")

    # Login
    steps.append("# Step 1: Login")
    steps.append(f"login|{scenario['workday_role']}")
    steps.append("")

    # Task-specific steps based on functional area
    if functional_area == "Talent Acquisition":
        steps.extend(generate_talent_acquisition_steps(scenario, rag_response))
    else:  # Talent Optimization
        steps.extend(generate_talent_optimization_steps(scenario, rag_response))

    # Logout
    steps.append("")
    steps.append("# Final Step: Logout")
    steps.append("logout")

    return "\n".join(steps)

def generate_talent_acquisition_steps(scenario, rag_response):
    """Generate Talent Acquisition specific steps"""
    steps = []
    task = scenario['task_step'].lower()

    # Security-related tasks
    if 'security' in task:
        steps.append("# Step 2: Navigate to Security")
        steps.append("search|View Domain")
        steps.append("click|View Domain")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Extract Security Assignments")
        steps.append("report|Security Group Assignments")
        steps.append("verify|Security groups are assigned correctly")

    # Candidate/Recruiting tasks
    elif 'candidate' in task or 'recruit' in task or 'job' in task:
        steps.append("# Step 2: Navigate to Recruiting")
        steps.append("search|Find Candidates")
        steps.append("click|Find Candidates")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Process Candidate")
        steps.append("filter|Active Candidates")
        steps.append("select|First candidate")
        steps.append("verify|Candidate details display correctly")

    # Application/Offer tasks
    elif 'application' in task or 'offer' in task:
        steps.append("# Step 2: Navigate to Applications")
        steps.append("search|Manage Job Applications")
        steps.append("click|Manage Job Applications")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Application")
        steps.append("select|Recent application")
        steps.append("verify|Application status is correct")

    # Generic recruiting task
    else:
        steps.append("# Step 2: Navigate to Recruiting Home")
        steps.append("search|Recruiting")
        steps.append("click|Recruiting")
        steps.append("wait|2")
        steps.append("")
        steps.append(f"# Step 3: {scenario['scenario_name']}")
        steps.append(f"# Task: {scenario['task_step'][:100]}")
        steps.append("# [NEEDS SPECIFIC STEPS]")

    return steps

def generate_talent_optimization_steps(scenario, rag_response):
    """Generate Talent Optimization specific steps"""
    steps = []
    task = scenario['task_step'].lower()

    # Performance/Goal tasks
    if 'performance' in task or 'goal' in task:
        steps.append("# Step 2: Navigate to Performance")
        steps.append("search|My Performance")
        steps.append("click|My Performance")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Goals")
        steps.append("click|Goals")
        steps.append("verify|Goals are displayed")

    # Development/Career tasks
    elif 'development' in task or 'career' in task:
        steps.append("# Step 2: Navigate to Career")
        steps.append("search|Career")
        steps.append("click|Career")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Career Plans")
        steps.append("click|Development")
        steps.append("verify|Career development items display")

    # Succession planning
    elif 'succession' in task:
        steps.append("# Step 2: Navigate to Succession")
        steps.append("search|Succession Planning")
        steps.append("click|Succession Planning")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Review Succession Plans")
        steps.append("verify|Succession data is available")

    # Talent Review/Calibration
    elif 'talent review' in task or 'calibration' in task:
        steps.append("# Step 2: Navigate to Talent Review")
        steps.append("search|Talent Review")
        steps.append("click|Talent Review")
        steps.append("wait|2")
        steps.append("")
        steps.append("# Step 3: Access Review")
        steps.append("verify|Talent review data displays")

    # Generic talent optimization task
    else:
        steps.append("# Step 2: Navigate to Talent")
        steps.append("search|Talent")
        steps.append("click|Talent")
        steps.append("wait|2")
        steps.append("")
        steps.append(f"# Step 3: {scenario['scenario_name']}")
        steps.append(f"# Task: {scenario['task_step'][:100]}")
        steps.append("# [NEEDS SPECIFIC STEPS]")

    return steps

def process_scenarios():
    """Main processing function"""
    # Load scenarios
    with open(SCENARIOS_FILE, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    print(f"Processing {len(scenarios)} scenarios...")

    stats = {
        'total': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'manual': 0,
        'by_area': {}
    }

    for idx, scenario in enumerate(scenarios, 1):
        functional_area = scenario['functional_area']
        scenario_id = scenario['scenario_id']
        scenario_name = scenario['scenario_name']

        print(f"\n[{idx}/{len(scenarios)}] Processing {scenario_id}: {scenario_name[:50]}...")

        # Query RAG
        query = scenario['task_step']
        if query and query != 'nan' and len(query) > 5:
            print(f"  Querying RAG: {query[:80]}...")
            rag_response = query_rag(query)
        else:
            rag_response = ""

        # Calculate confidence
        confidence = calculate_confidence(rag_response, scenario)
        print(f"  Confidence: {confidence:.1f}/10.0")

        # Generate test content
        test_content = generate_electron_steps(scenario, rag_response, confidence)

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

        print(f"  Generated: {filename}")

        # Update stats
        stats['total'] += 1
        stats['by_area'][functional_area] = stats['by_area'].get(functional_area, 0) + 1

        if confidence >= 7.0:
            stats['high_confidence'] += 1
        elif confidence >= 5.0:
            stats['medium_confidence'] += 1
        else:
            stats['manual'] += 1

    # Print summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    print(f"Total scenarios processed: {stats['total']}")
    print(f"High confidence (>= 7.0): {stats['high_confidence']}")
    print(f"Medium confidence (5.0-6.9): {stats['medium_confidence']}")
    print(f"Manual required (< 5.0): {stats['manual']}")
    print("\nBy Functional Area:")
    for area, count in stats['by_area'].items():
        print(f"  {area}: {count}")
    print("="*60)

if __name__ == "__main__":
    process_scenarios()
