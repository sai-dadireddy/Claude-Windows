#!/usr/bin/env python3
"""
Generate Electron tests for Talent & Learning modules
Processes: Talent Optimization (203), Talent Acquisition (114), Learning (146), Learning Extended Enterprise (59)
"""

import pandas as pd
import os
import sys
import subprocess
import re
from pathlib import Path

# Configuration
EXCEL_PATH = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx'
OUTPUT_BASE = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests'
RAG_SCRIPT = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py'

TARGET_MODULES = {
    'Talent Optimization': 'Talent_Optimization',
    'Talent Acquisition': 'Talent_Acquisition',
    'Learning': 'Learning',
    'Learning Extended Enterprise': 'Learning_Extended'
}

def query_rag(query_text):
    """Query Workday RAG for API/WSDL information"""
    try:
        result = subprocess.run(
            ['python', RAG_SCRIPT, query_text],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else f"RAG query failed: {result.stderr}"
    except Exception as e:
        return f"RAG error: {str(e)}"

def sanitize_filename(name):
    """Create safe filename from scenario name"""
    # Remove invalid characters
    safe = re.sub(r'[^\w\s-]', '', name)
    # Replace spaces with underscores
    safe = re.sub(r'\s+', '_', safe)
    # Limit length
    return safe[:100]

def calculate_confidence(scenario_data, rag_response):
    """Calculate confidence score based on available information"""
    score = 0.0
    reasons = []

    # Check if we have scenario description
    if pd.notna(scenario_data.get('Scenario Description')) and len(str(scenario_data.get('Scenario Description'))) > 20:
        score += 0.2
        reasons.append("Detailed scenario description")

    # Check if we have task/step info
    if pd.notna(scenario_data.get('Task / Step')) and len(str(scenario_data.get('Task / Step'))) > 10:
        score += 0.2
        reasons.append("Clear task/step definition")

    # Check if we have expected result
    if pd.notna(scenario_data.get('Customer Expected Result')) and len(str(scenario_data.get('Customer Expected Result'))) > 10:
        score += 0.2
        reasons.append("Expected result defined")

    # Check RAG response quality
    if rag_response and len(rag_response) > 100:
        if 'WSDL' in rag_response or 'REST' in rag_response or 'API' in rag_response:
            score += 0.3
            reasons.append("API/WSDL information found")
        elif 'operation' in rag_response.lower() or 'endpoint' in rag_response.lower():
            score += 0.2
            reasons.append("Operation/endpoint information found")
        else:
            score += 0.1
            reasons.append("General documentation found")

    # Check if we have role information
    if pd.notna(scenario_data.get('Workday Role')):
        score += 0.1
        reasons.append("Workday role specified")

    return min(score, 1.0), reasons

def generate_electron_test(scenario_data, rag_response, module_name):
    """Generate Electron test file content"""

    scenario_id = scenario_data.get('Scenario ID', 'UNKNOWN')
    scenario_name = scenario_data.get('Scenario Name', 'Unnamed Scenario')
    description = scenario_data.get('Scenario Description', 'No description available')
    task_step = scenario_data.get('Task / Step', 'No task specified')
    expected_result = scenario_data.get('Customer Expected Result', 'No expected result specified')
    workday_role = scenario_data.get('Workday Role', 'Unspecified Role')
    test_type = scenario_data.get('Test Type', 'Unspecified')

    confidence, confidence_reasons = calculate_confidence(scenario_data, rag_response)

    content = f"""# Electron Test: {scenario_id} - {scenario_name}

## Test Metadata
- **Scenario ID**: {scenario_id}
- **Module**: {module_name}
- **Test Type**: {test_type}
- **Workday Role**: {workday_role}
- **Confidence Score**: {confidence:.2f}

### Confidence Factors
"""
    for reason in confidence_reasons:
        content += f"- {reason}\n"

    content += f"""

## Scenario Description
{description}

## Test Steps

### Task/Step: {task_step}

**Expected Result**: {expected_result}

## Workday API Information

### RAG Query Results
```
{rag_response[:2000] if rag_response else 'No API information retrieved'}
```

## Electron Test Implementation

### Prerequisites
- User must have role: {workday_role}
- Test environment configured
- Authentication credentials available

### Test Code Structure

```javascript
const {{ test, expect }} = require('@playwright/test');

test.describe('{scenario_id}: {scenario_name}', () => {{
  test.beforeEach(async ({{ page }}) => {{
    // Login as {workday_role}
    await page.goto('https://{{{{tenant}}}}.myworkday.com');
    // TODO: Implement authentication
  }});

  test('{task_step}', async ({{ page }}) => {{
    // TODO: Implement test steps based on scenario

    // Navigate to appropriate module
    // Perform actions based on: {task_step}

    // Verify expected result: {expected_result}
  }});
}});
```

### API Integration Points

"""

    # Extract API information from RAG response
    if rag_response and ('WSDL' in rag_response or 'REST' in rag_response):
        content += "```\n"
        content += "API endpoints identified in RAG response:\n"
        content += rag_response[:1000]
        content += "\n```\n"
    else:
        content += "No specific API endpoints identified. Manual investigation required.\n"

    content += f"""

### Data Requirements
- Scenario Type: {scenario_data.get('Scope Type', 'Not specified')}
- Country Code: {scenario_data.get('Country Code (Scope)', 'Not specified')}
- Industry: {scenario_data.get('Industry (Scope)', 'Not specified')}

### Estimated Effort
- Workday Estimate: {scenario_data.get('Est. Effort (mins)', 'Not specified')} minutes
- Test Implementation: TBD

## Notes
- Cross-functional: {scenario_data.get('Cross Functional Scenario', 'No')}
- Business Process Level 2: {scenario_data.get('Business Process Alignment (Level 2)', 'Not specified')}
- Business Process Level 3: {scenario_data.get('Business Process Alignment (Level 3)', 'Not specified')}

## Test Status
- [ ] Test implemented
- [ ] Test executed
- [ ] Results verified
- [ ] Edge cases covered

---
Generated: {pd.Timestamp.now()}
Confidence: {confidence:.2%}
"""

    return content

def process_module(df, module_name, folder_name):
    """Process all scenarios for a given module"""

    # Filter for this module
    module_df = df[df['Functional Area'] == module_name].copy()

    print(f"\n{'='*80}")
    print(f"Processing: {module_name} ({len(module_df)} scenarios)")
    print(f"{'='*80}\n")

    # Create output directory
    output_dir = Path(OUTPUT_BASE) / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Track statistics
    stats = {
        'total': len(module_df),
        'processed': 0,
        'high_confidence': 0,
        'medium_confidence': 0,
        'low_confidence': 0,
        'errors': 0
    }

    # Group by Scenario ID to handle multi-row scenarios
    grouped = module_df.groupby('Scenario ID')

    for scenario_id, group in grouped:
        try:
            print(f"Processing {scenario_id}...", end=' ')

            # Use first row for main data
            scenario_data = group.iloc[0].to_dict()

            # Combine all task/steps if multiple rows
            all_tasks = []
            for _, row in group.iterrows():
                task = row.get('Task / Step')
                if pd.notna(task):
                    all_tasks.append(str(task))

            if all_tasks:
                scenario_data['Task / Step'] = ' | '.join(all_tasks)

            # Query RAG for API information
            scenario_name = scenario_data.get('Scenario Name', '')
            task_step = scenario_data.get('Task / Step', '')
            query = f"{module_name} {scenario_name} {task_step}"

            rag_response = query_rag(query)

            # Generate test content
            test_content = generate_electron_test(scenario_data, rag_response, module_name)

            # Calculate confidence for stats
            confidence, _ = calculate_confidence(scenario_data, rag_response)

            if confidence >= 0.7:
                stats['high_confidence'] += 1
            elif confidence >= 0.4:
                stats['medium_confidence'] += 1
            else:
                stats['low_confidence'] += 1

            # Create filename
            safe_name = sanitize_filename(str(scenario_name))
            filename = f"{scenario_id}_{safe_name}.txt"
            filepath = output_dir / filename

            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(test_content)

            stats['processed'] += 1
            print(f"OK (confidence: {confidence:.2f})")

        except Exception as e:
            print(f"ERROR: {str(e)}")
            stats['errors'] += 1

    # Print statistics
    print(f"\n{'-'*80}")
    print(f"Module: {module_name} - Statistics")
    print(f"{'-'*80}")
    print(f"Total scenarios: {stats['total']}")
    print(f"Processed: {stats['processed']}")
    print(f"High confidence (≥0.7): {stats['high_confidence']} ({stats['high_confidence']/stats['processed']*100:.1f}%)")
    print(f"Medium confidence (0.4-0.7): {stats['medium_confidence']} ({stats['medium_confidence']/stats['processed']*100:.1f}%)")
    print(f"Low confidence (<0.4): {stats['low_confidence']} ({stats['low_confidence']/stats['processed']*100:.1f}%)")
    print(f"Errors: {stats['errors']}")
    print(f"Output directory: {output_dir}")
    print(f"{'-'*80}\n")

    return stats

def main():
    """Main execution"""
    print("="*80)
    print("Workday Electron Test Generator - Talent & Learning Modules")
    print("="*80)

    # Load Excel
    print(f"\nLoading Excel file: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, sheet_name='Test Scenarios _ Source')
    print(f"Total rows loaded: {len(df)}")

    # Process each target module
    all_stats = {}

    for module_name, folder_name in TARGET_MODULES.items():
        stats = process_module(df, module_name, folder_name)
        all_stats[module_name] = stats

    # Overall summary
    print("\n" + "="*80)
    print("OVERALL SUMMARY")
    print("="*80)

    total_scenarios = sum(s['total'] for s in all_stats.values())
    total_processed = sum(s['processed'] for s in all_stats.values())
    total_high = sum(s['high_confidence'] for s in all_stats.values())
    total_medium = sum(s['medium_confidence'] for s in all_stats.values())
    total_low = sum(s['low_confidence'] for s in all_stats.values())
    total_errors = sum(s['errors'] for s in all_stats.values())

    print(f"\nTotal scenarios across all modules: {total_scenarios}")
    print(f"Successfully processed: {total_processed}")
    print(f"High confidence (≥0.7): {total_high} ({total_high/total_processed*100:.1f}%)")
    print(f"Medium confidence (0.4-0.7): {total_medium} ({total_medium/total_processed*100:.1f}%)")
    print(f"Low confidence (<0.4): {total_low} ({total_low/total_processed*100:.1f}%)")
    print(f"Errors: {total_errors}")

    print("\n" + "="*80)
    print("Generation complete!")
    print("="*80)

if __name__ == '__main__':
    main()
