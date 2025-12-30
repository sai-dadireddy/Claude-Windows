# TX-5-0250 - Company Tax Status
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the Tax Status is assigned to the company

# Test Steps
describe "TX-5-0250 - Company Tax Status" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Company Tax Status" do
    # Step 1: Navigate to task
    navigate_to_task "Related Action from Company - View Company Tax Details - Tax Statuses"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Company"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-5-0250_verification"
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
## Results for: Tax Company Tax Status Related Action from Company - View Company Tax Details - Tax Statuses

### 1. Admin Guide Adaptive Planning And Consolidation (score: 10)
Source: Admin-Guide-Adaptive-Planning-and-Consolidation.pdf
```
Adaptive Planning
and Consolidation
Product Summary
December 10, 2025
 | Contents | ii
Contents
Adaptive Planning and Consolidation (AP&C)............................
