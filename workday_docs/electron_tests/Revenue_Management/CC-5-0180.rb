# CC-5-0180 - Worktag Usages
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Common Finance Configurator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify all required Worktag Usages have been configured for:  Customer Contract

# Test Steps
describe "CC-5-0180 - Worktag Usages" do

  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Worktag Usages" do
    # Step 1: Navigate to task
    enter search box as "Maintain Worktag Usages"
    wait for search results
    click search result containing "Maintain Worktag Usages"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Maintain Worktag Usages

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-5-0180_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
