# Workday Documentation RAG System

## Overview
This folder contains a comprehensive RAG (Retrieval-Augmented Generation) system for Workday API and business process documentation, designed to generate confident Electron test automation steps.

## RAG Statistics
- **117 Documents Indexed**
- 30 PDFs (Admin/User Guides)
- 14 REST API OpenAPI schemas
- 55 WSDLs (3,169 SOAP operations)
- 10 KB Articles (step-by-step automation guides)
- Test scenarios index (6,767 scenarios)

---

## Workday URLs & Resources

### Official Documentation
| Resource | URL |
|----------|-----|
| Documentation Portal | `https://doc.workday.com/en-us/guides.html` |
| REST API Directory | `https://community.workday.com/sites/default/files/file-hosting/restapi/index.html` |
| SOAP API Directory | `https://community.workday.com/sites/default/files/file-hosting/productionapi/index.html` |
| Community/KB | `https://resourcecenter.workday.com/en-us/wrc/home.html` |
| Developer Portal | `https://developer.workday.com/documentation` |

### REST API Schema URL Pattern
```
https://community.workday.com/sites/default/files/file-hosting/restapi/{serviceName}_{version}_{YYYYMMDD}_oas2.json
```

Example:
```
staffing_v7_20251227_oas2.json
payroll_v2_20251227_oas2.json
```

---

## MCP BROWSER ACCESS (For general-purpose agents)

When deployed as a `general-purpose` agent, you have full MCP browser access.

### Create Your Browser Tab (ALWAYS DO THIS FIRST)
```python
# Step 1: Get context
mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=True)

# Step 2: Create YOUR tab (NEVER share tabs)
result = mcp__claude-in-chrome__tabs_create_mcp()
TAB_ID = result["tabId"]  # Save this for all operations!

# Step 3: Navigate
mcp__claude-in-chrome__navigate(url="https://community.workday.com", tabId=TAB_ID)

# Step 4: Wait (anti-bot - REQUIRED)
mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=TAB_ID)

# Step 5: Screenshot to verify
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)
```

### Search and Extract Content
```python
# Find search box
mcp__claude-in-chrome__find(query="search box", tabId=TAB_ID)

# Enter search term
mcp__claude-in-chrome__form_input(ref="ref_id", value="hire employee", tabId=TAB_ID)

# Submit search
mcp__claude-in-chrome__computer(action="key", text="Enter", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=TAB_ID)

# Extract page text
mcp__claude-in-chrome__get_page_text(tabId=TAB_ID)
```

### Anti-Bot Rules (CRITICAL)
1. **Wait 2-5 seconds** between actions
2. **Scroll before clicking** (human-like behavior)
3. **Max 10-20 pages** per session
4. Use logged-in Chrome session
5. Close tabs when done: `mcp__claude-in-chrome__navigate(url="about:blank", tabId=TAB_ID)`

---

## Enhancement Tracker (For parallel agent coordination)

```bash
TRACKER="$HOME/OneDrive - ERPA/Claude/workday_docs/electron_tests/_scripts/enhancement_tracker.py"

# Claim a file for processing
python "$TRACKER" claim AGENT_ID AREA

# Check overall status
python "$TRACKER" status

# Reset stuck files
python "$TRACKER" reset

# Report completion (Python)
from enhancement_tracker import complete_file
complete_file('AGENT_ID', FILE_ID, success=True, new_confidence='HIGH',
              rag_updated=True, kb_updated=True, steps_added=5, validation_added=3)
```

---

## How to Search Workday Knowledge

### CRITICAL: RAG-FIRST THEN BROWSER FALLBACK

**MANDATORY WORKFLOW for all Workday agents:**

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Query RAG FIRST                                     │
│  python workday_rag.py "{Task name}"                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
    Score >= 7.0?                  Score < 7.0?
         ↓                                ↓
┌─────────────────┐         ┌─────────────────────────────────┐
│ ✅ USE RAG DATA │         │ 🌐 MUST USE BROWSER             │
│ Skip browser    │         │ Open Chrome tab and research    │
│ Generate test   │         │ at resourcecenter.workday.com   │
└─────────────────┘         └─────────────────────────────────┘
```

**RAG Score Decision Matrix:**
| Score | Action | Browser Required? |
|-------|--------|-------------------|
| **>= 7.0** | Use RAG directly | ❌ No |
| **5.0-6.9** | Try more RAG queries, check KB files | ⚠️ If still < 7.0 |
| **< 5.0** | **MUST open browser** | ✅ **YES - MANDATORY** |

**DO NOT just mark as MANUAL without trying browser first when score < 7.0!**

---

### 1. RAG Query (Local - Fast)
```bash
cd workday_docs
python workday_rag.py "hire employee steps"
python workday_rag.py --list-wsdl
python workday_rag.py --wsdl Human_Resources
```

### 2. Community KB Search (Browser) - REQUIRED when RAG < 7.0
1. Navigate to: `https://resourcecenter.workday.com`
2. Use search box for: `{task} business process steps`
3. Filter by: Functional Area (HCM, Payroll, Finance, etc.)
4. Look for AI-generated answers + source documents

### 3. REST API Discovery
```bash
# Download new API schema
curl -o {service}_v{version}.json "https://community.workday.com/sites/default/files/file-hosting/restapi/{service}_{version}_{date}_oas2.json"
```

---

## KB Article Format

When creating new KB articles, use this structure:

```markdown
# Workday {Task Name} Business Process - Knowledge Base

## Source
- URL: {documentation URL}
- Release: {version}
- Updated: {date}

## Overview
{Brief description of the business process}

## Key Components
### 1. Initiation
{How the process starts}

### 2. Steps and Subprocesses
{Detailed step breakdown}

## Implementation Steps
1. {Step 1}
2. {Step 2}
...

## Automation Considerations for Electron
1. **Navigation**: {How to navigate to this task}
2. **UI Selectors**: {Key elements to interact with}
3. **Validation**: {What to verify}
4. **Error Handling**: {Common issues}
5. **Screenshots**: {What to capture}

## Related Business Processes
- {Related process 1}
- {Related process 2}
```

---

## Excel-to-Electron Mapping Template

### Excel Column to Electron Step Mapping

| Excel Column | Electron Usage | Example |
|--------------|----------------|---------|
| `Scenario ID` | Test ID prefix | `HCM-1-0010` → `HCM-1-0010_step1.png` |
| `Functional Area` | Test category | `HCM`, `Payroll`, `Procurement` |
| `Scenario Name` | Test title | `Audit Company Setup` |
| `Scenario Description` | What to validate | Verify configuration... |
| `Task / Step` | **Primary Workday task** | `Extract Companies` → search for this |
| `Sub Task` | Additional steps | Secondary actions |
| `Customer Expected Result` | **Verification criteria** | What to verify |
| `Est. Effort (mins)` | Timeout/wait hints | 5 mins → short wait, 120 → long process |
| `Workday Role` | Permission context | `HR Administrator` |

### Electron Test Output Template

```
================================================================================
TEST ID: {Scenario ID}
FUNCTIONAL AREA: {Functional Area}
TEST NAME: {Scenario Name}
WORKDAY ROLE: {Workday Role}
EST. DURATION: {Est. Effort (mins)} minutes
================================================================================

DESCRIPTION:
{Scenario Description}

PREREQUISITES:
- User logged in with {Workday Role} permissions
- Required data: {inferred from description}

ELECTRON STEPS:
1. enter search box as "{Task / Step}"
2. wait for search results
3. click search result containing "{Task / Step}"
4. wait for page to load
5. {generated steps from RAG/KB lookup}
6. screenshot as "{Scenario ID}_complete.png"

VERIFICATION:
- [ ] {Customer Expected Result}
- [ ] No error messages displayed
- [ ] Task completed successfully

SUB-TASKS (if any):
{Sub Task - converted to additional steps}

API ALTERNATIVE:
- REST: {matched endpoint from RAG}
- SOAP: {matched operation from WSDL index}

================================================================================
```

---

## SOP: Excel-to-Electron Test Generation

### Standard Operating Procedure v2.0

#### Purpose
Convert Workday test scenarios from Excel into detailed Electron automation steps for the ActiveGenie platform.

#### Scope
Applies to all 6,858 test scenarios across 48 functional areas.

#### Enhanced Workflow: SEARCH BEFORE CREATE

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Parse Excel Row                                    │
│  Extract: Scenario ID, Task/Step, Expected Result           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: Query RAG                                          │
│  python workday_rag.py "{Task / Step}"                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
    Score >= 7.0?                  Score < 7.0?
         ↓                                ↓
┌─────────────────┐         ┌─────────────────────────────────┐
│ PHASE 3a:       │         │ PHASE 3b: ENHANCE KNOWLEDGE     │
│ Generate Test   │         │ 1. Search KB articles (kb_*.txt)│
│ (Valid Electron)│         │ 2. If still < 7.0:              │
└─────────────────┘         │    → Scrape Workday KB (browser)│
                            │    → Download missing docs       │
                            │ 3. Re-calculate confidence       │
                            └─────────────────────────────────┘
                                          ↓
                            ┌─────────────┴─────────────┐
                            ↓                           ↓
                      Now >= 7.0?              Still < 7.0?
                            ↓                           ↓
                  ┌─────────────────┐     ┌─────────────────────┐
                  │ Generate Test   │     │ Generate MANUAL file│
                  │ (Valid Electron)│     │ (No placeholder     │
                  └─────────────────┘     │  steps - just flag) │
                                          └─────────────────────┘
```

#### PHASE 1: INPUT PARSING
```
1. Read Excel row
2. Extract key fields:
   - Scenario ID (unique identifier)
   - Task / Step (PRIMARY - what to search)
   - Scenario Description (what to validate)
   - Customer Expected Result (verification)
3. Skip rows with empty Task/Step → Flag as INCOMPLETE
```

#### PHASE 2: INITIAL RAG QUERY
```bash
python workday_rag.py "{Task / Step}"
```
- Extract confidence score from response
- If >= 7.0 → Proceed to generate
- If < 7.0 → Go to PHASE 3b (enhance knowledge)

#### PHASE 3a: GENERATE TEST (Score >= 7.0)
```
Only generate VALID Electron commands:
1. enter search box as "{Task / Step}"
2. click search result "{exact text from RAG}"
3. wait for page to load
4. {specific field interactions from RAG}
5. verify {Customer Expected Result}
6. screenshot as "{Scenario ID}_complete.png"
```

#### PHASE 3b: ENHANCE KNOWLEDGE (Score < 7.0)
```
STEP 1: Search local KB articles
  - Check kb_hcm_*.txt for HCM tasks
  - Check kb_payroll_*.txt for Payroll tasks
  - Match functional area to KB

STEP 2: If still < 7.0, use browser MCP to scrape Workday KB

  **CRITICAL: CREATE YOUR OWN TAB FIRST!**
  # Step 1: Create own tab (NEVER share with other agents)
  context = mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=True)
  new_tab = mcp__claude-in-chrome__tabs_create_mcp()
  tabId = new_tab.id  # Use THIS tabId for ALL calls

  # Step 2: Navigate and search
  mcp__claude-in-chrome__navigate(url="https://resourcecenter.workday.com", tabId=tabId)
  mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=tabId)
  mcp__claude-in-chrome__find(query="search box", tabId=tabId)
  mcp__claude-in-chrome__form_input(ref="search_ref", value="{Task / Step}", tabId=tabId)
  mcp__claude-in-chrome__computer(action="key", text="Enter", tabId=tabId)
  mcp__claude-in-chrome__get_page_text(tabId=tabId)

  **BROWSER TAB ISOLATION RULES:**
  - ALWAYS create own tab with tabs_create_mcp()
  - NEVER reuse tabs from other agents
  - wait 2-5 seconds between actions
  - scroll before clicking
  - max 10-20 pages per session

STEP 3: Save new knowledge to KB
  - Create kb_{area}_{task}.txt
  - Add to RAG index

STEP 4: Re-query RAG with enhanced knowledge
```

#### PHASE 4: OUTPUT DECISION
```
IF confidence >= 7.0:
  → Generate test file with valid Electron commands
  → Status: ✅ ACCEPTED

ELSE IF confidence 5.0-6.9:
  → Generate test with [NEEDS SME REVIEW] flag
  → Include what RAG found
  → List specific fields that need SME input
  → Status: ⚠️ REVIEW REQUIRED

ELSE (confidence < 5.0):
  → Generate MANUAL file only
  → NO placeholder steps
  → Include reason: "Insufficient KB coverage"
  → Status: ❌ MANUAL REQUIRED
```

#### KB Enhancement Commands
```bash
# Search existing KB
ls workday_docs/private/kb_*.txt

# Create new KB article after scraping
cat > workday_docs/private/kb_{area}_{task}.txt << 'EOF'
# {Task Name} - Knowledge Base
Source: Workday Community KB
Date: {today}

## Steps
1. Navigate to {task}
2. {field interactions}
3. Submit

## Field Names
- {actual field names from UI}
EOF

# Re-index RAG
python workday_rag.py --rebuild
```

#### Decision Tree

```
Excel Row
    │
    ├── Has "Task / Step"?
    │   ├── YES → Query RAG → Generate steps
    │   └── NO → Mark as INCOMPLETE, skip
    │
    ├── RAG Score >= 8.0?
    │   ├── YES → High confidence, generate directly
    │   └── NO → Check KB articles
    │
    ├── KB Article exists?
    │   ├── YES → Merge with RAG results
    │   └── NO → Score < 5.0? → Scrape Workday KB
    │
    └── Output formatted Electron test
```

#### Quality Checklist

- [ ] Scenario ID included in all screenshots
- [ ] Task / Step used as primary search term
- [ ] Verification matches Customer Expected Result
- [ ] API alternative provided when available
- [ ] Est. Effort considered for wait times
- [ ] Workday Role noted for permission context

#### Batch Processing Command

```bash
# Generate Electron tests for a functional area
python generate_electron_tests.py --area "HCM" --output tests/hcm/

# Generate single test
python generate_electron_tests.py --scenario "HCM-1-0010" --output tests/
```

---

## Electron Command Reference

| Command | Syntax | Example |
|---------|--------|---------|
| Search | `enter search box as "{text}"` | `enter search box as "Hire Employee"` |
| Click Result | `click search result "{text}"` | `click search result "Hire Employee"` |
| Wait | `wait for page to load` | `wait 3 seconds` |
| Enter Text | `enter {field} as "{value}"` | `enter worker as "21001"` |
| Select | `select {dropdown} as "{value}"` | `select reason as "Resignation"` |
| Click Button | `click button "{text}"` | `click button "Submit"` |
| Click Link | `click link "{text}"` | `click link "View Details"` |
| Verify | `verify {condition}` | `verify message contains "Success"` |
| Screenshot | `screenshot as "{filename}"` | `screenshot as "HCM-1-0010_done.png"` |
| Navigate | `navigate to "{task}"` | `navigate to "Related Actions"` |
| Scroll | `scroll to "{element}"` | `scroll to "Submit button"` |

---

## Confidence Scoring & Acceptance Criteria

| RAG Score | Confidence | Status | Action |
|-----------|------------|--------|--------|
| **>= 7.0** | HIGH | ✅ ACCEPTED | Valid Electron steps generated |
| **5.0-6.9** | MEDIUM | ⚠️ NEEDS REVIEW | SME must enhance before use |
| **< 5.0** | LOW | ❌ MANUAL REQUIRED | Cannot generate - mark as MANUAL |

**CRITICAL RULES:**
1. **ACCEPTED (>= 7.0)**: All steps must be valid Electron commands
2. **NEEDS REVIEW (5.0-6.9)**: Mark with `[NEEDS SME REVIEW]` - steps may be incomplete
3. **MANUAL (< 5.0)**: Do NOT generate placeholder steps - only generate MANUAL file

**INVALID - Never generate these:**
```
❌ [RAG data available but no specific steps found]
❌ [MANUAL] No RAG guidance available
❌ follow standard task flow
❌ complete required fields
❌ fill appropriate values
```

**VALID - Only use actual Electron commands:**
```
✅ enter search box as "Hire Employee"
✅ click button "Submit"
✅ select dropdown "Reason" as "Resignation"
✅ verify message contains "Success"
✅ screenshot as "HCM-1-0010_complete.png"
```

**If RAG doesn't provide specific field names → Mark as MANUAL, don't guess.**

---

## CRITICAL RULES

### 1. NO HALLUCINATIONS
- NEVER invent Workday task names or UI elements
- ONLY use task names from Excel "Task / Step" column
- ONLY use field names found in RAG/KB results
- If unsure, mark as `[NEEDS VERIFICATION]`
- Say "I don't know" rather than guess

### 2. ANTI-BOT PATTERNS (KB Scraping)
```python
# Human-like behavior for Workday KB scraping:
wait(3)              # 2-5 second delays
scroll_down()        # Scroll before clicking
wait(2)              # Pause between actions
# Max 10 pages per session
# Use YOUR logged-in session
```

### 3. DATA VALIDATION
- Scenario ID prefix must match area (HCM-, USP-, PRO-)
- Flag Est. Effort > 120 mins as unusual
- Validate Functional Area (48 known areas)

### 4. OUTPUT QUALITY
- Include confidence score in EVERY output
- Cite source: `[Source: RAG]`, `[Source: KB]`, `[INFERRED]`
- Flag incomplete: `[INCOMPLETE: missing Task/Step]`

### 5. VERIFICATION CHECKLIST
```
Before claiming "done":
- [ ] Confidence score displayed
- [ ] No invented task names
- [ ] Screenshots use Scenario ID
- [ ] Verification matches Excel
```

---

## File Structure

```
workday_docs/
├── CLAUDE.md              # This file
├── workday_rag.py         # RAG query tool
├── download_config.json   # Download URLs config
├── public/                # REST API schemas (14 files)
│   ├── staffing_v7.json
│   ├── payroll_v2.json
│   └── ...
├── private/               # PDFs + KB articles
│   ├── Admin-Guide-*.pdf  # Admin guides
│   ├── User-Guide-*.pdf   # User guides
│   ├── kb_*.txt           # KB articles (10)
│   └── test_scenarios.xlsx # Excel scenarios
└── wsdl/                  # SOAP WSDLs (55 files)
    ├── Human_Resources.wsdl
    ├── Payroll.wsdl
    └── ...
```

---

## Top Functional Areas (from Excel)

| Area | Scenarios | Key Tasks |
|------|-----------|-----------|
| HCM | 439 | Change Job, Terminate, Hire |
| Accounting & Finance | 389 | Journal Entry, Settlement |
| Procurement | 336 | Requisition, Purchase Order |
| Inventory | 313 | Consigned, Putaway |
| Payroll US | 312 | Run Payroll, Pay Calc |
| Benefits | 254 | Enrollment, Change Benefits |
| Talent | 203 | Calibration, Performance |

---

## MCP Access Required

Agents working with this system need:
- `mcp__claude-in-chrome__*` - Browser automation
- `mcp__playwright__*` - Cross-browser testing
- `Read`, `Write`, `Glob`, `Grep` - File operations

---

## Usage Examples

### Query RAG for automation steps:
```python
from workday_rag import WorkdayRAG
rag = WorkdayRAG()
results = rag.search("terminate employee", top_k=3)
for r in results:
    print(f"{r['doc']['title']}: {r['score']}")
```

### Generate Electron steps from scenario:
```
Input: "Terminate Employee" from HCM area
Output:
1. enter search box as "Terminate Employee"
2. click search result "Terminate Employee"
3. enter worker field as "{worker_id}"
4. select reason as "{termination_reason}"
5. enter last day worked as "{date}"
6. click submit
7. verify confirmation message
```
