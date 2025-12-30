# TX-5-0210 - Withholding Tax Status
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify withholding tax status for use in withholding tax rules

# Test Steps
describe "TX-5-0210 - Withholding Tax Status" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Status" do
    # Step 1: Navigate to task
    enter search box as "View Withholding Tax Statuses"
    wait for search results
    click search result containing "View Withholding Tax Statuses"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Withholding"

    # Step 3: Validate key elements present
    verify page contains "View Withholding Tax Statuses"

    # Step 5: Take screenshot evidence
    screenshot as "TX-5-0210_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
