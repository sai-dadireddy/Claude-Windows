# BA-4-0270-03 - Leases: Confirm Lease Configuration
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Supplier Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review Supplier Contract Types for leases.

# Test Steps
describe "BA-4-0270-03 - Leases: Confirm Lease Configuration" do

  before do
    login_as "Supplier Contract Specialist"
  end

  it "should complete: Leases: Confirm Lease Configuration" do
    # Step 1: Navigate to task
    enter search box as "View Supplier Contract Types"
    wait for search results
    click search result containing "View Supplier Contract Types"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "View Supplier Contract Types"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0270-03_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
