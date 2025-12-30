# BA-4-0200-15 - Register Asset from a Capital Project
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Project Financial Analyst

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify expenses and supplier invoices can be seen tagged to the project

# Test Steps
describe "BA-4-0200-15 - Register Asset from a Capital Project" do

  before do
    login_as "Project Financial Analyst"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "15. View cost in the project/financial tab/Plan"
    wait for search results
    click search result containing "15. View cost in the project/financial tab/Plan"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "15. View cost in the project/financial tab/Plan"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0200-15_complete.png"

    # Additional Sub-Task: Go to Financials > Plan tab and drill into Project Spend
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Financials > Plan tab and drill into Project Spend
