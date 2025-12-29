# Reranking & Cross-Encoders

<div class="topic-checkbox-container" data-topic-id="part4-reranking">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part4-reranking">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 5-7 hours | **Part**: Advanced Retrieval

## What is Reranking?

**Two-stage retrieval**:
1. **Stage 1**: Fast vector search (retrieve top-100)
2. **Stage 2**: Accurate reranking (rerank to top-5)

## Why Reranking?

Vector search (bi-encoder) is fast but less accurate.
Cross-encoder is accurate but slow.

**Solution**: Combine both!

## Implementation

```python
from sentence_transformers import CrossEncoder

# Stage 1: Vector search
vector_results = vector_db.query(query, n_results=20)

# Stage 2: Reranking
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
pairs = [[query, doc] for doc in vector_results]
scores = reranker.predict(pairs)

# Sort by reranker scores
ranked = sorted(zip(vector_results, scores), key=lambda x: x[1], reverse=True)
top_5 = [doc for doc, score in ranked[:5]]
```

## Cross-Encoder vs Bi-Encoder

| Aspect | Bi-Encoder | Cross-Encoder |
|--------|------------|---------------|
| **Speed** | Fast | Slow |
| **Accuracy** | Good | Excellent |
| **Use** | Stage 1 (retrieval) | Stage 2 (reranking) |

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part4-reranking"></textarea>
</div>

<div class="dashboard-actions">
    <a href="hybrid-search.md" class="btn btn-primary">Next: Hybrid Search →</a>
</div>

</div>
