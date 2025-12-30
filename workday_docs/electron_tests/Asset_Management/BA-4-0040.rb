# BA-4-0040 - Remove Asset
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Tracking Specialist

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Choose the date you want the asset removal to take place and the reason for removing it. You can remove assets that you registered: By mistake. Through a supplier invoice or receipt that was later canceled. Through a supplier invoice, but the invoice line with the asset was later deleted. (In this case, you must first cancel the invoice.) Through a supplier contract, but the contract receipt line with the asset was later deleted.  *No asset lifecycle events may have occurred on the asset prior to the removal

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0040 - Remove Asset" do

  before do
    login_as "Business Asset Tracking Specialist"
  end

  it "should complete: Remove Asset" do
    # Step 1: Navigate
    enter search box as "1. Find Assets (Status = Registered)"
    wait for search results
    click search result containing "1. Find Assets (Status = Registered)"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 1. Find Assets (Status = Registered)
    # Description: Choose the date you want the asset removal to take place and the reason for removing it. You can remove assets that you registered: By mistake. Through a supplier invoice or receipt that was later canceled. Through a supplier invoice, but the invoice line with the asset was later deleted. (In this case, you must first cancel the invoice.) Through a supplier contract, but the contract receipt line with the asset was later deleted.  *No asset lifecycle events may have occurred on the asset prior to the removal
    # Sub-Task: Related action > Remove off Business Asset

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0040_complete.png"
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
