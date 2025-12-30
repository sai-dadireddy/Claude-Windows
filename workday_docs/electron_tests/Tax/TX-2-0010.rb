# TX-2-0010 - Tax applicability
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the tax applicability configuration

# Test Steps
describe "TX-2-0010 - Tax applicability" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax applicability" do
    # Step 1: Navigate to task
    enter search box as "View Tax Applicability"
    wait for search results
    click search result containing "View Tax Applicability"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Tax"

    # Step 3: Validate key elements present
    verify page contains "View Tax Applicability"

    # Step 5: Take screenshot evidence
    screenshot as "TX-2-0010_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
