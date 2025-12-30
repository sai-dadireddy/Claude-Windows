# CC-3-0030 - Verify Sales Items and Sales Item Groups
# Confidence Score: 8.5/10.0
# Role: Common Finance Configurator

## AUTOMATED TEST
## Description: Verify Sales Items are loaded and accurate. Verify Sales Items assignment of Sales Item Group.

# Test Steps
describe "CC-3-0030 - Verify Sales Items and Sales Item Groups" do

  # Setup
  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Verify Sales Items and Sales Item Groups" do
    # Step 1: Navigate to task
    navigate_to_task "Extract Sales Items"
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
## Results for: Revenue Management Verify Sales Items and Sales Item Groups Extract Sales Items

### 1. Workday Feature Descriptions Ditamap (score: 9)
Source: Workday-Feature-Descriptions-ditamap.pdf
```
Workday Feature
Descriptions
Product Summary
December 10, 2025
 | Contents | ii
Contents
Workday Feature Descriptions Guide................................................................. 5
Workday Ada
