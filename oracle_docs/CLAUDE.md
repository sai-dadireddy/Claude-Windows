# Oracle/PeopleSoft Documentation Knowledge Base

## Overview

This folder contains Oracle and PeopleSoft documentation for RAG-based queries and integration development.

## Directory Structure

```
~/OneDrive - ERPA/Claude/oracle_docs/
├── public/           # Public documentation, REST APIs
├── private/          # MOS KB articles, patches, internal docs
├── peopletools/      # PeopleTools documentation
├── integration/      # Integration Broker guides
└── CLAUDE.md         # This file
```

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

## Scraping Strategy

### For MOS (My Oracle Support)
Use **Claude-in-Chrome** with human-like behavior:
1. Navigate using `mcp__claude-in-chrome__navigate`
2. Wait naturally between actions (2-5 seconds)
3. Scroll before clicking
4. Extract with `mcp__claude-in-chrome__read_page`
5. Save to `private/` folder

### Anti-Bot Best Practices
- Use your logged-in Chrome session
- Natural delays between actions (3-10 seconds)
- Don't scrape too fast
- Scroll naturally before interacting
- Avoid hidden elements (honeypots)

### For Public Docs (docs.oracle.com)
Can use direct fetch since no auth required:
```bash
curl -sL "https://docs.oracle.com/..." > output.html
```

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
