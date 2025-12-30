# CC-2-0030 - Change Customer Contract
# Confidence Score: 8.5/10.0
# Role: Customer Contract Specialist

## AUTOMATED TEST
## Description: Find and pull up an existing customer contract. Related Actions > Change Customer Contract. Change contract header to include header details such as PO, Description, etc. Verify changes are made successfully.

# Test Steps
describe "CC-2-0030 - Change Customer Contract" do

  # Setup
  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Change Customer Contract" do
    # Step 1: Navigate to task
    navigate_to_task "Customer Contract > Related Actions > Change Customer Contract"
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
## Results for: Revenue Management Change Customer Contract Customer Contract > Related Actions > Change Customer Contract

### 1. Admin Guide Education And Government (score: 8)
Source: Admin-Guide-Education-and-Government.pdf
```
Education and
Government
Product Summary
December 10, 2025
 | Contents | ii
Contents
Education and Government..................................................................
