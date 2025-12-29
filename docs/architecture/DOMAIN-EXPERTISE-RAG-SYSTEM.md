# Domain Expertise RAG System Architecture

**Date:** 2025-10-17
**Purpose:** Build domain-specific AI expertise through trusted web scraping + RAG
**Use Case:** "I want to work on Angular" → System becomes Angular expert

---

## Vision

**Goal:** Transform Claude Code into a domain expert by intelligently scraping trusted sources and building a specialized RAG knowledge base.

**Example Flow:**
```
User: "Make me an Angular expert"
  ↓
System:
1. Identifies trusted Angular sources (official docs, top blogs)
2. Scores source trustworthiness (authority, freshness, community rating)
3. Checks robots.txt compliance per site
4. Scrapes allowed content intelligently (web scraper)
5. Builds domain-specific RAG collection
6. Claude becomes Angular expert for this session
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ User Request: "Become expert in Angular"                        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Domain Expertise Orchestrator                                   │
│  - Domain analyzer (Angular → Framework → Web Dev)              │
│  - Source discovery engine                                      │
│  - Trust scoring system                                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Trusted Source Database                                         │
│                                                                  │
│  Domain: "Angular"                                              │
│   └─ Official: angular.io (trust: 1.0)                         │
│   └─ Community: angular.dev (trust: 0.95)                      │
│   └─ Blogs: blog.angular.io (trust: 0.9)                       │
│   └─ Tutorials: egghead.io/angular (trust: 0.85)              │
│   └─ Stack Overflow: tagged/angular (trust: 0.8)               │
│                                                                  │
│  Each source has:                                               │
│   - Trust score (0-1)                                           │
│   - robots.txt rules                                            │
│   - Scraping allowed? (boolean)                                 │
│   - Content freshness score                                     │
│   - Community rating                                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Compliance Checker                                              │
│  - Fetch robots.txt for each source                            │
│  - Parse User-agent rules                                       │
│  - Check crawl-delay                                            │
│  - Determine if scraping allowed                                │
│  - Store compliance status                                      │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Intelligent Web Scraper (from previous architecture)           │
│  - Only scrape sources with scraping_allowed=true              │
│  - Respect rate limits per source                              │
│  - Use appropriate tool (WebFetch/Playwright)                  │
│  - Extract clean, structured content                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Content Processing Pipeline                                     │
│  - Quality filtering (trust score × content quality)           │
│  - Deduplication across sources                                 │
│  - Semantic chunking (respect code blocks, sections)           │
│  - Metadata enrichment (source, date, author, trust)           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Domain-Specific RAG Collection                                  │
│                                                                  │
│  Vector Store: ChromaDB or Langchain                           │
│                                                                  │
│  Collection: "angular-expertise"                                │
│   └─ Chunks: ~5000 chunks from trusted sources                │
│   └─ Embeddings: OpenAI text-embedding-3-small                 │
│   └─ Metadata: source, trust_score, date, topic                │
│                                                                  │
│  Indexed by:                                                    │
│   - Semantic similarity                                         │
│   - Trust score                                                 │
│   - Freshness (date)                                            │
│   - Topic tags (routing, components, services, etc.)           │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────────────┐
│ Domain Expert Mode (Claude Code)                               │
│  - RAG-augmented context for every Angular question           │
│  - Trust-weighted answers (prefer official docs)               │
│  - Source attribution in responses                             │
│  - Automatic knowledge updates (weekly scrape)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Trust Scoring System

### Source Categories & Base Trust Scores

```python
SOURCE_CATEGORIES = {
    'official_docs': {
        'base_trust': 1.0,
        'examples': ['angular.io', 'reactjs.org', 'vuejs.org'],
        'weight': 1.0,  # Always highest priority
    },
    'official_blog': {
        'base_trust': 0.95,
        'examples': ['blog.angular.io', 'react.dev/blog'],
        'weight': 0.9,
    },
    'framework_team': {
        'base_trust': 0.9,
        'examples': ['github.com/angular/angular', 'twitter.com/angular'],
        'weight': 0.85,
    },
    'trusted_tutorials': {
        'base_trust': 0.85,
        'examples': ['egghead.io', 'frontendmasters.com', 'pluralsight.com'],
        'weight': 0.8,
    },
    'community_docs': {
        'base_trust': 0.8,
        'examples': ['angular.love', 'indepth.dev'],
        'weight': 0.75,
    },
    'expert_blogs': {
        'base_trust': 0.75,
        'examples': ['blog.nrwl.io', 'netbasal.com'],
        'weight': 0.7,
    },
    'stack_overflow': {
        'base_trust': 0.7,
        'examples': ['stackoverflow.com/questions/tagged/angular'],
        'weight': 0.6,
    },
    'general_blogs': {
        'base_trust': 0.6,
        'examples': ['medium.com', 'dev.to'],
        'weight': 0.5,
    },
}
```

### Dynamic Trust Score Calculation

```python
def calculate_trust_score(source: Source) -> float:
    """
    Calculate dynamic trust score based on multiple factors
    """
    # Base trust from category
    base_trust = SOURCE_CATEGORIES[source.category]['base_trust']

    # Freshness factor (newer content = higher trust)
    age_days = (now() - source.last_updated).days
    freshness_factor = max(0.5, 1.0 - (age_days / 365) * 0.5)  # Decay over 1 year

    # Authority indicators
    authority_score = 0.0

    # Has HTTPS (security)
    if source.url.startswith('https://'):
        authority_score += 0.1

    # Domain age (older = more established)
    if source.domain_age_years > 5:
        authority_score += 0.1
    elif source.domain_age_years > 2:
        authority_score += 0.05

    # Community signals
    if source.github_stars and source.github_stars > 10000:
        authority_score += 0.1
    elif source.github_stars and source.github_stars > 1000:
        authority_score += 0.05

    # Backlinks from trusted sources
    if source.backlinks_from_official > 0:
        authority_score += 0.15

    # Author reputation (if known expert)
    if source.author in KNOWN_EXPERTS[source.domain]:
        authority_score += 0.1

    # Combine factors
    final_score = (
        base_trust * 0.6 +           # Category is most important
        freshness_factor * 0.2 +     # Freshness matters
        authority_score * 0.2        # Authority signals
    )

    return min(1.0, final_score)  # Cap at 1.0
```

### Known Expert Authors (Domain-Specific)

```python
KNOWN_EXPERTS = {
    'angular': [
        'Minko Gechev',      # Angular team
        'Kara Erickson',     # Angular team
        'Deborah Kurata',    # Pluralsight author
        'Todd Motto',        # Ultimate Angular
        'Netanel Basal',     # indepth.dev
        'Manfred Steyer',    # Angular Architects
    ],
    'react': [
        'Dan Abramov',       # React team
        'Kent C. Dodds',     # Testing React
        'Tanner Linsley',    # React Query
    ],
    'vue': [
        'Evan You',          # Vue creator
        'Eduardo San Martin', # Vue core team
    ],
    # Add more domains as needed
}
```

---

## Compliance & Ethics Module

### robots.txt Checker

```python
class ComplianceChecker:
    """
    Check if scraping is allowed per source
    """
    def __init__(self):
        self.robots_cache = {}
        self.user_agent = "Claude-Code-Research-Bot/1.0"

    async def check_scraping_allowed(self, source: Source) -> ComplianceResult:
        """
        Comprehensive compliance check
        """
        result = ComplianceResult(
            source=source.url,
            scraping_allowed=False,
            reason=None,
            crawl_delay=1.0,
        )

        # 1. Check explicit allowlist (official docs always OK)
        if source.category == 'official_docs':
            result.scraping_allowed = True
            result.reason = "Official documentation (allowlisted)"
            return result

        # 2. Fetch and parse robots.txt
        robots_url = f"{source.base_url}/robots.txt"
        try:
            robots_txt = await self.fetch_robots_txt(robots_url)
            rules = self.parse_robots_txt(robots_txt, self.user_agent)

            # Check if our user-agent is allowed
            if rules.is_allowed(source.path):
                result.scraping_allowed = True
                result.crawl_delay = rules.crawl_delay or 1.0
                result.reason = "Allowed by robots.txt"
            else:
                result.scraping_allowed = False
                result.reason = "Disallowed by robots.txt"

        except Exception as e:
            # If can't fetch robots.txt, assume allowed but be cautious
            result.scraping_allowed = True
            result.crawl_delay = 2.0  # Conservative delay
            result.reason = f"No robots.txt found (permissive default)"

        # 3. Check rate limiting requirements
        if source.requires_auth:
            result.scraping_allowed = False
            result.reason = "Requires authentication (not supported)"

        # 4. Check if site explicitly requests no scraping (meta tags)
        if source.has_noindex_meta or source.has_nofollow_meta:
            result.scraping_allowed = False
            result.reason = "Site has noindex/nofollow meta tags"

        # 5. Store result in database for future reference
        await self.db.store_compliance_result(source.url, result)

        return result

    async def fetch_robots_txt(self, url: str) -> str:
        """Fetch robots.txt with caching"""
        if url in self.robots_cache:
            return self.robots_cache[url]

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            self.robots_cache[url] = response.text
            return response.text
```

---

## Domain-Specific RAG Collections

### Collection Structure

```python
DOMAIN_COLLECTIONS = {
    'angular': {
        'name': 'angular-expertise',
        'description': 'Angular framework expertise',
        'sources': [
            {'url': 'https://angular.io/docs', 'trust': 1.0},
            {'url': 'https://angular.io/guide', 'trust': 1.0},
            {'url': 'https://angular.io/api', 'trust': 1.0},
            {'url': 'https://blog.angular.io', 'trust': 0.95},
            {'url': 'https://github.com/angular/angular/discussions', 'trust': 0.9},
            # ... more sources
        ],
        'topics': [
            'components', 'directives', 'services', 'routing',
            'forms', 'http', 'testing', 'performance', 'security'
        ],
        'update_frequency': 'weekly',
    },
    'react': {
        'name': 'react-expertise',
        'description': 'React library expertise',
        'sources': [
            {'url': 'https://react.dev', 'trust': 1.0},
            {'url': 'https://react.dev/learn', 'trust': 1.0},
            {'url': 'https://react.dev/reference', 'trust': 1.0},
            # ... more sources
        ],
        'topics': [
            'hooks', 'components', 'state', 'props', 'context',
            'routing', 'forms', 'performance', 'server-components'
        ],
        'update_frequency': 'weekly',
    },
    # Add more domains as needed
}
```

### RAG Pipeline with Trust Weighting

```python
class DomainExpertRAG:
    """
    Domain-specific RAG with trust-weighted retrieval
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.collection_name = DOMAIN_COLLECTIONS[domain]['name']
        self.vector_store = ChromaDB(collection_name=self.collection_name)

    async def build_expertise(self):
        """
        Build domain expertise by scraping trusted sources
        """
        domain_config = DOMAIN_COLLECTIONS[self.domain]

        for source_config in domain_config['sources']:
            # Check compliance
            compliance = await compliance_checker.check_scraping_allowed(
                Source(url=source_config['url'])
            )

            if not compliance.scraping_allowed:
                logger.info(f"Skipping {source_config['url']}: {compliance.reason}")
                continue

            # Scrape content (using intelligent web scraper)
            content = await web_scraper.fetch_content(
                url=source_config['url'],
                respect_robots=True,
                crawl_delay=compliance.crawl_delay,
            )

            # Process and chunk content
            chunks = await self.process_content(
                content=content,
                source_url=source_config['url'],
                trust_score=source_config['trust'],
            )

            # Add to vector store
            await self.vector_store.add_documents(
                documents=chunks,
                embeddings=self.compute_embeddings(chunks),
                metadatas=[{
                    'source': source_config['url'],
                    'trust_score': source_config['trust'],
                    'domain': self.domain,
                    'chunk_id': i,
                    'timestamp': now(),
                } for i, _ in enumerate(chunks)]
            )

            logger.info(f"Added {len(chunks)} chunks from {source_config['url']}")

    async def query(self, question: str, top_k: int = 5) -> List[Document]:
        """
        Query with trust-weighted ranking
        """
        # Get semantic matches
        results = await self.vector_store.query(
            query_text=question,
            n_results=top_k * 2,  # Get more, then rerank
        )

        # Rerank by trust score × similarity score
        reranked = []
        for doc, similarity, metadata in results:
            trust_score = metadata['trust_score']
            final_score = similarity * 0.7 + trust_score * 0.3
            reranked.append((doc, final_score, metadata))

        # Sort by final score
        reranked.sort(key=lambda x: x[1], reverse=True)

        # Return top K
        return [
            Document(
                content=doc,
                metadata=metadata,
                relevance_score=score
            )
            for doc, score, metadata in reranked[:top_k]
        ]

    async def process_content(
        self,
        content: str,
        source_url: str,
        trust_score: float
    ) -> List[str]:
        """
        Process content into semantic chunks
        """
        # Use LangChain's semantic splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n# ",      # Markdown headers
                "\n\n## ",
                "\n\n### ",
                "\n\n",        # Paragraphs
                "\n",          # Lines
                ". ",          # Sentences
            ],
        )

        chunks = splitter.split_text(content)

        # Filter by quality (trust score × content quality)
        quality_filtered = []
        for chunk in chunks:
            chunk_quality = self.evaluate_chunk_quality(chunk)
            combined_score = trust_score * chunk_quality

            if combined_score > 0.5:  # Threshold
                quality_filtered.append(chunk)

        return quality_filtered

    def evaluate_chunk_quality(self, chunk: str) -> float:
        """
        Evaluate chunk quality
        """
        score = 0.0

        # Has code examples (valuable for technical content)
        if '```' in chunk or '<code>' in chunk:
            score += 0.3

        # Has sufficient length
        if len(chunk) > 200:
            score += 0.2

        # Has structure (bullets, numbering)
        if any(marker in chunk for marker in ['- ', '* ', '1. ', '2. ']):
            score += 0.2

        # Has links to related content
        if '[' in chunk or '<a href' in chunk:
            score += 0.1

        # Has keywords for this domain
        domain_keywords = DOMAIN_COLLECTIONS[self.domain]['topics']
        if any(keyword in chunk.lower() for keyword in domain_keywords):
            score += 0.2

        return min(1.0, score)
```

---

## Integration with Claude Code

### Expert Mode Command

```python
@app.command("/expert")
async def expert_mode(domain: str, depth: str = "comprehensive"):
    """
    Transform Claude into a domain expert

    Usage:
        /expert angular
        /expert react --depth quick
        /expert vue --depth comprehensive
    """
    # Validate domain
    if domain not in DOMAIN_COLLECTIONS:
        return f"Domain '{domain}' not supported. Available: {list(DOMAIN_COLLECTIONS.keys())}"

    # Check if expertise already built
    rag = DomainExpertRAG(domain)
    if await rag.is_built():
        logger.info(f"{domain} expertise already available")
    else:
        # Build expertise
        logger.info(f"Building {domain} expertise from trusted sources...")
        await rag.build_expertise()
        logger.info(f"✅ {domain} expertise ready!")

    # Activate expert mode
    claude_context.set_expert_mode(domain, rag)

    return f"""
    ✅ {domain.title()} Expert Mode Activated

    I now have access to:
    - {len(DOMAIN_COLLECTIONS[domain]['sources'])} trusted sources
    - Official documentation (trust: 1.0)
    - Community resources (trust: 0.7-0.9)
    - Latest best practices and patterns

    Ask me anything about {domain}!

    Note: All answers will cite sources with trust scores.
    """


@app.on_message
async def handle_message(message: str):
    """
    Intercept messages and augment with RAG if expert mode active
    """
    if not claude_context.expert_mode_active:
        return await claude.respond(message)

    # Get domain-specific context
    domain = claude_context.expert_domain
    rag = claude_context.expert_rag

    # Query RAG for relevant context
    relevant_docs = await rag.query(message, top_k=5)

    # Build augmented prompt
    augmented_prompt = f"""
    You are an expert in {domain}. Use the following trusted sources to answer the question.

    **Question:** {message}

    **Relevant Context from Trusted Sources:**
    """

    for i, doc in enumerate(relevant_docs, 1):
        source = doc.metadata['source']
        trust = doc.metadata['trust_score']
        augmented_prompt += f"""
        Source {i} (trust: {trust:.2f}): {source}
        {doc.content}

        ---
        """

    augmented_prompt += f"""
    **Instructions:**
    1. Answer based on the provided context
    2. Prefer higher-trust sources (1.0 = official docs)
    3. Cite sources in your answer
    4. If context insufficient, say so
    5. Provide code examples when relevant
    """

    return await claude.respond(augmented_prompt)
```

---

## Example Use Cases

### Use Case 1: Angular Expert

```bash
# User activates expert mode
/expert angular

# System builds expertise
Building angular expertise from trusted sources...
✅ Scraped angular.io/docs (trust: 1.0) - 500 chunks
✅ Scraped angular.io/guide (trust: 1.0) - 800 chunks
✅ Scraped blog.angular.io (trust: 0.95) - 300 chunks
⏭️ Skipping medium.com/angular (trust: 0.6, robots.txt disallows)
✅ Scraped egghead.io/angular (trust: 0.85) - 200 chunks

Total: 1,800 chunks from 4 trusted sources
✅ Angular expertise ready!

# User asks questions
User: How do I implement lazy loading in Angular 17?

Claude (with RAG):
Based on official Angular documentation (trust: 1.0):

In Angular 17, lazy loading is implemented using the `loadChildren` property
in your routing configuration:

```typescript
const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module')
      .then(m => m.AdminModule)
  }
];
```

[Source: angular.io/guide/lazy-loading-ngmodules]

Additionally, the Angular blog (trust: 0.95) highlights that Angular 17
introduces standalone components which simplify lazy loading:

```typescript
{
  path: 'admin',
  loadComponent: () => import('./admin/admin.component')
    .then(c => c.AdminComponent)
}
```

[Source: blog.angular.io/angular-17-standalone-components]

Would you like me to show a complete example with guards and preloading strategies?
```

### Use Case 2: React Hooks Expert

```bash
/expert react

User: What's the difference between useMemo and useCallback?

Claude (with RAG):
According to official React documentation (trust: 1.0):

**useMemo** memoizes the *result* of a computation:
```jsx
const expensiveValue = useMemo(() => computeExpensiveValue(a, b), [a, b]);
```

**useCallback** memoizes the *function itself*:
```jsx
const memoizedCallback = useCallback(() => doSomething(a, b), [a, b]);
```

Key difference: useCallback(fn, deps) is equivalent to useMemo(() => fn, deps)

[Source: react.dev/reference/react/useMemo]

Kent C. Dodds (expert, trust: 0.85) adds this practical advice:
"Don't optimize prematurely. Most of the time, you don't need either.
Use them when profiling shows performance issues."

[Source: kentcdodds.com/blog/usememo-and-usecallback]
```

---

## Database Schema Extensions

### Trusted Sources Table

```sql
CREATE TABLE trusted_sources (
    id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,

    -- Categorization
    category TEXT NOT NULL,  -- 'official_docs', 'expert_blogs', etc.

    -- Trust scoring
    base_trust_score REAL NOT NULL,
    dynamic_trust_score REAL NOT NULL,
    authority_score REAL DEFAULT 0.0,
    freshness_score REAL DEFAULT 1.0,

    -- Compliance
    robots_txt TEXT,
    scraping_allowed BOOLEAN DEFAULT FALSE,
    crawl_delay REAL DEFAULT 1.0,
    last_robots_check TIMESTAMP,

    -- Metadata
    author TEXT,
    domain_age_years INTEGER,
    github_stars INTEGER,
    backlinks_count INTEGER,

    -- Status
    last_scraped TIMESTAMP,
    next_scrape_due TIMESTAMP,
    scrape_frequency_days INTEGER DEFAULT 7,

    -- Stats
    total_chunks_extracted INTEGER DEFAULT 0,
    avg_chunk_quality REAL DEFAULT 0.0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sources_domain ON trusted_sources(domain);
CREATE INDEX idx_sources_trust ON trusted_sources(dynamic_trust_score);
CREATE INDEX idx_sources_allowed ON trusted_sources(scraping_allowed);
```

### RAG Collections Table

```sql
CREATE TABLE rag_collections (
    id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL UNIQUE,
    collection_name TEXT NOT NULL UNIQUE,

    -- Stats
    total_chunks INTEGER DEFAULT 0,
    total_sources INTEGER DEFAULT 0,
    avg_trust_score REAL DEFAULT 0.0,

    -- Status
    last_built TIMESTAMP,
    build_duration_seconds INTEGER,
    next_update_due TIMESTAMP,

    -- Configuration
    update_frequency_days INTEGER DEFAULT 7,
    min_trust_threshold REAL DEFAULT 0.5,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Implementation Priorities

### Phase 1: Foundation (Week 1-2)
1. ✅ Trust scoring system
2. ✅ Compliance checker (robots.txt)
3. ✅ Integration with web scraper
4. ✅ Basic RAG collection (Angular only)
5. ✅ `/expert` command MVP

### Phase 2: Expansion (Week 3-4)
1. ✅ Add React, Vue, Python domains
2. ✅ Dynamic trust score calculation
3. ✅ Automatic source discovery
4. ✅ Scheduled updates (weekly)
5. ✅ Quality filtering improvements

### Phase 3: Advanced (Week 5-6)
1. ✅ Multi-domain expertise (Angular + React simultaneously)
2. ✅ Cross-domain concept transfer
3. ✅ Community source suggestions
4. ✅ Expert author tracking
5. ✅ Trust score auto-adjustment based on feedback

---

## Benefits

### For You (User):
✅ **Instant expertise** in any domain
✅ **Trusted sources only** (no random blogs)
✅ **Always up-to-date** (weekly scrapes)
✅ **Source attribution** (know where info comes from)
✅ **Ethical scraping** (respects robots.txt)

### For Claude:
✅ **Domain-specific knowledge** beyond training data
✅ **Freshness** (2024-2025 content)
✅ **Accuracy** (official docs prioritized)
✅ **Context** (relevant examples and patterns)

### For Ecosystem:
✅ **Respects site rules** (robots.txt compliance)
✅ **Rate-limited** (doesn't overload servers)
✅ **Attributive** (credits original authors)
✅ **Transparent** (shows trust scores)

---

## Next Steps

1. **Review this architecture** - Does it match your vision?
2. **Choose MVP domain** - Start with Angular, React, or Python?
3. **Define trusted sources** - Which sites for your first domain?
4. **Implement Phase 1** - ~2 weeks to working expert mode
5. **Test and iterate** - Real usage with your projects

---

**Status:** ✅ ARCHITECTURE COMPLETE
**Estimated time to MVP:** 2-3 weeks
**Confidence:** High (builds on proven web scraper architecture)

Would you like me to start implementing Phase 1?
