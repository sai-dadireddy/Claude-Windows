# CC-4-0040-05 - Usage Based Contract & Billing
# Confidence Score: 7.5/10.0
# Functional Area: Revenue Management
# Role: Customer Billing Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review billable usage based transactions. Filter by billing status "Awaiting Review"

# Test Steps
describe "CC-4-0040-05 - Usage Based Contract & Billing" do

  before do
    login_as "Customer Billing Specialist"
  end

  it "should complete: Usage Based Contract & Billing" do
    # Step 1: Navigate to task
    enter search box as "4.1 Review Billable Usage Based Transactions"
    wait for search results
    click search result containing "4.1 Review Billable Usage Based Transactions"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Usage"

    # Step 3: Validate key elements present
    verify page contains "4.1 Review Billable Usage Based Transactions"

    # Step 5: Take screenshot evidence
    screenshot as "CC-4-0040-05_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
