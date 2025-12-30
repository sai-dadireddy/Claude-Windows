# CC-2-0090 - Verify that Schedules have been created
# Confidence Score: 9.5/10.0
# Role: Customer Contract Specialist

## AUTOMATED TEST
## Description: Go to Previously created customer contract and navigate to the "Schedules" Tab to verify that there is a Revenue Recognition and Billing Schedule in Approved Status.

# Test Steps
describe "CC-2-0090 - Verify that Schedules have been created" do

  # Setup
  before do
    login_as "Customer Contract Specialist"
  end

  it "should complete: Verify that Schedules have been created" do
    # Step 1: Navigate to task
    navigate_to_task "Find Customer Contracts"
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
## Results for: Revenue Management Verify that Schedules have been created Find Customer Contracts

### 1. WSDL: Resource_Management (score: 11)
Source: Resource_Management.wsdl
```
WSDL: Resource_Management
Description: The Resource Management  Web Service contains operations that expose Workday Financials Resource Management data. It includes data relative to Suppliers, Supplier Accounts, Expenses, Bus
