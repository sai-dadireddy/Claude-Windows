
## [2025-12-30 14:45:58]
Created Oracle/PeopleSoft KB system. Location: ~/OneDrive - ERPA/Claude/oracle_docs/. RAG: oracle_rag.py with KB article support. Agent: peoplesoft-expert.md. Skills: /oracle and /peoplesoft. Subdirs: public/, private/, peopletools/, integration/, patches/. Anti-bot strategy for MOS scraping documented.

## [2025-12-30 15:31:34]
Download strategy: Public docs.oracle.com use curl -sLO (direct URLs, no auth). MOS content use Claude-in-Chrome read_page (auth required). MOS downloads MUST CLICK - uses javascript:; handlers, can't curl. Move downloaded files from ~/Downloads to oracle_docs/private/.

## [2025-12-30 15:41:30]
Downloaded 45 PeopleTools 8.62 PeopleBooks PDFs (172MB) to oracle_docs/peopletools/. RAG indexes 47 docs total. Index file pt862_peoplebooks_index.txt maps cryptic filenames to titles. Batch download with curl + 3s delays works well for public docs.
