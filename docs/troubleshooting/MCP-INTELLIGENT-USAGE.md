# MCP Servers: Intelligent Usage Guide

**Date**: 2025-10-02
**Purpose**: Smart guidelines for when and how to use each MCP server
**Applies to**: Claude Code and Claude Desktop

---

## Overview

You have 6 MCP servers configured:
1. **filesystem** - File operations
2. **memory-auto** - Persistent memory with auto-classification
3. **langchain** - Vector embeddings and semantic search
4. **ai-workflows** - Code generation with Ollama (local AI)
5. **code-indexing** - Semantic code search
6. **testing** - Intelligent test execution and analysis

---

## 1. Filesystem MCP

### What it does
Basic file operations: read, write, list, search files.

### ✅ Use when
- Reading/writing files in allowed directories
- Listing directory contents
- Basic file searches
- File metadata operations

### ❌ Don't use when
- You need semantic search (use code-indexing instead)
- You need to remember information (use memory-auto instead)

### Examples
```
✅ "List all TypeScript files in src/"
✅ "Read package.json"
✅ "Write this config to settings.json"
❌ "Find code that handles authentication" → use code-indexing
❌ "Remember my AWS account details" → use memory-auto
```

---

## 2. Memory-Auto MCP

### What it does
Persistent memory with automatic classification into global vs project-specific context.

### ✅ Use when
- User shares personal information (preferences, account IDs, API keys)
- Learning project-specific patterns or conventions
- Storing decisions for future reference
- Tracking project architecture or design choices

### ❌ Don't use when
- Information is already in files (read files instead)
- Temporary conversation context (just keep in chat)
- Searching code semantically (use code-indexing instead)

### Auto-Classification
The server automatically determines:
- **Global**: User preferences, AWS accounts, personal info
- **Project**: Architecture decisions, conventions, project-specific patterns

### Examples
```
✅ "Remember my AWS account is 123456789"
✅ "Store that we use kebab-case for file names in this project"
✅ "Save that our API uses JWT authentication"
❌ "What functions are in utils.ts?" → read the file
❌ "Find all database queries" → use code-indexing
```

---

## 3. LangChain MCP

### What it does
Vector embeddings and semantic storage for cross-project knowledge.

### ✅ Use when
- Storing knowledge that applies across multiple projects
- Semantic similarity search across stored knowledge
- Building a knowledge base of patterns/techniques
- Finding related concepts or solutions

### ❌ Don't use when
- Searching current project code (use code-indexing instead)
- Storing simple key-value data (use memory-auto instead)
- Need immediate real-time code search (code-indexing is faster)

### Examples
```
✅ "Store this authentication pattern for future projects"
✅ "Find similar solutions to error handling I've used before"
✅ "Search knowledge base for React optimization techniques"
❌ "Find where we handle login in this project" → use code-indexing
❌ "Remember my AWS account" → use memory-auto
```

---

## 4. AI-Workflows MCP (Ollama)

### What it does
Local AI code generation, testing, documentation using Ollama (Qwen 2.5 Coder 7B).

### ✅ Use when (based on agent-optimization-rules.md)
- **Code generation >20 lines** (95% time savings, 100% token savings)
- **Test generation** (always!)
- **Documentation generation** (always for >5 functions)
- **Code review >100 lines** (90% time savings)
- **Complete features** (code + tests + docs workflow)

### ❌ Don't use when
- **Code <20 lines** (overhead not worth it, just type it)
- **Simple questions** (you can answer faster)
- **Debugging** (trace manually, Ollama only for suggestions)
- **Security-critical code without review** (always review AI output)

### Workflows Available
1. **generate_code** - Single code generation with validation
2. **generate_tests** - Test suite generation
3. **generate_documentation** - Function/module documentation
4. **review_code** - Code quality review
5. **complete_feature** - Full workflow (code + tests + docs + review)

### Performance
- **Speed**: 18.8 seconds average (optimized with Flash Attention + KV Cache Q8)
- **Token savings**: 90% (10,000 → 1,000 tokens per feature)
- **Quality**: 85-95% pass rate with 3-tier validation

### Examples
```
✅ "Generate CRUD operations for User model with tests"
✅ "Create authentication middleware with validation"
✅ "Write unit tests for all functions in utils.py"
✅ "Document all API endpoints"
❌ "Generate a 5-line helper function" → just type it (30s vs 18s)
❌ "What does this function do?" → read and explain it yourself
❌ "Debug why tests are failing" → debug manually first
```

### Decision Matrix (from agent-optimization-rules.md)
| Lines of Code | Use Ollama? | Reason |
|---------------|-------------|--------|
| <20 lines | ❌ | Overhead not worth it |
| 20-100 lines | ✅ | Good time/token savings |
| 100+ lines | ✅ Always | Excellent savings |
| Tests | ✅ Always | Perfect use case |
| Docs >5 functions | ✅ Always | 92% time savings |

---

## 5. Code-Indexing MCP

### What it does
Semantic code search using LangChain embeddings (sentence-transformers/all-MiniLM-L6-v2) and ChromaDB.

### ✅ Use when
- **Finding code by meaning**, not just keywords
- **Searching across large codebase** (>100 files)
- **Locating features/patterns** when you don't know exact terms
- **Understanding what code exists** for a concept

### ❌ Don't use when
- **Single file lookup** (just read the file)
- **Exact keyword search** (use grep/filesystem search)
- **Haven't indexed yet** (run index_codebase first!)
- **Code changes frequently** (re-index after major changes)

### How it works
1. **Indexing**: Splits code into chunks, creates embeddings, stores in ChromaDB
2. **Search**: Converts query to embedding, finds similar chunks via cosine similarity
3. **Results**: Returns relevant code chunks with file paths and context

### Tools
1. **index_codebase** - Index project files (run first or after code changes)
2. **search_code** - Semantic search by meaning

### Performance
- **Indexing**: ~2-5 seconds per 100 files
- **Search**: <1 second for most queries
- **Storage**: .code-index directory (persist between sessions)

### Examples
```
✅ "Find authentication logic" (semantic: finds auth, login, security, JWT, etc.)
✅ "Where do we handle database connections?"
✅ "Show me error handling patterns"
✅ "Find all API endpoints"
❌ "Read utils.ts" → just read the file directly
❌ "Search for exact string 'getUserById'" → use grep
❌ [Before indexing] "Find auth code" → run index_codebase first!
```

### Workflow
```bash
# First time or after major changes:
1. Run: index_codebase
   → Indexes all code files
   → Creates .code-index directory
   → Takes 2-5 seconds per 100 files

# Then search:
2. Run: search_code query="authentication logic" limit=5
   → Returns top 5 relevant code chunks
   → Shows file paths and line numbers
   → Includes surrounding context
```

---

## 6. Testing MCP

### What it does
Intelligent test execution with AI-powered failure analysis using Ollama.

### ✅ Use when
- **Running tests** (auto-detects pytest/jest/vitest)
- **Test failures need diagnosis** (AI root cause analysis)
- **Need test suggestions** for existing code
- **Want coverage reports**

### ❌ Don't use when
- **Simple test run** (just run pytest/jest directly if no analysis needed)
- **Debugging** (debug manually first, use AI for suggestions only)
- **Tests don't exist yet** (generate with ai-workflows first)

### Tools
1. **run_tests** - Execute tests with framework auto-detection
2. **analyze_failures** - AI analysis of test failures (root cause + fixes)
3. **suggest_tests** - AI suggestions for test cases (edge cases, boundaries)
4. **get_coverage** - Test coverage report

### Framework Support
- **Python**: pytest (auto-detected from pytest.ini, setup.py)
- **JavaScript/TypeScript**: jest, vitest (auto-detected from package.json)

### AI Analysis Features
- Root cause identification
- Suggested fixes with code examples
- Priority classification (critical, high, medium, low)
- Edge case detection
- Boundary condition testing

### Examples
```
✅ "Run all tests in test_auth.py"
✅ "Run tests and analyze any failures"
✅ "Suggest test cases for the UserService class"
✅ "Get test coverage report"
❌ "Run quick test" → just run pytest directly
❌ "Debug failing test" → debug manually, then use analyze_failures
```

### Workflow
```bash
# Scenario 1: Quick test run
run_tests test_path="tests/test_auth.py"
→ If passes: ✅ Done
→ If fails: Use analyze_failures

# Scenario 2: Test with AI analysis
1. run_tests
2. If failures → analyze_failures test_output="<output>"
   → Get root cause
   → Get suggested fixes
   → Get priority

# Scenario 3: Generate tests for new code
1. Write code in code_editor
2. suggest_tests code="<your_code>" language="python"
   → Get test case suggestions
   → Use ai-workflows to generate actual tests
```

---

## Decision Flowchart

```
Need to work with code?
  ↓
├─ Generate new code?
│  ├─ >20 lines? → ✅ ai-workflows
│  └─ <20 lines? → ❌ Type manually
│
├─ Find existing code?
│  ├─ Know file name? → ✅ filesystem (read file)
│  ├─ Know keyword? → ✅ filesystem (grep)
│  └─ Know concept only? → ✅ code-indexing (semantic search)
│
├─ Run tests?
│  ├─ Need failure analysis? → ✅ testing (run_tests + analyze_failures)
│  └─ Quick check? → ❌ pytest/jest directly
│
├─ Generate tests?
│  └─ Always → ✅ ai-workflows
│
├─ Remember something?
│  ├─ Personal/global? → ✅ memory-auto (auto-classifies)
│  ├─ Cross-project knowledge? → ✅ langchain
│  └─ Project-specific? → ✅ memory-auto (auto-classifies)
│
└─ Document code?
   ├─ >5 functions? → ✅ ai-workflows
   └─ <5 functions? → ❌ Write manually
```

---

## Common Workflows

### Workflow 1: Implement New Feature
```
1. User: "Add JWT authentication"

2. Me: Check if similar code exists
   → code-indexing: search_code query="authentication patterns"
   → Review existing patterns

3. Me: Generate implementation
   → ai-workflows: complete_feature
     description="JWT authentication middleware"
     language="typescript"
   → Gets: code + tests + docs + review (60 seconds, 0 tokens)

4. Me: Run tests
   → testing: run_tests test_path="tests/auth"
   → If failures: analyze_failures

5. Me: Store decision
   → memory-auto: "We use JWT with RS256 for this project"
```

**Time**: ~3 minutes (vs 30 minutes manual)
**Token savings**: 90% (15,000 → 1,500 tokens)

### Workflow 2: Fix Bug
```
1. User: "Fix login failing for OAuth users"

2. Me: Find related code
   → code-indexing: search_code query="OAuth login authentication"
   → Get relevant files

3. Me: Read and debug manually
   → Read files directly
   → Trace execution
   → Identify root cause

4. Me: Fix code
   → Edit files directly (AI not needed for debugging!)

5. Me: Generate regression test
   → ai-workflows: generate_tests
     code="<fixed_code>"
     language="python"

6. Me: Run tests
   → testing: run_tests test_path="tests/test_oauth.py"
```

**Key**: Debug manually, use AI only for test generation

### Workflow 3: Code Review
```
1. User: "Review the authentication module"

2. Me: Get code
   → filesystem: read src/auth/*.ts

3. If >100 lines:
   → ai-workflows: review_code (1 min, 0 tokens)
   → Get automated review

4. If <100 lines:
   → Review manually (faster)

5. Run tests to verify
   → testing: run_tests test_path="tests/auth"
   → testing: get_coverage
```

### Workflow 4: Understand Unfamiliar Codebase
```
1. User: "How does the payment system work?"

2. Me: Semantic search
   → code-indexing: search_code query="payment processing flow"
   → Get relevant code chunks

3. Me: Read key files
   → filesystem: read <identified_files>

4. Me: Explain architecture
   → Use what I found

5. Me: Store knowledge
   → memory-auto: "Payment uses Stripe with webhook verification"
```

---

## Performance Optimization Tips

### Tip 1: Batch Operations (from agent-optimization-rules.md)
```
❌ Bad: Sequential
search_code "auth"
wait...
search_code "database"
wait...
search_code "api"

✅ Good: Parallel (when using agents)
Launch 3 agents to search in parallel
Total time: 30s (vs 90s)
```

### Tip 2: Use Right Tool for Job
```
❌ Wrong tool: Use ai-workflows for 5-line function (18s + overhead)
✅ Right tool: Type 5 lines manually (30s, but simpler)

❌ Wrong tool: Use code-indexing before indexing (fails)
✅ Right tool: Run index_codebase first, then search

❌ Wrong tool: Use langchain for current project search
✅ Right tool: Use code-indexing (faster, more accurate)
```

### Tip 3: Workflow Chaining
```
❌ Bad: Step by step with waits
ai-workflows: generate_code → wait → review?
ai-workflows: generate_tests → wait → review?
ai-workflows: generate_docs → wait → review?

✅ Good: Complete workflow
ai-workflows: complete_feature
→ Does everything in one go (60s total)
```

### Tip 4: Cache and Reuse
```
✅ Index code once, search many times
code-indexing: index_codebase (one time, 2-5 min)
code-indexing: search_code (multiple times, <1s each)

✅ Store decisions in memory
memory-auto: save once, recall anytime (no re-reading files)
```

---

## Token Savings Summary

| Task | Manual Tokens | With MCP | Savings |
|------|---------------|----------|---------|
| Generate feature (100 lines) | 15,000 | 1,500 | 90% |
| Generate tests (50 tests) | 25,000 | 2,000 | 92% |
| Write docs (20 functions) | 8,000 | 800 | 90% |
| Code review (500 lines) | 10,000 | 1,000 | 90% |
| Search codebase | 5,000 | 500 | 90% |
| **Total per feature** | **63,000** | **5,800** | **91%** |

**Monthly savings** (assuming 20 features): 1,144,000 tokens saved

---

## Installation Checklist

### Prerequisites
- [x] Ollama installed (version 0.12.3)
- [x] Qwen 2.5 Coder 7B model pulled
- [x] Python 3.11+ with pip
- [x] Node.js (for JS/TS projects)

### Install Dependencies

#### For ai-workflows:
```bash
pip install requests pylint
```

#### For code-indexing:
```bash
pip install langchain langchain-community chromadb sentence-transformers
```

#### For testing:
```bash
# Python testing:
pip install pytest pytest-cov

# JavaScript testing (in your project):
npm install --save-dev jest  # or vitest
```

### Configuration Files

#### Claude Desktop: `claude_desktop_config.json`
Located at: `C:\Users\SainathreddyDadiredd\AppData\Roaming\Claude\claude_desktop_config.json`

#### Claude Code: Auto-configured (no action needed)

---

## Troubleshooting

### Issue: "code-indexing failed"
**Cause**: Server not installed or dependencies missing
**Fix**:
```bash
cd C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/code-indexing
pip install langchain langchain-community chromadb sentence-transformers
```

### Issue: "No results found" from code-indexing
**Cause**: Codebase not indexed yet
**Fix**:
```
1. Run: index_codebase
2. Wait for indexing to complete
3. Then: search_code query="your search"
```

### Issue: "Ollama not found" from ai-workflows
**Cause**: Ollama not running or not in PATH
**Fix**:
```bash
# Check if running:
ollama list

# If not running, start it:
ollama serve

# Verify model:
ollama list | grep qwen2.5-coder
```

### Issue: "Testing framework not detected"
**Cause**: No test framework installed
**Fix**:
```bash
# For Python:
pip install pytest

# For JavaScript:
npm install --save-dev jest  # or vitest
```

### Issue: AI analysis gives wrong suggestions
**Cause**: AI hallucination or insufficient context
**Fix**:
- Always review AI suggestions manually
- Provide more context in prompts
- Use AI for suggestions only, not final answers

---

## Best Practices

### 1. Always Index Before Searching
```
First time in project:
→ code-indexing: index_codebase
Then:
→ code-indexing: search_code
```

### 2. Use Complete Workflows
```
❌ Don't: Generate code separately, then tests, then docs
✅ Do: ai-workflows: complete_feature (does everything)
```

### 3. Review AI Output
```
✅ Always review:
- Security-critical code
- Complex algorithms
- Test logic
- Production deployments
```

### 4. Store Decisions
```
After making architectural decisions:
→ memory-auto: "Store this decision..."
Next time:
→ Recall automatically (no re-reading files)
```

### 5. Optimize Tool Usage
```
Follow agent-optimization-rules.md:
- Agents: 3+ parallel tasks only
- Ollama: Code >20 lines only
- Direct: Simple tasks <10 seconds
```

---

## Version History

**v1.0** (2025-10-02):
- Initial guide for all 6 MCP servers
- Usage guidelines based on agent-optimization-rules.md
- Token savings calculations
- Common workflows
- Troubleshooting section

**Review Schedule**: Monthly
**Next Review**: 2025-11-02

---

**Created**: 2025-10-02
**Applies to**: Claude Code and Claude Desktop
**Status**: Active guide - follow these for optimal performance
