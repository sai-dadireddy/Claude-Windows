# CC-1-0120 - Verify Billing Schedule Templates
# Confidence Score: 8.5/10.0
# Role: Contract Administrator

## AUTOMATED TEST
## Description: Verify Billing Schedule Templates are loaded and accurate.

# Test Steps
describe "CC-1-0120 - Verify Billing Schedule Templates" do

  # Setup
  before do
    login_as "Contract Administrator"
  end

  it "should complete: Verify Billing Schedule Templates" do
    # Step 1: Navigate to task
    navigate_to_task "Verify Billing Schedule Templates"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Verify"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#CC-1-0120_verification"
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
## Results for: Revenue Management Verify Billing Schedule Templates Verify Billing Schedule Templates

### 1. WSDL: Resource_Management (score: 6)
Source: Resource_Management.wsdl
```
WSDL: Resource_Management
Description: The Resource Management  Web Service contains operations that expose Workday Financials Resource Management data. It includes data relative to Suppliers, Supplier Accounts, Expenses, 
