# CC-4-0070-17 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Project Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: You should see transactions for your project on the "Transactions Ready to Review" tab  Hit the Review Transactions button for any of the transactions. Choose actions for each billable line. Try to choose an action of each type (Approve, Do Not Bill, Mark as Ready to Bill)

# Test Steps
describe "CC-4-0070-17 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Project Manager"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "17. Review Billable Project Transactions"
    wait for search results
    click search result containing "17. Review Billable Project Transactions"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Project"

    # Step 3: Validate key elements present
    verify page contains "17. Review Billable Project Transactions"

    # Step 5: Take screenshot evidence
    screenshot as "CC-4-0070-17_complete.png"

    # Additional Sub-Task: Go to Project Billing Work Area
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Project Billing Work Area
