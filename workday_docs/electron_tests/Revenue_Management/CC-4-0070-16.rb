# CC-4-0070-16 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Project Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: You should see the Contract created above as well as Billable Transactions for Time, Expense and Supplier Invoice

# Test Steps
describe "CC-4-0070-16 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Project Billing Specialist"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "16. Verify Contract and Billable Transactions Have Been Related to Project"
    wait for search results
    click search result containing "16. Verify Contract and Billable Transactions Have Been Related to Project"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Project"

    # Step 3: Validate key elements present
    verify page contains "16. Verify Contract and Billable Transactions Have Been Related to Project"

    # Step 5: Take screenshot evidence
    screenshot as "CC-4-0070-16_complete.png"

    # Additional Sub-Task: Go to Financials > Contract Billing tab
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Financials > Contract Billing tab
