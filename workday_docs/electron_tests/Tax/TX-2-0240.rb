# TX-2-0240 - Withholding Tax Rates
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify attributes for withholding tax calculation

# Test Steps
describe "TX-2-0240 - Withholding Tax Rates" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Withholding Tax Rates" do
    # Step 1: Navigate to task
    navigate_to_task "View Withholding Tax Rate"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Withholding"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-2-0240_verification"
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
## Results for: Tax Withholding Tax Rates View Withholding Tax Rate

### 1. Kb Hcm Change Job (score: 5)
Source: kb_hcm_change_job.txt
```
================================================================================
WORKDAY KB ARTICLE: CHANGE JOB / TRANSFER EMPLOYEE BUSINESS PROCESS
================================================================================

Source: Workday Community & WSDL Anal
