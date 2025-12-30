# BA-4-0080-01 - Transfer Single Asset
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Tracking Specialist

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Transfer the asset to a worker or location

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0080-01 - Transfer Single Asset" do

  before do
    login_as "Business Asset Tracking Specialist"
  end

  it "should complete: Transfer Single Asset" do
    # Step 1: Navigate
    enter search box as "1. Transfer Assets"
    wait for search results
    click search result containing "1. Transfer Assets"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 1. Transfer Assets
    # Description: Transfer the asset to a worker or location
    # Sub-Task: Related action > Transfer off Business Asset

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0080-01_complete.png"
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
