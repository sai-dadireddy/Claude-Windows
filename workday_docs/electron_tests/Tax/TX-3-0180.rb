# TX-3-0180 - Maintain Withholding Tax Codes
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the maintain withholding tax codes configuration

# Test Steps
describe "TX-3-0180 - Maintain Withholding Tax Codes" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Maintain Withholding Tax Codes" do
    # Step 1: Navigate to task
    enter search box as "View Withholding Tax Code"
    wait for search results
    click search result containing "View Withholding Tax Code"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Maintain"

    # Step 3: Validate key elements present
    verify page contains "View Withholding Tax Code"

    # Step 5: Take screenshot evidence
    screenshot as "TX-3-0180_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
