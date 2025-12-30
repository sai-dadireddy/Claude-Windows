# CC-2-0100 - Create Customer Invoice from Customer Contract
# Confidence Score: 8.5/10.0
# Role: Customer Billing Specialist

## AUTOMATED TEST
## Description: Create Customer invoice tied to a line on the previously created customer contract. Ensure accounting is accurate, debiting Accounts Receivable and crediting Deferred Revenue.

# Test Steps
describe "CC-2-0100 - Create Customer Invoice from Customer Contract" do

  # Setup
  before do
    login_as "Customer Billing Specialist"
  end

  it "should complete: Create Customer Invoice from Customer Contract" do
    # Step 1: Navigate to task
    navigate_to_task "Create Customer Invoice for Billing Installments"
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
## Results for: Revenue Management Create Customer Invoice from Customer Contract Create Customer Invoice for Billing Installments

### 1. Admin Guide Education And Government (score: 10)
Source: Admin-Guide-Education-and-Government.pdf
```
Education and
Government
Product Summary
December 10, 2025
 | Contents | ii
Contents
Education and Government.........................................................
