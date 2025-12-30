#!/usr/bin/env python3
"""Verify sheet names in Excel file"""
import pandas as pd

EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"

try:
    xl = pd.ExcelFile(EXCEL_PATH)
    print(f"Found {len(xl.sheet_names)} sheets:")
    print()

    for sheet in xl.sheet_names:
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
        print(f"  {sheet}: {len(df)} rows")

    print()
    print("Looking for target sheets:")
    targets = ['Expenses', 'Tax', 'Revenue_Management', 'Advanced_Compensation']

    for target in targets:
        if target in xl.sheet_names:
            df = pd.read_excel(EXCEL_PATH, sheet_name=target)
            print(f"  ✓ {target}: {len(df)} scenarios")
        else:
            print(f"  ✗ {target}: NOT FOUND")
            # Try to find similar
            similar = [s for s in xl.sheet_names if target.lower().replace('_', ' ') in s.lower()]
            if similar:
                print(f"    Similar: {similar}")

except Exception as e:
    print(f"Error: {e}")
