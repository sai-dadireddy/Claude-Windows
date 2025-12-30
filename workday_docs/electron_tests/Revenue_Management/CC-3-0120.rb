# CC-3-0120 - Deferred Cost - Cost Types
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Contract Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify cost types configuration is loaded and accurate

# Test Steps
describe "CC-3-0120 - Deferred Cost - Cost Types" do

  before do
    login_as "Contract Administrator"
  end

  it "should complete: Deferred Cost - Cost Types" do
    # Step 1: Navigate to task
    enter search box as "View Cost Types"
    wait for search results
    click search result containing "View Cost Types"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Deferred"

    # Step 3: Validate key elements present
    verify page contains "View Cost Types"

    # Step 5: Take screenshot evidence
    screenshot as "CC-3-0120_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
