# BERT vs GPT Model Families

<div class="topic-checkbox-container" data-topic-id="part1-bert-vs-gpt">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part1-bert-vs-gpt">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-learn">Learn</div>
<div class="provider-icon provider-claude">Best: Claude</div>

**Estimated Time**: 4-6 hours
**Prerequisites**: Transformer Architecture, Attention Mechanisms
**Part**: Core LLM & Transformer Fundamentals

## What, Why, When

### BERT: Bidirectional Encoder
- **Architecture**: Encoder-only transformer
- **Training**: Masked Language Modeling (MLM) + Next Sentence Prediction (NSP)
- **Use Cases**: Understanding tasks (classification, NER, Q&A)

### GPT: Autoregressive Decoder
- **Architecture**: Decoder-only transformer
- **Training**: Next-token prediction (causal language modeling)
- **Use Cases**: Generation tasks (text completion, chat, creative writing)

### Key Difference
- **BERT sees full context** (bidirectional): Good for understanding
- **GPT sees only left context** (unidirectional): Good for generation

## Core Comparisons

### 1. Architecture

| Aspect | BERT | GPT |
|--------|------|-----|
| **Type** | Encoder-only | Decoder-only |
| **Attention** | Bidirectional | Causal (masked) |
| **Training** | MLM | Next-token prediction |
| **Context** | Full sentence | Left-to-right |
| **Best For** | Understanding | Generation |

### 2. Training Objectives

**BERT (Masked Language Modeling)**:
```
Input:  "The [MASK] sat on the mat"
Task:   Predict [MASK] = "cat"
Uses:   Full context (left + right)
```

**GPT (Causal Language Modeling)**:
```
Input:  "The cat sat on"
Task:   Predict next token = "the"
Uses:   Only left context
```

### 3. Attention Masks

**BERT - Full Attention**:
```
      The  cat  sat  on  the  mat
The    ✓    ✓    ✓   ✓   ✓    ✓
cat    ✓    ✓    ✓   ✓   ✓    ✓
sat    ✓    ✓    ✓   ✓   ✓    ✓
```
Every token attends to every token.

**GPT - Causal Attention**:
```
      The  cat  sat  on  the  mat
The    ✓    ✗    ✗   ✗   ✗    ✗
cat    ✓    ✓    ✗   ✗   ✗    ✗
sat    ✓    ✓    ✓   ✗   ✗    ✗
```
Tokens only attend to previous tokens.

## Hands-On Exercises

### Exercise 1: Compare Model Outputs (45 min)

```python
from transformers import BertForMaskedLM, GPT2LMHeadModel, AutoTokenizer
import torch

# Load BERT
bert_model = BertForMaskedLM.from_pretrained("bert-base-uncased")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Load GPT-2
gpt_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt_tokenizer = AutoTokenizer.from_pretrained("gpt2")

# BERT: Masked prediction
text_bert = "The capital of France is [MASK]."
inputs_bert = bert_tokenizer(text_bert, return_tensors="pt")
mask_token_index = torch.where(inputs_bert["input_ids"] == bert_tokenizer.mask_token_id)[1]

with torch.no_grad():
    outputs_bert = bert_model(**inputs_bert)
    predictions = outputs_bert.logits[0, mask_token_index]
    top_tokens = torch.topk(predictions, 5, dim=1).indices[0].tolist()

print("BERT predictions for [MASK]:")
for token_id in top_tokens:
    print(f"  {bert_tokenizer.decode([token_id])}")

# GPT-2: Next token prediction
text_gpt = "The capital of France is"
inputs_gpt = gpt_tokenizer(text_gpt, return_tensors="pt")

with torch.no_grad():
    outputs_gpt = gpt_model(**inputs_gpt)
    next_token_logits = outputs_gpt.logits[0, -1, :]
    top_tokens = torch.topk(next_token_logits, 5).indices.tolist()

print("\nGPT-2 predictions for next token:")
for token_id in top_tokens:
    print(f"  {gpt_tokenizer.decode([token_id])}")
```

**Analysis**:
- Do both models predict "Paris"?
- How do predictions differ?
- Which is more confident?

---

### Exercise 2: Task-Specific Performance (60 min)

```python
# Test both models on different tasks

# Task 1: Sentiment Classification (BERT better)
from transformers import pipeline

bert_classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
text = "This movie was absolutely fantastic!"
print(f"BERT Sentiment: {bert_classifier(text)}")

# Task 2: Text Generation (GPT better)
gpt_generator = pipeline("text-generation", model="gpt2")
prompt = "Once upon a time"
print(f"\nGPT Generation: {gpt_generator(prompt, max_length=50)[0]['generated_text']}")

# Task 3: Question Answering (BERT better)
bert_qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
context = "The Eiffel Tower is located in Paris, France. It was built in 1889."
question = "Where is the Eiffel Tower?"
print(f"\nBERT Q&A: {bert_qa(question=question, context=context)['answer']}")
```

**Questions**:
1. Why is BERT better for sentiment classification?
2. Why is GPT better for generation?
3. Can GPT do question answering? How?

---

### Exercise 3: Architecture Comparison (30 min)

```python
# Compare model sizes and parameters

from transformers import AutoConfig

bert_config = AutoConfig.from_pretrained("bert-base-uncased")
gpt_config = AutoConfig.from_pretrained("gpt2")

print("BERT Architecture:")
print(f"  Layers: {bert_config.num_hidden_layers}")
print(f"  Hidden Size: {bert_config.hidden_size}")
print(f"  Attention Heads: {bert_config.num_attention_heads}")
print(f"  Vocabulary: {bert_config.vocab_size}")
print(f"  Max Position: {bert_config.max_position_embeddings}")

print("\nGPT-2 Architecture:")
print(f"  Layers: {gpt_config.n_layer}")
print(f"  Hidden Size: {gpt_config.n_embd}")
print(f"  Attention Heads: {gpt_config.n_head}")
print(f"  Vocabulary: {gpt_config.vocab_size}")
print(f"  Max Position: {gpt_config.n_positions}")

# Count parameters
def count_parameters(model):
    return sum(p.numel() for p in model.parameters())

bert_params = count_parameters(bert_model)
gpt_params = count_parameters(gpt_model)

print(f"\nBERT Parameters: {bert_params:,}")
print(f"GPT-2 Parameters: {gpt_params:,}")
```

---

## When to Use Each Model

### Use BERT (Encoder) When:
- ✅ **Classification**: Sentiment, spam detection
- ✅ **Named Entity Recognition**: Extract entities from text
- ✅ **Question Answering**: Find answer spans in context
- ✅ **Semantic Similarity**: Compare sentence embeddings
- ✅ **Understanding Tasks**: Need full context

### Use GPT (Decoder) When:
- ✅ **Text Generation**: Stories, articles, code
- ✅ **Chatbots**: Conversational AI
- ✅ **Completion**: Autocomplete, suggestions
- ✅ **Translation**: With training
- ✅ **Creative Writing**: Poems, scripts

### Use Encoder-Decoder (T5, BART) When:
- ✅ **Summarization**: Condense long documents
- ✅ **Translation**: Language-to-language
- ✅ **Paraphrasing**: Rewrite text
- ✅ **Question Generation**: Create questions from context

## Modern Variants

### BERT Family
- **RoBERTa**: BERT + better training (no NSP, larger batches)
- **ALBERT**: Smaller version with parameter sharing
- **DistilBERT**: Distilled, faster, 97% accuracy
- **ELECTRA**: Discriminator instead of MLM (more efficient)

### GPT Family
- **GPT-2**: 1.5B parameters, better generation
- **GPT-3**: 175B parameters, few-shot learning
- **GPT-3.5**: Instruction-tuned (ChatGPT base)
- **GPT-4**: Multimodal, better reasoning

### Claude (Anthropic)
- Constitutional AI approach
- Long context (200K tokens)
- Encoder-decoder hybrid architecture (speculated)

## Provider Comparison

| Provider | Model Family | Best Use Cases |
|----------|--------------|----------------|
| **Claude** | Hybrid (speculated) | Long context, reasoning, conversation |
| **GPT** | Decoder-only | Generation, chat, creative tasks |
| **BERT** | Encoder-only | Classification, NER, understanding |

## Real-World Examples

### BERT Use Cases
- Google Search (understanding queries)
- Gmail (spam classification)
- Healthcare (clinical note analysis)

### GPT Use Cases
- GitHub Copilot (code generation)
- ChatGPT (conversational AI)
- Content creation (articles, marketing copy)

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part1-bert-vs-gpt"
              placeholder="Compare BERT and GPT..."></textarea>
    <div class="notes-auto-save">💾 Auto-saves to browser localStorage</div>
</div>

## Related Topics

- [Transformer Architecture](transformer-architecture.md)
- [Attention Mechanisms](attention-mechanisms.md)
- [Tokenization & Embeddings](tokenization-embeddings.md)

<div class="dashboard-actions">
    <a href="tokenization-embeddings.md" class="btn btn-primary">Next: Tokenization →</a>
    <a href="attention-mechanisms.md" class="btn btn-secondary">← Previous</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>

</div>
