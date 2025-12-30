# CC-4-0020-01 - Modify Customer Contract Billing
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find an existing billing schedule. Using the related actions > change, change details on the billing schedule. Verify billing schedule is changed successfully and routed through the BP: Billing Schedule Event.

# Test Steps
describe "CC-4-0020-01 - Modify Customer Contract Billing" do

  before do
    login_as "Billing Specialist"
  end

  it "should complete: Modify Customer Contract Billing" do
    # Step 1: Navigate to task
    enter search box as "1. Change Billing Schedule"
    wait for search results
    click search result containing "1. Change Billing Schedule"
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
    screenshot as "CC-4-0020-01_updated.png"

    # Additional Sub-Task: Go to Find Billing Schedule and choose schedule to modify.  Billing Schedule > Related Actions > Change
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Find Billing Schedule and choose schedule to modify.  Billing Schedule > Related Actions > Change
