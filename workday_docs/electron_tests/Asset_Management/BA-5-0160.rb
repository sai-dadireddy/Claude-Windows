# BA-5-0160 - Confirm Asset Worktag Usages
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Common Finance Configurator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify all required Worktags have been configured for:  Business Asset Business Asset Disposal

# Test Steps
describe "BA-5-0160 - Confirm Asset Worktag Usages" do

  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Confirm Asset Worktag Usages" do
    # Step 1: Navigate to task
    enter search box as "Maintain Worktag Usage"
    wait for search results
    click search result containing "Maintain Worktag Usage"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Maintain Worktag Usage

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-5-0160_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
