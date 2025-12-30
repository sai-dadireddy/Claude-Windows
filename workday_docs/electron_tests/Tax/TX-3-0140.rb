# TX-3-0140 - Tax Rule Exception for Country
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax rule exception configuration for country

# Test Steps
describe "TX-3-0140 - Tax Rule Exception for Country" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax Rule Exception for Country" do
    # Step 1: Navigate to task
    navigate_to_task "View Transaction Tax Rule Exception for Country"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0140_verification"
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
## Results for: Tax Tax Rule Exception for Country View Transaction Tax Rule Exception for Country

### 1. Workday Feature Descriptions Ditamap (score: 7)
Source: Workday-Feature-Descriptions-ditamap.pdf
```
Workday Feature
Descriptions
Product Summary
December 10, 2025
 | Contents | ii
Contents
Workday Feature Descriptions Guide................................................................. 5
Workday 
