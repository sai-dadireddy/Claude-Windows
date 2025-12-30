# TX-5-0180 - Withholding Tax Rules for Items
# Confidence Score: 9.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify withholding tax rules for spend and revenue items

# Test Steps
describe "TX-5-0180 - Withholding Tax Rules for Items" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Rules for Items" do
    # Step 1: Navigate to task
    navigate_to_task "View Withholding Tax Rule for Items"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Withholding"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-5-0180_verification"
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
## Results for: Tax Withholding Tax Rules for Items View Withholding Tax Rule for Items

### 1. Kb Hcm Change Job (score: 7)
Source: kb_hcm_change_job.txt
```
================================================================================
WORKDAY KB ARTICLE: CHANGE JOB / TRANSFER EMPLOYEE BUSINESS PROCESS
================================================================================

Source: Workday C
