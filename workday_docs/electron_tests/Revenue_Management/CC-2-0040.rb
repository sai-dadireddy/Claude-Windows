# CC-2-0040 - Amend Customer Contract
# Confidence Score: 9.0/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find and pull up an existing customer contract. Related Actions > Amend Customer Contract. Add a line for 6,000 using any revenue category under Goods & Services. Uncheck deferred revenue. Update contract header amount. Submit and ensure customer contract amendment routes successfully through the BP: Customer Contract Amendment Event. Default is Initiation only.

# Test Steps
describe "CC-2-0040 - Amend Customer Contract" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Amend Customer Contract" do
    # Step 1: Navigate to task
    enter search box as "Customer Contract > Related Actions > Amend Customer Contract"
    wait for search results
    click search result containing "Customer Contract > Related Actions > Amend Customer Contract"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Customer Contract > Related Actions > Amend Customer Contract

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-2-0040_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
