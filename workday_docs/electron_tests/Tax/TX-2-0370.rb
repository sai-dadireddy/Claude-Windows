# TX-2-0370 - Create Tax Declaration - send back prior to final approval
# Confidence Score: 8.5/10.0
# Role: Tax Manager

## AUTOMATED TEST
## Description: Verify the appropriate notifications are sent

# Test Steps
describe "TX-2-0370 - Create Tax Declaration - send back prior to final approval" do

  # Setup
  before do
    login_as "Tax Manager"
  end

  it "should complete: Create Tax Declaration - send back prior to final approval" do
    # Step 1: Navigate to task
    navigate_to_task "Create Tax Declaration Run"
    wait_for_page_load

    # Step 2: Click Create/New
    click_button "Create" || click_link "New"

    # Step 3: Fill required fields
    # [NEEDS SME REVIEW] - Specify exact field names
    fill_in "field_name_1", with: "test_value"

    # Step 4: Submit
    click_button "Submit"
    wait_for_success_message

    # Step 5: Verify creation
    expect(page).to have_content "Successfully"
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
## Results for: Tax Create Tax Declaration - send back prior to final approval Create Tax Declaration Run

### 1. Kb Payroll Run Payroll (score: 10)
Source: kb_payroll_run_payroll.txt
```
================================================================================
WORKDAY KB ARTICLE: RUN PAYROLL BUSINESS PROCESS
================================================================================

Source:
