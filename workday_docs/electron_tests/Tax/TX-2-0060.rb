# TX-2-0060 - Tax authorities
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax authorities configuration

# Test Steps
describe "TX-2-0060 - Tax authorities" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax authorities" do
    # Step 1: Navigate to task
    navigate_to_task "View Tax Authority"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-2-0060_verification"
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
## Results for: Tax Tax authorities View Tax Authority

### 1. WSDL: Financial_Management (score: 4)
Source: Financial_Management.wsdl
```
WSDL: Financial_Management
Description: The Financial Management Web Service contains operations that expose Workday Financials data. It includes data relative to Accounts, Accounting, Business Plans, Financial Reporting, Tax, Financial Organizations, Basic Worktags, 
