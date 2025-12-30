# BA-4-0280-05 - Record interest expense for the operating lease.
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Supplier Contract Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Schedule Expense Recognition Accounting

# Test Steps
describe "BA-4-0280-05 - Record interest expense for the operating lease." do

  before do
    login_as "Supplier Contract Specialist"
  end

  it "should complete: Record interest expense for the operating lease." do
    # Step 1: Navigate to task
    enter search box as "Run Now
Preview Installments for Criteria"
    wait for search results
    click search result containing "Run Now
Preview Installments for Criteria"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Record"

    # Step 3: Validate key elements present
    verify page contains "Run Now
Preview Installments for Criteria"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0280-05_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
