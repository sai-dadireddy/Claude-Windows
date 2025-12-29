# Standard Track (10 Weeks)

**Goal**: Multi-agent production system with LLMOps

## Overview

- **Duration**: 10 weeks
- **Hours**: 150 (15 hours/week)
- **Topics**: 1-40
- **Projects**: 3
- **Outcome**: Production-ready multi-agent system with CI/CD

## Week-by-Week Plan

### Week 1-3: Foundation (Beginner Track Content - Accelerated)

Complete all Beginner Track content at faster pace:
- LLM Fundamentals
- Data Engineering & RAG Foundations
- Evaluation & Advanced Retrieval
- Production Basics & Security
- Projects 1-2 completed

**Accelerated Schedule**: 3 weeks instead of 6 (requires 15 hours/week focus)

---

### Week 4: Advanced Context Management (15h)

**Topics**:
- Prompt Compression & Summarization
- Long Context Strategies (RAG vs Long Context)
- Context Window Management
- Multi-Turn Conversation Design

**Exercises**:
- Implement prompt compression pipeline
- Compare RAG vs 200K context window
- Build multi-turn conversation system

**Deliverable**: Conversation manager with context optimization

---

### Week 5: RAG System Patterns (15h)

**Topics**:
- Self-RAG (Self-reflective retrieval)
- Graph RAG (Knowledge graphs + vector search)
- Agentic RAG (Tool-calling + retrieval)
- RAPTOR (Hierarchical retrieval)

**Project 3 Start**: Multi-Agent System
- Design agent architecture
- Implement supervisor pattern
- Set up LangGraph state machine

**Deliverable**: Multi-agent architecture design doc

---

### Week 6: Multi-Agent Systems (15h)

**Topics**:
- Supervisor Patterns
- Agent Communication Protocols
- Domain Expert Agents
- Tool Use & Function Calling

**Project 3 Continue**:
- Implement 3+ domain expert agents
- Build supervisor orchestration
- Add tool calling capabilities
- Implement state management

**Deliverable**: Working multi-agent system with 3+ experts

---

### Week 7: Model Optimization (15h)

**Topics**:
- Quantization (GGUF, AWQ, GPTQ)
- LoRA & QLoRA Fine-Tuning
- Model Distillation
- Pruning Techniques

**Exercises**:
- Quantize model to 4-bit/8-bit
- Fine-tune with LoRA on custom dataset
- Benchmark latency improvements

**Deliverable**: Optimized model deployment plan

---

### Week 8: Advanced Evaluation & Observability (15h)

**Topics**:
- RAGAS Advanced Metrics
- LLM-as-Judge Patterns
- Component-Wise Evaluation
- Distributed Tracing (OpenTelemetry)

**Project 3 Continue**:
- Add comprehensive evaluation suite
- Implement distributed tracing
- Set up metrics dashboard
- Create evaluation reports

**Deliverable**: Full observability stack with metrics

---

### Week 9: LLMOps & CI/CD (15h)

**Topics**:
- Prompt Version Control
- A/B Testing for Prompts
- Model Registry & Versioning
- Blue-Green Deployments

**Project 3 Continue**:
- Set up GitHub Actions CI/CD
- Implement automated testing pipeline
- Add prompt version control
- Configure blue-green deployment

**Deliverable**: Complete CI/CD pipeline

---

### Week 10: Advanced Security & Deployment (15h)

**Topics**:
- Advanced Prompt Injection Defense
- Data Poisoning Detection
- Red-Teaming LLM Systems
- Compliance (GDPR, HIPAA)

**Project 3 Complete**:
- Add advanced security controls
- Implement red-team testing
- Create compliance documentation
- Deploy to production environment
- Final security audit

**Deliverable**: Production-deployed multi-agent system with security certification

---

## Assessment: Intermediate Checkpoint

**After Week 10**, complete the [Intermediate Checkpoint](../assessments/intermediate.md):

**Conceptual Knowledge** (30 points):
- Understand multi-agent patterns
- Know when to use RAG vs long context
- Explain LLMOps best practices
- Understand model optimization techniques

**Technical Skills** (50 points):
- Completed Projects 1-3
- Deployed production multi-agent system
- Implemented CI/CD pipeline
- Achieved 95%+ test coverage

**Architecture & Design** (20 points):
- Clean agent architecture
- Proper state management
- Comprehensive observability
- Security-first design

**Pass Score**: 75+/100

---

## Projects Detail

### Projects 1-2
Complete all Beginner Track projects (see [Beginner Track](beginner.md))

### Project 3: Multi-Agent Production System (Weeks 5-10)

**Time**: 45-50 hours

**Requirements**:
- **Architecture**: Supervisor pattern with 3+ domain expert agents
- **State Management**: LangGraph state machine
- **Tool Calling**: Function calling with 5+ tools
- **Retrieval**: Advanced RAG (Self-RAG or Graph RAG)
- **Evaluation**: RAGAS suite with custom metrics
- **Observability**: OpenTelemetry distributed tracing
- **Security**: Advanced prompt injection defense, PII redaction
- **CI/CD**: GitHub Actions with automated testing
- **Deployment**: Production deployment with monitoring

**System Architecture**:
```
┌─────────────────────────────────────────────────┐
│              Supervisor Agent                    │
│  (Orchestration, routing, error handling)       │
└─────────────┬───────────────────────────────────┘
              │
    ┌─────────┴─────────┬──────────────────┬──────────────┐
    ▼                   ▼                  ▼              ▼
┌─────────┐      ┌─────────┐       ┌─────────┐   ┌─────────┐
│ Retrieval│      │ Analysis │       │  Code   │   │ Quality │
│  Agent   │      │  Agent   │       │  Agent  │   │ Control │
│          │      │          │       │         │   │  Agent  │
│ (RAG)    │      │ (LLM)    │       │ (Tools) │   │ (Eval)  │
└─────────┘      └─────────┘       └─────────┘   └─────────┘
```

**Tech Stack**:
- LangChain + LangGraph
- FastAPI (REST API)
- Redis (caching + state)
- PostgreSQL (metadata)
- Chroma/Pinecone (vector DB)
- OpenTelemetry (tracing)
- Prometheus + Grafana (metrics)
- GitHub Actions (CI/CD)

**API Endpoints**:
```python
POST /agent/query
{
  "query": "Analyze sales data for Q4",
  "user_id": "user123",
  "context": {...}
}

Response:
{
  "answer": "...",
  "agent_path": ["supervisor", "retrieval", "analysis"],
  "sources": [...],
  "latency_ms": 2345,
  "trace_id": "abc123"
}

GET /agent/status
GET /metrics
POST /agent/feedback
```

**Deliverables**:
1. **Architecture Document**: System design, agent responsibilities, communication protocols
2. **GitHub Repo**: Complete source code with README, tests, CI/CD
3. **Evaluation Report**: RAGAS metrics, component-wise scores, performance benchmarks
4. **Security Audit**: Penetration test results, compliance checklist
5. **Deployment Guide**: Infrastructure setup, monitoring configuration
6. **Demo Video**: 5-min walkthrough of system capabilities

**Evaluation Criteria**:
- **Functionality** (30%): All requirements met, system works end-to-end
- **Architecture** (20%): Clean design, proper separation of concerns
- **Code Quality** (15%): Tests, documentation, best practices
- **Performance** (15%): Latency <3s, cache hit rate >60%
- **Security** (10%): Passes injection tests, PII handling
- **Observability** (10%): Complete tracing, metrics, logging

---

## Study Tips

### Time Management
- **Weeks 1-3**: Fast-paced (covering Beginner content)
- **Weeks 4-10**: Deep dives into advanced topics
- **Project 3**: Parallelize work (e.g., implement agents while learning observability)

### Learning Strategy
- **Concept → Practice → Build**: Learn theory, do exercises, apply in project
- **Incremental Development**: Add one feature at a time to Project 3
- **Test Everything**: Write tests as you build, not after

### Getting Unstuck
- **Modular Development**: If stuck on agents, work on CI/CD instead
- **Use AI**: Ask Claude for architecture advice, GPT for debugging
- **Community**: LangChain Discord, GitHub issues are helpful
- **Checkpoint Reviews**: Review your work weekly, adjust as needed

---

## Next Steps

<div class="dashboard-actions">
    <a href="../topics/prompt-engineering.md" class="btn btn-primary">Start Week 4 →</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
    <a href="overview.md" class="btn btn-secondary">← All Tracks</a>
</div>

---

## Comparison with Other Tracks

| Aspect | Beginner | **Standard** | Deep Mastery |
|--------|----------|--------------|--------------|
| **Duration** | 6 weeks | **10 weeks** | 16 weeks |
| **Hours** | 90 | **150** | 240 |
| **Topics** | 1-20 | **1-40** | 1-52 (all) |
| **Projects** | 2 | **3** | 4 |
| **Multi-Agent** | ❌ | **✅** | ✅ |
| **LLMOps** | ❌ | **✅** | ✅ |
| **Fine-Tuning** | ❌ | ❌ | ✅ |
| **Edge Deploy** | ❌ | ❌ | ✅ |

**Ready for Standard Track?** You should have:
- ✅ Completed Projects 1-2 from Beginner Track
- ✅ Comfortable with Python, APIs, databases
- ✅ Understanding of RAG, embeddings, vector search
- ✅ 15 hours/week available for 10 weeks
