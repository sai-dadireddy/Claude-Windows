# BA-2-0230 - Register Asset from Supplier Invoice
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create a supplier invoice with a line for a trackable spend category above the depreciation threshold amount and a line below the threshold amount. Complete any supplier invoice approvals required

# Test Steps
describe "BA-2-0230 - Register Asset from Supplier Invoice" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Register Asset from Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "1. Create Supplier Invoice for Business Asset"
    wait for search results
    click search result containing "1. Create Supplier Invoice for Business Asset"
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
    screenshot as "BA-2-0230_created.png"

    # Additional Sub-Task: Create Supplier Invoice
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Create Supplier Invoice
