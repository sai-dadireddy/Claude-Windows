#!/bin/bash
# Batch fix 50 low-confidence test files (25 Procurement + 25 Inventory)

cd "$(dirname "$0")"

echo "================================================================================"
echo "BATCH FIXING 50 TEST FILES - Procurement & Inventory"
echo "================================================================================"

# Procurement tasks (25 files)
declare -A PROCUREMENT_TASKS=(
    ["PRO-1-0010"]="Find Suppliers"
    ["PRO-1-0020"]="Edit Company Accounting Options"
    ["PRO-1-0030"]="Edit Company Procurement Options"
    ["PRO-1-0040"]="Maintain Units of Measure"
    ["PRO-1-0050"]="Create Workcart Link Override"
    ["PRO-1-0060"]="Create Spend Transaction Instruction"
    ["PRO-1-0070"]="Create Supplier Contract Type"
    ["PRO-1-0080"]="Maintain Purchase Order Print Layouts"
    ["PRO-1-0090"]="Create Return Reason"
    ["PRO-1-0100"]="Create Requisition Type"
    ["PRO-1-0110"]="Create Supplier Link"
    ["PRO-1-0120"]="Create Match Rule"
    ["PRO-1-0130"]="Edit Procurement Posting Rule"
    ["PRO-1-0140"]="Create Procurement Custom Validation"
    ["PRO-1-0150"]="Create Role Based Procurement Assignment"
    ["PRO-1-0160"]="Create User Based Procurement Assignment"
    ["PRO-1-0170"]="Maintain Worktag Usages"
    ["PRO-1-0180"]="Edit Related Worktag Usage"
    ["PRO-2-0010"]="Create Requisition"
    ["PRO-2-0020"]="Approve Requisition"
    ["PRO-2-0030"]="View Business Process"
    ["PRO-2-0040"]="Create Requisition for Goods"
    ["PRO-2-0050"]="Create Requisition for Service"
    ["PRO-2-0060"]="Create Requisition with Line Splits by Quantity"
    ["PRO-2-0070"]="Create Requisition with Line Splits by Amount"
)

# Inventory tasks (25 files)
declare -A INVENTORY_TASKS=(
    ["INV-1-0010"]="Create Inventory Site"
    ["INV-1-0020"]="Create Stocking Location"
    ["INV-1-0030"]="Create Inventory Location Usage Type"
    ["INV-1-0040"]="Create Purchase Item"
    ["INV-1-0050"]="Create Item Identifier Type"
    ["INV-1-0060"]="Create Stock Request Reason"
    ["INV-1-0070"]="Create Inventory Adjustment Reason"
    ["INV-1-0080"]="Manage Item Collections"
    ["INV-1-0090"]="Manage Serialization Configuration"
    ["INV-1-0100"]="Edit Company Inventory Options"
    ["INV-2-0010"]="Create Inventory Move"
    ["INV-2-0020"]="Approve Inventory Move"
    ["INV-2-0030"]="Create Inventory Stock Request"
    ["INV-2-0040"]="Inventory Stock Fulfillment"
    ["INV-2-0050"]="Create Inventory Putaway"
    ["INV-2-0060"]="Create Inventory Adjustment"
    ["INV-2-0070"]="Create Inventory Cycle Count"
    ["INV-2-0080"]="Enter Cycle Count Results"
    ["INV-2-0090"]="Create Inventory Receipt"
    ["INV-2-0100"]="Manage Consigned Inventory"
    ["INV-3-0010"]="View Inventory Balance"
    ["INV-3-0020"]="View Inventory Transactions"
    ["INV-3-0030"]="View Inventory Stock Levels"
    ["INV-3-0040"]="View Inventory Lot Tracking"
    ["INV-3-0050"]="View Inventory Serial Tracking"
)

# Process Procurement files
echo ""
echo "PROCESSING PROCUREMENT TESTS (25 files)"
echo "--------------------------------------------------------------------------------"
for test_id in "${!PROCUREMENT_TASKS[@]}"; do
    task_name="${PROCUREMENT_TASKS[$test_id]}"
    echo "[$test_id] $task_name"
    python fix_single_test.py "$test_id" "$task_name" 2>&1 | grep -E "\[OK\]|Error|Traceback"
done

# Process Inventory files
echo ""
echo "PROCESSING INVENTORY TESTS (25 files)"
echo "--------------------------------------------------------------------------------"
for test_id in "${!INVENTORY_TASKS[@]}"; do
    task_name="${INVENTORY_TASKS[$test_id]}"
    echo "[$test_id] $task_name"
    python fix_single_test.py "$test_id" "$task_name" 2>&1 | grep -E "\[OK\]|Error|Traceback"
done

echo ""
echo "================================================================================"
echo "BATCH PROCESSING COMPLETE"
echo "================================================================================"

# Generate summary
echo ""
echo "Generating summary..."
python << 'PYTHON_SCRIPT'
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(".")
stats = defaultdict(int)
stats['total'] = 0
stats['high'] = 0
stats['medium'] = 0
stats['low'] = 0

# Check Procurement files
for f in (BASE_DIR / "electron_tests" / "Procurement").glob("PRO-*.txt"):
    content = f.read_text(encoding='utf-8')
    conf_match = re.search(r'Score:\s*(\d+)', content)
    if conf_match:
        score = int(conf_match.group(1))
        stats['total'] += 1
        if score >= 7:
            stats['high'] += 1
        elif score >= 5:
            stats['medium'] += 1
        else:
            stats['low'] += 1

# Check Inventory files
for f in (BASE_DIR / "electron_tests" / "Inventory").glob("INV-*.txt"):
    content = f.read_text(encoding='utf-8')
    conf_match = re.search(r'Score:\s*(\d+)', content)
    if conf_match:
        score = int(conf_match.group(1))
        stats['total'] += 1
        if score >= 7:
            stats['high'] += 1
        elif score >= 5:
            stats['medium'] += 1
        else:
            stats['low'] += 1

print(f"Files processed: {stats['total']}")
print(f"  HIGH confidence (>=7): {stats['high']}")
print(f"  MEDIUM confidence (5-6): {stats['medium']}")
print(f"  LOW confidence (<5): {stats['low']}")
PYTHON_SCRIPT

echo ""
echo "Done!"
