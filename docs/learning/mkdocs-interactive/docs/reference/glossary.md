# Glossary

Complete glossary of AI/ML terms used throughout this syllabus.

## A

**A/B Testing**
Comparing two versions (A and B) of a prompt, model, or system to determine which performs better.

**Activation Function**
Function that introduces non-linearity in neural networks (e.g., ReLU, sigmoid, softmax).

**Agent**
An AI system that can take actions, use tools, and make decisions autonomously.

**Agentic RAG**
RAG system where the model decides when to retrieve, what to retrieve, and how to use retrieved information.

**Attention Mechanism**
Neural network component that learns to focus on relevant parts of input. Foundation of transformers.

**AWQ (Activation-aware Weight Quantization)**
Advanced quantization method that preserves important weights while compressing model size.

## B

**BERT (Bidirectional Encoder Representations from Transformers)**
Encoder-only transformer model good for understanding tasks (classification, NER, Q&A).

**Bias (AI)**
Systematic errors or unfairness in AI systems, often reflecting biases in training data.

**BM25**
Traditional keyword-based search algorithm used in hybrid search systems.

**Byte Pair Encoding (BPE)**
Subword tokenization algorithm used by GPT and many modern LLMs.

## C

**Caching**
Storing results to avoid redundant computation. Types: memory, semantic, multi-layer.

**Chain-of-Thought (CoT)**
Prompting technique where model shows reasoning steps before final answer.

**Chunking**
Splitting long documents into smaller segments for processing. Strategies: fixed-size, recursive, semantic.

**CLIP (Contrastive Language-Image Pre-training)**
Multimodal model that understands images and text together.

**Constitutional AI**
Anthropic's approach to training AI systems with built-in values and safety constraints.

**Context Window**
Maximum number of tokens an LLM can process at once (e.g., 128K, 200K, 1M tokens).

**Cosine Similarity**
Measure of similarity between two vectors (embeddings), ranges from -1 to 1.

**Cross-Encoder**
Model that directly scores query-document pairs for better ranking accuracy (used in reranking).

## D

**Decoder**
Transformer component that generates output text autoregressively (e.g., GPT).

**Distillation**
Training a smaller "student" model to mimic a larger "teacher" model.

**DPO (Direct Preference Optimization)**
Training method where model learns from human preferences directly, simpler than RLHF.

## E

**Embeddings**
Dense vector representations of text (e.g., 384D, 1536D vectors). Capture semantic meaning.

**Encoder**
Transformer component that understands input text (e.g., BERT).

**Ensemble**
Combining multiple models to improve accuracy and robustness.

**Explainability**
Ability to understand why an AI system made a specific decision. Tools: LIME, SHAP.

## F

**Fairness Metrics**
Quantitative measures of bias and fairness in AI systems (e.g., demographic parity, equal opportunity).

**Few-Shot Learning**
Learning from just a few examples provided in the prompt (e.g., 2-5 examples).

**Fine-Tuning**
Training a pre-trained model on domain-specific data to specialize its behavior.

**Function Calling**
LLM capability to call external functions/tools and use their results.

## G

**GGUF (GPT-Generated Unified Format)**
Model format for quantized models, commonly used with llama.cpp.

**GPT (Generative Pre-trained Transformer)**
Decoder-only transformer model good for generation tasks (text completion, chat, creative writing).

**GPTQ**
Post-training quantization method for compressing LLM weights.

**Graph RAG**
RAG system using knowledge graphs for structured retrieval and reasoning.

**Guardrails**
Safety constraints and filters to prevent harmful or incorrect LLM outputs.

## H

**Hallucination**
When an LLM generates plausible-sounding but incorrect or fabricated information.

**HNSW (Hierarchical Navigable Small World)**
Efficient algorithm for approximate nearest neighbor search in vector databases.

**HyDE (Hypothetical Document Embeddings)**
RAG technique where LLM generates hypothetical answer, which is used for retrieval.

**Hybrid Search**
Combining keyword search (BM25) and vector search for better retrieval.

## I

**Inference**
Process of using a trained model to make predictions or generate output.

**INT4 / INT8**
Integer quantization formats (4-bit or 8-bit) for compressing model weights.

## J

**JSON Mode**
LLM feature that guarantees valid JSON output for structured data extraction.

## K

**k-NN (k-Nearest Neighbors)**
Finding k most similar vectors in vector search.

**Knowledge Graph**
Structured representation of knowledge as entities and relationships (used in Graph RAG).

## L

**LangChain**
Popular Python framework for building LLM applications with chains, agents, and tools.

**LangGraph**
LangChain's library for building stateful multi-agent systems with graph-based workflows.

**Latency**
Time delay between request and response. Critical metric for production systems.

**LIME (Local Interpretable Model-agnostic Explanations)**
Technique for explaining individual predictions of any ML model.

**LLM (Large Language Model)**
Neural network trained on massive text corpora (e.g., GPT-4, Claude, Gemini).

**LLMOps (Large Language Model Operations)**
Practices for deploying, monitoring, and maintaining LLM applications in production.

**LoRA (Low-Rank Adaptation)**
Parameter-efficient fine-tuning that adds small trainable matrices to frozen model weights.

**LSI (Latent Semantic Indexing)**
Technique for discovering hidden semantic relationships in text.

## M

**MCP (Model Context Protocol)**
Standard protocol for integrating tools and context with LLMs.

**Metadata Filtering**
Filtering search results based on structured metadata (e.g., date, author, category).

**Multi-Agent System**
System with multiple AI agents that communicate and collaborate to solve tasks.

**Multi-Head Attention**
Attention mechanism with multiple parallel attention operations (used in transformers).

**Multimodal AI**
AI systems that process multiple types of data (text, images, audio, video).

## N

**NER (Named Entity Recognition)**
Identifying and classifying entities in text (e.g., person names, locations, organizations).

**Normalization**
Scaling data to standard range (e.g., embeddings to unit length for cosine similarity).

## O

**Observability**
Ability to monitor and understand system behavior through logs, metrics, and traces.

**ONNX (Open Neural Network Exchange)**
Standard format for representing ML models for deployment across platforms.

**OpenTelemetry**
Framework for distributed tracing and observability in production systems.

## P

**Parameter-Efficient Fine-Tuning (PEFT)**
Fine-tuning methods that update only a small subset of model parameters (e.g., LoRA, adapters).

**PII (Personally Identifiable Information)**
Sensitive data that can identify individuals (names, emails, SSNs, etc.). Must be detected and redacted.

**Positional Encoding**
Adding position information to token embeddings so transformer knows word order.

**Precision**
Proportion of retrieved items that are relevant (TP / (TP + FP)).

**Prompt Engineering**
Crafting effective prompts to elicit desired behavior from LLMs.

**Prompt Injection**
Security attack where malicious instructions are inserted into LLM prompts.

**Pruning**
Removing unnecessary weights/neurons from models to reduce size.

## Q

**QLoRA**
LoRA with 4-bit quantization, enabling fine-tuning on consumer GPUs.

**Quantization**
Reducing model weight precision (e.g., FP32 → INT8) to compress size and speed up inference.

**Query Expansion**
Generating multiple variations of a query for better retrieval coverage.

**Query Rewriting**
Transforming user queries to improve retrieval effectiveness.

## R

**RAG (Retrieval Augmented Generation)**
Enhancing LLM responses by retrieving relevant documents from external knowledge base.

**RAGAS**
Evaluation framework for RAG systems (metrics: faithfulness, relevancy, precision, recall).

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)**
Hierarchical RAG approach with recursive summarization and tree-structured retrieval.

**Recall**
Proportion of relevant items that are retrieved (TP / (TP + FN)).

**Red-Teaming**
Adversarial testing to find vulnerabilities and weaknesses in AI systems.

**Reranking**
Re-scoring retrieved results with more accurate (but slower) cross-encoder model.

**RLHF (Reinforcement Learning from Human Feedback)**
Training method where human preferences guide model behavior.

**RRF (Reciprocal Rank Fusion)**
Algorithm for combining rankings from multiple retrievers (e.g., BM25 + vector).

## S

**Semantic Caching**
Caching based on meaning similarity rather than exact string match.

**Semantic Search**
Search based on meaning/semantics rather than keywords, using embeddings.

**Self-RAG**
RAG variant where model reflects on its retrieval and generation steps.

**Sentence Transformers**
Models optimized for generating sentence/paragraph embeddings (e.g., all-MiniLM-L6-v2).

**SHAP (SHapley Additive exPlanations)**
Game theory-based approach to explain ML model predictions.

**Softmax**
Function that converts scores to probability distribution (used in attention and output layers).

**Streaming**
Sending LLM output incrementally as it's generated, rather than waiting for completion.

**Structured Output**
LLM output in structured format like JSON, XML, or with specific schema.

**Supervisor Pattern**
Multi-agent architecture where one "supervisor" agent coordinates other "worker" agents.

**System Prompt**
Initial instructions that define LLM's role, behavior, and constraints.

## T

**Temperature**
Parameter controlling randomness in LLM generation (0 = deterministic, 1+ = creative).

**TensorRT**
NVIDIA library for optimizing deep learning inference on GPUs.

**Token**
Basic unit of text processing in LLMs (roughly 0.75 words in English).

**Tokenization**
Splitting text into tokens for LLM processing.

**Tool Use**
LLM capability to call external tools/APIs and integrate their results.

**Top-k Sampling**
Sampling from top k most likely tokens during generation.

**Top-p (Nucleus) Sampling**
Sampling from smallest set of tokens whose cumulative probability exceeds p.

**Transformer**
Neural network architecture based on attention mechanism. Foundation of modern LLMs.

## U

**Upsert**
Database operation: update if exists, insert if not (common in vector DBs).

## V

**Vector Database**
Database optimized for storing and searching high-dimensional vectors (embeddings). Examples: Chroma, Pinecone, Weaviate.

**Vector Search**
Finding similar items by comparing their vector embeddings (used in RAG).

**ViT (Vision Transformer)**
Transformer architecture adapted for image processing.

## W

**Warmup**
Gradually increasing learning rate at start of training for stability.

**Weight**
Learnable parameter in neural network (billions of weights in LLMs).

## Z

**Zero-Shot Learning**
Model performing task without any task-specific examples in prompt.

---

## Usage Tips

**Search this glossary**:
- Press `Ctrl+F` (Windows) or `Cmd+F` (Mac)
- Type the term you're looking for

**See terms in context**:
- Each topic page uses these terms
- Hover tooltips may appear in interactive version

**Suggest additions**:
- Missing a term? Let us know!

---

## Quick Reference by Category

### Core Concepts
Embeddings, RAG, Semantic Search, Vector Database, LLM, Transformer

### Retrieval Techniques
BM25, Hybrid Search, HyDE, Query Rewriting, Reranking, Self-RAG, Graph RAG, RAPTOR

### Model Optimization
Quantization, LoRA, QLoRA, Distillation, Pruning, GGUF, INT4, INT8

### Evaluation
RAGAS, Precision, Recall, Faithfulness, Relevancy, LLM-as-Judge

### Security
Prompt Injection, PII, Guardrails, Red-Teaming, Bias Detection

### Production
LLMOps, Observability, Caching, Latency, OpenTelemetry, CI/CD

### Advanced
Multi-Agent, Function Calling, Multimodal, DPO, RLHF, Constitutional AI

---

<div class="dashboard-actions">
    <a href="../tracks/overview.md" class="btn btn-primary">📚 Choose Your Track</a>
    <a href="topic-map.md" class="btn btn-secondary">📋 Topic Map</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>
