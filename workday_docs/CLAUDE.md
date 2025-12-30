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

## Electron Test Scenario Format

For generating Electron automation steps, use this format:

```
SCENARIO: {Scenario Name}
FUNCTIONAL AREA: {HCM/Payroll/Finance/etc.}
TASK: {Original task from Excel}

ELECTRON STEPS:
1. enter search box as "{task name}"
2. click search result "{exact result text}"
3. wait for page to load
4. select dropdown "{field}" as "{value}"
5. enter text field "{field}" as "{value}"
6. click button "{button text}"
7. verify message contains "{expected text}"
8. screenshot as "{scenario_name}_step{N}.png"

API ALTERNATIVE:
{REST/SOAP endpoint if available}

VALIDATION:
- [ ] {Validation check 1}
- [ ] {Validation check 2}
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
