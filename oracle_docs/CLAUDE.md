# Oracle/PeopleSoft Documentation Knowledge Base

## Overview

This folder contains Oracle and PeopleSoft documentation for RAG-based queries and integration development.

## How to Use Browser Automation

**Known Bug**: Custom subagents (`PeopleSoft Expert`) cannot access MCP tools due to Claude Code bug #7296/#13898.

**Solution**: Use `general-purpose` built-in subagent OR invoke skills directly:

```python
# Option 1: Use general-purpose agent (HAS MCP access)
Task(
    subagent_type="general-purpose",
    prompt="You are a PeopleSoft expert. Scrape MOS KB article KB593233..."
)

# Option 2: Use /peoplesoft or /oracle skill (runs in main session with full MCP)
# Just type: /peoplesoft scrape MOS article KB593233
```

**Skills available**: `/peoplesoft` (Integration Broker, MOS), `/oracle` (general Oracle docs)

## Directory Structure

```
~/OneDrive - ERPA/Claude/oracle_docs/
├── public/           # Public documentation, REST APIs
├── private/          # MOS KB articles, patches, internal docs
├── peopletools/      # PeopleTools documentation
├── integration/      # Integration Broker guides
└── CLAUDE.md         # This file
```

## MCP BROWSER ACCESS (For general-purpose agents)

When deployed as a `general-purpose` agent, you have full MCP browser access.

### Create Your Browser Tab (ALWAYS DO THIS FIRST)
```python
# Step 1: Get context
mcp__claude-in-chrome__tabs_context_mcp(createIfEmpty=True)

# Step 2: Create YOUR tab (NEVER share tabs)
result = mcp__claude-in-chrome__tabs_create_mcp()
TAB_ID = result["tabId"]  # Save this for all operations!

# Step 3: Navigate to MOS
mcp__claude-in-chrome__navigate(url="https://support.oracle.com/support/", tabId=TAB_ID)

# Step 4: Wait (anti-bot - REQUIRED)
mcp__claude-in-chrome__computer(action="wait", duration=3, tabId=TAB_ID)

# Step 5: Screenshot to verify login state
mcp__claude-in-chrome__computer(action="screenshot", tabId=TAB_ID)
```

### Search MOS and Extract Content
```python
# Find search box
mcp__claude-in-chrome__find(query="search box", tabId=TAB_ID)

# Enter search term
mcp__claude-in-chrome__form_input(ref="ref_id", value="PeopleSoft upgrade", tabId=TAB_ID)

# Submit search
mcp__claude-in-chrome__computer(action="key", text="Enter", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="wait", duration=5, tabId=TAB_ID)

# Extract page text
mcp__claude-in-chrome__get_page_text(tabId=TAB_ID)

# Read detailed page structure
mcp__claude-in-chrome__read_page(tabId=TAB_ID)
```

### Anti-Bot Rules (CRITICAL - Oracle is strict!)
1. **Wait 3-5 seconds** between actions (longer than Workday)
2. **Scroll naturally** before clicking
3. **Max 10 pages** per session
4. Use logged-in Chrome session (MOS requires auth)
5. Close tabs when done: `mcp__claude-in-chrome__navigate(url="about:blank", tabId=TAB_ID)`
6. **Never automate login** - use existing session only

---

## Knowledge Sources

### My Oracle Support (MOS)
- **URL**: https://support.oracle.com/support/
- **Auth Required**: Yes (Oracle SSO)
- **Scraping Method**: Claude-in-Chrome (uses your logged-in session)
- **Doc ID Format**: KB{number} (new) or {number}.1 (legacy)

### Oracle Docs (Public)
- **URL**: https://docs.oracle.com/en/applications/peoplesoft/
- **Auth Required**: No
- **robots.txt**: Allows most paths except /search/, /pdf/ (some allowed)

### PeopleSoft Information Portal
- **URL**: https://docs.oracle.com/cd/E52319_01/infoportal/
- **Content**: Central hub for all PeopleSoft resources

## PeopleSoft API Architecture

| API Type | Format | Auth | PeopleTools Version | Best For |
|----------|--------|------|---------------------|----------|
| REST | JSON | Basic/OAuth | 8.52+ | Modern integrations |
| SOAP | XML | WS-Security | All | Legacy, bulk data |
| ASF (Application Services Framework) | JSON/OpenAPI | OAuth | 8.59+ | Modern REST APIs |

### REST API Endpoint Format
```
https://{host}/PSIGW/RESTListeningConnector/{node}/{service}.v1/{resource}
```

### SOAP Endpoint Format
```
https://{host}/PSIGW/HttpListeningConnector
```

## Integration Broker Key Concepts

- **Service Operations**: Define input/output for web services
- **Documents**: Define message structure (like XSD schemas)
- **Nodes**: Define endpoints for routing
- **Routing**: Connect service operations to handlers
- **Connectors**: HTTP, REST, JMS, FTP, SMTP

## Download Strategy Decision Tree

| Source | Method | Why |
|--------|--------|-----|
| **docs.oracle.com** (public) | `curl -sLO` | No auth, direct URLs |
| **MOS KB articles** (content) | Claude-in-Chrome `read_page` | Auth required |
| **MOS downloads** (PDFs/ZIPs) | Claude-in-Chrome **click** | Uses `javascript:;` handlers |
| **PeopleBooks PDFs** | `curl -sLO` | Direct URLs, no auth |

### Public Docs (docs.oracle.com) - USE CURL
```bash
# Direct download - no auth needed
curl -sLO "https://docs.oracle.com/cd/G41076_01/psft/pdf/pt862tacs-b112025.pdf"

# Batch download with delays (3-5 sec)
for url in $pdf_urls; do
  curl -sLO "$url"
  sleep 3
done
```

### MOS (support.oracle.com) - USE CLAUDE-IN-CHROME

**For reading KB content:**
```python
mcp__claude-in-chrome__navigate(url="https://support.oracle.com/...", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="wait", duration=3)
mcp__claude-in-chrome__read_page(tabId=TAB_ID)  # Extract content
```

**For downloading files (PDFs/ZIPs):**
MOS uses `javascript:;` handlers - must click to download:
```python
# 1. Find download links
mcp__claude-in-chrome__find(query="PDF download", tabId=TAB_ID)

# 2. Click to trigger download (auth check happens here)
mcp__claude-in-chrome__computer(action="left_click", ref="download_ref", tabId=TAB_ID)

# 3. Wait for download
mcp__claude-in-chrome__computer(action="wait", duration=5)

# 4. Move from Downloads to oracle_docs
# mv ~/Downloads/file.pdf ~/oracle_docs/private/
```

### Anti-Bot Best Practices
- Use your logged-in Chrome session
- Natural delays between actions (3-10 seconds)
- Don't scrape too fast
- Scroll naturally before interacting
- Avoid hidden elements (honeypots)
- **MOS downloads**: Must click, can't curl (JavaScript handlers)

## Document ID Mapping

Oracle recently migrated MOS to new portal (Dec 2025). IDs changed:
- Old format: `2833770.1`
- New format: `KB42118`
- Mapping file: https://docs.oracle.com/cd/E52319_01/infoportal/pdfs/PeopleSoft_MOS_Document_ID_Mappings.pdf

## Key Resources

| Resource | URL |
|----------|-----|
| PeopleSoft Docs Home | https://docs.oracle.com/en/applications/peoplesoft/ |
| PeopleSoft Info Portal | https://docs.oracle.com/cd/E52319_01/infoportal/ |
| My Oracle Support | https://support.oracle.com/support/ |
| Integration Broker Manual | https://ib.books.cedarhillsgroup.com/ |
| PeopleTools API Repository | https://docs.oracle.com/cd/E92519_02/pt856pbr3/eng/pt/tpcr/ |

## RAG Usage

```bash
# Query all docs
python oracle_rag.py "PeopleSoft backup procedures"

# List all indexed docs
python oracle_rag.py --list

# List MOS KB articles
python oracle_rag.py --list-kb

# Get specific KB article
python oracle_rag.py --kb KB593233

# Filter by category
python oracle_rag.py --category peopletools "upgrade"

# Interactive mode
python oracle_rag.py --interactive
```

## Categories

| Category | Directory | Content |
|----------|-----------|---------|
| public | `public/` | Public API specs, docs |
| private | `private/` | MOS KB articles (auth-scraped) |
| peopletools | `peopletools/` | PeopleTools documentation |
| integration | `integration/` | Integration Broker guides |
| patches | `patches/` | Patch info and notes |

## Security Notes

- Never commit MOS credentials
- Store auth tokens in environment variables
- Private docs stay in `private/` (gitignored)
- Respect Oracle's terms of service
