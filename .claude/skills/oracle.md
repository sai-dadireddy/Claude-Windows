---
name: oracle
description: Query Oracle knowledge base, My Oracle Support (MOS), and Oracle documentation
---

# /oracle Skill

You are now in **Oracle Expert Mode**. Help with Oracle products, My Oracle Support (MOS), patches, and documentation.

## Scope

- My Oracle Support (MOS) KB articles
- Oracle Database, E-Business Suite, Cloud
- Patches and upgrades
- General Oracle documentation

**For PeopleSoft specifically, use `/peoplesoft` skill.**

## Knowledge Base

```
~/OneDrive - ERPA/Claude/oracle_docs/
├── public/           # Public docs
├── private/          # MOS KB articles (auth required)
├── patches/          # Downloaded patches info
└── CLAUDE.md         # Reference guide
```

## Quick Commands

```bash
# Query RAG
python oracle_docs/oracle_rag.py "query"

# List indexed docs
python oracle_docs/oracle_rag.py --list

# Search MOS (via Claude-in-Chrome)
# 1. Get tab: mcp__claude-in-chrome__tabs_context_mcp
# 2. Navigate: mcp__claude-in-chrome__navigate(url="https://support.oracle.com")
# 3. Search and extract
```

## Download Strategy

| Source | Method | Why |
|--------|--------|-----|
| **docs.oracle.com** | `curl -sLO` | Public, direct URLs |
| **MOS KB content** | Claude-in-Chrome `read_page` | Auth required |
| **MOS downloads** | Claude-in-Chrome **click** | JavaScript handlers |

### Public Docs - USE CURL
```bash
curl -sLO "https://docs.oracle.com/cd/.../file.pdf"
```

### MOS Content - USE CLAUDE-IN-CHROME
```python
mcp__claude-in-chrome__navigate(url="https://support.oracle.com/...", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="wait", duration=3)
mcp__claude-in-chrome__read_page(tabId=TAB_ID)
```

### MOS Downloads - MUST CLICK
```python
# MOS uses javascript:; handlers - can't curl
mcp__claude-in-chrome__find(query="download PDF", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="left_click", ref="download_ref", tabId=TAB_ID)
# Then: mv ~/Downloads/file.pdf ~/oracle_docs/private/
```

## Key Resources

| Resource | URL |
|----------|-----|
| MOS | https://support.oracle.com/support/ |
| Oracle Docs | https://docs.oracle.com/ |
| OTN | https://www.oracle.com/technical-resources/ |

## Usage Examples

- "Find MOS article about database backup"
- "Search for Oracle patch 12345678"
- "Oracle Cloud Infrastructure documentation"

## Lessons Learned

| Topic | Lesson |
|-------|--------|
| PDF names | Cryptic (pt862xxx.pdf) - use index file |
| Batch curl | 3-second delays prevent rate limits |
| MOS downloads | Must click (javascript:; handlers) |
| RAG | Handles PDFs automatically |
| PeopleBooks | 45 PDFs, 172MB in oracle_docs/peopletools/ |
