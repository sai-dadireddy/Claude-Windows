# BA-4-0280-02 - Leases: Operating Lease Operating Expense (non multi-book)
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Accounting Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review the expense recognition and supplier invoice schedules.

# Test Steps
describe "BA-4-0280-02 - Leases: Operating Lease Operating Expense (non multi-book)" do

  before do
    login_as "Accounting Operations Lead"
  end

  it "should complete: Leases: Operating Lease Operating Expense (non multi-book)" do
    # Step 1: Navigate to task
    enter search box as "View Supplier Contract"
    wait for search results
    click search result containing "View Supplier Contract"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "View Supplier Contract"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0280-02_complete.png"

    # Additional Sub-Task: Schedule tab
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Schedule tab
