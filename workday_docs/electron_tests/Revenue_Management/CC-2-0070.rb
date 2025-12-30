# CC-2-0070 - Create Customer Contract
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create Customer Contract. Enter a contract line for 12,000 using any revenue category under Goods & Services. Mark it as "Deferred" Revenue Treatment in the "Revenue and Billing" Tab and include Revenue Recognition Schedule Template. Add an Installment Billing Schedule Template on the Billing Tab. Ensure customer contract routes successfully through the BP: Customer Contract Event. Default is initiation ony.

# Test Steps
describe "CC-2-0070 - Create Customer Contract" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Create Customer Contract" do
    # Step 1: Navigate to task
    enter search box as "Create Customer Contract"
    wait for search results
    click search result containing "Create Customer Contract"
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
    screenshot as "CC-2-0070_created.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
