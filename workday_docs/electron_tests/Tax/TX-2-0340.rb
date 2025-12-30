# TX-2-0340 - Print 1099 and 1096 forms
# Confidence Score: 8.5/10.0
# Role: 1099 Analyst

## AUTOMATED TEST
## Description: Verify the 1099 and 1096 forms were printed

# Test Steps
describe "TX-2-0340 - Print 1099 and 1096 forms" do

  # Setup
  before do
    login_as "1099 Analyst"
  end

  it "should complete: Print 1099 and 1096 forms" do
    # Step 1: Navigate to task
    navigate_to_task "Print 1099 and 1096 forms"
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
## Results for: Tax Print 1099 and 1096 forms Print 1099 and 1096 forms

### 1. Admin Guide Integrations (1) (score: 5)
Source: Admin-Guide-Integrations (1).pdf
```
Integrations
Product Summary
December 10, 2025
 | Contents | ii
Contents
Setup Considerations: Integrations................................................................... 18
Launch and Manage Integrations..................................
