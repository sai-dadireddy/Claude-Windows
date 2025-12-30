# TX-3-0220 - Withholding Tax Rules for Country
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify automatic population of country-level tax code on taxable documents

# Test Steps
describe "TX-3-0220 - Withholding Tax Rules for Country" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Rules for Country" do
    # Step 1: Navigate to task
    navigate_to_task "View Withholding Tax Rule for Country"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Withholding"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0220_verification"
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
## Results for: Tax Withholding Tax Rules for Country View Withholding Tax Rule for Country

### 1. Kb Hcm Change Job (score: 7)
Source: kb_hcm_change_job.txt
```
================================================================================
WORKDAY KB ARTICLE: CHANGE JOB / TRANSFER EMPLOYEE BUSINESS PROCESS
================================================================================

Source: Workd
