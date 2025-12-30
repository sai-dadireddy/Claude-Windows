# BA-4-0220-01 - Leases: Supplier Contract
# Confidence Score: 7.0/10.0
# Functional Area: Asset Management
# Role: Accounting Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create supplier contracts - fixed lease type

# Test Steps
describe "BA-4-0220-01 - Leases: Supplier Contract" do

  before do
    login_as "Accounting Operations Lead"
  end

  it "should complete: Leases: Supplier Contract" do
    # Step 1: Navigate to task
    enter search box as "Create Supplier Contract"
    wait for search results
    click search result containing "Create Supplier Contract"
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
    screenshot as "BA-4-0220-01_created.png"

    # Additional Sub-Task: Verify the initial recognition ( view accounting related actions)
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Verify the initial recognition ( view accounting related actions)
