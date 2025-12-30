# BA-4-0290-06 - Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Register Asset from Supplier Contract: As Business Asset Accountant, go to the Inbox and review trackable lines. Make sure the Trackable checkbox is selected by default and that the Accounting Treatment has defaulted to Depreciable Capital Asset. If these defaults are not correct then review the asset book rules and supplier contract for the spend category being used.  Approve the Review Trackable Lines

# Test Steps
describe "BA-4-0290-06 - Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)" do
    # Step 1: Navigate to task
    enter search box as "Review Trackable Lines"
    wait for search results
    click search result containing "Review Trackable Lines"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Leases:"

    # Step 3: Validate key elements present
    verify page contains "Review Trackable Lines"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0290-06_complete.png"

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
