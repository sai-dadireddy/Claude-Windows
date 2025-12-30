# CC-4-0050-02 - Milestone Based Contract & Billing
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Customer Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create Billing Schedule for Customer Contract created in previous step. On Billing Schedule Add Milestone by selecting Milestone > Create Date Milestone 

Review that installment Status now say "Pending Milestone"

# Test Steps
describe "CC-4-0050-02 - Milestone Based Contract & Billing" do

  before do
    login_as "Customer Billing Specialist"
  end

  it "should complete: Milestone Based Contract & Billing" do
    # Step 1: Navigate to task
    enter search box as "1a. Create Customer Contract with Customer Milestone"
    wait for search results
    click search result containing "1a. Create Customer Contract with Customer Milestone"
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
    screenshot as "CC-4-0050-02_created.png"

    # Additional Sub-Task: Create Billing Schedule for Customer Contract
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Create Billing Schedule for Customer Contract
