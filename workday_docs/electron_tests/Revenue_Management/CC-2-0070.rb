# CC-2-0070 - Create Customer Contract
# Confidence Score: 8.5/10.0
# Role: Customer Contract Specialist

## AUTOMATED TEST
## Description: Create Customer Contract. Enter a contract line for 12,000 using any revenue category under Goods & Services. Mark it as "Deferred" Revenue Treatment in the "Revenue and Billing" Tab and include Revenue Recognition Schedule Template. Add an Installment Billing Schedule Template on the Billing Tab. Ensure customer contract routes successfully through the BP: Customer Contract Event. Default is initiation ony.

# Test Steps
describe "CC-2-0070 - Create Customer Contract" do

  # Setup
  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Create Customer Contract" do
    # Step 1: Navigate to task
    navigate_to_task "Create Customer Contract"
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
## Results for: Revenue Management Create Customer Contract Create Customer Contract

### 1. Admin Guide Education And Government (score: 5)
Source: Admin-Guide-Education-and-Government.pdf
```
Education and
Government
Product Summary
December 10, 2025
 | Contents | ii
Contents
Education and Government.................................................................................6
Grants Management....
