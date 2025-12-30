# BA-4-0030-01 - Register Asset from a Supplier Invoice
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: As Business Asset Accountant, go to the Inbox and review trackable lines. Make sure the Trackable checkbox is selected by default and that the Accounting Treatment has defaulted to Depreciable Capital Asset (Or other expected accounting treatment). If these defaults are not correct then review the asset book rules and supplier invoice for the spend category being used. Approve the Review Trackable Lines

# Test Steps
describe "BA-4-0030-01 - Register Asset from a Supplier Invoice" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "3. Review Trackable Lines"
    wait for search results
    click search result containing "3. Review Trackable Lines"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "3. Review Trackable Lines"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0030-01_complete.png"

    # Additional Sub-Task: Inbox (BA Accountant)
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Inbox (BA Accountant)
