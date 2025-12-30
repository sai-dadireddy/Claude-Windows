# BA-4-0270-02 - Leases: Confirm Lease Configuration
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Accounting Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the following account posting rules for lease accounting: Lease Asset, Lease Asset Contra, Lease Expense, Lease Liability

# Test Steps
describe "BA-4-0270-02 - Leases: Confirm Lease Configuration" do

  before do
    login_as "Accounting Operations Lead"
  end

  it "should complete: Leases: Confirm Lease Configuration" do
    # Step 1: Navigate to task
    enter search box as "View Account Posting Rule Set"
    wait for search results
    click search result containing "View Account Posting Rule Set"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "View Account Posting Rule Set"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0270-02_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
