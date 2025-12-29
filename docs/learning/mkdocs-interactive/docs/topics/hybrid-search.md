# Hybrid Search (BM25 + Vector)

<div class="topic-checkbox-container" data-topic-id="part4-hybrid-search">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part4-hybrid-search">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 5-7 hours | **Part**: Advanced Retrieval

## What is Hybrid Search?

**Combine keyword search (BM25) + semantic search (vectors)** for best of both worlds!

## BM25 vs Vector Search

| Aspect | BM25 | Vector Search |
|--------|------|---------------|
| **Type** | Keyword-based | Semantic |
| **Strengths** | Exact matches, names, IDs | Meaning, synonyms |
| **Weaknesses** | Misses semantics | Misses exact terms |

## Hybrid Search Formula

```
final_score = α × BM25_score + (1-α) × vector_score
```

Where α = 0.5 typically (equal weight).

## Implementation

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.vectorstores import Chroma

# BM25 retriever
bm25_retriever = BM25Retriever.from_documents(documents)

# Vector retriever
vector_store = Chroma.from_documents(documents, embeddings)
vector_retriever = vector_store.as_retriever()

# Hybrid ensemble
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.5, 0.5]  # Equal weight
)

# Search
results = ensemble_retriever.get_relevant_documents("query")
```

## When to Use Hybrid

✅ Use when:
- Both exact matches and semantics matter
- Diverse query types (names, concepts, descriptions)
- Maximum recall needed

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part4-hybrid-search"></textarea>
</div>

<div class="dashboard-actions">
    <a href="structured-output.md" class="btn btn-primary">Next: Structured Output →</a>
</div>

</div>
