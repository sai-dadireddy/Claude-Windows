# BA-2-0180 - Dispose of an Asset - Discard
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Scrap or throw away an asset by entering a disposal of type discard

# Test Steps
describe "BA-2-0180 - Dispose of an Asset - Discard" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Dispose of an Asset - Discard" do
    # Step 1: Navigate to task
    enter search box as "Discard an asset"
    wait for search results
    click search result containing "Discard an asset"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Discard an asset

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-2-0180_complete.png"

    # Additional Sub-Task: Related action > Dispose off Business Asset
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Related action > Dispose off Business Asset
