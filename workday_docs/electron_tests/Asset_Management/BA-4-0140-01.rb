# BA-4-0140-01 - Adjust Useful Life
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: You can change the default transaction effective date to the date that the useful life change came into effect. For depreciable assets, this date coupled with the depreciation convention of the asset determines the first date that Workday recalculates depreciation lines to reflect the revised useful life.

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0140-01 - Adjust Useful Life" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Adjust Useful Life" do
    # Step 1: Navigate
    enter search box as "1. Adjust asset useful life"
    wait for search results
    click search result containing "1. Adjust asset useful life"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 1. Adjust asset useful life
    # Description: You can change the default transaction effective date to the date that the useful life change came into effect. For depreciable assets, this date coupled with the depreciation convention of the asset determines the first date that Workday recalculates depreciation lines to reflect the revised useful life.
    # Sub-Task: Related action > Adjust Useful Life off Business Asset

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0140-01_complete.png"
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
