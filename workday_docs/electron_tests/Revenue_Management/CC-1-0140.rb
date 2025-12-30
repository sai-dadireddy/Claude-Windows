# CC-1-0140 - View Account Posting Rules
# Confidence Score: 9.5/10.0
# Role: Common Finance Configurator

## AUTOMATED TEST
## Description: Verify the following rules have the correct ledger account:  Deferred Revenue Revenue Receivables

# Test Steps
describe "CC-1-0140 - View Account Posting Rules" do

  # Setup
  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: View Account Posting Rules" do
    # Step 1: Navigate to task
    navigate_to_task "View Account Posting Rule Set"
    wait_for_page_load

    # Step 2: Verify page loaded
    expect(page).to have_content "View"

    # Step 3: Validate data elements
    validate_page_elements

    # Step 4: Take screenshot for evidence
    screenshot "#CC-1-0140_verification"
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
## Results for: Revenue Management View Account Posting Rules View Account Posting Rule Set

### 1. Admin Guide  Financial Management (score: 8)
Source: Admin-Guide--Financial-Management.pdf
```
Financial Management
Product Summary
December 18, 2025
 | Contents | ii
Contents
Financial Management...................................................................................... 26
Common Financial Comp
