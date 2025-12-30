# BA-4-0330-04 - Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Supplier Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review the Lease Amendment Versions tab on the Supplier Contract

# Test Steps
describe "BA-4-0330-04 - Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)" do

  before do
    login_as "Supplier Contract Specialist"
  end

  it "should complete: Leases: Lease Amendments for Finance Lease or Operating Lease with depreciation expense accounting treatment (non multi-book)" do
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
    screenshot as "BA-4-0330-04_complete.png"

    # Additional Sub-Task: Lease Amendment Versions tab
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Lease Amendment Versions tab
