# BA-4-0030-04 - Register Asset from a Supplier Invoice
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Upon approval, verify that Spend accounting entries have been created as expected via related action off the Supplier Invoice Transaction.  The accounting entries are generated after the business asset accountant reviews trackable lines, this test should be completed after the review trackable lines is completed.

# Test Steps
describe "BA-4-0030-04 - Register Asset from a Supplier Invoice" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Register Asset from a Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "6. Confirm Supplier Invoice Transaction to GL"
    wait for search results
    click search result containing "6. Confirm Supplier Invoice Transaction to GL"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 6. Confirm Supplier Invoice Transaction to GL

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0030-04_complete.png"

    # Additional Sub-Task: View Supplier Invoice Transaction
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: View Supplier Invoice Transaction
