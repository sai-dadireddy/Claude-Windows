# CC-4-0070-04 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**
# Confidence Score: 6.0/10.0
# Functional Area: Revenue Management
# Role: Project Resource Manager

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: Assign resources to the project.  Choose any project role and use the Assign a Worker Allocation type.  Be sure to include a Start Date/End Date and % Allocation in order for Resource Forecast to be correct.  Add specific Worker to Resource Plan Line  Submit

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "CC-4-0070-04 - Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do

  before do
    login_as "Project Resource Manager"
  end

  it "should complete: Project Creation through Transaction Entry. Reporting and Approval of Billable Transactions (Billable Project) **Only Use for PSA Project**" do
    # Step 1: Navigate
    enter search box as "4. Add Resources to Project"
    wait for search results
    click search result containing "4. Add Resources to Project"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 4. Add Resources to Project
    # Description: Assign resources to the project.  Choose any project role and use the Assign a Worker Allocation type.  Be sure to include a Start Date/End Date and % Allocation in order for Resource Forecast to be correct.  Add specific Worker to Resource Plan Line  Submit
    # Sub-Task: Complete any required Approval Steps

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "CC-4-0070-04_complete.png"
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
