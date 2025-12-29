# HyDE (Hypothetical Document Embeddings)

<div class="topic-checkbox-container" data-topic-id="part4-hyde">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part4-hyde">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 4-6 hours | **Part**: Advanced Retrieval

## What is HyDE?

**HyDE** = Hypothetical Document Embeddings

Instead of searching with the query, generate a hypothetical answer and search with that!

## Why HyDE Works

Queries and documents have different writing styles:
- **Query**: "best way to learn Python?"
- **Document**: "Python is learned through practice, tutorials, and projects..."

HyDE bridges this gap!

## Implementation

```python
def hyde_retrieve(query, llm, vector_db):
    # 1. Generate hypothetical answer
    prompt = f"Write a detailed answer to: {query}"
    hypothetical_answer = llm(prompt)
    
    # 2. Search using hypothetical answer
    results = vector_db.query(hypothetical_answer, n_results=5)
    
    return results

# Use
docs = hyde_retrieve("How do I learn Python?", llm, db)
```

## When to Use HyDE

✅ **Use when**:
- Query-document style mismatch
- Specific factual questions
- Technical domains

❌ **Avoid when**:
- Very short queries
- Exploratory searches
- Real-time constraints (HyDE adds latency)

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part4-hyde"></textarea>
</div>

<div class="dashboard-actions">
    <a href="reranking.md" class="btn btn-primary">Next: Reranking →</a>
</div>

</div>
