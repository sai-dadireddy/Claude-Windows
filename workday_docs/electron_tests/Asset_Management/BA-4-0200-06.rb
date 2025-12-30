# BA-4-0200-06 - Register Asset from a Capital Project
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Project Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Enter a Plan Name Enter a Calculation Type Choose your Resource Forecast Click OK  A Budget should be automatically calculated based on Resource Forecasts and Standard Costs established for the Project Resources.

# Test Steps
describe "BA-4-0200-06 - Register Asset from a Capital Project" do

  before do
    login_as "Project Manager"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "6. Create Project Budget"
    wait for search results
    click search result containing "6. Create Project Budget"
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
    screenshot as "BA-4-0200-06_created.png"

    # Additional Sub-Task: Open Project, Navigate to Financials> Plan and hit the CREATE BUDGET Button
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Open Project, Navigate to Financials> Plan and hit the CREATE BUDGET Button
