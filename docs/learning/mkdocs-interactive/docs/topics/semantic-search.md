# Semantic Search & Similarity

<div class="topic-checkbox-container" data-topic-id="part2-semantic-search">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part2-semantic-search">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 5-7 hours | **Prerequisites**: Embeddings, Vector DBs | **Part**: Data Engineering for AI

## What is Semantic Search?

Search based on **meaning**, not keywords.

**Traditional (Keyword) Search**:
- Query: "cat" → Finds documents with "cat"
- Misses: "feline", "kitten", "pet"

**Semantic Search**:
- Query: "cat" → Finds: "cat", "feline", "kitten", "pet", "animal"
- Uses embeddings to understand meaning

## Core Concepts

### 1. Cosine Similarity
```python
from numpy import dot
from numpy.linalg import norm

def cosine_sim(a, b):
    return dot(a, b) / (norm(a) * norm(b))

# Example
query_emb = [0.2, 0.5, 0.8]
doc_emb = [0.3, 0.6, 0.7]
similarity = cosine_sim(query_emb, doc_emb)
# Result: 0.99 (very similar!)
```

### 2. k-Nearest Neighbors (k-NN)
Find k most similar vectors to query.

### 3. Approximate Nearest Neighbors (ANN)
Faster but approximate (HNSW, IVF, LSH).

## Hands-On Example

```python
from sentence_transformers import SentenceTransformer
import chromadb

# Initialize
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("docs")

# Add documents
docs = ["Python programming", "JavaScript coding", "Coffee brewing"]
embeddings = model.encode(docs).tolist()
collection.add(documents=docs, embeddings=embeddings, ids=["1","2","3"])

# Semantic search
query = "Programming languages"
query_emb = model.encode([query]).tolist()
results = collection.query(query_embeddings=query_emb, n_results=2)

print(results['documents'])  # ["Python programming", "JavaScript coding"]
```

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part2-semantic-search"></textarea>
</div>

<div class="dashboard-actions">
    <a href="rag-architecture.md" class="btn btn-primary">Next: RAG Architecture →</a>
    <a href="embeddings-vector-dbs.md" class="btn btn-secondary">← Previous</a>
</div>

</div>
