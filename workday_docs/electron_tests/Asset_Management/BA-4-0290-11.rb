# BA-4-0290-11 - Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Accounting Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review the supplier invoice accounting.

# Test Steps
describe "BA-4-0290-11 - Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)" do

  before do
    login_as "Accounting Operations Lead"
  end

  it "should complete: Leases: Operating Lease Depreciation Expense (IFRS) (non multi-book)" do
    # Step 1: Navigate to task
    enter search box as "Find Journals > filter by Journal Source "Supplier Invoice""
    wait for search results
    click search result containing "Find Journals > filter by Journal Source "Supplier Invoice""
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Find Journals > filter by Journal Source "Supplier Invoice"

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0290-11_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
