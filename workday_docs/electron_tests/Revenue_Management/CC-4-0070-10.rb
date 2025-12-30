# CC-4-0070-10 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Enter a Supplier Invoice, coding to the Project. Select the Billable Checkbox  Carry the time through any approval process.  Complete any required steps until the Invoice is approved.

# Test Steps
describe "CC-4-0070-10 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "10. Enter Supplier Invoice"
    wait for search results
    click search result containing "10. Enter Supplier Invoice"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 10. Enter Supplier Invoice

    # Step 3: Validation
    verify task completed successfully
    screenshot as "CC-4-0070-10_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
