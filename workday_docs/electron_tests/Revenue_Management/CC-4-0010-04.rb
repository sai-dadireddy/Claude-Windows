# CC-4-0010-04 - Create, Change and Amend Customer Contract
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find existing customer contract ("Find Customer Contracts"). Related Actions > Copy. Verify contract is copied successfully.

# Test Steps
describe "CC-4-0010-04 - Create, Change and Amend Customer Contract" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Create, Change and Amend Customer Contract" do
    # Step 1: Navigate to task
    enter search box as "5. Copy a Customer Contract"
    wait for search results
    click search result containing "5. Copy a Customer Contract"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 5. Copy a Customer Contract

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-4-0010-04_complete.png"

    # Additional Sub-Task: Customer Contract > Related Actions > Copy
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Customer Contract > Related Actions > Copy
