# TX-5-0240 - VAT Groups
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify VAT group configuration

# Test Steps
describe "TX-5-0240 - VAT Groups" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: VAT Groups" do
    # Step 1: Navigate to task
    navigate_to_task "View VAT or GST Groups"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "VAT"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-5-0240_verification"
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
## Results for: Tax VAT Groups View VAT or GST Groups

### 1. Kb Hcm Terminate Employee (score: 5)
Source: kb_hcm_terminate_employee.txt
```
================================================================================
WORKDAY KB ARTICLE: TERMINATE EMPLOYEE BUSINESS PROCESS
================================================================================

Source: Workday Community & WSDL Analysis
URL: 
