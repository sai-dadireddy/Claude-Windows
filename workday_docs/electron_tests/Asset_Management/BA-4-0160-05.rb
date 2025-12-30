# BA-4-0160-05 - Dispose of an Asset
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: If the asset is capital then the asset will be sent to the BA Accountant for complete accounting information.

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0160-05 - Dispose of an Asset" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Dispose of an Asset" do
    # Step 1: Navigate
    enter search box as "2. Complete accounting information if required"
    wait for search results
    click search result containing "2. Complete accounting information if required"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 2. Complete accounting information if required
    # Description: If the asset is capital then the asset will be sent to the BA Accountant for complete accounting information.
    # Sub-Task: Inbox > Submit

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0160-05_complete.png"
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
