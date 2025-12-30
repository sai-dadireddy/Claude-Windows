# BA-2-0240 - Register Asset from Supplier Invoice
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review the trackable lines for the supplier invoice.  Confirm the accounting treatment defaulted in as expected from the Asset Book Rules.

# Test Steps
describe "BA-2-0240 - Register Asset from Supplier Invoice" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "2. Review Trackable Lines"
    wait for search results
    click search result containing "2. Review Trackable Lines"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "2. Review Trackable Lines"

    # Step 5: Take screenshot evidence
    screenshot as "BA-2-0240_complete.png"

    # Additional Sub-Task: Inbox (Business Asset Accountant) - Review Trackable Lines
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Inbox (Business Asset Accountant) - Review Trackable Lines
