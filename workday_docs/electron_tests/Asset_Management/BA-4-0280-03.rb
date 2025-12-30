# BA-4-0280-03 - Leases: Operating Lease Operating Expense (non multi-book)
# Confidence Score: 7.0/10.0
# Functional Area: Asset Management
# Role: Supplier Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create a Supplier Invoice from the Supplier Contract's Supplier Invoice schedule.

# Test Steps
describe "BA-4-0280-03 - Leases: Operating Lease Operating Expense (non multi-book)" do

  before do
    login_as "Supplier Contract Specialist"
  end

  it "should complete: Leases: Operating Lease Operating Expense (non multi-book)" do
    # Step 1: Navigate to task
    enter search box as "Create Supplier Invoices for Supplier Contract Installments"
    wait for search results
    click search result containing "Create Supplier Invoices for Supplier Contract Installments"
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
    screenshot as "BA-4-0280-03_created.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
