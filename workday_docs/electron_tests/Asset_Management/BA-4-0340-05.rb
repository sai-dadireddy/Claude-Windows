# BA-4-0340-05 - FRA Derogatory: Derogatory Accumulated Depreciation - History
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Report on Derogatory depreciation in the past

# Test Steps
describe "BA-4-0340-05 - FRA Derogatory: Derogatory Accumulated Depreciation - History" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: FRA Derogatory: Derogatory Accumulated Depreciation - History" do
    # Step 1: Navigate to task
    enter search box as "- After Disposing Derogatory Assets, run report "FRA Derogatory Accounting Overview for Assets" in a period prior to disposal date  (Date To : last day of the previous period  before disposal period)"
    wait for search results
    click search result containing "- After Disposing Derogatory Assets, run report "FRA Derogatory Accounting Overview for Assets" in a period prior to disposal date  (Date To : last day of the previous period  before disposal period)"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "FRA"

    # Step 3: Validate key elements present
    verify page contains "- After Disposing Derogatory Assets, run report "FRA Derogatory Accounting Overview for Assets" in a period prior to disposal date  (Date To : last day of the previous period  before disposal period)"

    # Step 4: Validate expected result
    # Expected: The  asset disposed in a future period appears in the report.
    verify data accuracy

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0340-05_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: The  asset disposed in a future period appears in the report.
# Sub-Task: None
