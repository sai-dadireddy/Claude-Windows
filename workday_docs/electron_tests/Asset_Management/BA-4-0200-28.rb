# BA-4-0200-28 - Register Asset from a Capital Project
# Confidence Score: 8.0/10.0
# Functional Area: Asset Management
# Role: Business Asset Accountant

## AUTOMATED TEST - HIGH CONFIDENCE
## Description: On the Asset page, navigate to the Lifecycle page and find the Asset Registration event.  In the Operational Transaction column, choose related action off the Primary Book and select Accounting > View Accounting.  Verify that entry was a DR to the Fixed Asset Account and a CR to WIP

# Test Steps
describe "BA-4-0200-28 - Register Asset from a Capital Project" do

  before do
    login_as "Business Asset Accountant"
  end

  it "should complete: Register Asset from a Capital Project" do
    # Step 1: Navigate to task
    enter search box as "28. Confirm Project Capitalization Transaction to GL"
    wait for search results
    click search result containing "28. Confirm Project Capitalization Transaction to GL"
    wait for page to load

    # Step 2: Execute task
    # [NEEDS SME INPUT] - Define specific actions for: 28. Confirm Project Capitalization Transaction to GL

    # Step 3: Validation
    verify task completed successfully
    screenshot as "BA-4-0200-28_complete.png"

    # Additional Sub-Task: View Project Capitalization Accounting
    # [NEEDS SME INPUT] - Define steps for sub-task
  end

  after do
    logout
  end
end

# Business Context:
# Expected Result: Per business requirements
# Sub-Task: View Project Capitalization Accounting
