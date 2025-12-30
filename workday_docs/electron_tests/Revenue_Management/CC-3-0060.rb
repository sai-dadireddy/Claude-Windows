# CC-3-0060 - Verify Schedule Types
# Confidence Score: 8.5/10.0
# Role: Contract Administrator

## AUTOMATED TEST
## Description: Verify Schedule Types are loaded and accurate.

# Test Steps
describe "CC-3-0060 - Verify Schedule Types" do

  # Setup
  before do
    login_as "Contract Administrator"
  end

  it "should complete: Verify Schedule Types" do
    # Step 1: Navigate to task
    navigate_to_task "Maintain Schedule Types"
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
## Results for: Revenue Management Verify Schedule Types Maintain Schedule Types

### 1. Workday Feature Descriptions Ditamap (score: 6)
Source: Workday-Feature-Descriptions-ditamap.pdf
```
Workday Feature
Descriptions
Product Summary
December 10, 2025
 | Contents | ii
Contents
Workday Feature Descriptions Guide................................................................. 5
Workday Adaptive Planning.
