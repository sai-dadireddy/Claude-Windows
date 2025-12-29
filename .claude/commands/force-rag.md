---
description: FORCE RAG MODE - Use semantic search instead of reading docs
---

# FORCE RAG MODE - Never Read Raw Documentation

**CRITICAL**: Reading raw docs wastes 10-30K tokens per lookup. Use RAG instead!

## BANNED ACTIONS (Token Wasters)

❌ **NEVER** read documentation files directly:
```bash
# DON'T DO THIS (wastes 10-30K tokens):
Read(file_path="docs/nextjs/server-components.md")
Read(file_path="docs/aws/cognito-authentication.md")
Read(file_path="node_modules/react/README.md")
```

✅ **ALWAYS** use RAG semantic search:
```bash
# DO THIS INSTEAD (costs <1K tokens):
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "Server Components"
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "Cognito auth" --tech aws-cognito
```

## RAG Collections Available (15,828 chunks!)

### Frontend (7,403 chunks)
```bash
# Next.js 15 (1,187 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "App Router routing" --tech nextjs

# TanStack Query (785 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "mutations and invalidation" --tech tanstack-query

# Shadcn UI (753 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "Button component props" --tech shadcn

# Tailwind (142 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "responsive utilities" --tech tailwind

# Zustand (336 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "store actions" --tech zustand

# Forms + Validation (9,220 chunks!)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "form validation schema" --tech forms-validation
```

### Backend & AWS (2,033 chunks)
```bash
# AWS Cognito (461 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "user pool authentication" --tech aws-cognito

# AWS API Gateway (409 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "REST API integration" --tech aws-api-gateway

# AWS ECS Fargate (763 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "task definition" --tech aws-ecs-fargate

# Backend APIs (352 chunks)
python projects/erpa/AGUPGRADE/tools/query-rag.py "REST API endpoints"
```

### Testing & Performance (863 chunks)
```bash
# Playwright (613 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "page object model" --tech playwright

# Web Performance (250 chunks)
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "Core Web Vitals" --tech web-performance
```

## Auto-Detection Rules (ENFORCE THESE!)

**When user asks about:**
- "How to use X in Next.js" → Query `nextjs` RAG
- "Data fetching with caching" → Query `nextjs` + `tanstack-query` RAGs
- "Form validation" → Query `forms-validation` RAG
- "AWS authentication" → Query `aws-cognito` RAG
- "Deployment" → Query `aws-ecs-fargate` RAG
- "Testing" → Query `playwright` RAG
- "UI components" → Query `shadcn` RAG

**Cross-technology queries:**
```bash
# Authenticated data fetching
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "authenticated API calls" --tech tanstack-query,aws-cognito

# Form with UI components
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "form with button" --tech shadcn,forms-validation
```

## Token Comparison

### ❌ Reading Raw Docs (OLD WAY)
```bash
# User asks: "How do I use Server Components in Next.js?"

Step 1: Search for docs
Glob(pattern="**/nextjs/**/server-components*.md")  # 2K tokens

Step 2: Read multiple files
Read(file_path="docs/nextjs/app-router.md")  # 8K tokens
Read(file_path="docs/nextjs/server-components.md")  # 12K tokens
Read(file_path="docs/nextjs/data-fetching.md")  # 10K tokens

Total: 32K tokens
Result: May or may not find the right answer
```

### ✅ Using RAG (NEW WAY)
```bash
# User asks: "How do I use Server Components in Next.js?"

Step 1: Query RAG directly
python projects/erpa/AGUPGRADE/tools/query-docs-rag.py "Server Components" --tech nextjs --show-code

Total: <1K tokens (just running the script)
Result: Precise answer with code examples
```

**Savings: 31K tokens** (97% reduction!)

## Enforcement Protocol

**Before ANY documentation lookup:**

1. ❓ Can this be answered by RAG?
   - If YES → Use RAG (cost: <1K tokens)
   - If NO → Explain why RAG can't help

2. ❓ Which RAG collection(s) to query?
   - Frontend question → Use frontend RAGs
   - AWS question → Use AWS RAGs
   - Testing question → Use testing RAGs

3. ✅ Query RAG with specific search term
4. ✅ Use --show-code flag for implementation examples
5. ✅ Use --tech flag to target specific collection

## Example Workflow

**Bad (Token Waste):**
```
User: "How do I implement authentication with Cognito?"
Claude: Let me read the Cognito documentation...
[Reads 5 files, uses 25K tokens]
Claude: Here's what I found... [may be incomplete]
```

**Good (Token Efficient):**
```
User: "How do I implement authentication with Cognito?"
Claude: Let me query the AWS Cognito RAG...
[Runs query-docs-rag.py, uses <1K tokens]
Claude: Here's the exact pattern with code examples [precise answer]
```

## Success Metrics

**Track these:**
- ✅ RAG queries per session: Should be HIGH
- ❌ Raw doc reads per session: Should be ZERO
- ✅ Token usage per documentation lookup: Should be <1K
- ❌ Token usage per task: Should decrease 30-50%

---

**REMEMBER: 15,828 chunks of knowledge are indexed and ready!**
**USE THEM instead of reading raw files!**
