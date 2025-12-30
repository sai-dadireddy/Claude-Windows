# BA-4-0090-05 - Transfer Asset to Different Company
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Status of Transferred OUT asset should be DISPOSED Accounting should DR Intercompany Receivable and CR Fixed Assets

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0090-05 - Transfer Asset to Different Company" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Transfer Asset to Different Company" do
    # Step 1: Navigate
    enter search box as "4. Confirm Status and Accounting for Asset Transferred OUT"
    wait for search results
    click search result containing "4. Confirm Status and Accounting for Asset Transferred OUT"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 4. Confirm Status and Accounting for Asset Transferred OUT
    # Description: Status of Transferred OUT asset should be DISPOSED Accounting should DR Intercompany Receivable and CR Fixed Assets
    # Sub-Task: Cost Detail Tab > Related Action > Cost Activity > Accounting > View Accounting

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0090-05_complete.png"
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
