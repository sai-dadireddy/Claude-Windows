# BA-4-0030-05 - Register Asset from a Supplier Invoice
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Confirm Asset has an accounting treatment of Depreciable Capital Asset  Place asset in service in current period  Confirm Depreciation Summary and Depreciation Info tabs have been added to the View Business Asset Composite View

# Test Steps
describe "BA-4-0030-05 - Register Asset from a Supplier Invoice" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "7. Manually Place Asset In Service"
    wait for search results
    click search result containing "7. Manually Place Asset In Service"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 7. Manually Place Asset In Service

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0030-05_complete.png"

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
