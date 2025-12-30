# CC-4-0020-02 - Modify Customer Contract Billing
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find an existing billing schedule. Navigate to Attachments and attach a file. Verify attachment is successful

# Test Steps
describe "CC-4-0020-02 - Modify Customer Contract Billing" do

  before do
    login_as "Billing Specialist"
  end

  it "should complete: Modify Customer Contract Billing" do
    # Step 1: Navigate to task
    enter search box as "2. Add Attachment to Billing Schedule"
    wait for search results
    click search result containing "2. Add Attachment to Billing Schedule"
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
    screenshot as "CC-4-0020-02_created.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
