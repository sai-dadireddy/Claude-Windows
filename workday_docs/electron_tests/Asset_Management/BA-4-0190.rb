# BA-4-0190 - Change Asset Book Configuration Information For Non-Accounting Book
# Confidence Score: 9.0/10.0
# Functional Area: Asset Management
# Role: Tax Manager

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify that you can modify Asset Book configuration

# Test Steps
describe "BA-4-0190 - Change Asset Book Configuration Information For Non-Accounting Book" do

  before do
    login_as "Tax Manager"
  end

  it "should complete: Change Asset Book Configuration Information For Non-Accounting Book" do
    # Step 1: Navigate to task
    enter search box as "1. Change Asset Book Configuration"
    wait for search results
    click search result containing "1. Change Asset Book Configuration"
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
    screenshot as "BA-4-0190_updated.png"

    # Additional Sub-Task: Open Asset   
Go to Book tab  
Related action of one of the Non-Accounting Books> Asset Book Configuration > Change
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Open Asset   
Go to Book tab  
Related action of one of the Non-Accounting Books> Asset Book Configuration > Change
