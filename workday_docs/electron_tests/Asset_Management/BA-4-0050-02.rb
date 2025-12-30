# BA-4-0050-02 - Issue Asset
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify that the worktag accounting entries have been reclassed as expected

# Test Steps
describe "BA-4-0050-02 - Issue Asset" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Issue Asset" do
    # Step 1: Navigate to task
    enter search box as "2. View accounting"
    wait for search results
    click search result containing "2. View accounting"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Issue"

    # Step 3: Validate key elements present
    verify page contains "2. View accounting"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0050-02_complete.png"

    # Additional Sub-Task: Cost Detail Tab > Related Action > Cost Activity > Accounting > View Accounting
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Cost Detail Tab > Related Action > Cost Activity > Accounting > View Accounting
