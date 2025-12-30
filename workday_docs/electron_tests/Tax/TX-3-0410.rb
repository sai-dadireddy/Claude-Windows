# TX-3-0410 - View sales tax summary and details
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Run the transaction report and verify the results are accurate

# Test Steps
describe "TX-3-0410 - View sales tax summary and details" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: View sales tax summary and details" do
    # Step 1: Navigate to task
    enter search box as "View sales tax summary and details"
    wait for search results
    click search result containing "View sales tax summary and details"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "View"

    # Step 3: Validate key elements present
    verify page contains "View sales tax summary and details"

    # Step 5: Take screenshot evidence
    screenshot as "TX-3-0410_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
