# CC-4-0070-08 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 7.0/10.0
# Functional Area: Revenue Management
# Role: Employee As Self

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: For a Worker Assigned to the Project, log in and enter Time, coding to the Project.  Complete any required steps until the Time is approved.

# Test Steps
describe "CC-4-0070-08 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Employee As Self"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "8. Enter Time to Project"
    wait for search results
    click search result containing "8. Enter Time to Project"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 8. Enter Time to Project

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-4-0070-08_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
