# TX-3-0250 - Withholding Tax Codes
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify attributes for withholding tax calculation

# Test Steps
describe "TX-3-0250 - Withholding Tax Codes" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Codes" do
    # Step 1: Navigate to task
    enter search box as "View Withholding Tax Codes"
    wait for search results
    click search result containing "View Withholding Tax Codes"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Withholding"

    # Step 3: Validate key elements present
    verify page contains "View Withholding Tax Codes"

    # Step 5: Take screenshot evidence
    screenshot as "TX-3-0250_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
