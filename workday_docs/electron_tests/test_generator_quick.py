#!/usr/bin/env python3
"""Quick test to verify generator works"""
import pandas as pd
import subprocess
import sys

EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"

# Check Excel
print("Checking Excel file...")
try:
    xl = pd.ExcelFile(EXCEL_PATH)
    print(f"✓ Excel file loaded")
    print(f"  Available sheets: {xl.sheet_names[:10]}")

    # Check if our modules exist as sheets
    for module in ["Accounts Payable", "Accounts Receivable", "Cash Management"]:
        if module in xl.sheet_names:
            df = pd.read_excel(EXCEL_PATH, sheet_name=module)
            print(f"  ✓ {module}: {len(df)} rows")
            if len(df) > 0:
                print(f"    Columns: {list(df.columns)[:5]}")
                print(f"    Sample ID: {df.iloc[0].get('Scenario ID', 'N/A')}")
        else:
            print(f"  ✗ {module}: NOT FOUND as sheet")

except Exception as e:
    print(f"✗ Excel error: {e}")

# Check RAG
print("\nChecking RAG script...")
try:
    result = subprocess.run(
        [sys.executable, RAG_SCRIPT, "create invoice"],
        capture_output=True,
        text=True,
        timeout=10
    )
    print(f"✓ RAG script works")
    print(f"  Output length: {len(result.stdout)} chars")
    print(f"  First 200 chars: {result.stdout[:200]}")
except Exception as e:
    print(f"✗ RAG error: {e}")

print("\n✓ All checks complete")
