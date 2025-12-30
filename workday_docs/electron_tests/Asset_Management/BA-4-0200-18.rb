# BA-4-0200-18 - Register Asset from a Capital Project
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create a Project Asset. Choose any trackable Spend Category Hit OK

# Test Steps
describe "BA-4-0200-18 - Register Asset from a Capital Project" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "18. Create Project Asset"
    wait for search results
    click search result containing "18. Create Project Asset"
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
    screenshot as "BA-4-0200-18_created.png"

    # Additional Sub-Task: Open Project, Navigate to Financials> Capitalization and hit the ADD PROJECT ASSETS Button
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Open Project, Navigate to Financials> Capitalization and hit the ADD PROJECT ASSETS Button
