# Beginner Fast Track (6 Weeks)

**Goal**: Build production RAG system with caching and security

## Overview

- **Duration**: 6 weeks
- **Hours**: 90 (15 hours/week)
- **Topics**: 1-20
- **Projects**: 2
- **Outcome**: Deployed RAG API

## Week-by-Week Plan

### Week 1: LLM Fundamentals (15h)
**Topics**:
- Transformer Architecture
- Attention Mechanisms
- BERT vs GPT Model Families
- Tokenization & Embeddings

**Exercises**:
- Visualize attention weights
- Implement attention from scratch
- Compare model architectures

**Deliverable**: Jupyter notebook explaining transformers

---

### Week 2: Data Engineering & Foundations (15h)
**Topics**:
- Data Ingestion Pipeline
- Advanced Chunking Strategies
- Embeddings & Semantic Search
- RAG Architecture Basics

**Project 1 Start**: Local RAG Q&A Bot
- Ingest 100+ documents
- Implement chunking
- Build Q&A interface

**Deliverable**: Working Q&A over local documents

---

### Week 3: RAG & Evaluation (15h)
**Topics**:
- Prompt Engineering
- Evaluation Basics (Precision/Recall)
- Quality Scoring

**Project 1 Complete**: Add evaluation
- Implement precision@5, recall@10 metrics
- Test with 20 queries
- Document results

**Deliverable**: Evaluated RAG system with metrics report

---

### Week 4: Advanced Retrieval (15h)
**Topics**:
- Query Rewriting & Expansion
- HyDE (Hypothetical Docs)
- Reranking & Cross-Encoders
- Hybrid Search (BM25 + Vector)

**Project 2 Start**: Conversational Agent
- LangGraph flow
- Multi-query expansion
- Cross-encoder reranking

**Deliverable**: Multi-query RAG with reranking

---

### Week 5: Production Basics (15h)
**Topics**:
- Structured Output (JSON)
- Function Calling & Tool Use
- Semantic Caching
- Observability Basics

**Project 2 Continue**:
- Add semantic caching
- Implement observability
- Monitor cache hit rates

**Deliverable**: Cached agent with metrics dashboard

---

### Week 6: Security & Deployment (15h)
**Topics**:
- Prompt Injection Defense
- PII Detection & Redaction
- Guardrails
- Real-Time Streaming

**Project 2 Complete**:
- Add security controls
- Deploy as REST API
- Security audit report

**Deliverable**: Production-ready REST API with security

---

## Assessment: Beginner Checkpoint

**After Week 6**, complete the [Beginner Checkpoint](../assessments/beginner.md):

**Conceptual Knowledge** (20 points):
- Explain transformer architecture
- Understand attention mechanisms
- Know when to use RAG vs fine-tuning
- Aware of prompt injection risks

**Technical Skills** (30 points):
- Completed Projects 1 & 2
- Implemented semantic search with evaluation
- Deployed secured API

**Pass Score**: 38+/50

---

## Projects Detail

### Project 1: Local RAG Q&A Bot (Weeks 2-3)
**Time**: 15-20 hours

**Requirements**:
- Ingest 100+ documents (PDF, Markdown, web scraping)
- Implement chunking (800 tokens, 100 overlap)
- Store in Chroma vector database
- Build Q&A interface (CLI or web)
- Evaluate: precision@5, recall@10 on 20 test questions

**GitHub Repo Structure**:
```
project1-rag-bot/
├── data/              # Your documents
├── src/
│   ├── ingest.py      # Data ingestion
│   ├── chunking.py    # Chunking logic
│   ├── rag.py         # RAG pipeline
│   └── evaluate.py    # Evaluation
├── notebooks/         # Exploration
├── tests/             # Unit tests
├── requirements.txt
└── README.md
```

**Evaluation Report Template**:
- **Metrics**: Precision@5, Recall@10, avg latency
- **Analysis**: Which chunk sizes worked best?
- **Challenges**: What problems did you face?
- **Next Steps**: What would you improve?

---

### Project 2: Conversational Agent (Weeks 4-6)
**Time**: 25-30 hours

**Requirements**:
- Evolve Project 1 into conversational agent
- LangGraph state machine
- Query rewriting (3 variations)
- Cross-encoder reranking (top-20 → top-5)
- Semantic caching (>50% hit rate)
- Prompt injection defense
- Deploy as FastAPI REST API
- Component-wise evaluation

**API Endpoints**:
```python
POST /chat
{
  "query": "How does attention work?",
  "user_id": "user123"
}

Response:
{
  "answer": "...",
  "sources": [...],
  "cached": false,
  "latency_ms": 1234
}
```

**Deliverable**:
- OpenAPI docs
- Caching hit rate report (target: >50%)
- Security testing report
- Performance benchmarks

---

## Study Tips

### Time Management
- **Daily**: 2 hours on weekdays, 2.5 hours on weekends
- **Focus**: One topic per session (no multitasking)
- **Breaks**: Take 10-min breaks every hour

### Learning Strategy
- **Morning**: Concepts and reading (Learn mode)
- **Afternoon**: Coding and exercises (Practice mode)
- **Evening**: Review notes, plan next day

### Getting Unstuck
- **Ask AI**: Use Claude for concepts, GPT for code
- **Search**: Check Stack Overflow, GitHub issues
- **Break it down**: Simplify the problem
- **Move on**: Come back later with fresh eyes

---

## Next Steps

<div class="dashboard-actions">
    <a href="../topics/transformer-architecture.md" class="btn btn-primary">Start Week 1 →</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
    <a href="overview.md" class="btn btn-secondary">← All Tracks</a>
</div>
