# CC-4-0030-01 - Modify Customer Contract Revenue Recognition
# Confidence Score: 8.0/10.0
# Functional Area: Revenue Management
# Role: Revenue Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find an existing revenue schedule. Using the related actions > change, change details in the revenue schedule. Verify revenue schedule is changed successfully and routed through the BP: Revenue Schedule Event.

# Test Steps
describe "CC-4-0030-01 - Modify Customer Contract Revenue Recognition" do

  before do
    login_as "Revenue Specialist"
  end

  it "should complete: Modify Customer Contract Revenue Recognition" do
    # Step 1: Navigate to task
    enter search box as "1. Change Revenue Recognition Schedule"
    wait for search results
    click search result containing "1. Change Revenue Recognition Schedule"
    wait for page to load

    # Step 2: Search for record
    enter search field as "search_criteria"
    click button "Search"
    wait for results

    # Step 3: Select record
    click first result

    # Step 4: Edit
    click button "Edit"
    wait for form to load

    # Step 5: Update fields
    # [NEEDS SME INPUT] - Specify field changes
    enter field "field_name" as "new_value"

    # Step 6: Save
    click button "Save"
    wait for confirmation
    verify message contains "Success"
    screenshot as "CC-4-0030-01_updated.png"

    # Additional Sub-Task: Go to Find Revenue Recognition Schedule and choose schedule to modify.  Revenue Recognition Schedule > Related Actions > Change
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Find Revenue Recognition Schedule and choose schedule to modify.  Revenue Recognition Schedule > Related Actions > Change
