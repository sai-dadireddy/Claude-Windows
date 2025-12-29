# Prompt Engineering

<div class="topic-checkbox-container" data-topic-id="part3-prompt-engineering">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part3-prompt-engineering">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 6-8 hours | **Part**: RAG Architecture

## What is Prompt Engineering?

**Prompt Engineering** = Crafting effective prompts to get desired LLM behavior.

## Key Techniques

### 1. Zero-Shot
```
Classify sentiment: "This movie was great!"
```

### 2. Few-Shot
```
Classify sentiment:
"Amazing!" → Positive
"Terrible!" → Negative
"This movie was great!" → ?
```

### 3. Chain-of-Thought (CoT)
```
Question: What is 15% of 80?
Let's think step by step:
1. 15% = 15/100 = 0.15
2. 0.15 × 80 = 12
Answer: 12
```

### 4. System Prompts
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant expert in Python."},
    {"role": "user", "content": "How do I reverse a string?"}
]
```

## Best Practices

- Be specific and clear
- Provide examples (few-shot)
- Use delimiters (```, ---, ###)
- Specify output format
- Iterate and test

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part3-prompt-engineering"></textarea>
</div>

<div class="dashboard-actions">
    <a href="evaluation-basics.md" class="btn btn-primary">Next: Evaluation →</a>
</div>

</div>
