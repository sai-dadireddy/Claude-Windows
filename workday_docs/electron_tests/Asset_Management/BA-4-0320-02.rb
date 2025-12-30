# BA-4-0320-02 - Leases: Finance Lease
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Accounting Operations Lead

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Review accounting for Initial Recognition of Lease.

# Test Steps
describe "BA-4-0320-02 - Leases: Finance Lease" do

  before do
    login_as "Accounting Operations Lead"
  end

  it "should complete: Leases: Finance Lease" do
    # Step 1: Navigate to task
    enter search box as "Find Journals > filter by Journal Source "Initial Recognition of Lease""
    wait for search results
    click search result containing "Find Journals > filter by Journal Source "Initial Recognition of Lease""
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: Find Journals > filter by Journal Source "Initial Recognition of Lease"

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0320-02_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
