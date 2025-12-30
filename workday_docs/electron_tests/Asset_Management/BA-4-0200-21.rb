# BA-4-0200-21 - Register Asset from a Capital Project
# Confidence Score: 6.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Choose Supplier Lines and Mark as Expense Cost Use Current Date  Click Submit

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0200-21 - Register Asset from a Capital Project" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate
    enter search box as "21. Expense Supplier Invoice Cost"
    wait for search results
    click search result containing "21. Expense Supplier Invoice Cost"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 21. Expense Supplier Invoice Cost
    # Description: Choose Supplier Lines and Mark as Expense Cost Use Current Date  Click Submit
    # Sub-Task: Open Project, Navigate to Financials> Capitalization and hit the ADD PROJECT ASSETS Button

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0200-21_complete.png"
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
