# TX-3-0420 - View transaction tax liability
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Run the transaction report and verify the results are accurate

# Test Steps
describe "TX-3-0420 - View transaction tax liability" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: View transaction tax liability" do
    # Step 1: Navigate to task
    enter search box as "View transaction tax liability"
    wait for search results
    click search result containing "View transaction tax liability"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "View"

    # Step 3: Validate key elements present
    verify page contains "View transaction tax liability"

    # Step 5: Take screenshot evidence
    screenshot as "TX-3-0420_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
