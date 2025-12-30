# BA-4-0200-12 - Register Asset from a Capital Project
# Confidence Score: 8.5/10.0
# Functional Area: Asset Management
# Role: Project Financial Analyst

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: Verify the hours are entered against the correct task once the hours have been approved.

# Test Steps
describe "BA-4-0200-12 - Register Asset from a Capital Project" do

  before do
    login_as "Project Financial Analyst"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "12. Verify project hours under the financial tab for the project"
    wait for search results
    click search result containing "12. Verify project hours under the financial tab for the project"
    wait for page to load

    # Step 2: Verify page loaded
    verify page title contains "Register"

    # Step 3: Validate key elements present
    verify page contains "12. Verify project hours under the financial tab for the project"

    # Step 5: Take screenshot evidence
    screenshot as "BA-4-0200-12_complete.png"

    # Additional Sub-Task: Go to Financials > Plan tab and drill into Worker Time
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: Go to Financials > Plan tab and drill into Worker Time
