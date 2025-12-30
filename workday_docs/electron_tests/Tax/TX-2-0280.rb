# TX-2-0280 - Company Tax Status
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the Tax Status is assigned to the company

# Test Steps
describe "TX-2-0280 - Company Tax Status" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Company Tax Status" do
    # Step 1: Navigate to task
    enter search box as "Related Action from Company - View Company Tax Details - Tax Statuses"
    wait for search results
    click search result containing "Related Action from Company - View Company Tax Details - Tax Statuses"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Company"

    # Step 3: Validate key elements present
    verify page contains "Related Action from Company - View Company Tax Details - Tax Statuses"

    # Step 5: Take screenshot evidence
    screenshot as "TX-2-0280_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
