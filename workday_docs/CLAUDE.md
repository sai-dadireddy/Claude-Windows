# Workday RAG System

## Stats
- 117 docs (30 PDFs, 14 REST APIs, 55 WSDLs, 10 KB articles)
- 3,169 SOAP operations
- 6,767 test scenarios

## RAG Commands
```bash
cd ~/OneDrive\ -\ ERPA/Claude/workday_docs
python workday_rag.py "hire employee"     # Search
python workday_rag.py --list-wsdl         # List WSDLs
python workday_rag.py --list              # List REST APIs
```

## Confidence Decision
| Score | Action |
|-------|--------|
| >= 7.0 | Use RAG directly |
| < 7.0 | Use browser to research KB |

## URLs
| Resource | URL |
|----------|-----|
| Docs | doc.workday.com |
| REST API | community.workday.com/sites/default/files/file-hosting/restapi/ |
| Community | resourcecenter.workday.com |

## Search URL Structure (doc.workday.com)

**Base:** `https://doc.workday.com/en-us/search.html#q={QUERY}&numberOfResults=30&firstResult={offset}`

| Param | Purpose | Example |
|-------|---------|---------|
| `q=` | URL-encoded query | `q=%22Tax%20Applicabilities%22` |
| `numberOfResults=` | Per page (max 30) | `numberOfResults=30` |
| `firstResult=` | Pagination offset | Page N: `firstResult=(N-1)*30` |

**Pagination:**
- Page 1: `firstResult=0` (or omit)
- Page 2: `firstResult=30`
- Page 3: `firstResult=60`

## Coveo Extraction (doc.workday.com)

Extract results via JS:
```javascript
var e = document.querySelector("atomic-search-interface").engine;
var r = e.state.search.results;
// Get total count
var total = e.state.search.response.totalCount;
// Filter English Admin Guide only
var filtered = r.filter(x => x.clickUri.includes('/en-us/') && x.clickUri.includes('admin-guide'));
// Extract
JSON.stringify(filtered.map(x => ({title: x.title, url: x.clickUri, excerpt: x.excerpt})));
```

## Electron Commands
| Command | Example |
|---------|---------|
| enter | `enter search box as "Hire Employee"` |
| click | `click button "Submit"` |
| select | `select reason as "Resignation"` |
| verify | `verify message contains "Success"` |
| screenshot | `screenshot as "HCM-1-0010.png"` |
| wait | `wait for page to load` |

## File Structure
```
workday_docs/
├── workday_rag.py      # Query tool
├── public/             # REST APIs (14)
├── private/            # PDFs, KB articles
└── wsdl/               # SOAP WSDLs (55)
```

## Top Areas
HCM (439), Finance (389), Procurement (336), Inventory (313), Payroll US (312)

## KB Article Template
```
# {Task Name} KB
Source: {URL}
## Steps
1. ...
## Fields
- {field}: {values}
## Validation
- Success: "{message}"
```
