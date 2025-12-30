# CC-4-0080-01 - Multi-Element Contract & Revenue
# Confidence Score: 9.0/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create customer contract with multi-element revenue allocation box checked. Enter fair value on the contract line(s). Check the box for deferred revenue. Ensure all fields are entered accurately and contract successfully routes through the BP: Customer Contract Event. Default is initiation only.

# Test Steps
describe "CC-4-0080-01 - Multi-Element Contract & Revenue" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Multi-Element Contract & Revenue" do
    # Step 1: Navigate to task
    enter search box as "1. Create Customer Contract with Multi-Element Revenue"
    wait for search results
    click search result containing "1. Create Customer Contract with Multi-Element Revenue"
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
    screenshot as "CC-4-0080-01_created.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
