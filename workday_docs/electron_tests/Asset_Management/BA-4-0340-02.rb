# BA-4-0340-02 - FRA Derogatory: Reconciliation between GL and Derogatory
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Post an accounting journal to record the Derogatory depreciation in GL and reconcile it with the FRA Derogatory Accounting Overview for Assets.

# Test Steps
describe "BA-4-0340-02 - FRA Derogatory: Reconciliation between GL and Derogatory" do

  before do
    login_as "Accountant"
  end

  it "should complete: FRA Derogatory: Reconciliation between GL and Derogatory" do
    # Step 1: Navigate to task
    enter search box as "- Run FRA Derogatory Accounting Overview for Assets
- Create Accounting Journal to Record the amount of depreciation of the period in the General Ledger."
    wait for search results
    click search result containing "- Run FRA Derogatory Accounting Overview for Assets
- Create Accounting Journal to Record the amount of depreciation of the period in the General Ledger."
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "FRA"

    # Step 3: Validate key elements present
    verify page contains "- Run FRA Derogatory Accounting Overview for Assets
- Create Accounting Journal to Record the amount of depreciation of the period in the General Ledger."

    # Step 4: Validate expected result
    # Expected: The accumulated balance for Derogatory Depreciation posted in the Balance should match with the  column : "Derogatory Accumulated - Assets in Service/Issued" from FRA Derogatory Accounting Overview for Assets.
    verify data accuracy

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0340-02_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: The accumulated balance for Derogatory Depreciation posted in the Balance should match with the  column : "Derogatory Accumulated - Assets in Service/Issued" from FRA Derogatory Accounting Overview for Assets.
# Sub-Task: None
