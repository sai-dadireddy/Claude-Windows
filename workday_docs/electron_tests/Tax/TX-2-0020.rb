# TX-2-0020 - 1099 and 1096 print form layouts
# Confidence Score: 8.5/10.0
# Functional Area: Tax
# Role: Finance Administrator

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the 1099 and 1096 print form layouts configuration

# Test Steps
describe "TX-2-0020 - 1099 and 1096 print form layouts" do

  before do
    login_as "Finance Administrator"
  end

  it "should complete: 1099 and 1096 print form layouts" do
    # Step 1: Navigate to task
    enter search box as "Edit 1099 and 1096 Print Form Layout"
    wait for search results
    click search result containing "Edit 1099 and 1096 Print Form Layout"
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
    screenshot as "TX-2-0020_updated.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
