# Attention Mechanisms

<div class="topic-checkbox-container" data-topic-id="part1-attention-mechanisms">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part1-attention-mechanisms">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-learn">Learn</div>
<div class="provider-icon provider-claude">Best: Claude</div>
<div class="provider-icon provider-gpt">Code: GPT</div>

**Estimated Time**: 4-6 hours
**Prerequisites**: Transformer Architecture basics, Linear algebra
**Part**: Core LLM & Transformer Fundamentals

## What, Why, When

### What is Attention?
Attention is a mechanism that allows models to focus on relevant parts of the input when processing information. Instead of treating all input equally, attention learns what to pay attention to.

**Key Components**:
- **Query (Q)**: "What am I looking for?"
- **Key (K)**: "What information do I have?"
- **Value (V)**: "What is the actual content?"

### Why Attention Matters
- **Long-range Dependencies**: Captures relationships across entire sequences
- **Parallel Processing**: Unlike RNNs, computes all positions simultaneously
- **Interpretability**: Attention weights show what the model focuses on
- **Foundation of Transformers**: Core innovation that powers GPT, BERT, Claude

### When to Use Attention
- Natural language processing tasks (translation, summarization)
- Sequence-to-sequence modeling
- Any task requiring contextual understanding
- Computer vision (Vision Transformers)

## Core Concepts

### 1. Self-Attention Mechanism

**Formula**:
```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
```

**Process**:
1. **Compute scores**: Q · K^T (how relevant is each key to each query?)
2. **Scale**: Divide by sqrt(d_k) for numerical stability
3. **Normalize**: Apply softmax to get probabilities
4. **Weight values**: Multiply by V to get weighted output

### 2. Multi-Head Attention

Instead of one attention operation, use multiple "heads" in parallel:
- Each head learns different aspects of relationships
- Heads are concatenated and projected
- Typical: 8-16 heads in modern transformers

**Benefits**:
- Captures multiple types of relationships simultaneously
- More expressive than single attention
- Parallel computation

### 3. Scaled Dot-Product Attention

**Why scaling?**
- Without scaling: For large d_k, dot products grow large
- Large values → softmax saturates → tiny gradients
- Scaling by sqrt(d_k) keeps values reasonable

### 4. Attention Patterns

Different types of attention for different tasks:
- **Self-Attention**: Tokens attend to other tokens in same sequence (BERT)
- **Cross-Attention**: Query from one sequence, K/V from another (translation)
- **Masked Attention**: Prevents looking at future tokens (GPT)

## Hands-On Exercises

### Exercise 1: Visualize Attention Weights (60 min)

```python
from transformers import AutoModel, AutoTokenizer
import torch
import matplotlib.pyplot as plt
import seaborn as sns

# Load model with attention outputs
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, output_attentions=True)

# Input text
text = "The cat sat on the mat because it was comfortable"
inputs = tokenizer(text, return_tensors="pt")

# Get attention weights
with torch.no_grad():
    outputs = model(**inputs)
    attention = outputs.attentions  # Tuple of attention weights per layer

# Visualize attention from layer 0, head 0
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
attn_weights = attention[0][0, 0].numpy()  # [seq_len, seq_len]

plt.figure(figsize=(10, 8))
sns.heatmap(attn_weights, xticklabels=tokens, yticklabels=tokens,
            cmap='viridis', annot=True, fmt='.2f')
plt.title('Attention Weights - Layer 0, Head 0')
plt.xlabel('Key')
plt.ylabel('Query')
plt.show()
```

**Questions**:
1. Which words does "cat" attend to most?
2. How does "it" resolve its reference?
3. Compare attention patterns across different layers

---

### Exercise 2: Implement Attention from Scratch (90 min)

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads=8):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads

        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"

        # Linear projections for Q, K, V
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        batch_size, seq_len, embed_dim = x.shape

        # Project to Q, K, V
        Q = self.q_proj(x)  # [batch, seq_len, embed_dim]
        K = self.k_proj(x)
        V = self.v_proj(x)

        # Reshape for multi-head attention
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        # Now: [batch, num_heads, seq_len, head_dim]

        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        # scores: [batch, num_heads, seq_len, seq_len]

        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        # Softmax to get attention weights
        attn_weights = F.softmax(scores, dim=-1)

        # Apply attention to values
        output = torch.matmul(attn_weights, V)
        # output: [batch, num_heads, seq_len, head_dim]

        # Reshape back
        output = output.transpose(1, 2).contiguous()
        output = output.view(batch_size, seq_len, embed_dim)

        # Final projection
        output = self.out_proj(output)

        return output, attn_weights

# Test
embed_dim = 512
num_heads = 8
seq_len = 10
batch_size = 2

x = torch.randn(batch_size, seq_len, embed_dim)
attention = SelfAttention(embed_dim, num_heads)
output, weights = attention(x)

print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {weights.shape}")
```

**Tasks**:
1. Add causal masking for GPT-style attention
2. Implement cross-attention variant
3. Benchmark speed vs naive implementation

---

### Exercise 3: Attention Patterns Analysis (30 min)

```python
# Compare attention patterns for different sentence structures

sentences = [
    "The quick brown fox jumps over the lazy dog",
    "Mary had a little lamb whose fleece was white as snow",
    "To be or not to be, that is the question"
]

for sent in sentences:
    inputs = tokenizer(sent, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    # Analyze pattern
    attention = outputs.attentions[0][0, 0]  # First layer, first head
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

    # Find max attention for each token
    max_attn_idx = attention.argmax(dim=1)

    print(f"\nSentence: {sent}")
    for i, token in enumerate(tokens):
        attended_token = tokens[max_attn_idx[i]]
        print(f"{token:15s} → {attended_token:15s}")
```

---

## Provider Comparison

| Provider | Best For | Example Prompt |
|----------|----------|----------------|
| **Claude** | Explaining attention concepts, intuition | "Claude, explain self-attention using an analogy from daily life" |
| **GPT-4** | Implementing attention mechanisms, code | "Implement multi-head attention with dropout in PyTorch" |
| **Gemini** | Attention in large-scale systems | "How does Google handle attention computation at billion-token scale?" |

---

## Common Pitfalls

1. **Forgetting to Scale**: Always divide by sqrt(d_k)
2. **Mask Confusion**: Use -inf for masked positions, not 0
3. **Dimension Errors**: Carefully track [batch, heads, seq_len, head_dim]
4. **Memory Issues**: Attention is O(n²) in sequence length

---

## Real-World Applications

- **Machine Translation**: Cross-attention between source and target languages
- **Summarization**: Attention to salient sentences
- **Question Answering**: Attention to relevant context passages
- **Code Generation**: Attention to variable definitions and usage

---

## Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Original paper)
- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Attention Mechanisms in Neural Networks](https://lilianweng.github.io/posts/2018-06-24-attention/)

---

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part1-attention-mechanisms"
              placeholder="Add your personal notes, code snippets, or insights..."></textarea>
    <div class="notes-auto-save">💾 Auto-saves to browser localStorage</div>
</div>

---

## Related Topics

- [Transformer Architecture](transformer-architecture.md) - Foundation
- [BERT vs GPT Model Families](bert-vs-gpt.md) - Different attention patterns
- [Tokenization & Embeddings](tokenization-embeddings.md) - Input to attention

---

<div class="dashboard-actions">
    <a href="bert-vs-gpt.md" class="btn btn-primary">Next: BERT vs GPT →</a>
    <a href="transformer-architecture.md" class="btn btn-secondary">← Previous: Transformers</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>

</div>
