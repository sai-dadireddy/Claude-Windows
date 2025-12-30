# BA-4-0090-02 - Transfer Asset to Different Company
# Confidence Score: 6.5/10.0
# Functional Area: Asset Management
# Role: Business Asset Tracking Specialist

## [NEEDS SME REVIEW] - MEDIUM CONFIDENCE
## Description: As Business Asset Tracking Specialist, complete Asset Intercompany Transfer Out Event and Submit.

# This test requires SME input for:
# 1. Exact field names and selectors
# 2. Business logic validation
# 3. Data values and test data

describe "BA-4-0090-02 - Transfer Asset to Different Company" do

  before do
    login_as "Business Asset Tracking Specialist"
  end

  it "should complete: Transfer Asset to Different Company" do
    # Step 1: Navigate
    enter search box as "2. Asset Intercompany Transfer Out Event"
    wait for search results
    click search result containing "2. Asset Intercompany Transfer Out Event"
    wait for page to load

    # Step 2: Main actions
    # [SME REVIEW REQUIRED]
    # Task: 2. Asset Intercompany Transfer Out Event
    # Description: As Business Asset Tracking Specialist, complete Asset Intercompany Transfer Out Event and Submit.
    # Sub-Task: Inbox (BA Tracking Specialist)

    # Step 3: Validation
    # Expected Result: Define validation criteria

    # Step 4: Evidence
    screenshot as "BA-4-0090-02_complete.png"
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
