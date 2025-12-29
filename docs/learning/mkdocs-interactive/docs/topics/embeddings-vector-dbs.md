# Embeddings & Vector Databases

<div class="topic-checkbox-container" data-topic-id="part2-embeddings-vector-dbs">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part2-embeddings-vector-dbs">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>
<div class="provider-icon provider-gpt">Code: GPT</div>

**Estimated Time**: 6-8 hours | **Prerequisites**: Embeddings basics | **Part**: Data Engineering for AI

## What, Why, When

**Vector Database** = Database optimized for storing and searching high-dimensional vectors (embeddings).

**Use Cases**:
- Semantic search in RAG systems
- Recommendation engines
- Similarity search
- Duplicate detection

## Popular Vector Databases

| Database | Type | Best For | Pricing |
|----------|------|----------|---------|
| **Chroma** | Open-source | Local development | Free |
| **Pinecone** | Cloud | Production, scale | Paid ($70+/mo) |
| **Weaviate** | Open-source/Cloud | Hybrid search | Free/Paid |
| **Milvus** | Open-source | Large scale | Free |
| **pgvector** | Postgres extension | Existing Postgres | Free |
| **Qdrant** | Open-source/Cloud | Fast queries | Free/Paid |

## Hands-On: Chroma Example

```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize Chroma
client = chromadb.Client()
collection = client.create_collection(
    name="my_documents",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

# Add documents
documents = [
    "The cat sits on the mat",
    "A dog barks at the mailman",
    "Python is a programming language"
]
metadatas = [{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}]
ids = ["id1", "id2", "id3"]

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

# Query
results = collection.query(
    query_texts=["Tell me about pets"],
    n_results=2
)

print(results['documents'])
print(results['distances'])
```

## Key Concepts

**HNSW Algorithm**: Hierarchical Navigable Small World - fast approximate nearest neighbor search

**Similarity Metrics**:
- Cosine similarity (most common)
- Euclidean distance
- Dot product

**Metadata Filtering**: `collection.query(where={"source": "doc1"})`

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part2-embeddings-vector-dbs"></textarea>
</div>

<div class="dashboard-actions">
    <a href="semantic-search.md" class="btn btn-primary">Next: Semantic Search →</a>
    <a href="chunking-strategies.md" class="btn btn-secondary">← Previous</a>
</div>

</div>
