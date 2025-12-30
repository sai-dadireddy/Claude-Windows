# TX-3-0010 - Tax applicability
# Confidence Score: 9.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax applicability configuration

# Test Steps
describe "TX-3-0010 - Tax applicability" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax applicability" do
    # Step 1: Navigate to task
    navigate_to_task "View Tax Applicability"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0010_verification"
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
## Results for: Tax Tax applicability View Tax Applicability

### 1. Kb Procurement Purchase Order (score: 3)
Source: kb_procurement_purchase_order.txt
```
================================================================================
WORKDAY KB ARTICLE: CREATE PURCHASE ORDER BUSINESS PROCESS
================================================================================

Source: Workday Community & W
