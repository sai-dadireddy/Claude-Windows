# Evaluation Basics

<div class="topic-checkbox-container" data-topic-id="part3-evaluation-basics">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part3-evaluation-basics">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>

**Estimated Time**: 5-7 hours | **Part**: RAG Architecture

## Why Evaluate?

You can't improve what you don't measure!

## Key Metrics

### 1. Precision
**Precision** = Relevant Retrieved / Total Retrieved

```
Retrieved 10 docs, 7 relevant → Precision = 0.7
```

### 2. Recall
**Recall** = Relevant Retrieved / Total Relevant

```
20 relevant docs exist, retrieved 15 → Recall = 0.75
```

### 3. F1 Score
Harmonic mean of precision and recall.

```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

## RAG-Specific Metrics

### Answer Relevance
Is the answer relevant to the question?

### Faithfulness
Does the answer come from retrieved context?

### Context Precision
How relevant are retrieved documents?

### Context Recall
Are all necessary documents retrieved?

## Code Example

```python
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

# Your data
questions = ["What is Python?"]
answers = ["Python is a programming language"]
contexts = [["Python is a high-level language..."]]

# Evaluate
results = evaluate(
    questions=questions,
    answers=answers,
    contexts=contexts,
    metrics=[answer_relevancy, faithfulness]
)

print(results)
```

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part3-evaluation-basics"></textarea>
</div>

<div class="dashboard-actions">
    <a href="quality-scoring.md" class="btn btn-primary">Next: Quality Scoring →</a>
</div>

</div>
