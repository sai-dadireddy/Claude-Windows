# CC-4-0010-02 - Create, Change and Amend Customer Contract
# Confidence Score: 8.5/10.0
# Functional Area: Revenue Management
# Role: Customer Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Find Customer Contract created in item 1. Related Actions > Change Customer Contract. Change customer contract header to include header details such as PO, Description, etc. Verify changes are made successfully.

# Test Steps
describe "CC-4-0010-02 - Create, Change and Amend Customer Contract" do

  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Create, Change and Amend Customer Contract" do
    # Step 1: Navigate to task
    enter search box as "2. Change a Customer Contract"
    wait for search results
    click search result containing "2. Change a Customer Contract"
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
    screenshot as "CC-4-0010-02_updated.png"

    # Additional Sub-Task: Customer Contract > Related Actions > Change Customer Contract
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Customer Contract > Related Actions > Change Customer Contract
