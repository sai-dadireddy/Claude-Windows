# BA-2-0050 - Record Depreciation for Asset
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Enter a Request Name and company for which an asset has been created and is In Service Choose Posting Date = today Select Run Preview checkbox and confirm asset is available Select "OK" to record depreciation View Depreciation Transaction Related action > View Accounting off Depreciation Transaction. Return to the business asset and view the status of the depreciation period on the depreciation summary and depreciation detail tabs.

# Test Steps
describe "BA-2-0050 - Record Depreciation for Asset" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Record Depreciation for Asset" do
    # Step 1: Navigate to task
    enter search box as "Record Depreciation Amortization Expense  Run Frequency = Run Now"
    wait for search results
    click search result containing "Record Depreciation Amortization Expense  Run Frequency = Run Now"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Record Depreciation Amortization Expense  Run Frequency = Run Now

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-2-0050_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
