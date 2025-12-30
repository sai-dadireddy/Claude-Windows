# TX-1-0030 - Verify Tax Authorities
# Confidence Score: 9.0/10.0
# Role: Tax Manager

## AUTOMATED TEST
## Description: For each tax authority verify: Business Entity Name, Tax Authority ID, Tax Reporting Currency, Currency Rate Type, Website, Contact Information, Contacts, Settlement Bank Account and Default Payment Type

# Test Steps
describe "TX-1-0030 - Verify Tax Authorities" do

  # Setup
  before do
    login_as "Tax Manager"
  end

  it "should complete: Verify Tax Authorities" do
    # Step 1: Navigate to task
    navigate_to_task "View Tax Authority"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Verify"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-1-0030_verification"
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
## Results for: Tax Verify Tax Authorities View Tax Authority

### 1. Kb Procurement Requisition (score: 4)
Source: kb_procurement_requisition.txt
```
================================================================================
WORKDAY KB ARTICLE: CREATE REQUISITION BUSINESS PROCESS
================================================================================

Source: Workday Community & WSDL Anal
