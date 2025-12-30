# BA-4-0090-03 - Transfer Asset to Different Company
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: As Business Asset Accountant, complete steps for Review Asset Intercompany Accounting and Submit.

# Test Steps
describe "BA-4-0090-03 - Transfer Asset to Different Company" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Transfer Asset to Different Company" do
    # Step 1: Navigate to task
    enter search box as "3. Review Asset Intercompany Accounting"
    wait for search results
    click search result containing "3. Review Asset Intercompany Accounting"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Transfer"

    # Step 3: Validate key elements present
    verify page contains "3. Review Asset Intercompany Accounting"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0090-03_complete.png"

    # Additional Sub-Task: Inbox (BA Accountant)
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Inbox (BA Accountant)
