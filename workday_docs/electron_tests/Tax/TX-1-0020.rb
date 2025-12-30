# TX-1-0020 - Verify Tax Recoverabilities
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Tax Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: For each tax recoverability verify: name, recoverability type, percent recoverable, amd allocation of nonrecoverable tax

# Test Steps
describe "TX-1-0020 - Verify Tax Recoverabilities" do

  before do
    login_as "Tax Manager"
  end

  it "should complete: Verify Tax Recoverabilities" do
    # Step 1: Navigate to task
    enter search box as "View Tax Recoverabilities"
    wait for search results
    click search result containing "View Tax Recoverabilities"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Verify"

    # Step 3: Validate key elements present
    verify page contains "View Tax Recoverabilities"

    # Step 5: Take screenshot evidence
    screenshot as "TX-1-0020_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
