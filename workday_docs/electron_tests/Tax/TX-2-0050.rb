# TX-2-0050 - Tax categories
# Confidence Score: 8.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify the tax categories configuration

# Test Steps
describe "TX-2-0050 - Tax categories" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Tax categories" do
    # Step 1: Navigate to task
    navigate_to_task "Tax Categories"
    wait_for_page_load

  end

  # Cleanup
  after do
    logout
  end
end

# RAG Context:
# Loaded 63 docs from public/private
Loaded 55 WSDLs with 3169 operations
Total: 118 documents
## Results for: Tax Tax categories Tax Categories

### 1. payroll (score: 2)
Source: payroll_v2.json
```
API: payroll
GET /jobs/{ID}/payGroup/{subresourceID} - Retrieves a single pay group instance.
GET /jobs/{ID}/payGroup - Retrieves the pay group for a specified job ID. This method always returns 1 pay group.
GET /payGroups/{ID} - Retrieves a single pay group instance.
GET /values/taxRatesGroup/compa..
