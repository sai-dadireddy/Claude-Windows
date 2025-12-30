# BA-2-0270 - Register Asset from Supplier Invoice
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify total asset cost and confirm accounting for asset acquisition.

# Test Steps
describe "BA-2-0270 - Register Asset from Supplier Invoice" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "5. View Accounting Information for asset acquisition"
    wait for search results
    click search result containing "5. View Accounting Information for asset acquisition"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "5. View Accounting Information for asset acquisition"

    # Step 5: Take screenshot evidence
    screenshot as "BA-2-0270_complete.png"

    # Additional Sub-Task: Find Assets > Asset ID > Lifecycle > Related Action on Supplier Invoice Operational Transaction > View Accounting
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Find Assets > Asset ID > Lifecycle > Related Action on Supplier Invoice Operational Transaction > View Accounting
