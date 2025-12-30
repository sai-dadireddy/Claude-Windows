# BA-4-0100-01 - Change In Service Date of Asset
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Tracking Specialist

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Change the date the asset was originally placed in service. Note: asset must be Issued or In Service for capitalized assets with place in service option of 'Manually or When Issued'

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0100-01 - Change In Service Date of Asset" do

  before do
    login_as "Business Asset Tracking Specialist"
  end

  it "should complete: Change In Service Date of Asset" do
    # Step 1: Navigate
    enter search box as "1. Change asset in service date"
    wait for search results
    click search result containing "1. Change asset in service date"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 1. Change asset in service date
    # Description: Change the date the asset was originally placed in service. Note: asset must be Issued or In Service for capitalized assets with place in service option of 'Manually or When Issued'
    # Sub-Task: Related action > Adjust In Service Date off Business Asset

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0100-01_complete.png"
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
