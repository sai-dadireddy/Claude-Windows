#!/usr/bin/env python3
import os
import re

os.chdir(r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\Payroll_US")

manual_count = 0
automated_count = 0
confidence_scores = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}

for filename in os.listdir('.'):
    if filename.endswith('.txt') and filename != 'GENERATION_SUMMARY.txt':
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

            if 'STATUS: [MANUAL REQUIRED]' in content:
                manual_count += 1
            elif 'CONFIDENCE:' in content:
                automated_count += 1
                match = re.search(r'CONFIDENCE: \[(HIGH|MEDIUM|LOW)\]', content)
                if match:
                    confidence_scores[match.group(1)] += 1

print(f'Total files: {manual_count + automated_count}')
print(f'Automated tests: {automated_count}')
print(f'Manual required: {manual_count}')
print(f'\nConfidence breakdown:')
print(f'  HIGH: {confidence_scores["HIGH"]}')
print(f'  MEDIUM: {confidence_scores["MEDIUM"]}')
print(f'  LOW: {confidence_scores["LOW"]}')
