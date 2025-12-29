# Tokenization & Embeddings

<div class="topic-checkbox-container" data-topic-id="part1-tokenization-embeddings">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part1-tokenization-embeddings">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-learn">Learn</div>
<div class="provider-icon provider-claude">Concepts: Claude</div>
<div class="provider-icon provider-gpt">Code: GPT</div>

**Estimated Time**: 5-7 hours
**Prerequisites**: Basic NLP concepts
**Part**: Core LLM & Transformer Fundamentals

## What: Tokenization

**Tokenization** = Converting text into tokens (subwords/words) that models can process.

**Why Not Character-Level?**
- Too many sequence steps (long sequences)
- Less semantic meaning per token

**Why Not Word-Level?**
- Huge vocabulary (100K+ words)
- Can't handle unknown words
- Misses subword patterns

**Solution: Subword Tokenization**
- Balance between characters and words
- Handles unknown words by breaking into known pieces
- Vocabulary size: 30K-50K tokens

### Common Algorithms

1. **BPE (Byte Pair Encoding)** - GPT, GPT-2
2. **WordPiece** - BERT
3. **SentencePiece** - T5, mT5
4. **Unigram** - Alternative approach

## What: Embeddings

**Embeddings** = Dense vector representations of tokens.

**Example**:
- Token "cat" → [0.2, -0.5, 0.8, ..., 0.1] (384 dimensions)
- Token "dog" → [0.3, -0.4, 0.7, ..., 0.0] (384 dimensions)

**Key Property**: Similar tokens have similar embeddings.
- cosine_similarity("cat", "dog") = 0.85 (high)
- cosine_similarity("cat", "car") = 0.32 (low)

## Hands-On Exercises

### Exercise 1: Tokenizer Comparison (45 min)

```python
from transformers import AutoTokenizer

# Load different tokenizers
tokenizers = {
    "GPT-2 (BPE)": AutoTokenizer.from_pretrained("gpt2"),
    "BERT (WordPiece)": AutoTokenizer.from_pretrained("bert-base-uncased"),
    "T5 (SentencePiece)": AutoTokenizer.from_pretrained("t5-small"),
}

text = "The quick brown fox jumps over the lazy dog. Antidisestablishmentarianism!"

for name, tokenizer in tokenizers.items():
    tokens = tokenizer.tokenize(text)
    token_ids = tokenizer.encode(text)

    print(f"\n{name}")
    print(f"  Tokens: {tokens}")
    print(f"  IDs: {token_ids}")
    print(f"  Count: {len(tokens)}")
```

**Analysis**:
1. How do they tokenize "Antidisestablishmentarianism"?
2. Which is most efficient (fewest tokens)?
3. How do they handle punctuation?

---

### Exercise 2: Embeddings Similarity (60 min)

```python
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example sentences
sentences = [
    "The cat sits on the mat",
    "A feline rests on a rug",
    "Dogs bark loudly at night",
    "Python is a programming language",
    "The weather is sunny today"
]

# Generate embeddings
embeddings = model.encode(sentences)
print(f"Embedding shape: {embeddings.shape}")  # (5, 384)

# Compute similarity matrix
similarities = cosine_similarity(embeddings)

# Print results
print("\nSimilarity Matrix:")
for i, sent1 in enumerate(sentences):
    for j, sent2 in enumerate(sentences):
        if i < j:
            sim = similarities[i][j]
            print(f"{sent1[:30]:30s} <-> {sent2[:30]:30s}: {sim:.3f}")
```

**Questions**:
1. Which sentences are most similar?
2. Why are cat/feline sentences similar?
3. How does dimensionality affect similarity?

---

### Exercise 3: Token-Level Embeddings (45 min)

```python
from transformers import AutoModel, AutoTokenizer
import torch

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

text = "The cat sat on the mat"
inputs = tokenizer(text, return_tensors="pt")

# Get token embeddings
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state  # [1, seq_len, 768]

tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

print(f"Text: {text}")
print(f"Tokens: {tokens}")
print(f"Embeddings shape: {embeddings.shape}")

# Similarity between "cat" and "mat"
cat_emb = embeddings[0, tokens.index('cat')]
mat_emb = embeddings[0, tokens.index('mat')]
sim = torch.cosine_similarity(cat_emb.unsqueeze(0), mat_emb.unsqueeze(0))
print(f"\nSimilarity('cat', 'mat'): {sim.item():.3f}")
```

---

## Common Tokenization Issues

### 1. Out-of-Vocabulary (OOV)
**Problem**: New words not in training vocabulary
**Solution**: Subword tokenization breaks unknown words

### 2. Different Vocabularies
**Problem**: GPT vs BERT tokens differ
**Solution**: Use model-specific tokenizer

### 3. Context Length
**Problem**: Max tokens (512 BERT, 2048 GPT-2)
**Solution**: Chunking or sliding window

### 4. Special Tokens
- `[CLS]`: Start token (BERT)
- `[SEP]`: Separator (BERT)
- `[PAD]`: Padding token
- `[UNK]`: Unknown token

## Embedding Dimensions

| Model | Embedding Dim | Use Case |
|-------|---------------|----------|
| all-MiniLM-L6-v2 | 384 | Fast, general purpose |
| all-mpnet-base-v2 | 768 | Better quality |
| text-embedding-ada-002 | 1536 | OpenAI (paid) |
| BERT-base | 768 | Token embeddings |
| GPT-2 | 768-1600 | Varies by size |

**Trade-off**: Higher dimensions = better quality but slower + more storage.

## Provider Comparison

| Provider | Tokenizer | Embedding API | Cost |
|----------|-----------|---------------|------|
| **OpenAI** | tiktoken | text-embedding-ada-002 | $0.0001/1K tokens |
| **Anthropic** | Custom | No public embedding API | - |
| **Sentence Transformers** | HuggingFace | all-MiniLM-L6-v2 (local) | Free |
| **Cohere** | Custom | embed-english-v3.0 | $0.0001/1K tokens |

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part1-tokenization-embeddings"
              placeholder="Notes on tokenization and embeddings..."></textarea>
    <div class="notes-auto-save">💾 Auto-saves</div>
</div>

## Related Topics

- [Transformer Architecture](transformer-architecture.md)
- [Embeddings & Vector Databases](embeddings-vector-dbs.md)
- [Semantic Search](semantic-search.md)

<div class="dashboard-actions">
    <a href="../tracks/beginner.md#week-2" class="btn btn-primary">Next: Week 2 →</a>
    <a href="bert-vs-gpt.md" class="btn btn-secondary">← Previous</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>

</div>
