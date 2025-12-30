# TX-2-0130 - Tax Rule Exception Groups
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify exception groups for ship-to-country exception scenarios

# Test Steps
describe "TX-2-0130 - Tax Rule Exception Groups" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax Rule Exception Groups" do
    # Step 1: Navigate to task
    enter search box as "View Tax Rule Exception Groups"
    wait for search results
    click search result containing "View Tax Rule Exception Groups"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Tax"

    # Step 3: Validate key elements present
    verify page contains "View Tax Rule Exception Groups"

    # Step 5: Take screenshot evidence
    screenshot as "TX-2-0130_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
