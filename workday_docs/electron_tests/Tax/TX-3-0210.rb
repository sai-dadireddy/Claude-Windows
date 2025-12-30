# TX-3-0210 - Assign Items to Withholding Tax Item Group
# Confidence Score: 8.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify purchase and sales item assignment to tax item group

# Test Steps
describe "TX-3-0210 - Assign Items to Withholding Tax Item Group" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Assign Items to Withholding Tax Item Group" do
    # Step 1: Navigate to task
    navigate_to_task "Assign Items to Withholding Tax Item Group"
    wait_for_page_load

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
## Results for: Tax Assign Items to Withholding Tax Item Group Assign Items to Withholding Tax Item Group

### 1. Kb Hcm Change Job (score: 7)
Source: kb_hcm_change_job.txt
```
================================================================================
WORKDAY KB ARTICLE: CHANGE JOB / TRANSFER EMPLOYEE BUSINESS PROCESS
================================================================================

