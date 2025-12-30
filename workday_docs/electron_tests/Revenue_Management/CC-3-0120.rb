# CC-3-0120 - Deferred Cost - Cost Types
# Confidence Score: 9.0/10.0
# Role: Contract Administrator

## AUTOMATED TEST
## Description: Verify cost types configuration is loaded and accurate

# Test Steps
describe "CC-3-0120 - Deferred Cost - Cost Types" do

  # Setup
  before do
    login_as "Contract Administrator"
  end

  it "should complete: Deferred Cost - Cost Types" do
    # Step 1: Navigate to task
    navigate_to_task "View Cost Types"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "Deferred"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#CC-3-0120_verification"
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
## Results for: Revenue Management Deferred Cost - Cost Types View Cost Types

### 1. Kb Finance Journal Entry (score: 7)
Source: kb_finance_journal_entry.txt
```
================================================================================
WORKDAY KB ARTICLE: CREATE JOURNAL ENTRY BUSINESS PROCESS
================================================================================

Source: Workday Communi
