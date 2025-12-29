# Transformer Architecture

<div data-topic-id="part1-transformer-architecture">

## Overview

<div class="study-mode-tag study-mode-learn">Learn</div>
<div class="provider-icon provider-claude">Best: Claude</div>
<div class="provider-icon provider-gpt">Code: GPT</div>
<div class="provider-icon provider-gemini">Math: Gemini</div>

**Estimated Time**: 6-8 hours
**Prerequisites**: Linear algebra basics, Python proficiency
**Next Topics**: Attention Mechanisms, BERT vs GPT

---

## What, Why, When

### What is the Transformer Architecture?

The Transformer is a neural network architecture introduced in "Attention Is All You Need" (2017) that revolutionized NLP. Unlike RNNs/LSTMs, it processes all tokens in parallel using **self-attention mechanisms**.

**Key Innovation**: Instead of processing sequences one token at a time, transformers use attention to look at the entire sequence simultaneously.

### Why Learn This?

1. **Foundation of all modern LLMs**: GPT, BERT, Claude, Gemini all built on transformers
2. **Better debugging**: Understanding architecture helps diagnose model behavior
3. **Model selection**: Know which architecture fits your task
4. **Required for fine-tuning**: Can't fine-tune effectively without understanding architecture

### When to Learn?

**NOW - Before any other topic.** This is the foundation. Without understanding transformers, you're using LLMs as black boxes.

---

## Core Components

The transformer has 6 main components:

### 1. Input Embeddings
Converts text tokens into dense vectors (e.g., 768 dimensions).

```python
# Simplified
token_ids = [101, 2023, 2003, ...]  # Token IDs
embeddings = embedding_layer(token_ids)  # [seq_len, d_model]
```

### 2. Positional Encoding
Adds position information (transformers have no inherent sequence awareness).

```python
def positional_encoding(position, d_model):
    PE = np.zeros((position, d_model))
    for pos in range(position):
        for i in range(0, d_model, 2):
            PE[pos, i] = np.sin(pos / (10000 ** (2*i/d_model)))
            PE[pos, i+1] = np.cos(pos / (10000 ** (2*i/d_model)))
    return PE
```

### 3. Multi-Head Self-Attention
Multiple attention mechanisms in parallel. Allows model to focus on different aspects simultaneously.

### 4. Feed-Forward Networks
Process attended representations independently for each position.

### 5. Layer Normalization
Stabilizes training by normalizing activations.

### 6. Output Layer
Generates next token probabilities (softmax over vocabulary).

---

## Architecture Diagram

```
Input Text → Tokenization → [tokens]
    ↓
Embedding Layer → [vectors]
    ↓
+ Positional Encoding
    ↓
[Repeated N times:]
    Multi-Head Self-Attention
    ↓
    Add & Normalize
    ↓
    Feed-Forward Network
    ↓
    Add & Normalize
    ↓
Output Layer (softmax over vocabulary)
```

---

## Provider Strengths

| Provider | Best For | Example Prompt |
|----------|----------|----------------|
| **Claude** | Conceptual understanding, explaining intuition | "Explain transformer self-attention using an analogy. Why is it called 'attention'?" |
| **GPT/Codex** | Implementing from scratch, debugging | "Implement multi-head attention in PyTorch with detailed comments" |
| **Gemini** | Mathematical foundations, paper summaries | "Explain the math behind scaled dot-product attention. Why divide by sqrt(d_k)?" |

---

## Hands-On Exercises

### Exercise 1: Attention Visualization (60 min)

**Goal**: Visualize which tokens attend to which.

```python
from transformers import AutoModel, AutoTokenizer
import matplotlib.pyplot as plt
import seaborn as sns

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name, output_attentions=True)

text = "The cat sat on the mat"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)

# Get attention from first layer, first head
attention = outputs.attentions[0][0, 0].detach().numpy()
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

# Plot
plt.figure(figsize=(10, 8))
sns.heatmap(attention, xticklabels=tokens, yticklabels=tokens, cmap="Blues")
plt.title("Attention Weights")
plt.show()
```

**Questions to Answer**:
- Which tokens does "cat" attend to most?
- Do all heads show the same pattern?
- What attends to [CLS] token?

**Deliverable**: Jupyter notebook with heatmaps and analysis

---

### Exercise 2: Implement Attention from Scratch (90 min)

**Goal**: Understand attention by building it yourself.

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V):
    """
    Q, K, V: [batch, seq_len, d_k]
    Returns: output, attention_weights
    """
    d_k = Q.shape[-1]

    # Compute scores
    scores = np.matmul(Q, K.transpose(0, 2, 1)) / np.sqrt(d_k)

    # Softmax
    attention = softmax(scores)

    # Apply to values
    output = np.matmul(attention, V)

    return output, attention
```

**Task**: Complete the implementation, test with toy data, verify shapes.

**Deliverable**: Python script with tests

---

### Exercise 3: Compare Model Architectures (60 min)

**Goal**: Understand differences between BERT, GPT-2, T5.

```python
from transformers import AutoModel

bert = AutoModel.from_pretrained("bert-base-uncased")
gpt2 = AutoModel.from_pretrained("gpt2")
t5 = AutoModel.from_pretrained("t5-small")

print("BERT config:", bert.config)
print("GPT-2 config:", gpt2.config)
print("T5 config:", t5.config)

# Compare:
# - Number of layers
# - Number of attention heads
# - Hidden size
# - Vocabulary size
```

**Deliverable**: Comparison table documenting differences

---

## Knowledge Rubric

**Self-Assessment**: Where are you?

- [ ] **Level 1 (Beginner)**: Can explain what transformers do at high level
- [ ] **Level 2 (Intermediate)**: Understands attention formula, can use pre-trained transformers
- [ ] **Level 3 (Advanced)**: Implements attention from scratch, understands positional encoding
- [ ] **Level 4 (Expert)**: Designs custom transformer variants, optimizes for specific tasks

---

## Common Pitfalls

### Problem: Attention weights all similar (no focus)
**Debug**:
1. Check temperature/scaling: too high → uniform attention
2. Verify positional encoding added correctly
3. Inspect gradients: vanishing gradient issue?

### Problem: Model output makes no sense
**Debug**:
1. Verify tokenization: `print(tokenizer.convert_ids_to_tokens(input_ids))`
2. Check mask applied correctly
3. Ensure model in eval mode: `model.eval()`

### Problem: Slow inference
**Solutions**:
- Use smaller model (distilbert vs bert-large)
- Batch inputs together
- Use quantization (int8)
- Enable Flash Attention

---

## Observability

**Metrics to Track**:

```python
# Model inspection
total_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total_params:,}")

# Inference metrics
import time
start = time.time()
outputs = model(**inputs)
latency = time.time() - start
print(f"Inference latency: {latency*1000:.2f}ms")

# Attention entropy (how focused?)
import scipy.stats
attention_entropy = scipy.stats.entropy(attention.flatten())
print(f"Attention entropy: {attention_entropy:.3f}")
```

---

## Security Considerations

1. **Model Weights Integrity**: Verify checksums when loading pre-trained models
2. **Input Length Limits**: Enforce max sequence length to prevent DoS
3. **Tokenization Attacks**: Some tokenizers vulnerable to adversarial inputs

---

## Connections to Other Topics

- → **Embeddings**: Transformer output = contextualized embeddings
- → **Fine-Tuning**: Understanding architecture required for LoRA, PEFT
- → **Prompt Engineering**: Attention patterns explain why prompt structure matters
- → **RAG**: Retrieval provides additional context for transformer's attention

---

## Resources

**Papers**:
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (original paper)

**Tutorials**:
- [The Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)
- [Harvard NLP Annotated Transformer](https://nlp.seas.harvard.edu/2018/04/03/attention.html)

**Code**:
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)

---

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea
        class="topic-notes-textarea"
        data-notes-for="part1-transformer-architecture"
        placeholder="Add your personal notes here...&#10;&#10;Examples:&#10;- Key insights you discovered&#10;- Code snippets that worked&#10;- Questions to research later&#10;- Links to helpful resources"
    ></textarea>
    <div class="notes-auto-save">💾 Auto-saves to browser localStorage</div>
</div>

---

## Next Steps

<div class="dashboard-actions">
    <a href="attention-mechanisms.md" class="btn btn-primary">Next: Attention Mechanisms →</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 View Dashboard</a>
    <a href="../reference/topic-map.md" class="btn btn-secondary">🗺️ Topic Map</a>
</div>

</div>

<script>
// Load saved notes for this topic
document.addEventListener('DOMContentLoaded', () => {
    const topicId = 'part1-transformer-architecture';
    const notesTextarea = document.querySelector(`textarea[data-notes-for="${topicId}"]`);

    if (notesTextarea) {
        const progress = JSON.parse(localStorage.getItem('ai-syllabus-progress') || '{}');
        const savedNotes = progress.notes?.[topicId]?.content || '';
        notesTextarea.value = savedNotes;
    }
});
</script>
