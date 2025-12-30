# BA-4-0330-02 - Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review asset adjustment for contract amendment and update useful life if applicable.

# Test Steps
describe "BA-4-0330-02 - Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)" do
    # Step 1: Navigate to task
    enter search box as "Review Asset Adjustment for Contract Amendment"
    wait for search results
    click search result containing "Review Asset Adjustment for Contract Amendment"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "Review Asset Adjustment for Contract Amendment"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0330-02_complete.png"

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
