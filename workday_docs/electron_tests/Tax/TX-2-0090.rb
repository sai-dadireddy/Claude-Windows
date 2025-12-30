# TX-2-0090 - Tax transaction rules for items
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax rules for items configuration

# Test Steps
describe "TX-2-0090 - Tax transaction rules for items" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax transaction rules for items" do
    # Step 1: Navigate to task
    navigate_to_task "View Transaction Tax Rule for Items"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-2-0090_verification"
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
## Results for: Tax Tax transaction rules for items View Transaction Tax Rule for Items

### 1. Kb Expense Report (score: 7)
Source: kb_expense_report.txt
```
================================================================================
WORKDAY KB ARTICLE: CREATE EXPENSE REPORT BUSINESS PROCESS
================================================================================

Source: Workday Community 
