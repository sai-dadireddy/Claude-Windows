# CC-2-0040 - Amend Customer Contract
# Confidence Score: 9.0/10.0
# Role: Customer Contract Specialist

## AUTOMATED TEST
## Description: Find and pull up an existing customer contract. Related Actions > Amend Customer Contract. Add a line for 6,000 using any revenue category under Goods & Services. Uncheck deferred revenue. Update contract header amount. Submit and ensure customer contract amendment routes successfully through the BP: Customer Contract Amendment Event. Default is Initiation only.

# Test Steps
describe "CC-2-0040 - Amend Customer Contract" do

  # Setup
  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Amend Customer Contract" do
    # Step 1: Navigate to task
    navigate_to_task "Customer Contract > Related Actions > Amend Customer Contract"
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
## Results for: Revenue Management Amend Customer Contract Customer Contract > Related Actions > Amend Customer Contract

### 1. Admin Guide Education And Government (score: 8)
Source: Admin-Guide-Education-and-Government.pdf
```
Education and
Government
Product Summary
December 10, 2025
 | Contents | ii
Contents
Education and Government....................................................................
