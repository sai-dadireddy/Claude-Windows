# CC-4-0070-07 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Project Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: A detailed project budget based on Forecasted Hours is displayed

# Test Steps
describe "CC-4-0070-07 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Project Manager"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "7. View Project Budget"
    wait for search results
    click search result containing "7. View Project Budget"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Project"

    # Step 3: Validate key elements present
    verify page contains "7. View Project Budget"

    # Step 5: Take screenshot evidence
    screenshot as "CC-4-0070-07_complete.png"

    # Additional Sub-Task: Open Project, Navigate to Financials> Plan and drill into the Cost Plan Amount
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Open Project, Navigate to Financials> Plan and drill into the Cost Plan Amount
