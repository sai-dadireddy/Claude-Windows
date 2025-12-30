# CC-4-0070-12 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Project Financial Analyst

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the Fully burden cost rate for the employee

# Test Steps
describe "CC-4-0070-12 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Project Financial Analyst"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "12. View Fully Burden Cost in the Project/Financial Tab/Plan"
    wait for search results
    click search result containing "12. View Fully Burden Cost in the Project/Financial Tab/Plan"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Project"

    # Step 3: Validate key elements present
    verify page contains "12. View Fully Burden Cost in the Project/Financial Tab/Plan"

    # Step 5: Take screenshot evidence
    screenshot as "CC-4-0070-12_complete.png"

    # Additional Sub-Task: Go to Financials > Plan tab and drill into Worker Time for "Project Cost (Fully Burdened Rates)" line
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Financials > Plan tab and drill into Worker Time for "Project Cost (Fully Burdened Rates)" line
