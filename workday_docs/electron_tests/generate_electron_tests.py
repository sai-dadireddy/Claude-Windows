#!/usr/bin/env python3
"""
Generate Electron test files for Time/Absence/Scheduling scenarios
Uses RAG to find relevant SOAP operations and generates confidence scores
"""
import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for workday_rag
sys.path.insert(0, str(Path(__file__).parent.parent))

def query_rag(query: str) -> str:
    """Query the Workday RAG system"""
    try:
        result = subprocess.run(
            ['python', '../workday_rag.py', query],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        return result.stdout
    except Exception as e:
        return f"RAG query failed: {e}"

def determine_confidence(scenario: Dict, rag_result: str) -> tuple[str, str]:
    """
    Determine confidence level and reasoning based on RAG results and scenario data

    Returns: (confidence_level, reasoning)
    confidence_level: HIGH | MEDIUM | LOW | MANUAL
    """
    task_step = scenario.get('task_step')
    scenario_name = scenario.get('scenario_name')
    description = scenario.get('scenario_description')

    # MANUAL if no Task/Step
    if not task_step or task_step == 'None' or str(task_step).strip() == '':
        return 'MANUAL', 'No task/step defined - manual review required'

    # Check RAG results for SOAP operations
    has_soap_ops = 'Get_' in rag_result or 'Submit_' in rag_result or 'Request_' in rag_result
    has_wsdl = 'WSDL:' in rag_result or '.wsdl' in rag_result.lower()

    # HIGH: Clear SOAP operations found and task is well-defined
    if has_soap_ops and has_wsdl and task_step:
        return 'HIGH', f'Found SOAP operations in RAG for task: {task_step}'

    # MEDIUM: Some RAG results but not definitive
    if (has_soap_ops or has_wsdl) and task_step:
        return 'MEDIUM', f'Partial RAG match for task: {task_step}, may need manual verification'

    # LOW: Task defined but no RAG matches
    if task_step and not has_soap_ops:
        return 'LOW', f'Task defined ({task_step}) but no clear SOAP operations found in RAG'

    return 'MANUAL', 'Unable to determine automation approach'

def generate_electron_test(scenario: Dict, functional_area: str) -> str:
    """Generate an Electron test file for a single scenario"""

    scenario_id = scenario.get('scenario_id', 'UNKNOWN')
    scenario_name = scenario.get('scenario_name', 'Unnamed Scenario')
    description = scenario.get('scenario_description', '')
    task_step = scenario.get('task_step', '')

    # Query RAG for relevant information
    rag_query = f"{functional_area} {scenario_name} {task_step}"
    rag_result = query_rag(rag_query)

    # Determine confidence
    confidence, reasoning = determine_confidence(scenario, rag_result)

    # Generate test content
    test_content = f'''/**
 * Electron Test: {scenario_id} - {scenario_name}
 * Functional Area: {functional_area}
 *
 * CONFIDENCE: {confidence}
 * REASONING: {reasoning}
 *
 * Scenario Description:
 * {description}
 *
 * Task/Step: {task_step}
 * Expected Result: {scenario.get('expected_result', 'N/A')}
 * Estimated Effort: {scenario.get('effort_mins', 'N/A')} minutes
 * Workday Role: {scenario.get('workday_role', 'N/A')}
 */

const {{ test, expect }} = require('@playwright/test');

test.describe('{scenario_id}: {scenario_name}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Login to Workday tenant
    await page.goto('https://your-tenant.workday.com');
    // Add authentication steps
  }});

  test('Execute: {task_step}', async ({{ page }}) => {{
'''

    if confidence == 'MANUAL':
        test_content += f'''    // MANUAL TEST - No automation steps generated
    // Task/Step: {task_step}
    //
    // Manual Steps Required:
    // 1. Review scenario description above
    // 2. Execute in Workday UI
    // 3. Validate expected results

    test.skip('Manual test execution required');
'''
    else:
        # Add RAG-based automation hints
        test_content += f'''    // RAG Query Results:
    // {rag_result[:500].replace(chr(10), chr(10) + '    // ')}...

    // TODO: Implement automation steps based on RAG results
    // Task: {task_step}

    // Step 1: Navigate to {task_step}
    // await page.click('text="{task_step}"');

    // Step 2: Execute scenario actions
    // ... automation steps here ...

    // Step 3: Verify expected results
    // const result = await page.locator('...').textContent();
    // expect(result).toContain('{scenario.get('expected_result', '')}');

    test.skip('Automation implementation pending - CONFIDENCE: {confidence}');
'''

    test_content += '''  });
});

/**
 * RAG REFERENCE DATA:
 *
'''
    test_content += f' * Query: {rag_query}\n'
    test_content += ' * Results:\n'
    for line in rag_result.split('\n')[:20]:  # First 20 lines
        test_content += f' * {line}\n'
    test_content += ' */\n'

    return test_content

def process_scenarios():
    """Process all scenarios and generate test files"""

    base_dir = Path(__file__).parent
    scenarios_file = base_dir / 'time_absence_scheduling_scenarios.json'

    # Load scenarios
    with open(scenarios_file, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    print(f"Loaded {len(scenarios)} scenarios")

    # Group by functional area
    by_area = {}
    for scenario in scenarios:
        area = scenario.get('functional_area')
        if area not in by_area:
            by_area[area] = []
        by_area[area].append(scenario)

    # Generate tests for each functional area
    stats = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'MANUAL': 0}

    for area, area_scenarios in by_area.items():
        print(f"\n=== Processing {area} ({len(area_scenarios)} scenarios) ===")

        # Create output directory
        area_dir = base_dir / area.replace(' ', '_')
        area_dir.mkdir(exist_ok=True)

        for idx, scenario in enumerate(area_scenarios, 1):
            scenario_id = scenario.get('scenario_id', f'UNKNOWN_{idx}')

            print(f"  [{idx}/{len(area_scenarios)}] Generating test for {scenario_id}...")

            # Generate test content
            test_content = generate_electron_test(scenario, area)

            # Extract confidence from test content
            if 'CONFIDENCE: HIGH' in test_content:
                stats['HIGH'] += 1
            elif 'CONFIDENCE: MEDIUM' in test_content:
                stats['MEDIUM'] += 1
            elif 'CONFIDENCE: LOW' in test_content:
                stats['LOW'] += 1
            else:
                stats['MANUAL'] += 1

            # Write test file
            test_file = area_dir / f'{scenario_id}.spec.js'
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

    # Print summary
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total scenarios processed: {len(scenarios)}")
    print(f"\nConfidence Distribution:")
    print(f"  HIGH:   {stats['HIGH']:3d} ({stats['HIGH']/len(scenarios)*100:5.1f}%)")
    print(f"  MEDIUM: {stats['MEDIUM']:3d} ({stats['MEDIUM']/len(scenarios)*100:5.1f}%)")
    print(f"  LOW:    {stats['LOW']:3d} ({stats['LOW']/len(scenarios)*100:5.1f}%)")
    print(f"  MANUAL: {stats['MANUAL']:3d} ({stats['MANUAL']/len(scenarios)*100:5.1f}%)")

    print(f"\nOutput directories:")
    for area in by_area.keys():
        area_dir = base_dir / area.replace(' ', '_')
        print(f"  {area_dir}")

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    process_scenarios()
