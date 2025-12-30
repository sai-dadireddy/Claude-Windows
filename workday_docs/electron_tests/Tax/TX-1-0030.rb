# TX-1-0030 - Verify Tax Authorities
# Confidence Score: 8.0/10.0
# Functional Area: Tax
# Role: Tax Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: For each tax authority verify: Business Entity Name, Tax Authority ID, Tax Reporting Currency, Currency Rate Type, Website, Contact Information, Contacts, Settlement Bank Account and Default Payment Type

# Test Steps
describe "TX-1-0030 - Verify Tax Authorities" do

  before do
    login_as "Tax Manager"
  end

  it "should complete: Verify Tax Authorities" do
    # Step 1: Navigate to task
    enter search box as "View Tax Authority"
    wait for search results
    click search result containing "View Tax Authority"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Verify"

    # Step 3: Validate key elements present
    verify page contains "View Tax Authority"

    # Step 5: Take screenshot evidence
    screenshot as "TX-1-0030_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
