# Quality Scoring & Filtering

<div class="topic-checkbox-container" data-topic-id="part3-quality-scoring">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part3-quality-scoring">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 4-6 hours | **Part**: RAG Architecture

## What is Quality Scoring?

Assign scores to retrieved documents to filter low-quality results.

## Scoring Methods

### 1. Similarity Score
Vector search returns similarity (0-1).

```python
results = collection.query(query_texts=["query"], n_results=10)
scores = results['distances']  # Lower = more similar

# Filter by threshold
threshold = 0.3
filtered = [doc for doc, score in zip(results['documents'], scores) if score < threshold]
```

### 2. Cross-Encoder Reranking
More accurate scoring (covered in Reranking topic).

### 3. LLM-as-Judge
Use LLM to score relevance:

```python
def score_relevance(query, document):
    prompt = f"""
    Query: {query}
    Document: {document}
    
    Score relevance (0-10): 
    """
    response = llm(prompt)
    return int(response)
```

## Filtering Strategies

- **Top-K**: Keep top K results
- **Threshold**: Keep scores above threshold
- **Dynamic**: Adjust based on score distribution

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part3-quality-scoring"></textarea>
</div>

<div class="dashboard-actions">
    <a href="query-rewriting.md" class="btn btn-primary">Next: Query Rewriting →</a>
</div>

</div>
