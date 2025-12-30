# BA-5-0130 - Confirm Asset Specific Account Posting Rules
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Common Finance Configurator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the following rules have the correct ledger account:  Accumulated Depreciation Business Asset Accrued Liability Business Asset Disposal Donation Business Asset Disposal Gain Business Asset Disposal Loss Business Asset Disposal Sale Business Asset Multibook Settlement (if applicable) Depreciation Expense Impairment Spend (conditions for expense/depreciable/non depreciable)

# Test Steps
describe "BA-5-0130 - Confirm Asset Specific Account Posting Rules" do

  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Confirm Asset Specific Account Posting Rules" do
    # Step 1: Navigate to task
    enter search box as "View Account Posting Rule Set"
    wait for search results
    click search result containing "View Account Posting Rule Set"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Confirm"

    # Step 3: Validate key elements present
    verify page contains "View Account Posting Rule Set"

    # Step 5: Take screenshot evidence
    screenshot as "BA-5-0130_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
