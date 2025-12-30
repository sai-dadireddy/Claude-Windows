#!/usr/bin/env python3
"""
Generate Electron tests for Lease Accounting only.
"""

import pandas as pd
import os
import subprocess
import re
from pathlib import Path

# Paths
EXCEL_PATH = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests\WD_Test_Scenarios_Master.xlsx"
RAG_SCRIPT = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\workday_rag.py"
OUTPUT_BASE = r"C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\workday_docs\electron_tests"

# Load Excel
print("Loading Excel file...")
df = pd.read_excel(EXCEL_PATH)

print(f"Total rows: {len(df)}")
print(f"\nUnique Functional Areas:")
print(df['Functional Area'].value_counts().head(30))

# Check for Lease Accounting
lease_df = df[df['Functional Area'].str.contains("Lease", case=False, na=False)]
print(f"\nLease-related entries: {len(lease_df)}")
if len(lease_df) > 0:
    print(lease_df[['Functional Area', 'Scenario ID', 'Scenario Name']].head(10))
