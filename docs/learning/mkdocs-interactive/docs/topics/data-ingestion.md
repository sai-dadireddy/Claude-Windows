# Data Ingestion Pipeline

<div class="topic-checkbox-container" data-topic-id="part2-data-ingestion">
    <label>
        <input type="checkbox" class="topic-checkbox" data-topic-id="part2-data-ingestion">
        <span class="topic-checkbox-label">Mark as complete</span>
    </label>
</div>

## Overview

<div class="study-mode-tag study-mode-practice">Practice</div>
<div class="provider-icon provider-gpt">Code: GPT</div>

**Estimated Time**: 5-7 hours | **Prerequisites**: Python, APIs | **Part**: Data Engineering for AI

## What, Why, When

**Data Ingestion** = Collecting and loading data from various sources into your AI system.

**Sources**: PDFs, websites, APIs, databases, cloud storage
**Goal**: Clean, structured data ready for chunking and embedding

## Key Techniques

### 1. Document Loaders
- **PDFs**: PyPDF2, pdfplumber, Unstructured
- **Web**: BeautifulSoup, Scrapy, Playwright
- **Databases**: SQLAlchemy, psycopg2
- **APIs**: requests, httpx

### 2. Data Cleaning
- Remove HTML tags, special characters
- Normalize whitespace
- Handle encodings (UTF-8)
- Extract text from tables/images (OCR)

### 3. Metadata Extraction
- Document title, author, date
- Source URL, file path
- Content type, language
- Custom fields (category, tags)

## Hands-On Exercise

```python
from langchain.document_loaders import PyPDFLoader, WebBaseLoader, DirectoryLoader
import os

# Load PDFs
pdf_loader = DirectoryLoader("./docs", glob="**/*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()

# Load websites
urls = ["https://example.com/doc1", "https://example.com/doc2"]
web_loader = WebBaseLoader(urls)
web_docs = web_loader.load()

# Combine and add metadata
all_docs = pdf_docs + web_docs
for doc in all_docs:
    doc.metadata["ingestion_date"] = "2024-01-15"
    doc.metadata["pipeline_version"] = "v1.0"

print(f"Loaded {len(all_docs)} documents")
```

## Provider Comparison

| Task | Best Provider | Why |
|------|---------------|-----|
| Design pipeline | Claude | Architecture decisions |
| Implement loaders | GPT-4 | Code quality |
| Handle edge cases | GPT-4 | Debugging |

## Personal Notes

<div class="topic-notes-container">
    <h4>📝 Your Notes</h4>
    <textarea class="topic-notes-textarea" data-notes-for="part2-data-ingestion"></textarea>
    <div class="notes-auto-save">💾 Auto-saves</div>
</div>

<div class="dashboard-actions">
    <a href="chunking-strategies.md" class="btn btn-primary">Next: Chunking →</a>
    <a href="../dashboard.md" class="btn btn-secondary">📊 Dashboard</a>
</div>

</div>
