# BA-4-0030-03 - Register Asset from a Supplier Invoice
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: As Business Asset Accountant, go to the Inbox and complete asset accounting information and Submit. Confirm the defaulted accounting information for depreciation profile, convention, and useful life are as expected from Asset Book Rules.  If these defaults are not correct then review the asset book rules for the asset's spend category.

# Test Steps
describe "BA-4-0030-03 - Register Asset from a Supplier Invoice" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Supplier Invoice" do
    # Step 1: Navigate to task
    enter search box as "5. Assign Asset Accounting Information"
    wait for search results
    click search result containing "5. Assign Asset Accounting Information"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 5. Assign Asset Accounting Information

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0030-03_complete.png"

    # Additional Sub-Task: Inbox (BA Accountant)
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Inbox (BA Accountant)
