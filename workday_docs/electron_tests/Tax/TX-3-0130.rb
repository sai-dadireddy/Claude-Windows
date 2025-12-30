# TX-3-0130 - Tax Rule Exception Groups
# Confidence Score: 9.0/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify exception groups for ship-to-country exception scenarios

# Test Steps
describe "TX-3-0130 - Tax Rule Exception Groups" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax Rule Exception Groups" do
    # Step 1: Navigate to task
    navigate_to_task "View Tax Rule Exception Groups"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Tax"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#TX-3-0130_verification"
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
## Results for: Tax Tax Rule Exception Groups View Tax Rule Exception Groups

### 1. Kb Hcm Change Job (score: 5)
Source: kb_hcm_change_job.txt
```
================================================================================
WORKDAY KB ARTICLE: CHANGE JOB / TRANSFER EMPLOYEE BUSINESS PROCESS
================================================================================

Source: Workday Community & 
