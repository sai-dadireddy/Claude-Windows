# CC-3-0020 - Verify Revenue Categories and Hierarchies
# Confidence Score: 9.0/10.0
# Role: Common Finance Configurator

## AUTOMATED TEST
## Description: Verify Revenue Categories are loaded and accurate. Verify the assignment of Revenue Hierarchies.

# Test Steps
describe "CC-3-0020 - Verify Revenue Categories and Hierarchies" do

  # Setup
  before do
    login_as "Common Finance Configurator"
  end

  it "should complete: Verify Revenue Categories and Hierarchies" do
    # Step 1: Navigate to task
    navigate_to_task "Extract Revenue Categories"
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
## Results for: Revenue Management Verify Revenue Categories and Hierarchies Extract Revenue Categories

### 1. Electron Test Samples (score: 6)
Source: electron_test_samples.txt
```
================================================================================
WORKDAY ELECTRON TEST SCENARIOS - SAMPLE SET
Generated: 2025-12-30
Source: test_scenarios_v2.xlsx
=============================================
