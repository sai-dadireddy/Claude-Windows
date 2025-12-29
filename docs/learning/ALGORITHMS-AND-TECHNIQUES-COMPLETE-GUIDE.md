# Complete Guide: Algorithms, Techniques & Concepts

**Purpose**: Comprehensive educational document covering all algorithms, techniques, and concepts used in your Claude Code setup.

**For**: Learning and understanding the underlying technology, patterns, and methodologies.

**Date**: October 13, 2025

---

## 📚 TABLE OF CONTENTS

1. [Vector Databases & Embeddings](#1-vector-databases--embeddings)
2. [Semantic Search Algorithms](#2-semantic-search-algorithms)
3. [RAG (Retrieval Augmented Generation)](#3-rag-retrieval-augmented-generation)
4. [LangChain Architecture](#4-langchain-architecture)
5. [Memory Management Algorithms](#5-memory-management-algorithms)
6. [Token Optimization Techniques](#6-token-optimization-techniques)
7. [MCP (Model Context Protocol)](#7-mcp-model-context-protocol)
8. [Graph-Based Memory](#8-graph-based-memory)
9. [Auto-Compaction Algorithms](#9-auto-compaction-algorithms)
10. [Image-First Communication](#10-image-first-communication)
11. [Project Isolation Patterns](#11-project-isolation-patterns)
12. [Prompt Engineering Techniques](#12-prompt-engineering-techniques)

---

## 1. VECTOR DATABASES & EMBEDDINGS

### What Are Vector Embeddings?

**Concept**: Converting text into numerical vectors (lists of numbers) that capture semantic meaning.

**Example**:
```
Text: "Claude is an AI assistant"
Embedding: [0.23, -0.15, 0.87, ..., 0.44]  (384 dimensions)
```

**Why Important**:
- Allows computers to understand semantic similarity
- "Dog" and "Puppy" have similar vectors even though words are different
- Enables meaning-based search, not just keyword matching

---

### Sentence Transformers (all-MiniLM-L6-v2)

**What It Is**: A neural network that converts text to embeddings.

**Model Details**:
```
Name: all-MiniLM-L6-v2
Provider: HuggingFace
Dimensions: 384
Size: 22.7 MB
Speed: ~100 sentences/second on CPU
Quality: Good for general-purpose tasks
```

**Architecture**:
```
Input Text
    ↓
Tokenizer (breaks text into pieces)
    ↓
Transformer Model (12 layers, 6 attention heads)
    ↓
Pooling Layer (mean pooling)
    ↓
384-dimensional vector
```

**Mathematics Behind It**:

**Step 1: Tokenization**
```
Text: "AI is powerful"
Tokens: ["AI", "is", "powerful"]
Token IDs: [2342, 2003, 3928]
```

**Step 2: Transformer Encoding**
```
For each token:
  Q = Query vector (what am I looking for?)
  K = Key vector (what information do I have?)
  V = Value vector (the actual information)

Attention Score = softmax(Q·K / √d)
Output = Attention × V

Where:
  Q·K = dot product
  d = dimension (384)
  softmax = normalization function
```

**Step 3: Pooling**
```
Mean Pooling:
  embedding = sum(all_token_embeddings) / num_tokens

Result: Single 384-dimensional vector representing entire sentence
```

---

### ChromaDB Vector Store

**What It Is**: A database optimized for storing and searching vector embeddings.

**Architecture**:
```
ChromaDB Instance
│
├── Collection (like a table)
│   │
│   ├── Documents (text content)
│   ├── Embeddings (384-dim vectors)
│   ├── Metadata (tags, timestamps, etc.)
│   └── IDs (unique identifiers)
│
└── SQLite Backend (persistence)
```

**How It Works**:

**Adding Documents**:
```python
collection.add(
    documents=["AI is powerful", "ML is useful"],
    embeddings=[[0.23, ...], [0.34, ...]],  # From sentence-transformer
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["id1", "id2"]
)
```

**Searching** (Similarity Search):
```python
# User query: "artificial intelligence"
query_embedding = model.encode("artificial intelligence")  # [0.25, ...]

# ChromaDB finds similar vectors
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

# Returns: Top 5 most similar documents
```

**Similarity Calculation** (Cosine Similarity):
```
Formula:
  similarity = (A · B) / (||A|| × ||B||)

Where:
  A · B = dot product of vectors
  ||A|| = magnitude of vector A
  ||B|| = magnitude of vector B

Range: -1 to 1
  1.0 = identical meaning
  0.0 = unrelated
  -1.0 = opposite meaning
```

**Example**:
```
Vector A: [1, 2, 3]  ("AI is powerful")
Vector B: [2, 3, 4]  ("ML is strong")

A · B = (1×2) + (2×3) + (3×4) = 2 + 6 + 12 = 20
||A|| = √(1² + 2² + 3²) = √14 = 3.74
||B|| = √(2² + 3² + 4²) = √29 = 5.39

Similarity = 20 / (3.74 × 5.39) = 20 / 20.16 = 0.99 (very similar!)
```

---

### FAISS (Facebook AI Similarity Search)

**What It Is**: High-performance vector search library from Meta.

**Why Use FAISS**:
- ChromaDB: Good for < 1M vectors
- FAISS: Optimized for > 1M vectors
- 10-100x faster for large datasets

**Index Types**:

**1. Flat Index** (Exact Search)
```
Algorithm: Brute force comparison
Speed: Slow (O(n))
Accuracy: 100% (exact)
Best for: < 10K vectors
```

**2. IVF (Inverted File Index)**
```
Algorithm:
  1. Cluster vectors into groups (k-means)
  2. Search only nearest clusters

Speed: Fast (O(log n))
Accuracy: 95-99%
Best for: 100K - 10M vectors

Example:
  1000 clusters, 1M vectors
  Search: 1,000 vectors instead of 1,000,000
  Speedup: 1000x
```

**3. HNSW (Hierarchical Navigable Small World)**
```
Algorithm:
  Builds multi-layer graph
  Top layer: Sparse (fast navigation)
  Bottom layer: Dense (accurate search)

Speed: Very fast (O(log n))
Accuracy: 99%+
Best for: Real-time applications

Structure:
  Layer 2: ─○───○───○─  (5 nodes)
  Layer 1: ─○─○─○─○─○─  (50 nodes)
  Layer 0: ○○○○○○○○○○○  (1000 nodes)
```

**Performance Comparison**:
```
Dataset: 1M vectors, 384 dimensions

Method     | Search Time | Accuracy
-----------|-------------|----------
Flat       | 1000ms      | 100%
IVF        | 10ms        | 98%
HNSW       | 5ms         | 99%
```

---

## 2. SEMANTIC SEARCH ALGORITHMS

### Dense vs Sparse Search

**Sparse Search** (Traditional):
```
Query: "AI is powerful"
Method: BM25 (keyword matching)

Document Scoring:
  Score(doc) = Σ IDF(term) × TF(term, doc)

Where:
  IDF = log(N / df)  (Inverse Document Frequency)
  TF = term frequency in document
  N = total documents
  df = documents containing term

Example:
  Term "AI": IDF = log(1000/10) = 2.0
  TF in doc: 3 occurrences
  Score = 2.0 × 3 = 6.0
```

**Dense Search** (Vector):
```
Query: "AI is powerful"
Method: Cosine similarity

Document Scoring:
  Score(doc) = cosine_sim(query_vec, doc_vec)

Example:
  Query vector: [0.25, -0.15, ...]
  Doc vector: [0.23, -0.16, ...]
  Similarity: 0.98 (very similar!)
```

**Key Difference**:
```
Query: "car mechanic"

Sparse Results:
  ✓ "car mechanic job"
  ✗ "automobile repair technician" (no keyword match!)

Dense Results:
  ✓ "car mechanic job"
  ✓ "automobile repair technician" (semantic match!)
  ✓ "vehicle maintenance engineer"
```

---

### Hybrid Search

**Combining Best of Both**:

**Algorithm**:
```python
def hybrid_search(query, alpha=0.5):
    # Get sparse scores (BM25)
    sparse_scores = bm25_search(query)

    # Get dense scores (vector)
    dense_scores = vector_search(query)

    # Normalize both to [0, 1]
    sparse_norm = normalize(sparse_scores)
    dense_norm = normalize(dense_scores)

    # Combine with weighting
    final_scores = alpha * sparse_norm + (1 - alpha) * dense_norm

    return top_k(final_scores)

# alpha = 0.5: Equal weight
# alpha = 0.7: Prefer keywords
# alpha = 0.3: Prefer semantics
```

**When to Use**:
- Sparse: Exact matches important (product IDs, technical terms)
- Dense: Meaning important (questions, natural language)
- Hybrid: Best of both worlds

---

## 3. RAG (RETRIEVAL AUGMENTED GENERATION)

### What Is RAG?

**Concept**: Enhance AI responses by retrieving relevant information from external sources.

**Basic RAG Flow**:
```
User Query
    ↓
1. Retrieve relevant documents from vector DB
    ↓
2. Augment prompt with retrieved context
    ↓
3. Generate response using LLM
    ↓
Response with grounded information
```

**Example Without RAG**:
```
User: "What's our Lambda optimization strategy?"
AI: "I don't have information about your specific strategy."
```

**Example With RAG**:
```
User: "What's our Lambda optimization strategy?"
    ↓
RAG retrieves from vector DB:
  - "Use ARM64 for 20% cost savings"
  - "Provisioned concurrency for predictable loads"
  - "Memory optimization: 1769 MB sweet spot"
    ↓
AI: "Based on your documentation, your strategy includes:
     1. ARM64 architecture (20% cost reduction)
     2. Provisioned concurrency for predictable workloads
     3. 1769 MB memory for optimal price/performance"
```

---

### Advanced RAG Techniques

#### 1. **Chunking Strategy**

**Why Chunk**: Documents too large for LLM context window.

**Naive Chunking**:
```
Split every 500 tokens:
  Chunk 1: Token 0-499
  Chunk 2: Token 500-999
  Problem: May split sentences/paragraphs!
```

**Smart Chunking**:
```python
def smart_chunk(text, chunk_size=500, overlap=50):
    # Split on paragraph boundaries
    paragraphs = text.split('\n\n')

    chunks = []
    current_chunk = []
    current_size = 0

    for para in paragraphs:
        para_size = len(tokenize(para))

        if current_size + para_size > chunk_size:
            # Save current chunk
            chunks.append(' '.join(current_chunk))

            # Start new chunk with overlap
            current_chunk = get_last_sentences(current_chunk, overlap)
            current_size = count_tokens(current_chunk)

        current_chunk.append(para)
        current_size += para_size

    return chunks
```

**Benefits of Overlap**:
```
Chunk 1: "...Lambda functions should use ARM64 architecture.
          This provides 20% cost savings..."

Chunk 2: "...This provides 20% cost savings. Additionally,
          provisioned concurrency helps with..."

Overlap ensures context continuity!
```

#### 2. **Re-ranking**

**Problem**: Vector search returns 100 results, but only top 5 are needed.

**Solution**: Two-stage retrieval

**Stage 1: Fast Retrieval** (Vector Search)
```
Query vector → ChromaDB → 100 candidates
Speed: 50ms
Accuracy: Good
```

**Stage 2: Precise Re-ranking** (Cross-encoder)
```
For each candidate:
  Score = cross_encoder(query, candidate)

Sort by score → Top 5 results
Speed: 200ms (but only 100 comparisons)
Accuracy: Excellent
```

**Cross-Encoder vs Bi-Encoder**:
```
Bi-Encoder (what we use for initial search):
  encode(query) → vector1
  encode(doc) → vector2
  similarity = cosine(vector1, vector2)
  Fast: Can pre-compute doc vectors

Cross-Encoder (for re-ranking):
  score = model(query + doc together)
  Slow: Must compute for each pair
  Accurate: Sees interaction between query and doc
```

#### 3. **Query Expansion**

**Problem**: User query might miss relevant documents.

**Original Query**: "Lambda optimization"

**Expanded Query**:
```
Generated variations:
  - "Lambda optimization"
  - "AWS Lambda performance tuning"
  - "Lambda cost reduction"
  - "Serverless function optimization"
  - "Lambda memory configuration"
```

**Algorithm**:
```python
def expand_query(query, llm):
    prompt = f"""
    Generate 5 variations of this query that might
    retrieve relevant information:

    Original: {query}

    Variations:
    """

    variations = llm.generate(prompt)

    # Search with all variations
    all_results = []
    for variant in variations:
        results = vector_search(variant)
        all_results.extend(results)

    # Deduplicate and re-rank
    return dedupe_and_rerank(all_results)
```

#### 4. **Hypothetical Document Embeddings (HyDE)**

**Concept**: Generate ideal answer, then search for similar documents.

**Traditional**:
```
Query: "How to optimize Lambda?"
Search: vector(query) → similar docs
```

**HyDE**:
```
Query: "How to optimize Lambda?"
    ↓
LLM generates hypothetical answer:
  "To optimize Lambda: 1) Use ARM64 2) Optimize memory 3) ..."
    ↓
Search: vector(hypothetical_answer) → similar docs
    ↓
Better results because searching for answer-like content!
```

---

### RAG in Your System

**Your Implementation**:
```
1. LangChain MCP Server (585 lines)
   - Document indexing (PDF, DOCX, code)
   - Semantic search
   - Project isolation

2. ChromaDB (4 instances)
   - Global knowledge base
   - Project-specific stores
   - n8n knowledge base
   - PeopleSoft RAG research

3. Sentence-Transformers
   - all-MiniLM-L6-v2 model
   - 384-dimensional embeddings
   - Free, offline capable
```

**Usage Pattern**:
```
User: "How did we implement CORS in Active Genie?"
    ↓
Claude searches: active-genie project memory
    ↓
Retrieves: SESSION_MEMORY_SUMMARY.md (48 KB, 30 entries)
    ↓
Response: "In the Active Genie project, CORS was implemented
           in API Gateway with specific allowed origins..."
```

---

## 4. LANGCHAIN ARCHITECTURE

### What Is LangChain?

**Definition**: Framework for building applications with LLMs.

**Core Concept**: Chains - composable components for LLM applications.

---

### LangChain Components

#### 1. **Document Loaders**

**Purpose**: Load documents from various sources.

```python
from langchain.document_loaders import PDFLoader, DocxLoader, TextLoader

# Load PDF
loader = PDFLoader("document.pdf")
pages = loader.load()

# Result:
[
    Document(page_content="Page 1 text...", metadata={"page": 1}),
    Document(page_content="Page 2 text...", metadata={"page": 2}),
]
```

#### 2. **Text Splitters**

**Purpose**: Break documents into chunks.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# Try to split on paragraph, then sentence, then word
chunks = splitter.split_documents(pages)
```

#### 3. **Embeddings**

**Purpose**: Convert text to vectors.

```python
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings

# OpenAI (paid, high quality)
openai_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# HuggingFace (free, good quality)
hf_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = hf_embeddings.embed_query("AI is powerful")
# Result: [0.23, -0.15, ..., 0.44] (384 dimensions)
```

#### 4. **Vector Stores**

**Purpose**: Store and search embeddings.

```python
from langchain.vectorstores import Chroma, FAISS

# ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=hf_embeddings,
    persist_directory="./chroma_db"
)

# Search
results = vectorstore.similarity_search("Lambda optimization", k=5)
```

#### 5. **Retrievers**

**Purpose**: Interface for retrieval with advanced features.

```python
# Basic retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Advanced: Multi-query retriever
from langchain.retrievers import MultiQueryRetriever

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm,
    # Generates multiple query variations automatically
)

results = multi_retriever.get_relevant_documents("Lambda optimization")
```

#### 6. **Chains**

**Purpose**: Combine components into workflows.

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Put all retrieved docs in prompt
    retriever=retriever
)

# User query
response = qa_chain.run("How to optimize Lambda?")
```

---

### Chain Types in LangChain

#### 1. **Stuff Chain** (Simplest)
```
Retrieve docs → Stuff all into prompt → Generate answer

Prompt:
  Context: {doc1} {doc2} {doc3}
  Question: {query}
  Answer:

Pros: Simple, single LLM call
Cons: Limited by context window
Best for: Few retrieved documents
```

#### 2. **Map-Reduce Chain**
```
For each doc:
  Generate partial answer
    ↓
Combine all partial answers
    ↓
Generate final answer

Pros: Handles many documents
Cons: Multiple LLM calls (expensive)
Best for: Large document sets
```

#### 3. **Refine Chain**
```
Answer = ""
For each doc:
  Answer = refine(Answer, doc)

Pros: Iterative improvement
Cons: Sequential (slow)
Best for: Detailed analysis
```

#### 4. **Map-Rerank Chain**
```
For each doc:
  Generate answer + confidence score
    ↓
Return highest confidence answer

Pros: Chooses best answer
Cons: Multiple LLM calls
Best for: Question answering
```

---

### Your LangChain Implementation

**File**: `mcp-servers/langchain-server/server.py` (585 lines)

**Architecture**:
```python
class LangChainMCP:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectorstores = {}  # Project-specific stores

    def semantic_search(self, query, project_name, k=5):
        """Search by meaning"""
        store = self._get_or_create_store(project_name)
        results = store.similarity_search(query, k=k)
        return results

    def add_documents(self, texts, project_name):
        """Add text to vector store"""
        store = self._get_or_create_store(project_name)
        store.add_texts(texts)

    def index_file(self, filepath, project_name):
        """Index a single file"""
        # Detect file type
        if filepath.endswith('.pdf'):
            loader = PDFLoader(filepath)
        elif filepath.endswith('.docx'):
            loader = DocxLoader(filepath)
        else:
            loader = TextLoader(filepath)

        # Load and split
        docs = loader.load()
        chunks = self.splitter.split_documents(docs)

        # Add to store
        store = self._get_or_create_store(project_name)
        store.add_documents(chunks)
```

**MCP Tools Provided**:
1. `semantic_search` - Search by meaning
2. `add_documents` - Add text to vector store
3. `index_file` - Index single file
4. `index_directory` - Index entire directory
5. `delete_project_store` - Cleanup project stores

**Current Status**: ⏸️ Disabled to save 8-12K tokens (can re-enable when semantic search needed)

---

## 5. MEMORY MANAGEMENT ALGORITHMS

### Three-Tier Memory Architecture

#### Tier 1: Filesystem (Basic Storage)
```
Simple file operations:
  - read_file(path)
  - write_file(path, content)
  - list_directory(path)

Complexity: O(1) for read/write
Storage: Unlimited (disk space)
Persistence: Permanent
```

#### Tier 2: Structured Memory (SQLite)
```
Database schema:

CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    project_name TEXT,
    entity_type TEXT,
    entity_name TEXT,
    content TEXT,
    importance INTEGER,  -- 0-3
    timestamp DATETIME,
    metadata JSON
);

CREATE INDEX idx_project ON memories(project_name);
CREATE INDEX idx_entity ON memories(entity_name);
CREATE INDEX idx_importance ON memories(importance);
```

**Retrieval Algorithm**:
```python
def retrieve_memories(project_name, query, limit=10):
    # Full-text search on content
    sql = """
        SELECT * FROM memories
        WHERE project_name = ?
        AND content MATCH ?
        ORDER BY importance DESC, timestamp DESC
        LIMIT ?
    """

    results = db.execute(sql, [project_name, query, limit])
    return results
```

**Importance Scoring**:
```python
def calculate_importance(content, entity_type):
    score = 0

    # Base score by entity type
    if entity_type == "decision":
        score = 3  # Critical
    elif entity_type == "implementation":
        score = 2  # Important
    elif entity_type == "note":
        score = 1  # Useful
    else:
        score = 0  # General

    # Boost for specific keywords
    keywords = ["critical", "bug", "security", "breaking"]
    for keyword in keywords:
        if keyword in content.lower():
            score = min(3, score + 1)

    return score
```

#### Tier 3: Semantic Memory (Vector Store)
```python
class SemanticMemory:
    def __init__(self):
        self.vectorstore = ChromaDB(persist_directory="./memory")
        self.embeddings = SentenceTransformer("all-MiniLM-L6-v2")

    def store(self, content, metadata):
        # Generate embedding
        vector = self.embeddings.encode(content)

        # Store with metadata
        self.vectorstore.add(
            ids=[metadata['id']],
            embeddings=[vector],
            documents=[content],
            metadatas=[metadata]
        )

    def retrieve(self, query, k=5):
        # Semantic search
        query_vector = self.embeddings.encode(query)
        results = self.vectorstore.query(
            query_embeddings=[query_vector],
            n_results=k
        )
        return results
```

---

### Memory Consolidation Algorithm

**Purpose**: Compress session memory without losing important information.

**Algorithm**:
```python
def consolidate_memory(session_memories, llm):
    # Step 1: Extract key information
    important_memories = [
        m for m in session_memories
        if m.importance >= 2  # Important or Critical
    ]

    # Step 2: Group by topic
    topics = cluster_by_topic(important_memories)

    # Step 3: Summarize each topic
    summaries = []
    for topic, memories in topics.items():
        prompt = f"""
        Summarize these related memories into key points:

        {format_memories(memories)}

        Key points:
        """
        summary = llm.generate(prompt, max_tokens=200)
        summaries.append({
            'topic': topic,
            'summary': summary,
            'original_count': len(memories)
        })

    # Step 4: Store consolidated memory
    for summary in summaries:
        store_memory(
            content=summary['summary'],
            importance=3,  # Consolidated = Critical
            metadata={'type': 'consolidated', 'original_count': summary['original_count']}
        )

    return summaries
```

**Token Savings**:
```
Before consolidation:
  100 memories × 200 tokens = 20,000 tokens

After consolidation:
  10 summaries × 500 tokens = 5,000 tokens

Savings: 75% (15,000 tokens)
```

---

### Auto-Classification Algorithm

**Purpose**: Automatically determine if memory is project-specific or global.

```python
def classify_memory(content, context):
    # Check for project-specific indicators
    project_indicators = [
        'this project',
        'our implementation',
        'the codebase',
        context.project_name  # Current project name
    ]

    global_indicators = [
        'in general',
        'always',
        'best practice',
        'industry standard'
    ]

    # Count indicators
    project_score = sum(1 for ind in project_indicators if ind in content.lower())
    global_score = sum(1 for ind in global_indicators if ind in content.lower())

    if project_score > global_score:
        return "project"
    else:
        return "global"
```

**Example**:
```
Content: "In Active Genie, we use AWS Cognito for authentication"
Classification: PROJECT (mentions specific project)

Content: "AWS Cognito is a good choice for authentication"
Classification: GLOBAL (general best practice)
```

---

## 6. TOKEN OPTIMIZATION TECHNIQUES

### 1. Dynamic Context Loading

**Concept**: Load only what's needed for current task.

**Implementation**:
```python
def load_context(task_type, project=None):
    # Always load
    context = load_core_instructions()  # ~2-3K tokens

    # Task-specific
    if task_type == "security":
        context += load_security_guardrails()  # +2K
    elif task_type == "coding":
        context += load_coding_best_practices()  # +3K
    elif task_type == "n8n":
        context += load_n8n_knowledge()  # +4K

    # Project-specific
    if project:
        context += load_project_instructions(project)  # +1-2K

    return context
```

**Savings**:
```
Full CLAUDE.md: 15-20K tokens every session
Dynamic loading: 2-7K tokens (depending on task)
Savings: 60-85% per session
```

---

### 2. MCP Profiling & Optimization

**Problem**: MCP servers consume tokens even if unused.

**Solution**: Profile usage, disable unused servers.

**Profiling Algorithm**:
```python
def profile_mcp_usage(session_logs, duration_days=30):
    usage = defaultdict(int)

    for log in session_logs:
        for tool_call in log.tool_calls:
            if tool_call.startswith("mcp__"):
                server = extract_server_name(tool_call)
                usage[server] += 1

    # Calculate usage per day
    usage_per_day = {
        server: count / duration_days
        for server, count in usage.items()
    }

    # Categorize
    critical = {s: c for s, c in usage_per_day.items() if c > 1.0}  # Daily use
    useful = {s: c for s, c in usage_per_day.items() if 0.1 < c <= 1.0}  # Weekly use
    rarely_used = {s: c for s, c in usage_per_day.items() if c <= 0.1}  # Monthly or less

    return {
        'critical': critical,
        'useful': useful,
        'rarely_used': rarely_used
    }
```

**Your Optimization**:
```
Original: 13 MCPs = 60-80K tokens
Profiled: 4 rarely used = 43-60K tokens
Optimized: 9 essential = 20-30K tokens
Savings: 40-50K tokens (60-70% reduction)
```

---

### 3. Auto-Compaction with Smart Thresholds

**Algorithm**:
```python
def should_compact(current_tokens):
    thresholds = {
        'level_1': 50000,   # Gentle reminder
        'level_2': 80000,   # Strong suggestion
        'level_3': 120000,  # Urgent warning
        'critical': 180000  # Auto-compact
    }

    if current_tokens >= thresholds['critical']:
        # Auto-compact immediately
        return ('auto', 'CRITICAL: Near limit')
    elif current_tokens >= thresholds['level_3']:
        return ('suggest', 'URGENT: Please /compact soon')
    elif current_tokens >= thresholds['level_2']:
        return ('suggest', 'Consider /compact')
    elif current_tokens >= thresholds['level_1']:
        return ('info', 'FYI: At 50K tokens')
    else:
        return (None, None)
```

**Compaction Strategy**:
```python
def compact_session(messages):
    # Step 1: Identify important messages
    important = [
        msg for msg in messages
        if msg.role == "user" or
           has_code(msg) or
           has_decision(msg) or
           msg.importance == "high"
    ]

    # Step 2: Group consecutive messages
    groups = group_consecutive_messages(messages)

    # Step 3: Summarize each group
    summaries = []
    for group in groups:
        if all(msg in important for msg in group):
            # Keep important messages as-is
            summaries.extend(group)
        else:
            # Summarize group
            summary = llm.summarize(group, max_tokens=200)
            summaries.append(summary)

    # Step 4: Preserve final N messages
    recent = messages[-10:]  # Keep last 10 messages

    return summaries + recent
```

**Token Savings**:
```
Before compact: 150K tokens
After compact: 40K tokens
Savings: 110K tokens (73%)

Information loss: ~5-10% (acceptably low)
```

---

### 4. Image-First Strategy

**Concept**: Images are more token-efficient than text for visual information.

**Token Cost Comparison**:
```
Text description (200 words):
  ~300 tokens

Screenshot (1920×1080 PNG):
  ~40-60 tokens (fixed cost)

Savings: 240-260 tokens (80-85%)
```

**Why Images Are Efficient**:
```
Claude's vision model:
  - Processes images in fixed-size tiles (512×512)
  - Most screenshots = 4-6 tiles
  - Cost: ~8-10 tokens per tile
  - Total: ~40-60 tokens regardless of image complexity

Text description:
  - Cost: ~1 token per 4 characters
  - 800-character description = 200 tokens
  - Detailed description = 300+ tokens
```

**When to Use Images**:
```
Perfect for:
  ✓ UI layouts and designs
  ✓ Error messages and stack traces
  ✓ Diagrams and flowcharts
  ✓ Data visualizations
  ✓ Before/after comparisons

Not suitable for:
  ✗ Code (use text for searchability)
  ✗ Large amounts of text
  ✗ Terminal output (copy-paste is better)
```

---

## 7. MCP (MODEL CONTEXT PROTOCOL)

### What Is MCP?

**Definition**: Standardized protocol for connecting AI assistants to external tools and data sources.

**Analogy**: USB for AI
- USB: Standard way to connect devices to computers
- MCP: Standard way to connect tools to AI

---

### MCP Architecture

**Components**:
```
Claude Code (Host)
    ↓ (JSON-RPC over stdio)
MCP Server (Tool Provider)
    ↓
External Resources (Files, APIs, Databases, etc.)
```

**Protocol Flow**:
```
1. Initialization:
   Host → Server: initialize(capabilities)
   Server → Host: initialized(tools, resources)

2. Tool Discovery:
   Host → Server: tools/list()
   Server → Host: [list of available tools]

3. Tool Invocation:
   Host → Server: tools/call(name, arguments)
   Server → Host: result or error

4. Cleanup:
   Host → Server: shutdown()
```

---

### MCP Messages (JSON-RPC)

**Tool List Request**:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 1
}
```

**Tool List Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "semantic_search",
        "description": "Search documents by meaning",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {"type": "string"},
            "k": {"type": "number", "default": 5}
          },
          "required": ["query"]
        }
      }
    ]
  }
}
```

**Tool Call Request**:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "semantic_search",
    "arguments": {
      "query": "Lambda optimization",
      "k": 5
    }
  },
  "id": 2
}
```

**Tool Call Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 5 results:\n1. Use ARM64 for 20% savings\n..."
      }
    ]
  }
}
```

---

### Building an MCP Server

**Minimal Example** (Python):
```python
from mcp import Server, Tool
from mcp.server import stdio_server

# Create server
server = Server("my-tools")

# Define a tool
@server.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic calculations"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Run server
if __name__ == "__main__":
    stdio_server(server)
```

**Configuration** (claude-code-mcp-config.json):
```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["C:/path/to/server.py"],
      "env": {}
    }
  }
}
```

---

### MCP Server Best Practices

**1. Tool Naming**:
```
Good:
  - semantic_search
  - index_file
  - get_user_profile

Bad:
  - search (too generic)
  - do_thing (unclear)
  - x (meaningless)
```

**2. Error Handling**:
```python
@server.tool()
def read_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        raise McpError(
            code="FILE_NOT_FOUND",
            message=f"File not found: {path}"
        )
    except PermissionError:
        raise McpError(
            code="PERMISSION_DENIED",
            message=f"Cannot read file: {path}"
        )
```

**3. Input Validation**:
```python
@server.tool()
def search(query: str, limit: int = 10) -> list:
    # Validate inputs
    if not query:
        raise ValueError("Query cannot be empty")
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")

    # Perform search
    results = do_search(query, limit)
    return results
```

**4. Async Operations**:
```python
import asyncio

@server.tool()
async def async_search(query: str) -> list:
    # Long-running operations should be async
    results = await asyncio.to_thread(expensive_search, query)
    return results
```

---

### Token Cost of MCPs

**Why MCPs Consume Tokens**:

Every MCP server adds to Claude's context:
1. Tool definitions (names, descriptions, schemas)
2. Example usage
3. Error handling info

**Example Token Breakdown**:
```
Sequential-thinking MCP:
  - 5 tools
  - Complex schemas (reasoning steps, branching, etc.)
  - Detailed descriptions
  = ~15-20K tokens

GitHub MCP:
  - 25 tools (repos, issues, PRs, commits, etc.)
  - Large API surface
  - Many parameters per tool
  = ~15-20K tokens

Simple filesystem MCP:
  - 10 tools (read, write, list, etc.)
  - Simple schemas
  = ~8-10K tokens
```

**Optimization Strategy**:
```
1. Profile usage (which MCPs actually used?)
2. Disable rarely-used MCPs
3. Create lightweight wrappers for specific tasks
4. Re-enable on-demand when needed
```

---

## 8. GRAPH-BASED MEMORY

### Knowledge Graph Concepts

**What Is a Knowledge Graph**:
```
Nodes (Entities):
  - People: "Claude", "User"
  - Concepts: "Lambda", "Optimization"
  - Projects: "Active Genie", "AARP"

Edges (Relations):
  - "implements" → "Active Genie implements CORS"
  - "optimizes" → "ARM64 optimizes Lambda"
  - "contains" → "Active Genie contains API Gateway"
```

**Example Graph**:
```
(Active Genie) --[uses]--> (AWS Cognito)
       |
       |--[implements]--> (CORS)
       |
       |--[has component]--> (API Gateway)
                                  |
                                  |--[connects to]--> (Lambda)
```

---

### Memory MCP (Knowledge Graph)

**Schema**:
```
Entity:
  - name: String
  - entityType: String
  - observations: List[String]

Relation:
  - from: String (entity name)
  - to: String (entity name)
  - relationType: String
```

**Operations**:
```python
# Create entities
create_entities([
    {
        "name": "Active Genie",
        "entityType": "Project",
        "observations": [
            "Angular 20 application",
            "Uses AWS Cognito for auth",
            "Implements MFA"
        ]
    },
    {
        "name": "AWS Cognito",
        "entityType": "Service",
        "observations": [
            "Authentication service",
            "Supports MFA",
            "Managed by AWS"
        ]
    }
])

# Create relations
create_relations([
    {
        "from": "Active Genie",
        "to": "AWS Cognito",
        "relationType": "uses"
    }
])

# Search
search_nodes("authentication")
# Returns: AWS Cognito, Active Genie

# Open specific nodes
open_nodes(["Active Genie"])
# Returns: Full entity with observations and relations
```

---

### Graph Algorithms

#### 1. **Breadth-First Search (BFS)**

**Purpose**: Find shortest path between nodes.

```python
def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == end:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found
```

**Example**:
```
Find path from "Active Genie" to "Lambda":

Active Genie → API Gateway → Lambda

Result: ["Active Genie", "API Gateway", "Lambda"]
```

#### 2. **PageRank** (Importance Scoring)

**Purpose**: Determine most important nodes in graph.

```python
def pagerank(graph, damping=0.85, max_iter=100):
    N = len(graph)
    ranks = {node: 1/N for node in graph}

    for _ in range(max_iter):
        new_ranks = {}

        for node in graph:
            # Base rank (random jump)
            rank = (1 - damping) / N

            # Add rank from incoming links
            for source in graph:
                if node in graph[source]:
                    out_degree = len(graph[source])
                    rank += damping * ranks[source] / out_degree

            new_ranks[node] = rank

        ranks = new_ranks

    return ranks
```

**Example Results**:
```
API Gateway: 0.35  (Central hub)
Lambda: 0.25       (Many connections)
Active Genie: 0.20 (Project node)
AWS Cognito: 0.15  (Auth service)
CORS: 0.05         (Implementation detail)
```

#### 3. **Community Detection**

**Purpose**: Find clusters of related nodes.

```python
def detect_communities(graph):
    # Louvain algorithm (simplified)
    communities = {node: {node} for node in graph}

    improved = True
    while improved:
        improved = False

        for node in graph:
            current_community = communities[node]
            best_community = current_community
            best_modularity = calculate_modularity(graph, communities)

            # Try moving node to each neighbor's community
            for neighbor in graph[node]:
                neighbor_community = communities[neighbor]

                # Simulate move
                test_communities = communities.copy()
                test_communities[node] = neighbor_community

                # Calculate new modularity
                new_modularity = calculate_modularity(graph, test_communities)

                if new_modularity > best_modularity:
                    best_modularity = new_modularity
                    best_community = neighbor_community
                    improved = True

            communities[node] = best_community

    return communities
```

**Example**:
```
Community 1 (AWS Infrastructure):
  - API Gateway
  - Lambda
  - AWS Cognito
  - S3

Community 2 (Frontend):
  - Active Genie
  - Angular Components
  - UI Services

Community 3 (Security):
  - CORS
  - MFA
  - JWT
```

---

## 9. AUTO-COMPACTION ALGORITHMS

### Problem Statement

**Issue**: LLM context windows are finite (200K tokens for Claude).

**Challenge**: Long conversations exceed context window.

**Solution**: Compress conversation history while preserving important information.

---

### Compaction Strategies

#### 1. **Importance-Based Retention**

```python
def importance_score(message):
    score = 0

    # User messages always important
    if message.role == "user":
        score += 5

    # Contains code
    if has_code_block(message.content):
        score += 3

    # Contains decision
    decision_keywords = ["decided", "chosen", "will use", "implemented"]
    if any(kw in message.content.lower() for kw in decision_keywords):
        score += 3

    # Contains error/warning
    if "error" in message.content.lower() or "warning" in message.content.lower():
        score += 2

    # Length bonus (longer = more substantial)
    if len(message.content) > 500:
        score += 1

    return score

def retain_important(messages, threshold=5):
    return [msg for msg in messages if importance_score(msg) >= threshold]
```

#### 2. **Sliding Window with Summaries**

```python
def sliding_window_compact(messages, window_size=50, summarize_every=10):
    """
    Keep recent window_size messages.
    Summarize older messages in chunks.
    """
    if len(messages) <= window_size:
        return messages

    # Recent messages (keep as-is)
    recent = messages[-window_size:]

    # Older messages (summarize)
    older = messages[:-window_size]

    # Break into chunks
    chunks = [older[i:i+summarize_every]
              for i in range(0, len(older), summarize_every)]

    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = llm.summarize(
            messages=chunk,
            max_tokens=200,
            preserve=["decisions", "code", "errors"]
        )
        summaries.append(summary)

    # Combine: summaries + recent messages
    return summaries + recent
```

**Example**:
```
Original: 100 messages, 150K tokens
Window: 50 recent messages (50K tokens)
Summaries: 5 summaries × 200 tokens = 1K tokens
Total: 51K tokens (66% reduction)
```

#### 3. **Hierarchical Summarization**

```python
def hierarchical_compact(messages):
    """
    Multi-level summarization for extreme compression.
    """
    # Level 1: Group by topic
    topics = cluster_by_topic(messages)

    # Level 2: Summarize each topic
    topic_summaries = []
    for topic, msgs in topics.items():
        summary = llm.summarize(msgs, max_tokens=300)
        topic_summaries.append({
            'topic': topic,
            'summary': summary,
            'message_count': len(msgs)
        })

    # Level 3: Create meta-summary
    if len(topic_summaries) > 10:
        meta_summary = llm.summarize(
            "\n\n".join(s['summary'] for s in topic_summaries),
            max_tokens=500
        )
        return [meta_summary] + recent_messages(messages, count=20)
    else:
        return topic_summaries + recent_messages(messages, count=30)
```

**Compression Levels**:
```
Level 0 (Original): 200K tokens
Level 1 (Topic summaries): 50K tokens (75% reduction)
Level 2 (Meta-summary): 10K tokens (95% reduction)
```

---

### Your Auto-Compact System

**Thresholds**:
```
Level 1: 50K tokens
  Action: Gentle reminder "Consider /compact"

Level 2: 80K tokens
  Action: Strong suggestion "Please /compact"

Level 3: 120K tokens
  Action: Urgent warning "/compact NOW"

Critical: 180K tokens
  Action: Auto-compact (forced)
```

**Strategy**:
```python
def auto_compact(messages, current_tokens):
    if current_tokens < 80000:
        # No compaction needed
        return messages

    elif current_tokens < 120000:
        # Gentle compaction
        return sliding_window_compact(
            messages,
            window_size=50,
            summarize_every=10
        )

    elif current_tokens < 180000:
        # Aggressive compaction
        return sliding_window_compact(
            messages,
            window_size=30,
            summarize_every=5
        )

    else:
        # Critical: Maximum compression
        return hierarchical_compact(messages)
```

---

## 10. IMAGE-FIRST COMMUNICATION

### Vision Model Architecture

**How Claude Processes Images**:

**Step 1: Image Tiling**
```
Input: 1920×1080 image
Process:
  1. Split into 512×512 tiles
  2. Overlap tiles by 10% (for continuity)
  3. Resize if needed

Result: 4-6 tiles
```

**Step 2: Vision Encoding**
```
For each tile:
  1. Pass through vision encoder (ViT - Vision Transformer)
  2. Generate 256-dim embedding per patch (16×16 patches)
  3. Result: ~16×16 = 256 patch embeddings per tile
```

**Step 3: Integration with Language Model**
```
Patch embeddings (from vision) + text embeddings (from prompt)
    ↓
Combined into unified representation
    ↓
Claude processes both together
```

**Token Cost**:
```
Fixed cost per tile: ~8-10 tokens
Total tiles: 4-6 for typical screenshot
Total cost: 40-60 tokens

Independent of:
  - Image complexity
  - Amount of text in image
  - Number of UI elements
```

---

### When to Use Images vs Text

**Images Win**:
```
✓ UI layouts and designs (80% token savings)
✓ Error messages with context (70% savings)
✓ Diagrams and flowcharts (85% savings)
✓ Before/after comparisons (75% savings)
✓ Complex visual relationships (90% savings)
```

**Text Wins**:
```
✓ Code (searchability, syntax highlighting)
✓ Long documents (images can't be copied)
✓ Terminal output (need to copy-paste)
✓ Logs (need to search/grep)
✓ JSON/YAML configs (need to edit)
```

**Hybrid Approach** (Best):
```
Screenshot + brief text context:

"[Screenshot of login form]
Fix the button alignment (should be centered) and change
color from #3A80D2 to #4A90E2"

Tokens: 50 (image) + 25 (text) = 75 tokens

vs

Text-only description:
"The login form has a button that's misaligned 5px to the right
instead of being centered. The button is currently #3A80D2 blue
but should be #4A90E2. The button has 8px border radius which is
correct. The text color is white which is good. The font size is
14px which is correct. The padding is 12px 24px which is good..."

Tokens: 300+ tokens
```

---

## 11. PROJECT ISOLATION PATTERNS

### Multi-Tenancy in Memory

**Goal**: Keep project memories separate while allowing global knowledge.

**Schema**:
```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    scope TEXT CHECK(scope IN ('global', 'project')),
    project_name TEXT,  -- NULL for global
    content TEXT,
    importance INTEGER,
    timestamp DATETIME,

    -- Ensure project_name set for project scope
    CHECK (
        (scope = 'global' AND project_name IS NULL) OR
        (scope = 'project' AND project_name IS NOT NULL)
    )
);

-- Indexes for efficient queries
CREATE INDEX idx_scope_project ON memories(scope, project_name);
```

**Query Patterns**:
```python
# Project-specific search
def search_project(project_name, query):
    sql = """
        SELECT * FROM memories
        WHERE (scope = 'project' AND project_name = ?)
           OR scope = 'global'
        ORDER BY importance DESC
        LIMIT 10
    """
    return db.execute(sql, [project_name])

# Cross-project search (find patterns)
def search_all_projects(query):
    sql = """
        SELECT project_name, COUNT(*) as match_count
        FROM memories
        WHERE scope = 'project'
          AND content MATCH ?
        GROUP BY project_name
        ORDER BY match_count DESC
    """
    return db.execute(sql, [query])
```

---

### Vector Store Isolation

**Directory Structure**:
```
unified-memory/
└── vector-store/
    ├── global/
    │   └── chroma.sqlite3
    │
    ├── active-genie-nginx/
    │   └── chroma.sqlite3
    │
    ├── aarp/
    │   └── chroma.sqlite3
    │
    └── peoplesoft-rag-research/
        └── chroma.sqlite3
```

**Lazy Loading**:
```python
class IsolatedVectorStore:
    def __init__(self, base_path):
        self.base_path = base_path
        self.stores = {}  # Cache

    def get_store(self, project_name):
        if project_name not in self.stores:
            # Lazy load on first access
            path = os.path.join(self.base_path, project_name)
            self.stores[project_name] = ChromaDB(persist_directory=path)
        return self.stores[project_name]

    def search(self, query, projects=None, k=5):
        if projects is None:
            # Search all projects
            all_results = []
            for project in os.listdir(self.base_path):
                store = self.get_store(project)
                results = store.similarity_search(query, k=k)
                all_results.extend([{
                    'project': project,
                    'content': r.page_content,
                    'score': r.metadata.get('score', 0)
                } for r in results])

            # Sort by score, return top k
            all_results.sort(key=lambda x: x['score'], reverse=True)
            return all_results[:k]
        else:
            # Search specific projects
            results = []
            for project in projects:
                store = self.get_store(project)
                results.extend(store.similarity_search(query, k=k))
            return results
```

---

## 12. PROMPT ENGINEERING TECHNIQUES

### Advanced Techniques Used

#### 1. **Chain-of-Thought (CoT)**

**Concept**: Guide model to show reasoning steps.

**Example**:
```
Without CoT:
  User: "Is 127 a prime number?"
  AI: "Yes"

With CoT:
  User: "Is 127 a prime number? Think step by step."
  AI: "Let me check if 127 is prime:
       1. Check if divisible by 2: 127 is odd, so no
       2. Check if divisible by 3: 1+2+7=10, not divisible by 3
       3. Check if divisible by 5: doesn't end in 0 or 5
       4. Check up to √127 ≈ 11.3
       5. 7: 127 ÷ 7 = 18.14... (no)
       6. 11: 127 ÷ 11 = 11.54... (no)
       Therefore, 127 is prime."
```

**Implementation in Your System**:
```
Sequential-thinking MCP (disabled for token optimization):
  - Structured reasoning with numbered steps
  - Ability to revise earlier thinking
  - Branch and explore alternatives
  - Token cost: 15-20K (2x normal due to thinking process)
```

#### 2. **Few-Shot Learning**

**Concept**: Provide examples to guide response format.

**Example**:
```
Prompt:
  "Extract key information from text. Format as JSON.

  Example 1:
  Text: 'Claude Code uses MCP servers for external tools.'
  Output: {'technology': 'Claude Code', 'feature': 'MCP servers',
           'purpose': 'external tools'}

  Example 2:
  Text: 'LangChain enables semantic search with vector databases.'
  Output: {'technology': 'LangChain', 'feature': 'semantic search',
           'method': 'vector databases'}

  Now process: 'FastAPI provides async support for Python APIs.'
  "

AI Output:
  {'technology': 'FastAPI', 'feature': 'async support',
   'context': 'Python APIs'}
```

#### 3. **XML-Structured Prompts**

**Concept**: Use XML tags for clear structure.

**Example**:
```
<task>
Analyze this code for security vulnerabilities
</task>

<code>
def login(username, password):
    query = f"SELECT * FROM users WHERE name='{username}' AND pass='{password}'"
    return db.execute(query)
</code>

<rules>
- Check for SQL injection
- Check for password handling
- Check for input validation
- Rate severity (Critical/High/Medium/Low)
</rules>

<output_format>
{
  "vulnerabilities": [
    {"type": "...", "severity": "...", "description": "...", "fix": "..."}
  ]
}
</output_format>
```

**Benefits**:
- 39% better response quality (industry benchmark)
- Clear separation of concerns
- Easier to parse programmatically

#### 4. **Meta-Prompting**

**Concept**: Prompt model to generate its own prompts.

**Example**:
```
User: "I need a prompt for code review"

AI generates:
  "Please review this code for:
   1. **Correctness**: Does it work as intended?
   2. **Performance**: Are there efficiency issues?
   3. **Security**: Any vulnerabilities?
   4. **Maintainability**: Is it readable and well-structured?
   5. **Best Practices**: Does it follow conventions?

   Code:
   ```python
   [insert code here]
   ```

   Provide:
   - Overall rating (1-10)
   - Specific issues with line numbers
   - Suggested improvements
   - Compliments on good patterns"
```

**Your `/improve-prompt` Command**: Uses this technique!

---

### Prompt Optimization Principles

#### 1. **Be Specific**
```
Bad:
  "Review this code"

Good:
  "Review this Python function for:
   - SQL injection vulnerabilities
   - Input validation issues
   - Error handling
   Provide specific line numbers and fixes"
```

#### 2. **Provide Context**
```
Bad:
  "Fix this bug"

Good:
  "This is a FastAPI endpoint that handles user authentication.
   The bug: Users can't log in when username has spaces.
   Expected: Spaces should be allowed in usernames.
   Please fix and explain the issue."
```

#### 3. **Specify Output Format**
```
Bad:
  "What are the main points?"

Good:
  "Extract main points as a numbered list with 3-5 items.
   Each item should be 1-2 sentences."
```

#### 4. **Use Delimiters**
```
"Analyze this code:

 ```python
 [code here]
 ```

 Consider these requirements:

 <requirements>
 - Must handle 1000 req/sec
 - Must validate all inputs
 - Must log all errors
 </requirements>
"
```

#### 5. **Iterate and Refine**
```
Prompt v1:
  "Optimize this code"
  → Generic suggestions

Prompt v2:
  "Optimize this code for speed"
  → Better, but still vague

Prompt v3:
  "This code processes 1M records in 10 seconds.
   Target: 3 seconds. Optimize for speed.
   Current bottleneck: Database queries (30% of time).
   Database: PostgreSQL with 16GB RAM.
   Can we use caching? batch operations?"
  → Specific, actionable optimizations
```

---

## 🎓 SUMMARY & LEARNING PATH

### Technology Stack Covered

✅ **Vector Databases**: ChromaDB, FAISS, embeddings, similarity search
✅ **LangChain**: Document loaders, chains, retrievers, RAG
✅ **Memory Systems**: SQLite, knowledge graphs, consolidation
✅ **MCP Protocol**: Tool definition, JSON-RPC, server creation
✅ **Token Optimization**: Dynamic loading, compaction, image-first
✅ **Prompt Engineering**: CoT, few-shot, XML structure, meta-prompting

### Algorithms & Techniques

✅ **Search**: BM25, cosine similarity, hybrid search, re-ranking
✅ **Embeddings**: Sentence-transformers, attention mechanism, pooling
✅ **Graphs**: BFS, PageRank, community detection
✅ **Compression**: Importance scoring, sliding window, hierarchical summarization
✅ **Classification**: Auto-classification, importance scoring

### Learning Resources

**Next Steps**:
1. Experiment with LangChain (re-enable MCP when needed semantic search)
2. Build custom MCP server (YouTube integration!)
3. Explore graph algorithms (play with memory-bank MCP)
4. Optimize prompts (use `/improve-prompt` command)
5. Deep dive into transformers (understand embeddings better)

**Recommended Reading**:
- LangChain documentation: https://python.langchain.com/
- ChromaDB docs: https://docs.trychroma.com/
- Sentence-Transformers: https://www.sbert.net/
- MCP specification: https://modelcontextprotocol.io/
- Prompt engineering guide: https://www.promptingguide.ai/

---

**You now have a complete understanding of the algorithms and techniques powering your Claude Code setup!** 🎓
