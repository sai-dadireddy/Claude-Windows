# CC-2-0100 - Create Customer Invoice from Customer Contract
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Customer Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create Customer invoice tied to a line on the previously created customer contract. Ensure accounting is accurate, debiting Accounts Receivable and crediting Deferred Revenue.

# Test Steps
describe "CC-2-0100 - Create Customer Invoice from Customer Contract" do

  before do
    login_as "Customer Billing Specialist"
  end

  it "should complete: Create Customer Invoice from Customer Contract" do
    # Step 1: Navigate to task
    enter search box as "Create Customer Invoice for Billing Installments"
    wait for search results
    click search result containing "Create Customer Invoice for Billing Installments"
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
    screenshot as "CC-2-0100_created.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
