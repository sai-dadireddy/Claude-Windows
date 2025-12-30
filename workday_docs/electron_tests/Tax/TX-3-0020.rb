# TX-3-0020 - 1099 and 1096 print form layouts
# Confidence Score: 8.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the 1099 and 1096 print form layouts configuration

# Test Steps
describe "TX-3-0020 - 1099 and 1096 print form layouts" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: 1099 and 1096 print form layouts" do
    # Step 1: Navigate to task
    navigate_to_task "Edit 1099 and 1096 Print Form Layout"
    wait_for_page_load

    # Step 2: Search for record
    search_for "record_identifier"

    # Step 3: Open record
    click_first_result

    # Step 4: Click Edit
    click_button "Edit"

    # Step 5: Update fields
    # [NEEDS SME REVIEW] - Specify exact field changes
    fill_in "field_name", with: "updated_value"

    # Step 6: Save changes
    click_button "Save"
    wait_for_success_message
  end

  # Cleanup
  after do
    logout
  end
end

# RAG Context:
# Loaded 63 docs from public/private
Loaded 55 WSDLs with 3169 operations
Total: 118 documents
## Results for: Tax 1099 and 1096 print form layouts Edit 1099 and 1096 Print Form Layout

### 1. Admin Guide Release Notes (score: 8)
Source: Admin-Guide-Release-Notes.pdf
```
Administrator Guide
Release Notes
Product Summary
December 18, 2025
 | Contents | ii
Contents
About Workday Documentation...........................................................................5
October 31, 2025................
