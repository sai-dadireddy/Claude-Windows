# BA-4-0200-14 - Register Asset from a Capital Project
# Confidence Score: 7.5/10.0
# Functional Area: Asset Management
# Role: Project Financial Analyst

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the standard cost rate for the employee if not using fully burden rate

# Test Steps
describe "BA-4-0200-14 - Register Asset from a Capital Project" do

  before do
    login_as "Project Financial Analyst"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "14. View Standard cost in the project/financial tab/Plan"
    wait for search results
    click search result containing "14. View Standard cost in the project/financial tab/Plan"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "14. View Standard cost in the project/financial tab/Plan"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0200-14_complete.png"

    # Additional Sub-Task: Go to Financials > Plan tab and drill into Worker Time for "Project Cost (Standard Cost Rates)" line
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Financials > Plan tab and drill into Worker Time for "Project Cost (Standard Cost Rates)" line
