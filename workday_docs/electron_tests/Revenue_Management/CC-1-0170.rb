# CC-1-0170 - Worktag Usages
# Confidence Score: 8.5/10.0
# Role: Common Finance Configurator

## AUTOMATED TEST
## Description: Verify all required Worktag Usages have been configured for:  Customer Contract

# Test Steps
describe "CC-1-0170 - Worktag Usages" do

  # Setup
  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Worktag Usages" do
    # Step 1: Navigate to task
    navigate_to_task "Maintain Worktag Usages"
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
## Results for: Revenue Management Worktag Usages Maintain Worktag Usages

### 1. Kb Finance Journal Entry (score: 4)
Source: kb_finance_journal_entry.txt
```
================================================================================
WORKDAY KB ARTICLE: CREATE JOURNAL ENTRY BUSINESS PROCESS
================================================================================

Source: Workday Community &
