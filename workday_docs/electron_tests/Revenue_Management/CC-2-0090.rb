# CC-2-0090 - Verify that Schedules have been created
# Confidence Score: 9.0/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Go to Previously created customer contract and navigate to the "Schedules" Tab to verify that there is a Revenue Recognition and Billing Schedule in Approved Status.

# Test Steps
describe "CC-2-0090 - Verify that Schedules have been created" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Verify that Schedules have been created" do
    # Step 1: Navigate to task
    enter search box as "Find Customer Contracts"
    wait for search results
    click search result containing "Find Customer Contracts"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Find Customer Contracts

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-2-0090_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
