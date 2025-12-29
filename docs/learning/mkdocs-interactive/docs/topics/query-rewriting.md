# Query Rewriting & Expansion

<div class="topic-checkbox-container" data-topic-id="part4-query-rewriting">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part4-query-rewriting">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 5-7 hours | **Part**: Advanced Retrieval

## What is Query Rewriting?

Transform user query to improve retrieval.

**Original**: "best restaurants nyc"
**Rewritten**: "What are the best restaurants in New York City?"

## Techniques

### 1. Query Expansion
```python
def expand_query(query, llm):
    prompt = f"Generate 3 similar queries to: '{query}'"
    variations = llm(prompt).split('\n')
    return [query] + variations

# Result: ["best restaurants nyc", "top dining NYC", "where to eat New York"]
```

### 2. HyDE (next topic)
### 3. Multi-Query RAG

```python
from langchain.retrievers import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm
)

docs = retriever.get_relevant_documents("query")
```

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part4-query-rewriting"></textarea>
</div>

<div class="dashboard-actions">
    <a href="hyde.md" class="btn btn-primary">Next: HyDE →</a>
</div>

</div>
