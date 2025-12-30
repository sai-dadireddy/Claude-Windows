# CC-4-0050-04 - Milestone Based Contract & Billing
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Customer Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Populate contract criteria from item 1 and select installments to create invoices for. Process invoice(s). Verify accounting by Related Actions > Accounting > View Accounting

# Test Steps
describe "CC-4-0050-04 - Milestone Based Contract & Billing" do

  before do
    login_as "Customer Billing Specialist"
  end

  it "should complete: Milestone Based Contract & Billing" do
    # Step 1: Navigate to task
    enter search box as "3. Create Customer invoice for Customer Milestone Contract"
    wait for search results
    click search result containing "3. Create Customer invoice for Customer Milestone Contract"
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
    screenshot as "CC-4-0050-04_created.png"

    # Additional Sub-Task: Customer Contract Work Area > Create Customer Invoices from Billing Installments
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Customer Contract Work Area > Create Customer Invoices from Billing Installments
