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
## Sources
- [2025 RAG Guide](https://www.edenai.co/post/the-2025-guide-to-retrieval-augmented-generation-rag)
- [RAG Best Practices Research](https://arxiv.org/abs/2501.07391)
- [Stack Overflow RAG Tips](https://stackoverflow.blog/2024/08/15/practical-tips-for-retrieval-augmented-generation-rag/)
