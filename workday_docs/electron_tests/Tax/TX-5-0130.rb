# TX-5-0130 - Tax Rule Exception for Country
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the tax rule exception configuration for country

# Test Steps
describe "TX-5-0130 - Tax Rule Exception for Country" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax Rule Exception for Country" do
    # Step 1: Navigate to task
    enter search box as "View Transaction Tax Rule Exception for Country"
    wait for search results
    click search result containing "View Transaction Tax Rule Exception for Country"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Tax"

    # Step 3: Validate key elements present
    verify page contains "View Transaction Tax Rule Exception for Country"

    # Step 5: Take screenshot evidence
    screenshot as "TX-5-0130_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
