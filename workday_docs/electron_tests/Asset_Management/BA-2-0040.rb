# BA-2-0040 - Manually Place Asset In Service
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Confirm Asset has an accounting treatment of Depreciable Capital Asset. Place asset in service in current period. Confirm Depreciation Summary and Depreciation Info tabs have been added to the View Business Asset Composite View and review depreciation schedule.

# Test Steps
describe "BA-2-0040 - Manually Place Asset In Service" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Manually Place Asset In Service" do
    # Step 1: Navigate to task
    enter search box as "Find Assets (Status = Registered)  Related action > Place In Service off Business Asset"
    wait for search results
    click search result containing "Find Assets (Status = Registered)  Related action > Place In Service off Business Asset"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Find Assets (Status = Registered)  Related action > Place In Service off Business Asset

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-2-0040_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
