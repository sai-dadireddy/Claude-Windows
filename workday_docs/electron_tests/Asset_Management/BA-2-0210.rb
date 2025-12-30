# BA-2-0210 - Dispose of an Asset - Sale
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Sell an asset using a disposal type of sale and enter a sale price.

# Test Steps
describe "BA-2-0210 - Dispose of an Asset - Sale" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Dispose of an Asset - Sale" do
    # Step 1: Navigate to task
    enter search box as "Sell an asset"
    wait for search results
    click search result containing "Sell an asset"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Sell an asset

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-2-0210_complete.png"

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
