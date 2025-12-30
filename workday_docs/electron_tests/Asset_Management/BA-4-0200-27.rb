# BA-4-0200-27 - Register Asset from a Capital Project
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Confirm Asset has an accounting treatment of Depreciable Capital Asset  Place asset in service in current period  Confirm Depreciation Summary and Depreciation Info tabs have been added to the View Business Asset Composite View

# Test Steps
describe "BA-4-0200-27 - Register Asset from a Capital Project" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "27. Manually Place Asset from Capital Project In Service"
    wait for search results
    click search result containing "27. Manually Place Asset from Capital Project In Service"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 27. Manually Place Asset from Capital Project In Service

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0200-27_complete.png"

    # Additional Sub-Task: Find Assets (Status = Registered)  Related action > Place In Service off Business Asset
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Find Assets (Status = Registered)  Related action > Place In Service off Business Asset
