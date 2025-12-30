# BA-4-0200-03 - Register Asset from a Capital Project
# Confidence Score: 7.0/10.0
# Functional Area: Asset Management
# Role: Project Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Create project plan. Use Project Plan template if available.  Make sure Project Start Date = First Day of Current Month and Project End Date = Last Day of Current Year

# Test Steps
describe "BA-4-0200-03 - Register Asset from a Capital Project" do

  before do
    login_as "Project Administrator"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "3. Create Project Plan"
    wait for search results
    click search result containing "3. Create Project Plan"
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
    screenshot as "BA-4-0200-03_created.png"

    # Additional Sub-Task: Complete any required Approval Steps
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Complete any required Approval Steps
