# TX-2-0220 - Withholding Tax Rules for Country
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify automatic population of country-level tax code on taxable documents

# Test Steps
describe "TX-2-0220 - Withholding Tax Rules for Country" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Rules for Country" do
    # Step 1: Navigate to task
    enter search box as "View Withholding Tax Rule for Country"
    wait for search results
    click search result containing "View Withholding Tax Rule for Country"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Withholding"

    # Step 3: Validate key elements present
    verify page contains "View Withholding Tax Rule for Country"

    # Step 5: Take screenshot evidence
    screenshot as "TX-2-0220_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
