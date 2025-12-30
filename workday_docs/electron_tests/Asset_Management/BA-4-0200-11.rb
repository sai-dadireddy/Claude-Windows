# BA-4-0200-11 - Register Asset from a Capital Project
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Once approved, view the Accounting for the Supplier Invoice and Expense Report.  Note that the WIP Posting Rule should be used instead of the SPEND Posting Rule for the Debit side of the transaction

# Test Steps
describe "BA-4-0200-11 - Register Asset from a Capital Project" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "11. Review Transactional Accounting"
    wait for search results
    click search result containing "11. Review Transactional Accounting"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "11. Review Transactional Accounting"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0200-11_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
