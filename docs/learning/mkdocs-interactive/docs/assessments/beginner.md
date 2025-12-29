# Beginner Checkpoint Assessment

Complete this assessment after finishing Week 6 of the Beginner Track.

## Overview

**Total Points**: 50
**Pass Score**: 38+ (75%)
**Time Limit**: 2 hours

## Part 1: Conceptual Knowledge (20 points)

### Question 1: Transformer Architecture (5 points)

Explain the transformer architecture and its key components. Include:
- What problem does it solve compared to RNNs?
- Name and describe the 6 main components
- Why is self-attention important?

**Grading Rubric**:
- (5) Comprehensive explanation with all components
- (3-4) Good explanation, missing some details
- (1-2) Basic understanding, significant gaps
- (0) Incorrect or no answer

---

### Question 2: Attention Mechanisms (5 points)

Explain how self-attention works:
- What are Query, Key, and Value vectors?
- How does the attention mechanism compute relevance?
- What is the purpose of multi-head attention?

**Grading Rubric**:
- (5) Clear explanation with correct understanding
- (3-4) Good explanation with minor gaps
- (1-2) Partial understanding
- (0) Incorrect or no answer

---

### Question 3: RAG vs Fine-Tuning (5 points)

When should you use RAG vs fine-tuning?

Provide a decision framework considering:
- Cost
- Latency
- Data requirements
- Use cases for each

**Grading Rubric**:
- (5) Comprehensive trade-off analysis
- (3-4) Good understanding with minor gaps
- (1-2) Basic understanding
- (0) Incorrect or no answer

---

### Question 4: Security Awareness (5 points)

Explain prompt injection attacks:
- What is a prompt injection?
- Give 2 examples of attacks
- Name 3 defense strategies

**Grading Rubric**:
- (5) Complete explanation with examples and defenses
- (3-4) Good understanding, some details missing
- (1-2) Basic awareness
- (0) Incorrect or no answer

---

## Part 2: Technical Skills (30 points)

### Project 1: Local RAG Q&A Bot (15 points)

**Checklist**:
- [ ] (3) Ingested 100+ documents successfully
- [ ] (3) Implemented chunking (800 tokens, 100 overlap)
- [ ] (3) Built working Q&A interface (CLI or web)
- [ ] (3) Calculated precision@5 and recall@10 on 20 test queries
- [ ] (3) Documented results and challenges

**Submission**:
- GitHub repo URL
- README with setup instructions
- Evaluation report (metrics, analysis, next steps)

---

### Project 2: Conversational Agent (15 points)

**Checklist**:
- [ ] (2) LangGraph state machine implemented
- [ ] (2) Query rewriting with 3 variations
- [ ] (2) Cross-encoder reranking (top-20 → top-5)
- [ ] (3) Semantic caching with >50% hit rate
- [ ] (2) Prompt injection defense implemented
- [ ] (2) Deployed as FastAPI REST API
- [ ] (2) Security testing report included

**Submission**:
- GitHub repo URL
- OpenAPI documentation
- Caching hit rate report
- Security testing results
- Performance benchmarks

---

## Part 3: Code Review (Bonus)

Submit one code snippet from your projects that you're most proud of. Explain:
- What problem it solves
- Why you chose this approach
- What you learned

**Bonus Points**: +5 for exceptional code quality and explanation

---

## Scoring Guide

| Score | Grade | Interpretation |
|-------|-------|----------------|
| 45-50 | A+ | Exceptional - Ready for Standard Track |
| 38-44 | A | Pass - Ready for Standard Track |
| 30-37 | B | Close - Review weak areas, then proceed |
| 20-29 | C | Not Ready - Complete more exercises |
| 0-19 | D/F | Restart Track - Fundamental gaps |

---

## Self-Assessment

Before submitting, rate yourself honestly:

### Conceptual Understanding
- [ ] I can explain transformers to a non-technical person
- [ ] I understand when to use RAG vs fine-tuning
- [ ] I'm aware of security risks in LLM applications
- [ ] I can explain attention mechanisms clearly

### Technical Skills
- [ ] Both projects are complete and working
- [ ] I've tested my code thoroughly
- [ ] My code follows best practices (tests, docs, error handling)
- [ ] I can deploy my application

### Areas for Improvement
List 2-3 topics you want to strengthen:
1. _____________________________
2. _____________________________
3. _____________________________

---

## Submission

Submit your assessment via:

1. **GitHub Repository** with:
   - Both projects (Project 1 & 2)
   - README files with setup instructions
   - Evaluation reports
   - Test results

2. **Written Responses** (PDF or Markdown):
   - Answers to all conceptual questions
   - Self-assessment checklist
   - Areas for improvement

3. **Optional**: Demo video (5-10 minutes)

---

## What's Next?

### If You Pass (38+)
**Congratulations!** 🎉 You're ready for the [Standard Track](../tracks/standard.md).

**Next Steps**:
1. Take a 1-week break or review weak areas
2. Start planning Project 3 (Multi-Agent System)
3. Begin Week 4 of Standard Track

### If You Don't Pass (<38)
**Don't worry!** Learning AI takes time.

**Recommended Actions**:
1. Review topics where you scored lowest
2. Redo exercises you struggled with
3. Ask AI assistants (Claude, GPT) for help
4. Join AI learning communities (Discord, Reddit)
5. Retake assessment in 2 weeks

---

## Common Mistakes

**Conceptual Questions**:
- ❌ Memorizing definitions without understanding
- ✅ Explain concepts in your own words with examples

**Projects**:
- ❌ Copying code without understanding
- ✅ Build incrementally, test each component

**Evaluation**:
- ❌ Skipping metric calculation
- ✅ Actually run 20 test queries and measure results

---

## Resources for Review

If you need to review before assessment:

- [Transformer Architecture](../topics/transformer-architecture.md)
- [RAG Architecture Basics](../tracks/beginner.md#week-2)
- [Security Basics](../tracks/beginner.md#week-6)
- [Main Syllabus](../../AI-Prep-Syllabus-Provider-Map-v2.0-FINAL.md)

---

<div class="dashboard-actions">
    <a href="../tracks/standard.md" class="btn btn-primary">Continue to Standard Track →</a>
    <a href="../tracks/beginner.md" class="btn btn-secondary">← Review Beginner Track</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>
