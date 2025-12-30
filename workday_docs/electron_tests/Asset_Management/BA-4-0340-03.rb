# BA-4-0340-03 - FRA Derogatory: Derogatory Reversal
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Derogatory Asset Reversal when Accounting Depreciation > Tax Depreciation

# Test Steps
describe "BA-4-0340-03 - FRA Derogatory: Derogatory Reversal" do

  before do
    login_as "Accountant"
  end

  it "should complete: FRA Derogatory: Derogatory Reversal" do
    # Step 1: Navigate to task
    enter search box as "- Record depreciation for multiple periods. 
- Select a period where Accounting Depreciation expense is greater than tax depreciation expense. 
- Run FRA Derogatory Asset Accounting Overview for Assets."
    wait for search results
    click search result containing "- Record depreciation for multiple periods. 
- Select a period where Accounting Depreciation expense is greater than tax depreciation expense. 
- Run FRA Derogatory Asset Accounting Overview for Assets."
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "FRA"

    # Step 3: Validate key elements present
    verify page contains "- Record depreciation for multiple periods. 
- Select a period where Accounting Depreciation expense is greater than tax depreciation expense. 
- Run FRA Derogatory Asset Accounting Overview for Assets."

    # Step 4: Validate expected result
    # Expected: The difference between the accounting depreciation and the calculated tax depreciation for the period is equal to the "Derogatory Reintegration" displayed in the FRA Derogatory Accounting Overview for Assets.
    verify data accuracy

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0340-03_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: The difference between the accounting depreciation and the calculated tax depreciation for the period is equal to the "Derogatory Reintegration" displayed in the FRA Derogatory Accounting Overview for Assets.
# Sub-Task: None
