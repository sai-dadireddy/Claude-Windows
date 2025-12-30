# BA-4-0160-03 - Dispose of an Asset - Expire
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Dispose of expired assets

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0160-03 - Dispose of an Asset - Expire" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Dispose of an Asset - Expire" do
    # Step 1: Navigate
    enter search box as "1c. Expire an asset"
    wait for search results
    click search result containing "1c. Expire an asset"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 1c. Expire an asset
    # Description: Dispose of expired assets
    # Sub-Task: Dispose Expired Assets

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0160-03_complete.png"
  end

  after do
    logout
  end
end

# SME Actions Required:
# [ ] Define exact field names
# [ ] Specify test data values
# [ ] Define validation criteria
# [ ] Review business logic accuracy
