# Advanced Chunking Strategies

<div class="topic-checkbox-container" data-topic-id="part2-chunking-strategies">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part2-chunking-strategies">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>
<div class="provider-icon provider-claude">Strategy: Claude</div>
<div class="provider-icon provider-gpt">Code: GPT</div>

**Estimated Time**: 4-6 hours | **Prerequisites**: Data Ingestion | **Part**: Data Engineering for AI

## What, Why, When

**Chunking** = Splitting documents into smaller segments for embedding and retrieval.

**Why?** LLMs and embeddings have token limits (512-8192 tokens). Long documents must be split.

**Goal**: Chunks that are semantically meaningful and self-contained.

## Chunking Strategies

### 1. Fixed-Size Chunking
```python
def fixed_size_chunk(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

**Pros**: Simple, predictable
**Cons**: May split sentences/paragraphs awkwardly

### 2. Recursive Character Splitting
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(document)
```

**Pros**: Respects document structure
**Cons**: Still somewhat arbitrary

### 3. Semantic Chunking
```python
# Split by meaning, not just characters
# Uses embeddings to group similar sentences

from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

chunker = SemanticChunker(OpenAIEmbeddings())
chunks = chunker.split_text(document)
```

**Pros**: Meaningful chunks
**Cons**: Slower, requires embeddings

### 4. Document-Aware Chunking
- Markdown: Split by headers (#, ##, ###)
- Code: Split by functions/classes
- HTML: Split by sections/divs

## Best Practices

- **Chunk Size**: 500-1000 tokens typically
- **Overlap**: 10-20% of chunk size
- **Metadata**: Keep source, page number, section
- **Test**: Evaluate retrieval quality with different strategies

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part2-chunking-strategies"></textarea>
    <div class="notes-auto-save">💾 Auto-saves</div>
</div>

<div class="dashboard-actions">
    <a href="embeddings-vector-dbs.md" class="btn btn-primary">Next: Embeddings →</a>
    <a href="data-ingestion.md" class="btn btn-secondary">← Previous</a>
</div>

</div>
