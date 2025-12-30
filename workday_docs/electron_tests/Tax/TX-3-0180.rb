# TX-3-0180 - Maintain Withholding Tax Codes
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the maintain withholding tax codes configuration

# Test Steps
describe "TX-3-0180 - Maintain Withholding Tax Codes" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Maintain Withholding Tax Codes" do
    # Step 1: Navigate to task
    navigate_to_task "View Withholding Tax Code"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Maintain"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0180_verification"
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
## Results for: Tax Maintain Withholding Tax Codes View Withholding Tax Code

### 1. Admin Guide  Financial Management (score: 6)
Source: Admin-Guide--Financial-Management.pdf
```
Financial Management
Product Summary
December 18, 2025
 | Contents | ii
Contents
Financial Management...................................................................................... 26
Common Financial Components.........
