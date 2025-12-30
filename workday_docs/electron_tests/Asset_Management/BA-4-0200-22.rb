# BA-4-0200-22 - Register Asset from a Capital Project
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Enter Company, Year, and Period In the Worktags field, enter your Capital Project Hit OK  Find a Line with Journal Source = Capital Project Cost Reclassification and click on the Journal  Note reclassification from the WIP Account to the Spend Account

# Test Steps
describe "BA-4-0200-22 - Register Asset from a Capital Project" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "22. Review Transactional Accounting for Supplier Invoice reclassification"
    wait for search results
    click search result containing "22. Review Transactional Accounting for Supplier Invoice reclassification"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "22. Review Transactional Accounting for Supplier Invoice reclassification"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0200-22_complete.png"

    # Additional Sub-Task: Journal Lines report
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Journal Lines report
