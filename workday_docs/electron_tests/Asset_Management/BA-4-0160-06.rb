# BA-4-0160-06 - Dispose of an Asset
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review accounting information based on disposal method (discard, sale, donation, expire)

# Test Steps
describe "BA-4-0160-06 - Dispose of an Asset" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Dispose of an Asset" do
    # Step 1: Navigate to task
    enter search box as "3. Confirm GL activity"
    wait for search results
    click search result containing "3. Confirm GL activity"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 3. Confirm GL activity

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0160-06_complete.png"

    # Additional Sub-Task: Cost Detail Tab > Related Action > Cost Activity > Accounting > View Accounting
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Cost Detail Tab > Related Action > Cost Activity > Accounting > View Accounting
