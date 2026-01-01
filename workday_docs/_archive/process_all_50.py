#!/usr/bin/env python3
"""Process all 50 test files automatically"""

import subprocess
import sys
from pathlib import Path

# Task mappings
PROCUREMENT_TASKS = {
    "PRO-1-0010": "Find Suppliers",
    "PRO-1-0020": "Edit Company Accounting Options",
    "PRO-1-0030": "Edit Company Procurement Options",
    "PRO-1-0040": "Maintain Units of Measure",
    "PRO-1-0050": "Create Workcart Link Override",
    "PRO-1-0060": "Create Spend Transaction Instruction",
    "PRO-1-0070": "Create Supplier Contract Type",
    "PRO-1-0080": "Maintain Purchase Order Print Layouts",
    "PRO-1-0090": "Create Return Reason",
    "PRO-1-0100": "Create Requisition Type",
    "PRO-1-0110": "Create Supplier Link",
    "PRO-1-0120": "Create Match Rule",
    "PRO-1-0130": "Edit Procurement Posting Rule",
    "PRO-1-0140": "Create Procurement Custom Validation",
    "PRO-1-0150": "Create Role Based Procurement Assignment",
    "PRO-1-0160": "Create User Based Procurement Assignment",
    "PRO-1-0170": "Maintain Worktag Usages",
    "PRO-1-0180": "Edit Related Worktag Usage",
    "PRO-2-0010": "Create Requisition",
    "PRO-2-0020": "Approve Requisition",
    "PRO-2-0030": "View Business Process",
    "PRO-2-0040": "Create Requisition for Goods",
    "PRO-2-0050": "Create Requisition for Service",
    "PRO-2-0060": "Create Requisition with Line Splits by Quantity",
    "PRO-2-0070": "Create Requisition with Line Splits by Amount",
}

INVENTORY_TASKS = {
    "INV-1-0010": "Create Inventory Site",
    "INV-1-0020": "Create Stocking Location",
    "INV-1-0030": "Create Inventory Location Usage Type",
    "INV-1-0040": "Create Purchase Item",
    "INV-1-0050": "Create Item Identifier Type",
    "INV-1-0060": "Create Stock Request Reason",
    "INV-1-0070": "Create Inventory Adjustment Reason",
    "INV-1-0080": "Manage Item Collections",
    "INV-1-0090": "Manage Serialization Configuration",
    "INV-1-0100": "Edit Company Inventory Options",
    "INV-2-0010": "Create Inventory Move",
    "INV-2-0020": "Approve Inventory Move",
    "INV-2-0030": "Create Inventory Stock Request",
    "INV-2-0040": "Inventory Stock Fulfillment",
    "INV-2-0050": "Create Inventory Putaway",
    "INV-2-0060": "Create Inventory Adjustment",
    "INV-2-0070": "Create Inventory Cycle Count",
    "INV-2-0080": "Enter Cycle Count Results",
    "INV-2-0090": "Create Inventory Receipt",
    "INV-2-0100": "Manage Consigned Inventory",
    "INV-3-0010": "View Inventory Balance",
    "INV-3-0020": "View Inventory Transactions",
    "INV-3-0030": "View Inventory Stock Levels",
    "INV-3-0040": "View Inventory Lot Tracking",
    "INV-3-0050": "View Inventory Serial Tracking",
}

def process_file(test_id, task_name):
    """Process a single test file"""
    try:
        result = subprocess.run(
            [sys.executable, "fix_single_test.py", test_id, task_name],
            capture_output=True,
            text=True,
            timeout=60
        )
        # Extract just the [OK] line
        for line in result.stdout.split('\n'):
            if '[OK]' in line:
                return line.strip()
        return "Completed"
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print("=" * 80)
    print("BATCH PROCESSING: 50 TEST FILES")
    print("=" * 80)

    results = []

    # Process Procurement
    print("\n" + "=" * 80)
    print("PROCUREMENT TESTS (25 files)")
    print("=" * 80)
    for test_id, task_name in sorted(PROCUREMENT_TASKS.items()):
        print(f"\n[{test_id}] {task_name}")
        result = process_file(test_id, task_name)
        print(f"  {result}")
        results.append((test_id, task_name, result))

    # Process Inventory
    print("\n" + "=" * 80)
    print("INVENTORY TESTS (25 files)")
    print("=" * 80)
    for test_id, task_name in sorted(INVENTORY_TASKS.items()):
        print(f"\n[{test_id}] {task_name}")
        result = process_file(test_id, task_name)
        print(f"  {result}")
        results.append((test_id, task_name, result))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    success = sum(1 for r in results if '[OK]' in r[2])
    print(f"Total processed: {len(results)}")
    print(f"Successful: {success}")
    print(f"Errors: {len(results) - success}")

if __name__ == "__main__":
    main()
