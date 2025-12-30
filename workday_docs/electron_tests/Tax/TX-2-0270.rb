# TX-2-0270 - Assign Companies to VAT Group
# Confidence Score: 8.5/10.0
# Role: Finance Administrator

## AUTOMATED TEST
## Description: Verify company is assigned to a VAT group

# Test Steps
describe "TX-2-0270 - Assign Companies to VAT Group" do

  # Setup
  before do
    login_as "Finance Administrator"
  end

  it "should complete: Assign Companies to VAT Group" do
    # Step 1: Navigate to task
    navigate_to_task "Assign Companies to VAT or GST Groups"
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
## Results for: Tax Assign Companies to VAT Group Assign Companies to VAT or GST Groups

### 1. Admin Guide  Financial Management (score: 8)
Source: Admin-Guide--Financial-Management.pdf
```
Financial Management
Product Summary
December 18, 2025
 | Contents | ii
Contents
Financial Management...................................................................................... 26
Common Financial Componen
