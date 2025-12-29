# RAG Architecture Basics

<div class="topic-checkbox-container" data-topic-id="part3-rag-architecture">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part3-rag-architecture">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-learn">Learn</div>

**Estimated Time**: 5-7 hours | **Prerequisites**: Embeddings, Vector DBs | **Part**: RAG Architecture

## What is RAG?

**RAG = Retrieval Augmented Generation**

Instead of relying solely on LLM's training data:
1. **Retrieve** relevant documents from knowledge base
2. **Augment** prompt with retrieved context
3. **Generate** response using LLM + context

## Basic RAG Flow

```
Query → Embed → Vector Search → Retrieve Top-K → Build Prompt → LLM → Response
```

## Code Example

```python
import openai
import chromadb

client = chromadb.Client()
collection = client.get_collection("docs")

def rag_query(question):
    # 1. Retrieve
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results['documents'][0])
    
    # 2. Augment prompt
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    
    # 3. Generate
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

answer = rag_query("What is Python?")
```

## Key Components

1. **Document Store**: Where documents live
2. **Embedding Model**: Converts text to vectors
3. **Vector Database**: Stores and searches embeddings
4. **Retriever**: Finds relevant documents
5. **LLM**: Generates final response

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part3-rag-architecture"></textarea>
</div>

<div class="dashboard-actions">
    <a href="prompt-engineering.md" class="btn btn-primary">Next: Prompt Engineering →</a>
</div>

</div>
