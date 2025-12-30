# BA-4-0200-10 - Register Asset from a Capital Project
# Confidence Score: 7.0/10.0
# Functional Area: Asset Management
# Role: Accounts Payable Data Entry Specialist

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Enter a Supplier Invoice. Carry the time through any approval process.  Complete any required steps until the Invoice is approved.

# Test Steps
describe "BA-4-0200-10 - Register Asset from a Capital Project" do

  before do
    login_as "Accounts Payable Data Entry Specialist"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "10. Enter Supplier Invoice"
    wait for search results
    click search result containing "10. Enter Supplier Invoice"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 10. Enter Supplier Invoice

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0200-10_complete.png"
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: None
