# BA-4-0010 - Register Asset from a Supplier Invoice
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create supplier invoice: use a trackable spend category and choose cost centers for which there are are cost center managers assigned. Make sure amount for the trackable spend invoice line exceeds cost threshold from asset book rules.

# Test Steps
describe "BA-4-0010 - Register Asset from a Supplier Invoice" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Register Asset from a Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "1. Create Supplier Invoice"
    wait for search results
    click search result containing "1. Create Supplier Invoice"
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
    screenshot as "BA-4-0010_created.png"

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
