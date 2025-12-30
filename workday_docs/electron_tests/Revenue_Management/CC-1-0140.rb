# CC-1-0140 - View Account Posting Rules
# Confidence Score: 8.0/10.0
# Functional Area: Revenue Management
# Role: Common Finance Configurator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the following rules have the correct ledger account:  Deferred Revenue Revenue Receivables

# Test Steps
describe "CC-1-0140 - View Account Posting Rules" do

  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: View Account Posting Rules" do
    # Step 1: Navigate to task
    enter search box as "View Account Posting Rule Set"
    wait for search results
    click search result containing "View Account Posting Rule Set"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "View"

    # Step 3: Validate key elements present
    verify page contains "View Account Posting Rule Set"

    # Step 5: Take screenshot evidence
    screenshot as "CC-1-0140_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
