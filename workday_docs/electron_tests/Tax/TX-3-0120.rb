# TX-3-0120 - Tax rules for country
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax rules for country configuration

# Test Steps
describe "TX-3-0120 - Tax rules for country" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax rules for country" do
    # Step 1: Navigate to task
    navigate_to_task "View Transaction Tax Rule for Country"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0120_verification"
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
## Results for: Tax Tax rules for country View Transaction Tax Rule for Country

### 1. Admin Guide Adaptive Planning And Consolidation (score: 7)
Source: Admin-Guide-Adaptive-Planning-and-Consolidation.pdf
```
Adaptive Planning
and Consolidation
Product Summary
December 10, 2025
 | Contents | ii
Contents
Adaptive Planning and Consolidation (AP&C).................................................... 7
Fin
