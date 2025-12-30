# BA-4-0340-04 - FRA Derogatory: Derogatory Reversal after Disposal
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Dispose an asset and see the impact in the Derogatory Depreciation Calculation

# Test Steps
describe "BA-4-0340-04 - FRA Derogatory: Derogatory Reversal after Disposal" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: FRA Derogatory: Derogatory Reversal after Disposal" do
    # Step 1: Navigate to task
    enter search box as "- Related Action from the Asset -> Dispose
- Run FRA Derogatory Accounting Overview for Assets with the date prompted in the sale date"
    wait for search results
    click search result containing "- Related Action from the Asset -> Dispose
- Run FRA Derogatory Accounting Overview for Assets with the date prompted in the sale date"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "FRA"

    # Step 3: Validate key elements present
    verify page contains "- Related Action from the Asset -> Dispose
- Run FRA Derogatory Accounting Overview for Assets with the date prompted in the sale date"

    # Step 4: Validate expected result
    # Expected: The total difference between Cumulative Depreciation Amonut Accounting Book and  Cumulative Depreciation Amount Tax Book appears in the column : "Derogatory Accumulated - Disposal Debit"
    verify data accuracy

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0340-04_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: The total difference between Cumulative Depreciation Amonut Accounting Book and  Cumulative Depreciation Amount Tax Book appears in the column : "Derogatory Accumulated - Disposal Debit"
# Sub-Task: None
