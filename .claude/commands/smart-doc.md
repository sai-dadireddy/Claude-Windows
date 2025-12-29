---
description: Intelligently handle documentation - RAG search, scrape, or read
---

# Smart Documentation Handler

**Automatically decide the best way to access documentation based on importance and availability.**

## Usage

```bash
# Let Claude decide automatically when you ask about documentation
"How do I use Server Components in Next.js?"
"Explain Prisma migrations"
"What's new in React 19?"
```

Claude will automatically:
1. Check if we have RAG for this technology
2. Use RAG if available (97% token savings)
3. Offer to scrape if important but not indexed
4. Read directly if low-frequency need
5. Skip if irrelevant

## Decision Process

### Step 1: Detect Technology

**From your question, identify:**
- Technology/library name
- Specific topic/feature
- Expected usage frequency

### Step 2: Check RAG Availability

**Query existing RAG collections:**

```bash
# Check AGUPGRADE RAG collections (12 available)
Available: nextjs, tanstack-query, shadcn, tailwind, zustand,
           forms-validation, aws-cognito, aws-api-gateway,
           aws-ecs-fargate, playwright, web-performance,
           agupgrade-backend
```

### Step 3: Make Smart Decision

**Decision matrix:**

| Scenario | RAG Exists? | Importance | Action | Token Cost |
|----------|-------------|------------|--------|------------|
| Next.js Server Components | ✅ Yes | High | **Use RAG** | <1K |
| Prisma ORM | ❌ No | High | **Scrape to RAG** | 7K (one-time) |
| Small utility lib | ❌ No | Medium | **Read once** | 5-10K |
| Marketing content | ❌ No | Low | **Skip** | 0K |

### Step 4: Execute with Transparency

**For each decision, show:**

#### ✅ Using Existing RAG (Best Case)
```
📚 Using existing RAG for Next.js (1,187 chunks indexed)
🔍 Query: "Server Components"
💾 Token cost: <1K

[Precise answer with code examples]
```

#### 📥 Scraping New Documentation (Investment)
```
📥 Prisma documentation not in RAG yet

**Should I add it for future use?**

**One-time cost:**
- Scraping docs: ~5K tokens
- Indexing to RAG: ~2K tokens
- Total: ~7K tokens

**Future benefits:**
- Each query: <1K tokens (vs 25K reading raw docs)
- Break-even: After 1 query
- ROI: 97% token savings

**Recommended:** YES (you'll likely need this multiple times)

Add to RAG? [Y/n]
```

#### 📖 Reading Once (Acceptable)
```
📖 Reading changelog directly

**Reasoning:**
- One-time reference (low reuse)
- Small document (~3K tokens)
- Not worth adding to RAG

**Cost:** ~3K tokens
**Action:** Reading directly...
```

#### ⏭️ Skipping (Smart Avoidance)
```
⏭️ This appears to be marketing content

**Reasoning:**
- Not technical documentation
- Low project relevance
- Would waste tokens

**Suggestion:** Can you clarify what technical information you need?
```

## Automatic Scraping Workflow

**When scraping is recommended:**

### Phase 1: Preparation
```bash
# 1. Identify documentation source
SOURCE_URL="https://www.prisma.io/docs"
COLLECTION_NAME="agupgrade-prisma-docs"

# 2. Estimate scope
ESTIMATED_PAGES=50
ESTIMATED_TOKENS=5000
```

### Phase 2: Scraping
```bash
# Use appropriate scraper
python projects/erpa/AGUPGRADE/tools/scrape-docs.py \
  --url "$SOURCE_URL" \
  --collection "$COLLECTION_NAME" \
  --max-pages 100

# Token cost: ~5K
```

### Phase 3: Indexing
```bash
# Index scraped content to RAG
python projects/erpa/AGUPGRADE/tools/index-docs.py \
  --source "scraped-docs/prisma" \
  --collection "$COLLECTION_NAME"

# Token cost: ~2K
```

### Phase 4: Verification
```bash
# Test the new RAG
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py \
  "Prisma client setup" \
  --tech prisma \
  --show-code

# Confirm it works
```

### Phase 5: Update Metadata
```bash
# Add to RAG registry for future sessions
echo "New RAG collection: $COLLECTION_NAME" >> .claude/rag-registry.md
```

## Examples

### Example 1: Using Existing RAG (Common Case)

**User asks:** "How do I use useQuery with caching in TanStack Query?"

**Claude's decision process:**
```
1. Technology detected: TanStack Query
2. Check RAG: ✅ tanstack-query RAG exists (785 chunks)
3. Decision: Use existing RAG
4. Action: Query RAG
```

**Execution:**
```bash
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py \
  "useQuery with caching" \
  --tech tanstack-query \
  --show-code
```

**Result:**
- Token cost: <1K
- Answer: Precise with code examples
- User happy: Instant answer

### Example 2: Scraping New Important Docs

**User asks:** "How do I set up Supabase authentication?"

**Claude's decision process:**
```
1. Technology detected: Supabase
2. Check RAG: ❌ No supabase RAG collection
3. Importance evaluation:
   - Official major service: ✅ High
   - Likely frequent use: ✅ High
   - Complex documentation: ✅ High
   - Score: 9/10
4. Decision: Scrape to RAG (investment worth it)
```

**Claude's proposal:**
```
📥 Supabase authentication docs not in RAG

**Analysis:**
- Major service (likely frequent use)
- Complex authentication patterns
- Large documentation
- Importance score: 9/10

**Investment:**
- One-time scraping cost: ~7K tokens
- Future query cost: <1K tokens each
- Break-even: After 1 query
- ROI: 97% savings

**Recommendation:** Add to RAG

Proceed with scraping? [Y/n]
```

**If user says YES:**
```bash
# Scrape Supabase auth docs
python projects/erpa/AGUPGRADE/tools/scrape-docs.py \
  --url "https://supabase.com/docs/guides/auth" \
  --collection "agupgrade-supabase-auth"

# Index to RAG
python projects/erpa/AGUPGRADE/tools/index-docs.py \
  --source "scraped-docs/supabase-auth" \
  --collection "agupgrade-supabase-auth"

# Query the new RAG
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py \
  "authentication setup" \
  --tech supabase-auth \
  --show-code
```

### Example 3: Reading Once (Medium Importance)

**User asks:** "Check what changed in version 2.0 of library-x"

**Claude's decision process:**
```
1. Technology detected: library-x changelog
2. Check RAG: ❌ No RAG (and shouldn't have one for changelogs)
3. Importance evaluation:
   - One-time reference: ⚠️ Medium
   - Low reuse probability: ⚠️ Medium
   - Small document: ⚠️ Medium
   - Score: 5/10
4. Decision: Read once (acceptable cost)
```

**Execution:**
```bash
📖 Reading changelog directly (one-time reference)

Read(file_path="node_modules/library-x/CHANGELOG.md")

# Cost: ~3K tokens
# Not adding to RAG (low reuse probability)
```

### Example 4: Skipping (Low Value)

**User asks:** "What does the marketing page say?"

**Claude's decision process:**
```
1. Content type: Marketing (not technical)
2. Importance evaluation:
   - Technical value: ❌ Low
   - Project relevance: ❌ Low
   - Score: 2/10
3. Decision: Skip
```

**Response:**
```
⏭️ Marketing content detected

This doesn't appear to be technical documentation.
Would waste tokens on non-technical content.

**Alternative suggestions:**
1. Clarify specific technical requirement
2. Point me to technical docs instead
3. Ask a specific technical question

What technical information do you actually need?
```

## Token Savings Tracking

**Track ROI for each decision:**

```markdown
# .claude/smart-doc-stats.md

## Today's Documentation Decisions

### RAG Queries (Token Efficient)
- Next.js Server Components: <1K tokens (saved ~24K)
- TanStack Query mutations: <1K tokens (saved ~28K)
- Shadcn Button props: <1K tokens (saved ~18K)
**Total: 3K tokens used, 70K tokens saved** ✅

### New RAG Scrapes (Investment)
- Supabase auth: 7K tokens (one-time investment)
- Expected ROI: 97% after 10 queries

### Read Once (Acceptable)
- Library-x changelog: 3K tokens (one-time need)

### Skipped (Smart Avoidance)
- Marketing content: 0K tokens (avoided waste)

## Session Summary
- Total tokens used: 13K
- Total tokens saved: 70K
- Net efficiency: 84% reduction
```

## Auto-Learning System

**Improve decisions over time:**

```python
# Track each decision's outcome
def learn_from_decision(tech, decision, outcome):
    """
    Learn from each documentation interaction

    Outcomes:
    - "success": Decision was correct
    - "missing_info": RAG had gaps, should update
    - "wasted": Read once but needed multiple times, should have scraped
    """

    if outcome == "missing_info":
        suggest_rag_update(tech)

    if outcome == "wasted":
        suggest_future_scrape(tech)
        log_pattern("Should have added to RAG earlier")

    if outcome == "success":
        increment_confidence(decision_type)
```

## Success Indicators

**Good session:**
- ✅ 90%+ queries answered by existing RAG
- ✅ <5% missing information in RAG
- ✅ Smart scraping decisions (high ROI)
- ✅ Zero token waste on irrelevant docs

**Bad session:**
- ❌ Reading raw docs repeatedly
- ❌ Not using available RAGs
- ❌ Scraping low-value content
- ❌ Wasting tokens on irrelevant docs

---

**The smart-doc system ensures:**
1. ✅ Maximum use of existing RAGs (97% savings)
2. ✅ Strategic scraping of important new docs
3. ✅ Minimal one-time reads when appropriate
4. ✅ Zero waste on irrelevant content

**Result: Self-optimizing documentation strategy!**
