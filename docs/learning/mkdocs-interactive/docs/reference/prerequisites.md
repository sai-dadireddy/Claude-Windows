# Prerequisites

Before starting, ensure you have the following skills and tools ready.

## Technical Skills Required

### ✅ Programming (Essential)

**Python 3.9+**:
- [ ] Variables, data types, control flow
- [ ] Functions and classes (OOP basics)
- [ ] List comprehensions, lambda functions
- [ ] Exception handling
- [ ] File I/O and JSON parsing

**Recommended Resources**:
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- Practice: Complete 20 Python exercises on LeetCode Easy

**Self-Assessment**:
```python
# Can you understand and write code like this?
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

If yes → You're ready! If no → Study Python basics first.

---

### ✅ APIs & HTTP (Essential)

**Concepts**:
- [ ] RESTful API basics (GET, POST, PUT, DELETE)
- [ ] JSON request/response format
- [ ] API authentication (API keys, Bearer tokens)
- [ ] Status codes (200, 404, 500, etc.)

**Tools**:
- [ ] `requests` library in Python
- [ ] Postman or curl for testing
- [ ] FastAPI or Flask basics

**Self-Assessment**:
```python
import requests

# Can you write and understand API calls like this?
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello"}]
    }
)
data = response.json()
```

If yes → You're ready! If no → Study REST APIs and HTTP basics.

---

### ✅ Command Line / Terminal (Essential)

**Basic Commands**:
- [ ] `cd`, `ls/dir`, `mkdir`, `rm/del`
- [ ] `pip install`, `python script.py`
- [ ] Environment variables
- [ ] Virtual environments (`venv`, `conda`)

**Self-Assessment**:
```bash
# Can you run these commands?
cd my-project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If yes → You're ready! If no → Study command line basics.

---

### ⚡ Math & Statistics (Recommended)

**Linear Algebra** (Basic):
- [ ] Vectors and matrices
- [ ] Dot product and matrix multiplication
- [ ] Understand what embeddings are (vectors in high-dimensional space)

**Statistics** (Basic):
- [ ] Mean, median, standard deviation
- [ ] Probability basics
- [ ] Understand "similarity" and "distance" metrics

**Note**: Deep math NOT required for this course. You'll learn AI engineering (using models), not AI research (building models from scratch).

**Good to Know**:
- Cosine similarity: How similar are two vectors?
- Softmax: Converts scores to probabilities
- Embeddings: Text represented as 384D or 1536D vectors

**Resources**:
- [3Blue1Brown - Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab) (visual intuition)
- [Khan Academy - Statistics](https://www.khanacademy.org/math/statistics-probability)

---

## Tools & Environment

### ✅ Development Environment

**Text Editor / IDE** (Choose One):
- [ ] **VS Code** (recommended) - Free, great Python support
- [ ] **PyCharm** - Professional Python IDE
- [ ] **Jupyter** - Interactive notebooks

**Python Package Manager**:
- [ ] `pip` (comes with Python)
- [ ] Optional: `conda` for environment management

**Git** (Version Control):
- [ ] Install Git
- [ ] Basic commands: `clone`, `commit`, `push`, `pull`
- [ ] GitHub account for hosting projects

---

### ✅ Required Python Libraries

Install these before starting:

```bash
# Core AI/ML libraries
pip install openai anthropic google-generativeai

# Vector database and embeddings
pip install chromadb sentence-transformers

# Web frameworks
pip install fastapi uvicorn pydantic

# Data processing
pip install pandas numpy

# LangChain (for multi-agent systems)
pip install langchain langchain-openai langchain-anthropic langgraph

# Utilities
pip install python-dotenv requests httpx
```

**Verify Installation**:
```python
# Run this in Python to verify
import openai
import chromadb
import fastapi
import langchain
print("All packages installed successfully!")
```

---

### ✅ API Keys & Accounts

**Required for All Tracks**:
- [ ] **OpenAI API** - Sign up at [platform.openai.com](https://platform.openai.com)
  - Get API key (pay-as-you-go, ~$5-10 for this course)
- [ ] **Anthropic API** (Claude) - Sign up at [console.anthropic.com](https://console.anthropic.com)
  - Get API key (~$5-10 for this course)

**Optional but Recommended**:
- [ ] **Google AI Studio** (Gemini) - Free tier at [ai.google.dev](https://ai.google.dev)
- [ ] **Hugging Face** - Free account at [huggingface.co](https://huggingface.co)
- [ ] **Pinecone** - Free vector database at [pinecone.io](https://pinecone.io)

**Environment Setup**:
Create `.env` file:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AI...
```

---

## Time Commitment

### Beginner Track (6 weeks)
- **15 hours/week**
- **Best schedule**: 2 hours/day on weekdays, 2.5 hours on weekends
- **Minimum**: 10 hours/week (extend to 8 weeks)

### Standard Track (10 weeks)
- **15 hours/week**
- **Best schedule**: 2 hours/day on weekdays, 2.5 hours on weekends
- **Minimum**: 10 hours/week (extend to 15 weeks)

### Deep Mastery (16 weeks)
- **15 hours/week**
- **Best schedule**: 2 hours/day on weekdays, 2.5 hours on weekends
- **Minimum**: 10 hours/week (extend to 24 weeks)

---

## Self-Assessment Quiz

Answer these questions honestly:

### Python
1. Can you write a function that takes a list and returns unique items?
2. Can you read/write JSON files?
3. Can you make HTTP requests with the `requests` library?

### APIs
4. Do you know what a REST API is?
5. Can you explain what JSON is?
6. Have you used Postman or curl before?

### Command Line
7. Can you navigate directories in terminal?
8. Can you install Python packages with pip?
9. Can you create and activate virtual environments?

**Scoring**:
- **7-9 Yes**: You're ready to start immediately! 🎉
- **4-6 Yes**: Brush up on weak areas (1-2 weeks prep)
- **0-3 Yes**: Complete Python basics first (4-6 weeks prep)

---

## Recommended Prep Resources

### Python Basics (If Needed)
- **Course**: [Python for Everybody](https://www.py4e.com/) (Free, ~40 hours)
- **Book**: "Automate the Boring Stuff with Python" (Free online)
- **Practice**: [Exercism Python Track](https://exercism.org/tracks/python) (Free)

### API & Web Basics (If Needed)
- **Tutorial**: [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) (Official, ~4 hours)
- **Video**: [APIs for Beginners](https://www.youtube.com/watch?v=GZvSYJDk-us) (freeCodeCamp)
- **Practice**: Build a simple REST API with FastAPI

### Command Line (If Needed)
- **Tutorial**: [Command Line Crash Course](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) (MDN)
- **Practice**: Use terminal for 1 week instead of GUI

---

## Optional But Helpful

### Cloud Basics (For Deployment)
- [ ] AWS/GCP/Azure basics
- [ ] Docker basics (containerization)
- [ ] CI/CD concepts

### Databases (For Projects)
- [ ] SQL basics (PostgreSQL)
- [ ] NoSQL basics (MongoDB)
- [ ] Redis basics (caching)

---

## Ready to Start?

Once you've checked off most items above:

<div class="dashboard-actions">
    <a href="../tracks/overview.md" class="btn btn-primary">📚 Choose Your Track</a>
    <a href="../guide/quick-start.md" class="btn btn-secondary">🚀 Quick Start Guide</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 View Dashboard</a>
</div>

---

## Still Not Ready?

**No problem!** Here's a 4-week prep plan:

### Week 1-2: Python Basics
- Complete Python for Everybody (Chapters 1-7)
- Practice: 20 LeetCode Easy problems
- Build: Simple text processing script

### Week 3: APIs & Web
- Complete FastAPI tutorial
- Build: Simple REST API with 3 endpoints
- Practice: Call OpenAI API manually

### Week 4: Integration
- Set up development environment
- Install all required libraries
- Build: Simple chatbot using OpenAI API
- **Then start Week 1 of your chosen track!**
