---
name: peoplesoft
description: Query PeopleSoft/Oracle knowledge base, scrape MOS articles, and get Integration Broker guidance
---

# /peoplesoft Skill

You are now in **PeopleSoft Expert Mode**. This skill runs in the main session with full MCP access for browser automation.

## Knowledge Base Location

```
~/OneDrive - ERPA/Claude/oracle_docs/
├── public/           # Public docs, REST APIs
├── private/          # MOS KB articles, patches (auth required)
├── peopletools/      # PeopleTools documentation (45 PDFs)
├── integration/      # Integration Broker guides
└── CLAUDE.md         # KB reference guide
```

## RAG Commands

```bash
KB_PATH="$HOME/OneDrive - ERPA/Claude/oracle_docs"

# Query documentation
python "$KB_PATH/oracle_rag.py" "your question"

# List all indexed docs
python "$KB_PATH/oracle_rag.py" --list

# List KB articles only
python "$KB_PATH/oracle_rag.py" --list-kb

# Get specific KB article
python "$KB_PATH/oracle_rag.py" --kb KB593233
```

## PeopleSoft API Architecture

| API Type | Format | Auth | PeopleTools | Best For |
|----------|--------|------|-------------|----------|
| REST | JSON | Basic/OAuth | 8.52+ | Modern integrations |
| SOAP | XML | WS-Security | All | Legacy, bulk data |
| ASF | JSON/OpenAPI | OAuth | 8.59+ | Modern REST, OpenAPI spec |

### REST Endpoint Format
```
https://{host}/PSIGW/RESTListeningConnector/{node}/{service}.v1/{resource}
```

### SOAP Endpoint Format
```
https://{host}/PSIGW/HttpListeningConnector
```

## Integration Broker Knowledge

**Key Components:**
- **Service Operations**: Define web service contracts
- **Documents**: Message structure (input/output)
- **Nodes**: Endpoint configuration
- **Routing**: Message routing rules
- **Handlers**: Application/Transform/Connector

### Creating REST Service
1. Define Documents (PeopleTools > Documents > Document Builder)
2. Create Messages (PeopleTools > Integration Broker > Messages)
3. Create Service Operation (Service Operations)
4. Publish Service (Provide Web Service wizard)

### Authentication
```bash
# Basic Auth
Authorization: Basic {base64(user:password)}

# OAuth 2.0 (PeopleTools 8.55+)
Authorization: Bearer {access_token}
```

---

## Browser Automation (Claude-in-Chrome)

**This skill has FULL MCP access.** Use for MOS scraping:

```python
# Get/create tab
context = mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=True)
tabId = context["availableTabs"][0]["tabId"]

# Navigate to MOS
mcp__claude-in-chrome__navigate(url="https://support.oracle.com/support/", tabId=tabId)
mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=tabId)

# Search for KB articles
mcp__claude-in-chrome__find(query="search box", tabId=tabId)
mcp__claude-in-chrome__form_input(ref="search_ref", value="PeopleSoft upgrade", tabId=tabId)
mcp__claude-in-chrome__computer(action="key", text="Enter", tabId=tabId)

# Extract content
mcp__claude-in-chrome__read_page(tabId=tabId)
```

### Anti-Bot Rules
- Wait 2-5 seconds between actions
- Scroll before clicking (human behavior)
- Max 10-20 page loads per session
- Use logged-in Chrome session (YOUR auth)

### Human Behavior Simulation
```python
# GOOD: Human-like pattern
mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=tabId)  # Think time
mcp__claude-in-chrome__computer(action="scroll", scroll_direction="down", scroll_amount=2, tabId=tabId)
mcp__claude-in-chrome__computer(action="wait", duration=1, tabId=tabId)  # Read time
mcp__claude-in-chrome__computer(action="left_click", ref="element_ref", tabId=tabId)
```

### Timing Best Practices

| Action | Delay After |
|--------|-------------|
| Page load | 3-5 seconds |
| Before click | 1-2 seconds |
| After form input | 0.5-1 second |
| Between pages | 5-10 seconds |
| Reading content | 2-4 seconds per scroll |

---

## Download Strategy

| Source | Method | Why |
|--------|--------|-----|
| **docs.oracle.com** (public) | `curl -sLO` | No auth, direct URLs |
| **MOS KB articles** (content) | Claude-in-Chrome `read_page` | Auth required |
| **MOS downloads** (PDFs/ZIPs) | Claude-in-Chrome **click** | JavaScript handlers |
| **PeopleBooks PDFs** | `curl -sLO` | Direct URLs, no auth |

### Public Docs - USE CURL
```bash
curl -sLO "https://docs.oracle.com/cd/G41076_01/psft/pdf/file.pdf"
```

### MOS Downloads - MUST CLICK (Not Curl)
MOS uses JavaScript handlers for downloads - direct URLs won't work:
```python
# Find and click download link
mcp__claude-in-chrome__find(query="PDF download", tabId=tabId)
mcp__claude-in-chrome__computer(action="left_click", ref="download_ref", tabId=tabId)
mcp__claude-in-chrome__computer(action="wait", duration=5, tabId=tabId)
# Then move: mv ~/Downloads/file.pdf ~/oracle_docs/private/
```

---

## MOS Document ID Mapping

Oracle migrated MOS in Dec 2025. Use mapping:
- Old: `2833770.1` → New: `KB42118`
- Mapping PDF: https://docs.oracle.com/cd/E52319_01/infoportal/pdfs/PeopleSoft_MOS_Document_ID_Mappings.pdf

---

## Key Resources

| Resource | URL |
|----------|-----|
| PeopleSoft Docs | https://docs.oracle.com/en/applications/peoplesoft/ |
| Info Portal | https://docs.oracle.com/cd/E52319_01/infoportal/ |
| MOS | https://support.oracle.com/support/ |
| IB Manual | https://ib.books.cedarhillsgroup.com/ |

---

## What to Avoid

1. **No rapid-fire requests** - Space actions 3-10 seconds apart
2. **No predictable patterns** - Vary delays randomly
3. **No hidden element interaction** - Honeypot traps
4. **No excessive scrolling** - Scroll like reading
5. **No direct URL API calls** - Use UI navigation for MOS

### If Blocked
1. **Stop immediately** - Don't retry
2. **Wait 15-30 minutes** - Let session cool down
3. **Check for CAPTCHA** - May need manual solve
4. **Verify login status** - Session may have expired

---

## Lessons Learned

| Topic | Lesson |
|-------|--------|
| PDF names | Cryptic (pt862xxx.pdf) - use index file |
| Batch curl | 3-second delays prevent rate limits |
| MOS downloads | Must click (javascript:; handlers) |
| RAG | Handles PDFs automatically |
| PeopleBooks | 45 PDFs, 172MB in oracle_docs/peopletools/ |

---

## Usage Examples

- "Scrape MOS article KB593233"
- "How to create REST service in PeopleSoft"
- "Integration Broker SOAP setup"
- "PeopleTools 8.62 upgrade path"
- "Query local KB for component interface"

$ARGUMENTS
