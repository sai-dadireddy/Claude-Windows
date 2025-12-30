# CC-3-0160 - Confirm Role Based Customer Contract Assignments Assignments
# Confidence Score: 8.5/10.0
# Role: Security Administrator

## AUTOMATED TEST
## Description: Confirm that these Role Based Security Roles have been properly assigned or are defaulting to each Company:  Customer Contract Specialist  Billing Specialist  Revenue Specialist

# Test Steps
describe "CC-3-0160 - Confirm Role Based Customer Contract Assignments Assignments" do

  # Setup
  before do
    login_as "Security Administrator"
  end

  it "should complete: Confirm Role Based Customer Contract Assignments Assignments" do
    # Step 1: Navigate to task
    navigate_to_task "Roles for Organization and Subordinates"
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
## Results for: Revenue Management Confirm Role Based Customer Contract Assignments Assignments Roles for Organization and Subordinates

### 1. WSDL: Financial_Management (score: 12)
Source: Financial_Management.wsdl
```
WSDL: Financial_Management
Description: The Financial Management Web Service contains operations that expose Workday Financials data. It includes data relative to Accounts, Accounting, B
