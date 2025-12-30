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

## How to Search Workday Knowledge

### 1. RAG Query (Local - Fast)
```bash
cd workday_docs
python workday_rag.py "hire employee steps"
python workday_rag.py --list-wsdl
python workday_rag.py --wsdl Human_Resources
```

### 2. Community KB Search (Browser)
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

### Standard Operating Procedure v1.0

#### Purpose
Convert Workday test scenarios from Excel into detailed Electron automation steps for the ActiveGenie platform.

#### Scope
Applies to all 6,858 test scenarios across 20+ functional areas.

#### Procedure

**PHASE 1: INPUT PARSING**
```
1. Read Excel row
2. Extract key fields:
   - Scenario ID (unique identifier)
   - Functional Area (test category)
   - Task / Step (PRIMARY - what to search in Workday)
   - Scenario Description (what to validate)
   - Customer Expected Result (verification criteria)
```

**PHASE 2: KNOWLEDGE LOOKUP**
```
1. Query RAG: python workday_rag.py "{Task / Step}"
2. Check confidence score:
   - >= 8.0: Use RAG results directly
   - 5.0-7.9: Also check KB articles (kb_*.txt)
   - < 5.0: Use browser MCP to scrape Workday KB
3. Match REST/SOAP endpoints for API alternative
```

**PHASE 3: STEP GENERATION**
```
1. Start with: enter search box as "{Task / Step}"
2. Add navigation steps from RAG/KB
3. Add field interactions (enter, select, click)
4. Add verification: verify {Customer Expected Result}
5. Add screenshot: screenshot as "{Scenario ID}_complete.png"
```

**PHASE 4: OUTPUT FORMATTING**
```
1. Use Electron Test Output Template
2. Include all metadata from Excel
3. Add API alternatives if available
4. Flag low-confidence scenarios for review
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

## Confidence Scoring

| RAG Score | Confidence | Action | Output Flag |
|-----------|------------|--------|-------------|
| >= 8.0 | HIGH | Generate directly | `[CONFIDENCE: HIGH]` ✅ |
| 5.0-7.9 | MEDIUM | Check KB articles | `[CONFIDENCE: MEDIUM]` ⚠️ |
| < 5.0 | LOW | Scrape Workday KB or manual | `[CONFIDENCE: LOW]` ❌ |

**ALWAYS display confidence score in output header.**

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
