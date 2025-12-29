# Claude Code Power User Guide
**The Ultimate Reference for Maximum AI Productivity**

**Date**: 2025-10-10
**Status**: ✅ Complete Arsenal

---

## Table of Contents
1. [MCP Servers](#mcp-servers) (10 configured)
2. [AI Agents](#ai-agents) (60+ available)
3. [Local AI](#local-ai) (Llama integration)
4. [Parallel Agent Strategies](#parallel-agents)
5. [Thinking & Transparency](#thinking-mode)
6. [Auto-Approval Settings](#auto-approval)
7. [Best Practices](#best-practices)

---

## MCP Servers

### 1. **memory-auto** 🧠
**What**: Automatic memory classification and storage
**Location**: Custom Python MCP
**Tools**:
- `auto_store_memory` - Auto-classify and store
- `store_global_memory` - Manual global storage
- `search_global_memory` - Search all projects
- `store_project_memory` - Project-specific storage
- `search_project_memory` - Within project only

**Databases**:
- `global.db` - Cross-project memory
- `projects-index.db` - Project-specific memory

**When to Use**:
- ✅ Storing user preferences
- ✅ Remembering past decisions
- ✅ Cross-session context
- ✅ Important findings

**Auto-Trigger**: User shares important info, mentions past work

---

### 2. **langchain** 🔍
**What**: Vector search with semantic embeddings
**Location**: Custom Python MCP
**Tools**:
- `semantic_search` - Find semantically similar content
- `add_to_vector_store` - Index new documents/code
- `query_vector_store` - Retrieve context

**Technology**:
- Embeddings: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- Vector Store: Chroma
- Location: `unified-memory/vector-store/`

**When to Use**:
- ✅ Finding code patterns
- ✅ Similar document search
- ✅ Semantic code discovery
- ✅ Large codebase navigation

**Performance**: 90% faster than reading all files

---

### 3. **ai-workflows** (Llama) 🦙
**What**: Local AI delegation (qwen2.5-coder:7b)
**Location**: Custom Python MCP
**Tools**:
- `delegate_to_llama` - Send task to local Llama
- `analyze_code_with_llama` - Code analysis
- `generate_with_llama` - Text/code generation

**When to Use**:
- ✅ Simple code generation
- ✅ Test case creation
- ✅ Boilerplate code
- ✅ Repetitive tasks

**Benefits**:
- FREE (no API costs)
- FAST (local model)
- Good for simple tasks
- Saves Claude credits

**When NOT to Use**:
- ❌ Complex architecture
- ❌ Security analysis
- ❌ Critical business logic

---

### 4. **code-indexing** 📇
**What**: Custom code indexing for your projects
**Location**: Custom Python MCP
**Project**: `C:/Users/.../Claude`

**When to Use**:
- ✅ Project-specific code search
- ✅ Custom indexing patterns
- ✅ Repository analysis

---

### 5. **testing** 🧪
**What**: Test automation and generation
**Location**: Custom Python MCP
**Project**: `C:/Users/.../Claude`

**When to Use**:
- ✅ Test generation
- ✅ Test automation
- ✅ Coverage analysis

---

### 6. **code-index-mcp** 🗂️
**What**: Industry-standard semantic code search (50+ languages)
**Location**: NPM package via uvx
**Performance**: Sub-100ms queries

**When to Use**:
- ✅ >5 files to analyze
- ✅ >1000 lines of code
- ✅ Multi-language codebases
- ✅ Fast file discovery

**Auto-Trigger**: Large file operations detected

---

### 7. **sequential-thinking** 🤔
**What**: Extended reasoning for complex problems
**Location**: Official Anthropic MCP

**When to Use**:
- ✅ Complex debugging
- ✅ Architecture decisions
- ✅ Multi-step problem solving
- ✅ Security analysis

**Performance**: +54% on complex tasks

**Auto-Trigger**: Complex problem detected

---

### 8. **github** 🐙
**What**: GitHub API integration
**Location**: Official MCP
**Config**: Needs GITHUB_PERSONAL_ACCESS_TOKEN

**When to Use**:
- ✅ PR/issue operations
- ✅ Repository analysis
- ✅ GitHub automation

**Note**: Token not configured yet (line 64 of config)

---

### 9. **aws** ☁️
**What**: AWS operations and management
**Location**: Custom Python MCP
**Profile**: agdemo
**Region**: us-east-2

**When to Use**:
- ✅ AWS resource management
- ✅ Infrastructure operations
- ✅ Cloud deployments

---

### 10. **playwright** 🎭
**What**: Web browser automation
**Location**: NPM package
**Package**: `@executeautomation/playwright-mcp-server`

**Tools**:
- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Get page content
- `browser_click` - Click elements
- `browser_type` - Type into inputs
- `browser_take_screenshot` - Capture screenshots

**When to Use**:
- ✅ ANY web URL user shares
- ✅ Web scraping
- ✅ UI testing
- ✅ Interactive web tasks

**Auto-Trigger**: User shares URL

---

## AI Agents

Claude Code has **60+ specialized agents**. Here are the key ones:

### Development Agents

#### **python-pro** 🐍
**Expertise**: Python 3.12+, async, decorators, type hints
**Use For**:
- Python refactoring
- Performance optimization
- Complex Python features
- Best practices

#### **javascript-pro** / **typescript-pro** 📜
**Expertise**: ES6+, async patterns, Node.js, strict TypeScript
**Use For**:
- JavaScript optimization
- TypeScript architecture
- Async debugging
- Type inference

#### **react-pro** / **nextjs-pro** ⚛️
**Expertise**: React 18+, Next.js 14+, hooks, SSR/SSG
**Use For**:
- Component development
- Performance optimization
- SEO-friendly apps
- Modern React patterns

#### **golang-pro** 🔵
**Expertise**: Go 1.21+, concurrency, channels, goroutines
**Use For**:
- Go architecture
- Concurrency challenges
- Performance tuning
- Idiomatic Go code

#### **rust-pro** 🦀
**Expertise**: Rust 1.75+, ownership, async, systems programming
**Use For**:
- Rust development
- Memory safety
- Systems programming
- Performance-critical code

### Architecture & Design

#### **backend-architect** 🏗️
**Expertise**: Scalable systems, microservices, databases
**Use For**:
- System design
- Architecture decisions
- Scalability planning
- Technology selection

#### **cloud-architect** ☁️
**Expertise**: AWS/Azure/GCP, IaC, FinOps, multi-cloud
**Use For**:
- Cloud architecture
- Cost optimization
- Migration planning
- Multi-cloud strategies

#### **kubernetes-architect** ⎈
**Expertise**: K8s, GitOps, service mesh, platform engineering
**Use For**:
- K8s architecture
- GitOps implementation
- Cloud-native design
- Container orchestration

### Security & DevOps

#### **security-auditor** 🔒
**Expertise**: DevSecOps, OWASP, compliance, vulnerability assessment
**Use For**:
- Security audits
- Vulnerability scanning
- Compliance (GDPR/HIPAA)
- Threat modeling

#### **devops-troubleshooter** 🚨
**Expertise**: Incident response, debugging, observability
**Use For**:
- Production issues
- System debugging
- Root cause analysis
- Performance problems

#### **deployment-engineer** 🚀
**Expertise**: CI/CD, GitOps, progressive delivery
**Use For**:
- Pipeline design
- Deployment automation
- Zero-downtime deploys
- Release strategies

### Data & AI

#### **data-scientist** 📊
**Expertise**: ML, analytics, statistical modeling
**Use For**:
- Data analysis
- ML modeling
- Statistical analysis
- Predictive models

#### **ai-engineer** 🤖
**Expertise**: LLMs, RAG, vector search, prompt engineering
**Use For**:
- LLM applications
- RAG systems
- AI features
- Prompt optimization

#### **ml-engineer** 🧠
**Expertise**: ML pipelines, model deployment, MLOps
**Use For**:
- ML deployment
- Model monitoring
- Pipeline automation
- Production ML

### Testing & Quality

#### **test-automator** 🧪
**Expertise**: Modern testing frameworks, AI-assisted testing
**Use For**:
- Test automation
- Quality assurance
- CI/CD integration
- Test strategies

#### **qa-expert** ✅
**Expertise**: QA processes, test planning, quality engineering
**Use For**:
- Testing strategies
- Test plans
- Quality assurance
- QA workflows

#### **debugger** 🐛
**Expertise**: Error analysis, test failures, debugging
**Use For**:
- Bug fixing
- Test failures
- Error investigation
- Systematic debugging

### Code Review & Optimization

#### **code-reviewer-pro** 👀
**Expertise**: Code quality, security, best practices
**Use For**:
- Code reviews
- Security analysis
- Best practice checks
- Quality assurance

#### **performance-engineer** ⚡
**Expertise**: Observability, optimization, scalability
**Use For**:
- Performance optimization
- Observability setup
- Scalability challenges
- Load testing

### Specialized

#### **database-optimizer** / **database-architect** 🗄️
**Expertise**: Query optimization, schema design, indexing
**Use For**:
- Database optimization
- Schema design
- Query tuning
- Database selection

#### **prompt-engineer** 💭
**Expertise**: Advanced prompting, LLM optimization
**Use For**:
- Prompt design
- LLM workflows
- Agentic systems
- Prompt optimization

#### **graphql-architect** 🕸️
**Expertise**: GraphQL schema, resolvers, federation
**Use For**:
- GraphQL APIs
- Schema design
- Performance optimization
- Federated services

---

## Local AI (Llama Integration)

### **qwen2.5-coder:7b** via ai-workflows MCP

**Capabilities**:
- Code generation
- Simple analysis
- Boilerplate creation
- Test generation

**Performance**:
- Speed: FAST (local)
- Cost: FREE
- Quality: Good for simple tasks

**Decision Tree**:
```
Is task complex? (architecture, security, optimization)
├─ YES → Claude handles it
└─ NO → Is it repetitive/boilerplate?
    ├─ YES → Delegate to Llama
    └─ NO → Evaluate cost vs speed
        ├─ Speed critical → Llama
        └─ Quality critical → Claude
```

**Usage via MCP**:
```
ai-workflows MCP → delegate_to_llama(task)
```

---

## Parallel Agent Strategies

### When to Use Parallel Agents

**Rule**: Use parallel agents when tasks are **independent** (no dependencies between them).

### Examples

#### ✅ **GOOD - Parallel**
```
Task: "Analyze 3 microservices for security issues"

Agent 1: security-auditor → Service A
Agent 2: security-auditor → Service B
Agent 3: security-auditor → Service C

All run in parallel (independent)
```

#### ✅ **GOOD - Parallel**
```
Task: "Research auth options AND optimize database AND review API"

Agent 1: general-purpose → Research auth
Agent 2: database-optimizer → Optimize DB
Agent 3: code-reviewer-pro → Review API

All run in parallel (different domains)
```

#### ❌ **BAD - Sequential needed**
```
Task: "Find all API endpoints, then generate tests for them"

Agent 1: general-purpose → Find endpoints (must finish first)
↓ (wait for results)
Agent 2: test-automator → Generate tests (needs endpoint list)

MUST run sequentially (dependency)
```

### How to Trigger Parallel Agents

**In Claude Code**, send a SINGLE message with multiple Task tool calls:

```
<thinking>
I need to analyze auth, optimize DB, and review API.
These are independent - I'll launch 3 agents in parallel.
</thinking>

[Uses Task tool 3 times in one message]
```

### Maximum Parallelization

**Recommended**: 2-4 agents in parallel
**Maximum**: No hard limit, but diminishing returns after 4

**Why limit**:
- Token usage increases
- Harder to track progress
- Results harder to synthesize

---

## Thinking & Transparency

### Current Thinking Mode
**Mode**: `interleaved`

**What this means**:
- Thinking blocks appear BETWEEN tool calls
- You see Claude's reasoning process
- More transparent decision-making

### Thinking Modes Available

1. **enabled** - Always show thinking
2. **interleaved** - Show thinking between tools (CURRENT)
3. **disabled** - No thinking blocks
4. **auto** - Claude decides when to show

### See Agent Activity

**Currently**: When agents are used, you see:
- "Using code-reviewer agent to..."
- Tool results from agents
- Agent summaries

**Want MORE transparency?** I can add:
- Agent selection reasoning
- Parallel agent coordination
- Why specific agent was chosen

---

## Auto-Approval

### Currently Auto-Approved

These operations **never ask for permission**:

```
- Bash(git commit:*)
- Bash(pip install:*)
- Bash(pip show:*)
- Bash(pip search:*)
- WebFetch(domain:claude.ai)
- Bash(playwright install:*)
- WebFetch(domain:www.builder.io)
- Bash(mcp list-tools:*)
- Bash(mcp list:*)
- Bash(cd:*)
- Bash(echo:*)
- Bash(ls:*)
- Read(C:/Users/.../AppData/Roaming/Claude/**)
- Bash(node:*)
- Bash(npx --version)
- WebSearch (always approved)
- Bash(git log:*)
- Bash(claude mcp:*)
```

### Want to Add More?

**Common additions**:
- All git operations
- All npm/node operations
- All file operations in project
- All MCP operations
- All agent delegations

**To add**: I can update your settings to auto-approve more operations.

---

## Best Practices

### MCP Usage

1. **Memory First**: Check memory-auto before re-explaining
2. **Vector Search**: Use langchain for >5 files
3. **Llama for Simple**: Delegate boilerplate to ai-workflows
4. **Sequential Thinking**: Use for complex problems
5. **Playwright for URLs**: Always use for web browsing

### Agent Usage

1. **Right Agent, Right Job**: Match agent expertise to task
2. **Parallel When Possible**: Independent tasks → parallel agents
3. **Sequential When Needed**: Dependencies → sequential execution
4. **Batch Similar Tasks**: Multiple similar analyses → parallel agents

### Performance Optimization

1. **Prompt Optimization**: Use `/improve-prompt` for complex prompts
2. **Parallel Tools**: Independent reads → parallel Read calls
3. **MCP Over Manual**: Semantic search > reading all files
4. **Cache Results**: AI news cached 24h, memory persists

### Workflow Examples

#### Example 1: Full-Stack Feature
```
1. backend-architect → Design API (sequential)
2. [Parallel]:
   - python-pro → Implement backend
   - react-pro → Build frontend
   - test-automator → Generate tests
3. code-reviewer-pro → Review all (sequential, after parallel completes)
```

#### Example 2: Security Audit
```
[Parallel]:
- security-auditor → Backend security
- frontend-security-coder → Frontend security
- database-optimizer → DB security
- devops-troubleshooter → Infrastructure security

Then synthesize results
```

#### Example 3: Research → Implement
```
1. general-purpose → Research best practices (sequential)
2. Based on research → [Parallel]:
   - Implement in Service A
   - Implement in Service B
   - Update documentation
```

---

## Quick Reference Card

| Task Type | Primary Tool | Agent | Parallel? |
|-----------|-------------|-------|-----------|
| **Code Search** | langchain MCP | general-purpose | Yes (multiple dirs) |
| **Security Review** | N/A | security-auditor | Yes (multiple files) |
| **API Design** | N/A | backend-architect | No (design first) |
| **Test Generation** | ai-workflows (Llama) | test-automator | Yes (per file) |
| **Bug Fixing** | N/A | debugger | No (systematic) |
| **Performance** | sequential-thinking | performance-engineer | Depends |
| **Web Browsing** | playwright MCP | general-purpose | Yes (multiple URLs) |
| **Memory Storage** | memory-auto MCP | N/A | Always |
| **Complex Problem** | sequential-thinking | Relevant expert | No |
| **Simple Code** | ai-workflows (Llama) | N/A | Yes |

---

**Created**: 2025-10-10
**Last Updated**: 2025-10-10
**Status**: ✅ Complete
**Power Level**: OVER 9000! 🔥
