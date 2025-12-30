#!/bin/bash
################################################################################
# Electron Test Generation - AP/AR/Cash Management
# Run this script to generate all 633 test scenarios
################################################################################

echo "================================================================================"
echo "WORKDAY ELECTRON TEST GENERATOR"
echo "AP / AR / CASH MANAGEMENT"
echo "================================================================================"
echo ""

# Change to correct directory
cd "/c/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/workday_docs/electron_tests"

echo "Step 1: Validating setup..."
echo "--------------------------------------------------------------------------------"
python3 test_generator_quick.py
if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Please check configuration."
    exit 1
fi
echo ""

echo "Step 2: Generating all tests..."
echo "--------------------------------------------------------------------------------"
echo "This will process 633 scenarios and may take 30-60 minutes."
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

python3 generate_ap_ar_cash_tests.py 2>&1 | tee generation_log.txt
if [ $? -ne 0 ]; then
    echo "❌ Generation failed. Check generation_log.txt for details."
    exit 1
fi
echo ""

echo "Step 3: Verifying output..."
echo "--------------------------------------------------------------------------------"

AP_COUNT=$(ls Accounts_Payable/*.txt 2>/dev/null | wc -l)
AR_COUNT=$(ls Accounts_Receivable/*.txt 2>/dev/null | wc -l)
CM_COUNT=$(ls Cash_Management/*.txt 2>/dev/null | wc -l)
TOTAL=$((AP_COUNT + AR_COUNT + CM_COUNT))

echo "Files generated:"
echo "  Accounts Payable:    $AP_COUNT / 244"
echo "  Accounts Receivable: $AR_COUNT / 221"
echo "  Cash Management:     $CM_COUNT / 168"
echo "  TOTAL:               $TOTAL / 633"
echo ""

if [ $TOTAL -eq 633 ]; then
    echo "✅ All 633 test files generated successfully!"
else
    echo "⚠️  Warning: Expected 633 files, got $TOTAL"
fi

echo ""
echo "Step 4: Confidence score summary..."
echo "--------------------------------------------------------------------------------"

for dir in "Accounts_Payable" "Accounts_Receivable" "Cash_Management"; do
    if [ -d "$dir" ]; then
        HIGH=$(grep -l "CONFIDENCE: HIGH" $dir/*.txt 2>/dev/null | wc -l)
        MEDIUM=$(grep -l "CONFIDENCE: MEDIUM" $dir/*.txt 2>/dev/null | wc -l)
        LOW=$(grep -l "CONFIDENCE: LOW" $dir/*.txt 2>/dev/null | wc -l)
        MANUAL=$(grep -l "MANUAL REQUIRED" $dir/*.txt 2>/dev/null | wc -l)
        TOTAL_DIR=$(ls $dir/*.txt 2>/dev/null | wc -l)

        echo "$dir:"
        echo "  HIGH:   $HIGH ($(awk "BEGIN {printf \"%.1f\", $HIGH/$TOTAL_DIR*100}")%)"
        echo "  MEDIUM: $MEDIUM ($(awk "BEGIN {printf \"%.1f\", $MEDIUM/$TOTAL_DIR*100}")%)"
        echo "  LOW:    $LOW ($(awk "BEGIN {printf \"%.1f\", $LOW/$TOTAL_DIR*100}")%)"
        echo "  MANUAL: $MANUAL ($(awk "BEGIN {printf \"%.1f\", $MANUAL/$TOTAL_DIR*100}")%)"
        echo ""
    fi
done

echo "================================================================================"
echo "✅ GENERATION COMPLETE"
echo "================================================================================"
echo "Check generation_log.txt for detailed output"
echo "Review files in Accounts_Payable/, Accounts_Receivable/, Cash_Management/"
echo "================================================================================"
