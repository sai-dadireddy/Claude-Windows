# Workday RAG System

## Stats (Updated 2026-01-01)
- 237 documents (182 KB/docs + 55 WSDLs)
- 30 PDFs, 14 REST APIs, 128 KB articles
- 3,169 SOAP operations
- 6,767 test scenarios

## RAG Commands
```bash
cd ~/OneDrive\ -\ ERPA/Claude/workday_docs
python workday_rag.py "hire employee"     # Search
python workday_rag.py --list-wsdl         # List WSDLs
python workday_rag.py --list              # List REST APIs
python workday_rag.py --rebuild           # Rebuild index
```

## Confidence Decision Matrix
| Score | Level | Action |
|-------|-------|--------|
| >= 7 | HIGH | Use RAG directly |
| 4-6 | MEDIUM | Use RAG + verify with browser |
| < 4 | LOW | Use browser to research KB |

---
## ANTI-BOT SCRAPING RULES (doc.workday.com)

### Human-Like Behavior
| Rule | Value | Why |
|------|-------|-----|
| Wait between pages | 3-5 seconds | Avoid rate limiting |
| Max searches/session | 10 topics | Anti-bot threshold |
| Random delays | +/- 1 second | Pattern breaking |
| Scroll before click | Yes | Natural behavior |
| Mouse movement | Simulate hover | Detection evasion |

### Session Management
```
1. Use Claude-in-Chrome (your logged-in session)
2. Create NEW tab for each session (tabs_create_mcp)
3. Don't reuse tab IDs across sessions
4. Take screenshots periodically (appears interactive)
```

### Request Pacing
```
Page 1-5:   3 second wait
Page 6-10:  4 second wait
Page 11+:   5 second wait
Between topics: 5-8 seconds
```

### Detection Avoidance
- Use quoted exact match queries: `"Tax Applicabilities"`
- Don't rapid-fire multiple searches
- Scroll to bottom before pagination
- Wait for `atomic-search-interface` to fully load
- Check for CAPTCHA/block before extraction

---
## URLs & Search Structure

| Resource | URL |
|----------|-----|
| Admin Guide | doc.workday.com/admin-guide/en-us/ |
| REST API | community.workday.com/sites/default/files/file-hosting/restapi/ |
| Community | resourcecenter.workday.com |

### Search URL Template
```
https://doc.workday.com/en-us/search.html#q={QUERY}&numberOfResults=30&firstResult={offset}
```

| Param | Purpose | Example |
|-------|---------|---------|
| `q=` | URL-encoded query (use quotes!) | `q=%22Tax%20Applicabilities%22` |
| `numberOfResults=` | Results per page (max 30) | `numberOfResults=30` |
| `firstResult=` | Pagination offset | `firstResult=30` (page 2) |

### Pagination Offsets
| Page | firstResult |
|------|-------------|
| 1 | 0 (or omit) |
| 2 | 30 |
| 3 | 60 |
| N | (N-1) * 30 |

---
## Coveo Extraction Scripts

### Step 1: Check Total Count
```javascript
var e = document.querySelector("atomic-search-interface").engine;
var total = e.state.search.response.totalCount;
var pages = Math.ceil(total / 30);
JSON.stringify({total: total, pages: pages});
```

### Step 2: Extract EN Admin Guide Results
```javascript
var e = document.querySelector("atomic-search-interface").engine;
var r = e.state.search.results;
var filtered = r.filter(x =>
  x.clickUri.includes('/en-us/') &&
  x.clickUri.includes('admin-guide')
);
JSON.stringify({
  count: filtered.length,
  titles: filtered.map(x => x.title)
});
```

### Step 3: Full Extraction (with URLs)
```javascript
var e = document.querySelector("atomic-search-interface").engine;
var r = e.state.search.results;
var filtered = r.filter(x =>
  x.clickUri.includes('/en-us/') &&
  x.clickUri.includes('admin-guide')
);
JSON.stringify(filtered.map(x => ({
  title: x.title,
  url: x.clickUri,
  excerpt: x.excerpt?.substring(0, 200)
})));
```

### Workflow
1. Navigate to search URL with quoted query
2. Wait 4 seconds for page load
3. Extract page 1 results
4. Navigate to page 2 (firstResult=30)
5. Wait 3 seconds, extract
6. Repeat until page 12 (pages 13+ are translations)
7. Save KB file with page-by-page summary

---
## RAG Best Practices (2025)

### Chunking Strategy
- **Optimal chunk size**: 500-1000 tokens
- **Overlap**: 10-20% between chunks
- **Semantic chunking**: Split at natural boundaries (sections, paragraphs)

### Retrieval Optimization
- **Hybrid search**: Combine keyword + vector search
- **Re-ranking**: Use cross-encoder for top results
- **Cache frequent queries**: Pre-index common searches

### Embedding Best Practices
- Use domain-specific embeddings when possible
- Normalize vectors for consistent similarity scores
- Compress vectors for faster retrieval (ANN indexes)

### Prompt Engineering
```
Use only the provided context.
If the answer is not in the context, say "I don't know."
Do not make up information.
```

### Quality Metrics
| Metric | Target |
|--------|--------|
| Precision@5 | > 80% |
| Recall@10 | > 90% |
| Factual accuracy | > 95% |

---
## DSL Executor (Playwright-based)

Run tests without Electron app using `_scripts/dsl_executor.py`:

```bash
cd electron_tests/_scripts
python dsl_executor.py ../Student_Application/STU-1-0010.txt              # Basic run
python dsl_executor.py ../Student_Application/STU-1-0010.txt --screenshots # Step-by-step proof
python dsl_executor.py ../Student_Application/STU-1-0010.txt --headless   # CI mode
```

### Key Implementation Details
| Feature | Implementation |
|---------|---------------|
| Dropdown selection | Label-index matching (`labels[i]` → `inputs[i]`) |
| Hierarchical dropdowns | ArrowDown → ArrowRight → Enter |
| Search button | Multiple Workday selectors with fallback |
| Screenshots | `screenshots/{test_name}/step_01_PASS.png` |

---

## Electron DSL Commands

Natural language commands for test scripts (see `private/kb_electron_dsl.txt`).

| Command | Example | Usage |
|---------|---------|-------|
| enter | `enter search box as "Hire Employee"` | Text input |
| click | `click button "Submit"` | Click element |
| select | `select reason as "Resignation"` | Dropdown |
| verify | `verify success message displays` | Assertion |
| screenshot | `screenshot as "HCM-1-0010.png"` | Capture |
| wait | `wait for page to load (3 seconds)` | Delay |
| navigate | `navigate back to Benefits Hub` | Navigation |
| complete | `complete required fields` | Form fill |
| review | `review configuration settings` | Visual check |

**Top commands (270+ scripts):**
- wait for search results (2899)
- wait for page to load (2784)
- click "Submit" (413)

---
## File Structure
```
workday_docs/
├── CLAUDE.md              # This file
├── workday_rag.py         # RAG query tool
├── research_tracker.txt   # KB research status
├── private/               # KB articles, PDFs (182 files)
├── public/                # REST API specs (14)
├── wsdl/                  # SOAP WSDLs (55)
├── electron_tests/        # Test scripts
├── skills/                # Workday skills
└── _archive/              # Old temp files
```

## Top Areas by Coverage
HCM (439), Finance (389), Procurement (336), Inventory (313), Payroll US (312)

---
## KB Article Template
```markdown
# Workday KB: {Task Name}
# Searched: {DATE}
# Query: "{EXACT QUERY}"
# Total Results: {N} ({M} English Admin Guide)
# Pages: {P}

## Summary by Page
Page 1: {X} EN Admin Guide results
Page 2: {Y} EN Admin Guide results
...
Pages {N}-17: 0 EN (translations only)

## Key Topics Found
- {Topic 1}
- {Topic 2}

## Primary URLs
- https://doc.workday.com/admin-guide/en-us/{area}/
```

---
## Electron Script Generation Process (2026-01-08)

### STEP-BY-STEP WORKFLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 1: QUERY RAG FIRST                                                      │
│ python workday_rag.py "{Task Name}"                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                            ↓
              ┌─────────────┴─────────────┐
              ↓                           ↓
    Score >= 7.0?                  Score < 7.0?
         ↓                                ↓
┌─────────────────┐         ┌─────────────────────────────────────────────────┐
│ USE RAG DATA    │         │ USE BROWSER TO MAP FIELDS                        │
│ Generate script │         │ 1. Login to Workday tenant                       │
│ directly        │         │ 2. Navigate to task                              │
└─────────────────┘         │ 3. Document ALL field names, types, options      │
                            │ 4. Note dropdowns vs text vs search fields       │
                            │ 5. Screenshot each dialog for reference          │
                            └─────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 2: CREATE SCRIPT WITH VARIABLES                                         │
│ - Use {{VARIABLE}} format for ALL tenant-specific data                       │
│ - Group in CUSTOM DATA VARIABLES section at top                              │
│ - Include default values as examples                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 3: TEST SCRIPT                                                          │
│ python dsl_executor.py <script.txt> --headless                              │
│ (Expect login failures in headless - validates DSL syntax only)             │
└─────────────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ STEP 4: CREATE EMAIL_SUMMARY.txt                                             │
│ - List ALL variables with descriptions                                       │
│ - Explain how to customize for different tenants                             │
│ - Include feedback checklist for reviewers                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Template Location
`electron_tests/_templates/ELECTRON_TEST_TEMPLATE.txt`

### Script Format (v4.0)
```
================================================================================
TEST: {TEST_ID} {Name}
AREA: {Module} > {Sub-Area}
CONFIDENCE: {X.X}/10
PRIORITY: {High|Medium|Low}
VERSION: 4.0 | UPDATED: {YYYY-MM-DD}
================================================================================

PURPOSE
{Why this test matters}

PREREQUISITES
- {Required role/permission}
- {Required data/setup}

--------------------------------------------------------------------------------
CUSTOM DATA VARIABLES
--------------------------------------------------------------------------------
# Tenant Configuration (UPDATE THESE FOR YOUR ENVIRONMENT)
{{TENANT_LOGIN_URL}} = https://your-tenant.workday.com/...
{{USERNAME}} = your_username
{{PASSWORD}} = your_password

# Task-Specific Fields (UPDATE THESE FOR TEST DATA)
{{FIELD_NAME}} = default_value

--------------------------------------------------------------------------------
AUTOMATED STEPS
--------------------------------------------------------------------------------
# Login Steps
Navigate to {{TENANT_LOGIN_URL}}
wait for 3 seconds
enter the username as {{USERNAME}}
wait for 1 second
enter the password as {{PASSWORD}}
click on the 'Sign In' button
wait for 5 seconds

# Task Steps
click on the 'Search' button
enter {Task Name} in the search field
wait for 3 seconds
click on '{Task Name}' link
wait for 3 seconds

# Form Fields
select {Field} as {{VARIABLE}}
wait for 1 second

# Exit
click cancel button
wait for 2 seconds

VERIFICATION:
- [ ] Login successful
- [ ] Task opens correctly
- [ ] Fields accept data

--------------------------------------------------------------------------------
FIELD REFERENCE
--------------------------------------------------------------------------------
| Field Name | Type | Required | Variable |
|------------|------|----------|----------|
| {Field}    | {Type} | {Yes/No} | {{VAR}} |

--------------------------------------------------------------------------------
ON FAILURE
--------------------------------------------------------------------------------
- {Step} fails: {Fallback action}

--------------------------------------------------------------------------------
EXPECTED OUTCOME
--------------------------------------------------------------------------------
- {Expected result}

================================================================================
```

### DSL Commands Reference (VALID)

| Command | Format | Example |
|---------|--------|---------|
| Navigate | `Navigate to {URL}` | `Navigate to {{TENANT_LOGIN_URL}}` |
| Wait | `wait for N seconds` | `wait for 3 seconds` |
| Username | `enter the username as {value}` | `enter the username as {{USERNAME}}` |
| Password | `enter the password as {value}` | `enter the password as {{PASSWORD}}` |
| Sign In | `click on the 'Sign In' button` | - |
| Search | `click on the 'Search' button` | - |
| Search Text | `enter {text} in the search field` | `enter Hire Employee in the search field` |
| Click Link | `click on '{text}' link` | `click on 'Hire Employee' link` |
| Select/Fill | `select {Field} as {value}` | `select Country as {{HIRE_COUNTRY}}` |
| Cancel | `click cancel button` | - |
| OK | `click OK button` | - |

### Variable Naming Convention

| Category | Prefix | Examples |
|----------|--------|----------|
| Tenant | None | `{{TENANT_LOGIN_URL}}`, `{{USERNAME}}`, `{{PASSWORD}}` |
| Hire | `HIRE_` | `{{HIRE_COUNTRY}}`, `{{HIRE_FIRST_NAME}}` |
| Employee | `EMPLOYEE_` | `{{EMPLOYEE_NAME}}`, `{{EMPLOYEE_ID}}` |
| Date | None | `{{EFFECTIVE_DATE}}`, `{{COVERAGE_START_DATE}}` |
| Deduction | `_DEDUCTION` | `{{MEDICAL_DEDUCTION}}`, `{{DENTAL_DEDUCTION}}` |

### Best Practices

1. **ALWAYS use {{VARIABLE}}** for tenant-specific data
2. **Group variables** by purpose (Tenant, Employee, Expected Values)
3. **Use `wait for N seconds`** - NOT `wait for page load`
4. **Use `select`** for ALL field types (works for dropdowns and text)
5. **End with `click cancel button`** for safe test exit
6. **Version scripts** (v4.0) with UPDATED date
7. **Create EMAIL_SUMMARY.txt** explaining variables for client

### Parallel Agent Coordination

**Tracker:** `electron_tests/script_tracker.txt`

| Status | Meaning |
|--------|---------|
| [_] | Pending |
| [G] | Generated |
| [V] | Verified |
| [R] | Needs Re-review |

**Agent IDs:** electron-1, electron-2, electron-3, electron-4

**Workflow:**
1. Check tracker for [_] pending scripts
2. Query RAG: `python workday_rag.py "{task}"`
3. Generate script if RAG >= 7.0
4. Update tracker with trust score
5. Mark [R] if trust < 7.0

### Confidence Scoring
| RAG Score | Trust | Action |
|-----------|-------|--------|
| >= 8.0 | HIGH (8-10) | Generate immediately |
| 5.0-7.9 | MEDIUM (5-7) | Generate + flag review |
| < 5.0 | LOW (1-4) | Mark MANUAL, skip |

### Strict Rules
1. **NO HALLUCINATIONS** - Only RAG/KB content
2. **NO GUESSING** - Unknown = MANUAL
3. **VERIFY** - Cross-check task names
4. **SCREENSHOT** - Every verification step
5. **UPDATE TRACKER** - Always log work

---
## Sources
- [2025 RAG Guide](https://www.edenai.co/post/the-2025-guide-to-retrieval-augmented-generation-rag)
- [RAG Best Practices Research](https://arxiv.org/abs/2501.07391)
- [Stack Overflow RAG Tips](https://stackoverflow.blog/2024/08/15/practical-tips-for-retrieval-augmented-generation-rag/)
