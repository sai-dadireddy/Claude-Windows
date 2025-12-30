# BA-4-0340-01 - FRA Derogatory: Derogatory Depreciation
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Derogatory Depreciation for the period after asset registration.
Prerqusite :  Accounting Asset book and Tax Asset Book and assigning it to your company,

# Test Steps
describe "BA-4-0340-01 - FRA Derogatory: Derogatory Depreciation" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: FRA Derogatory: Derogatory Depreciation" do
    # Step 1: Navigate to task
    enter search box as "- Register Asset where the Accounting Book depreciation method is different from the Tax Book depreciation method (smaller usefull life for Tax Asset Book). 
- Record the Depreciation Expense for the period. 
- Run FRA Derogatory Accounting Overview for Assets."
    wait for search results
    click search result containing "- Register Asset where the Accounting Book depreciation method is different from the Tax Book depreciation method (smaller usefull life for Tax Asset Book). 
- Record the Depreciation Expense for the period. 
- Run FRA Derogatory Accounting Overview for Assets."
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "FRA"

    # Step 3: Validate key elements present
    verify page contains "- Register Asset where the Accounting Book depreciation method is different from the Tax Book depreciation method (smaller usefull life for Tax Asset Book). 
- Record the Depreciation Expense for the period. 
- Run FRA Derogatory Accounting Overview for Assets."

    # Step 4: Validate expected result
    # Expected: The difference between the accounting depreciation and the calculated tax depreciation for the period is equal to the "Derogatory Amount" displayed in the FRA Derogatory Accounting Overview for Assets.
    verify data accuracy

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0340-01_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: The difference between the accounting depreciation and the calculated tax depreciation for the period is equal to the "Derogatory Amount" displayed in the FRA Derogatory Accounting Overview for Assets.
# Sub-Task: None
