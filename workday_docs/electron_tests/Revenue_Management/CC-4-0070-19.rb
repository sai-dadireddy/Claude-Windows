# CC-4-0070-19 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: As a related action off the invoice, go to Accounting > View Accounting  Verify Accounting

# Test Steps
describe "CC-4-0070-19 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Billing Specialist"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate to task
    enter search box as "19.Create Customer Invoices for Billable Transactions"
    wait for search results
    click search result containing "19.Create Customer Invoices for Billable Transactions"
    wait for page to load

    # Step 2: Initiate creation
    click button "Create" or click link "New"
    wait for form to load

    # Step 3: Fill required fields
    # [NEEDS SME INPUT] - Specify exact field names and values
    enter field "field_name_1" as "value_1"
    enter field "field_name_2" as "value_2"

    # Step 4: Submit
    click button "Submit"
    wait for confirmation

    # Step 5: Verify success
    verify message contains "Success" or verify message contains "Completed"
    screenshot as "CC-4-0070-19_created.png"

    # Additional Sub-Task: View Customer Invoice Accounting
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: View Customer Invoice Accounting
