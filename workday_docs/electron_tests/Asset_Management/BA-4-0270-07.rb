# BA-4-0270-07 - Leases: Confirm Lease Configuration
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review Company Asset Book Restrictions

# Test Steps
describe "BA-4-0270-07 - Leases: Confirm Lease Configuration" do

  before do
    login_as "Business Asset Operations Lead"
  end

  it "should complete: Leases: Confirm Lease Configuration" do
    # Step 1: Navigate to task
    enter search box as "View Company Asset Book Restrictions"
    wait for search results
    click search result containing "View Company Asset Book Restrictions"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "View Company Asset Book Restrictions"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0270-07_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
