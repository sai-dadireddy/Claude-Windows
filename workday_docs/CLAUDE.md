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

## Coveo Extraction (doc.workday.com)

Extract ALL search results via JS (no manual clicking):
```javascript
var e = document.querySelector("atomic-search-interface").engine;
var results = e.state.search.results;
JSON.stringify(results.map(function(r){
  return {title: r.title, url: r.clickUri, excerpt: r.excerpt};
}));
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
