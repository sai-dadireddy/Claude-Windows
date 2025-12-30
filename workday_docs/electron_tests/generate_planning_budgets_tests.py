#!/usr/bin/env python3
"""
Generate Electron Tests for Planning and Budgets Functional Areas
Processes 257 scenarios across:
- PLN - Financial Planning (89)
- PLN - Workforce Planning (52)
- Budgets (56)
- Accounting Center (60)
"""

import pandas as pd
import numpy as np
import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path to import workday_rag
sys.path.insert(0, str(Path(__file__).parent.parent))
from workday_rag import WorkdayRAG

class ElectronTestGenerator:
    def __init__(self, excel_path, output_base_dir):
        self.excel_path = excel_path
        self.output_base_dir = Path(output_base_dir)
        self.rag = WorkdayRAG()

        # Target functional areas
        self.target_areas = {
            'PLN - Financial Planning': 'Financial_Planning',
            'PLN - Workforce Planning': 'Workforce_Planning',
            'Budgets': 'Budgets',
            'Accounting Center': 'Accounting_Center'
        }

        self.stats = {
            'total_processed': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0,
            'no_task': 0,
            'generated': 0
        }

    def load_scenarios(self):
        """Load scenarios from Excel"""
        print(f"Loading scenarios from {self.excel_path}...")
        df = pd.read_excel(self.excel_path, sheet_name='Test Scenarios _ Source')

        # Filter for target areas
        filtered = df[df['Functional Area'].isin(self.target_areas.keys())]
        print(f"Found {len(filtered)} scenarios across {len(self.target_areas)} functional areas\n")

        for area, count in filtered['Functional Area'].value_counts().items():
            print(f"  {area}: {count} scenarios")

        return filtered

    def query_rag(self, task, description=""):
        """Query RAG for relevant documentation"""
        if not task or pd.isna(task) or task == '[NO TASK]':
            return None, 0.0

        # Combine task and description for better search
        query = str(task)
        if description and pd.notna(description) and len(str(description)) > 10:
            query += f" {str(description)[:100]}"

        try:
            results = self.rag.search(query, top_k=3)
            if results and len(results) > 0:
                top_result = results[0]
                return top_result, top_result.get('score', 0.0)
            return None, 0.0
        except Exception as e:
            print(f"RAG query error: {e}")
            return None, 0.0

    def get_confidence_level(self, score):
        """Determine confidence level from RAG score"""
        if score >= 8.0:
            return "HIGH", "✅"
        elif score >= 5.0:
            return "MEDIUM", "⚠️"
        else:
            return "LOW", "❌"

    def parse_task_steps(self, task_str):
        """Parse task string into actionable steps"""
        if not task_str or pd.isna(task_str):
            return []

        steps = []
        task_str = str(task_str)

        # Split by newlines or common separators
        lines = task_str.replace('\n', '|').split('|')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Convert to Electron commands
            if line.startswith('Go to '):
                # Navigation step
                target = line.replace('Go to ', '').strip()
                steps.append(f'enter search box as "{target}"')
                steps.append('wait for search results')
                steps.append(f'click search result containing "{target}"')
                steps.append('wait for page to load')
            elif 'validate' in line.lower() or 'verify' in line.lower():
                # Verification step
                steps.append(f'verify {line}')
            elif 'generate' in line.lower():
                # Action step
                if 'Excel' in line:
                    steps.append('click button "Generate Printable View"')
                    steps.append('wait for export to complete')
            else:
                # Generic action
                steps.append(f'# {line}')

        return steps

    def generate_electron_test(self, row, rag_result, rag_score):
        """Generate Electron test content for a scenario"""
        scenario_id = row.get('Scenario ID', 'UNKNOWN')
        functional_area = row.get('Functional Area', 'UNKNOWN')
        scenario_name = row.get('Scenario Name', 'Untitled')
        task = row.get('Task / Step', '')
        sub_task = row.get('Sub Task', '')
        description = row.get('Scenario Description', '')
        expected_result = row.get('Customer Expected Result', '')
        effort = row.get('Est. Effort (mins)', 0)
        role = row.get('Workday Role', 'N/A')

        # Handle NaN values
        task = task if pd.notna(task) else '[NO TASK]'
        sub_task = sub_task if pd.notna(sub_task) else ''
        description = description if pd.notna(description) else ''
        expected_result = expected_result if pd.notna(expected_result) else ''
        effort = effort if pd.notna(effort) else 0
        role = role if pd.notna(role) else 'N/A'

        # Determine confidence
        confidence, icon = self.get_confidence_level(rag_score)

        # Build test content
        output = []
        output.append("=" * 80)
        output.append(f"TEST ID: {scenario_id}")
        output.append(f"FUNCTIONAL AREA: {functional_area}")
        output.append(f"TEST NAME: {scenario_name}")
        output.append(f"WORKDAY ROLE: {role}")
        output.append(f"EST. DURATION: {effort} minutes")
        output.append(f"CONFIDENCE: {confidence} {icon} (RAG Score: {rag_score:.1f})")
        output.append("=" * 80)
        output.append("")

        # Description
        if description:
            output.append("DESCRIPTION:")
            output.append(description)
            output.append("")

        # Prerequisites
        output.append("PREREQUISITES:")
        output.append(f"- User logged in with {role} permissions")
        if description:
            output.append(f"- Required context: {description[:100]}")
        output.append("")

        # Generate steps
        output.append("ELECTRON STEPS:")

        if task == '[NO TASK]':
            output.append("# [INCOMPLETE: No Task/Step provided in source data]")
            output.append("# This scenario requires manual review")
        else:
            # Parse task into steps
            steps = self.parse_task_steps(task)
            for i, step in enumerate(steps, 1):
                output.append(f"{i}. {step}")

            # Add screenshot step
            output.append(f"{len(steps) + 1}. screenshot as \"{scenario_id}_complete.png\"")

        output.append("")

        # Verification
        output.append("VERIFICATION:")
        if expected_result:
            output.append(f"- [ ] {expected_result}")
        else:
            output.append("- [ ] Task completed successfully")
        output.append("- [ ] No error messages displayed")
        output.append("")

        # Sub-tasks
        if sub_task:
            output.append("SUB-TASKS:")
            output.append(sub_task)
            output.append("")

        # RAG source info
        if rag_result:
            output.append("KNOWLEDGE SOURCE:")
            doc_info = rag_result.get('doc', {})
            output.append(f"- Source: {doc_info.get('title', 'Unknown')}")
            output.append(f"- Type: {doc_info.get('type', 'Unknown')}")
            if rag_score >= 5.0:
                content = rag_result.get('content', '')[:200]
                output.append(f"- Excerpt: {content}...")
            output.append("")

        # API alternatives (if available from RAG)
        if rag_result and rag_score >= 7.0:
            output.append("API ALTERNATIVE:")
            doc_type = rag_result.get('doc', {}).get('type', '')
            if 'wsdl' in doc_type.lower():
                output.append(f"- SOAP: {rag_result.get('doc', {}).get('title', 'N/A')}")
            elif 'rest' in doc_type.lower():
                output.append(f"- REST: {rag_result.get('doc', {}).get('title', 'N/A')}")
            else:
                output.append("- Check RAG for API endpoints")
            output.append("")

        output.append("=" * 80)
        output.append("")

        return "\n".join(output)

    def generate_tests_for_area(self, area_name, scenarios_df):
        """Generate all tests for a functional area"""
        folder_name = self.target_areas[area_name]
        output_dir = self.output_base_dir / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nGenerating tests for {area_name}...")
        print(f"Output directory: {output_dir}")
        print(f"Total scenarios: {len(scenarios_df)}\n")

        area_stats = {
            'total': len(scenarios_df),
            'generated': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'no_task': 0
        }

        for idx, row in scenarios_df.iterrows():
            scenario_id = row.get('Scenario ID', f'UNKNOWN_{idx}')
            task = row.get('Task / Step', '')

            # Check if task exists
            if not task or pd.isna(task):
                self.stats['no_task'] += 1
                area_stats['no_task'] += 1
                task = '[NO TASK]'

            # Query RAG
            rag_result, rag_score = self.query_rag(task, row.get('Scenario Description', ''))

            # Track confidence
            confidence, _ = self.get_confidence_level(rag_score)
            if confidence == "HIGH":
                self.stats['high_confidence'] += 1
                area_stats['high'] += 1
            elif confidence == "MEDIUM":
                self.stats['medium_confidence'] += 1
                area_stats['medium'] += 1
            else:
                self.stats['low_confidence'] += 1
                area_stats['low'] += 1

            # Generate test
            test_content = self.generate_electron_test(row, rag_result, rag_score)

            # Save to file
            safe_id = str(scenario_id).replace('/', '_').replace('\\', '_')
            output_file = output_dir / f"{safe_id}.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(test_content)

            self.stats['generated'] += 1
            area_stats['generated'] += 1
            self.stats['total_processed'] += 1

            # Progress indicator
            if area_stats['generated'] % 10 == 0:
                print(f"  Progress: {area_stats['generated']}/{area_stats['total']} tests generated...")

        # Area summary
        print(f"\n{area_name} Summary:")
        print(f"  Total scenarios: {area_stats['total']}")
        print(f"  Generated: {area_stats['generated']}")
        print(f"  High confidence: {area_stats['high']}")
        print(f"  Medium confidence: {area_stats['medium']}")
        print(f"  Low confidence: {area_stats['low']}")
        print(f"  No task data: {area_stats['no_task']}")

        return area_stats

    def generate_all_tests(self):
        """Generate tests for all functional areas"""
        print("="*80)
        print("Electron Test Generation: Planning & Budgets")
        print("="*80)
        print()

        # Load scenarios
        df = self.load_scenarios()

        # Process each functional area
        area_summaries = {}
        for area_name in self.target_areas.keys():
            area_df = df[df['Functional Area'] == area_name]
            if len(area_df) > 0:
                summary = self.generate_tests_for_area(area_name, area_df)
                area_summaries[area_name] = summary

        # Final summary
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
        print(f"Total scenarios processed: {self.stats['total_processed']}")
        print(f"Tests generated: {self.stats['generated']}")
        print(f"\nConfidence breakdown:")
        print(f"  HIGH (≥8.0):   {self.stats['high_confidence']} ({self.stats['high_confidence']/self.stats['total_processed']*100:.1f}%) ✅")
        print(f"  MEDIUM (5-8):  {self.stats['medium_confidence']} ({self.stats['medium_confidence']/self.stats['total_processed']*100:.1f}%) ⚠️")
        print(f"  LOW (<5):      {self.stats['low_confidence']} ({self.stats['low_confidence']/self.stats['total_processed']*100:.1f}%) ❌")
        print(f"  No task data:  {self.stats['no_task']}")
        print()
        print(f"Output location: {self.output_base_dir}")
        print("="*80)

        return area_summaries

def main():
    excel_path = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx'
    output_dir = r'C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests'

    generator = ElectronTestGenerator(excel_path, output_dir)
    generator.generate_all_tests()

if __name__ == '__main__':
    main()
