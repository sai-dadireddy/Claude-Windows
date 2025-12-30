# BA-4-0300-12 - Leases: Operating Lease Multi-book
# Confidence Score: 6.0/10.0
# Functional Area: Asset Management
# Role: Supplier Contract Specialist

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Record interest expense for the operating lease.

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0300-12 - Leases: Operating Lease Multi-book" do

  before do
    login_as "Supplier Contract Specialist"
  end

  it "should complete: Leases: Operating Lease Multi-book" do
    # Step 1: Navigate
    enter search box as "Schedule Expense Recognition Accounting"
    wait for search results
    click search result containing "Schedule Expense Recognition Accounting"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: Schedule Expense Recognition Accounting
    # Description: Record interest expense for the operating lease.
    # Sub-Task: Run Now
Preview Installments for Criteria

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0300-12_complete.png"
  end

  after do
    logout
  end
end

# SME Actions Required:
# [ ] Define exact field names
# [ ] Specify test data values
# [ ] Define validation criteria
# [ ] Review business logic accuracy
