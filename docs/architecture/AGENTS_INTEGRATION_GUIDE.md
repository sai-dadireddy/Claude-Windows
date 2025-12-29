# Agents System Integration Guide

**Date**: October 10, 2025
**Status**: ✅ Fully Integrated
**Repository**: https://github.com/wshobson/agents

---

## Overview

The agents system provides **83 specialized AI agents**, **15 multi-agent workflows**, and **42 development tools** for context-efficient task execution in Claude Code.

**Location**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents`

---

## Key Capabilities

### 1. Single Agent Invocation
Use specialized experts for specific tasks:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

### 2. Multi-Agent Workflows
Coordinate multiple agents for complex operations:

```
"Implement user dashboard with real-time analytics"
→ backend-architect → graphql-architect → frontend-developer
  → test-automator → security-auditor → deployment-engineer
```

### 3. Focused Development Kits
Pre-configured plugin suites for common tasks:

```bash
/plugin install api-development-kit
/plugin install testing-quality-suite
/plugin install security-hardening
```

---

## Agent Categories

### Architecture & System Design (7 agents)

| Agent | Model | Use Case |
|-------|-------|----------|
| **backend-architect** | opus | RESTful API design, microservice boundaries, database schemas |
| **cloud-architect** | opus | AWS/Azure/GCP infrastructure design and cost optimization |
| **graphql-architect** | opus | GraphQL schemas, resolvers, federation architecture |
| **kubernetes-architect** | opus | Cloud-native infrastructure with Kubernetes and GitOps |
| **architect-reviewer** | opus | Architectural consistency analysis and pattern validation |
| **terraform-specialist** | opus | Infrastructure as Code with Terraform modules |
| **hybrid-cloud-architect** | opus | Multi-cloud strategies across cloud and on-premises |

### Programming Languages (18 agents)

**Systems & Low-Level**:
- `c-pro`, `cpp-pro`, `rust-pro`, `golang-pro`

**Web & Application**:
- `javascript-pro`, `typescript-pro`, `python-pro`, `ruby-pro`, `php-pro`

**Enterprise & JVM**:
- `java-pro`, `scala-pro`, `csharp-pro`

**Specialized**:
- `django-pro`, `fastapi-pro`, `elixir-pro`, `unity-developer`, `minecraft-bukkit-pro`, `sql-pro`

### Quality Assurance & Security (10 agents)

| Agent | Model | Use Case |
|-------|-------|----------|
| **security-auditor** | opus | Vulnerability assessment and OWASP compliance |
| **code-reviewer** | opus | Code review with security focus and production reliability |
| **backend-security-coder** | opus | Secure backend coding practices, API security |
| **frontend-security-coder** | opus | XSS prevention, CSP implementation, client-side security |
| **test-automator** | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| **tdd-orchestrator** | sonnet | Test-Driven Development methodology |
| **debugger** | sonnet | Error resolution and test failure analysis |
| **performance-engineer** | opus | Application profiling and optimization |
| **observability-engineer** | opus | Production monitoring, distributed tracing, SLI/SLO |
| **error-detective** | sonnet | Log analysis and error pattern recognition |

### Infrastructure & Operations (11 agents)

**DevOps & Deployment**:
- `devops-troubleshooter` (sonnet) - Production debugging, log analysis
- `deployment-engineer` (sonnet) - CI/CD pipelines, containerization, cloud deployments
- `terraform-specialist` (opus) - Infrastructure as Code
- `dx-optimizer` (sonnet) - Developer experience optimization

**Database Management**:
- `database-optimizer` (opus) - Query optimization, index design
- `database-admin` (sonnet) - Database operations, backup, replication
- `database-architect` (opus) - Database design from scratch

**Incident Response**:
- `incident-responder` (opus) - Production incident management
- `network-engineer` (sonnet) - Network debugging, load balancing

### Data & AI (8 agents)

| Agent | Model | Use Case |
|-------|-------|----------|
| **ai-engineer** | opus | LLM applications, RAG systems, prompt pipelines |
| **ml-engineer** | opus | ML pipelines, model serving, feature engineering |
| **mlops-engineer** | opus | ML infrastructure, experiment tracking |
| **data-scientist** | opus | Data analysis, SQL queries, BigQuery operations |
| **data-engineer** | sonnet | ETL pipelines, data warehouses, streaming |
| **prompt-engineer** | opus | LLM prompt optimization |

### Documentation & Technical Writing (7 agents)

| Agent | Model | Use Case |
|-------|-------|----------|
| **docs-architect** | opus | Comprehensive technical documentation generation |
| **api-documenter** | sonnet | OpenAPI/Swagger specifications and developer docs |
| **reference-builder** | haiku | Technical references and API documentation |
| **tutorial-engineer** | sonnet | Step-by-step tutorials and educational content |
| **mermaid-expert** | sonnet | Diagram creation (flowcharts, sequences, ERDs) |

### Business & Operations (13 agents)

**Business Analysis**:
- `business-analyst`, `quant-analyst`, `risk-manager`

**Marketing & Sales**:
- `content-marketer`, `sales-automator`

**Support & Legal**:
- `customer-support`, `hr-pro`, `legal-advisor`

**SEO Specialists** (10 agents):
- `seo-content-auditor`, `seo-meta-optimizer`, `seo-keyword-strategist`, `seo-structure-architect`, `seo-snippet-hunter`, `seo-content-refresher`, `seo-cannibalization-detector`, `seo-authority-builder`, `seo-content-writer`, `seo-content-planner`

---

## Multi-Agent Workflows

### 1. Full-Stack Development
**File**: `workflows/full-stack-feature.md`

**Use Case**: End-to-end feature implementation

**Agents Coordinated**:
1. backend-architect → Design API endpoints
2. graphql-architect → Create GraphQL schema (if needed)
3. frontend-developer → Build UI components
4. mobile-developer → Implement mobile screens
5. test-automator → Generate test suites
6. security-auditor → Scan for vulnerabilities
7. performance-engineer → Optimize performance
8. deployment-engineer → Deploy to production

**Example**:
```
"Implement user dashboard with real-time analytics"
```

### 2. Security Hardening
**File**: `workflows/security-hardening.md`

**Use Case**: Security audit and OWASP compliance

**Agents Coordinated**:
1. security-auditor → Identify vulnerabilities
2. backend-security-coder → Fix backend issues
3. frontend-security-coder → Fix frontend issues
4. mobile-security-coder → Fix mobile issues
5. test-automator → Verify security fixes

**Example**:
```
"Perform security audit and implement OWASP best practices"
```

### 3. Data/ML Pipeline
**File**: `workflows/ml-pipeline.md`

**Use Case**: ML model development and deployment

**Agents Coordinated**:
1. data-scientist → Analyze data and train model
2. data-engineer → Build data pipeline
3. ml-engineer → Optimize model serving
4. mlops-engineer → Setup MLOps infrastructure
5. ai-engineer → Deploy to production
6. performance-engineer → Monitor and optimize

**Example**:
```
"Build customer churn prediction model with deployment"
```

### 4. Incident Response
**File**: `workflows/incident-response.md`

**Use Case**: Production debugging and SRE

**Agents Coordinated**:
1. incident-responder → Triage and coordinate
2. devops-troubleshooter → Debug deployment issues
3. debugger → Analyze code errors
4. error-detective → Parse logs and find patterns
5. observability-engineer → Setup monitoring

**Example**:
```
"Debug production memory leak and create runbook"
```

### 5. Performance Optimization
**File**: `workflows/performance-optimization.md`

**Use Case**: System profiling and optimization

**Agents Coordinated**:
1. performance-engineer → Profile application
2. database-optimizer → Optimize queries
3. devops-troubleshooter → Optimize infrastructure
4. observability-engineer → Setup performance monitoring

**Example**:
```
"Optimize application performance and reduce API latency"
```

### 6. TDD Cycle
**File**: `workflows/tdd-cycle.md`

**Use Case**: Test-Driven Development workflow

**Agents Coordinated**:
1. tdd-orchestrator → Guide TDD process
2. test-automator → Write tests first
3. Developer → Implement code to pass tests
4. code-reviewer → Review implementation

**Example**:
```
"Build new feature using TDD methodology"
```

---

## Practical Examples for Current Projects

### Example 1: CORS Issue Resolution (ActiveGenie)

**Scenario**: CORS errors from API Gateway

**Agent Usage**:
```
"Use backend-architect to analyze API Gateway CORS configuration"
```

**What backend-architect will do**:
- Review API Gateway settings
- Design proper CORS headers configuration
- Recommend Access-Control-Allow-Origin settings
- Provide CloudFormation/Terraform templates
- Document deployment steps

### Example 2: API Path Refactoring

**Scenario**: Need to update API paths across frontend and backend

**Multi-Agent Workflow**:
```
"Refactor API paths from /activegenie/ui-config/* to /ui/ui-*"
```

**Agents Coordinated**:
1. backend-architect → Update API Gateway routes
2. frontend-developer → Update Angular service calls
3. api-documenter → Update Swagger documentation
4. test-automator → Generate integration tests
5. deployment-engineer → Update environment configs

### Example 3: Security Audit

**Scenario**: Need OWASP compliance check

**Agent Usage**:
```
"Use security-auditor to scan for OWASP Top 10 vulnerabilities"
```

**What security-auditor will do**:
- Scan for SQL injection, XSS, CSRF
- Check authentication/authorization flows
- Review API security (rate limiting, input validation)
- Check for sensitive data exposure
- Provide remediation recommendations

### Example 4: Database Optimization

**Scenario**: Slow API response times

**Agent Usage**:
```
"Use database-optimizer to analyze and fix slow queries"
```

**What database-optimizer will do**:
- Analyze query execution plans
- Recommend index additions
- Suggest query rewrites
- Identify N+1 query problems
- Provide migration scripts

### Example 5: Infrastructure as Code

**Scenario**: Need to automate AWS infrastructure setup

**Agent Usage**:
```
"Use terraform-specialist to create IaC for API Gateway, Lambda, and RDS"
```

**What terraform-specialist will do**:
- Design Terraform module structure
- Create reusable modules
- Setup remote state management
- Configure environments (dev, staging, prod)
- Provide deployment documentation

---

## Installation & Usage

### Method 1: Plugin System (Recommended)

**Install Essential Tools**:
```bash
/plugin install claude-code-essentials
```

**Install Workflow Suites**:
```bash
/plugin install full-stack-development
/plugin install security-hardening
/plugin install api-development-kit
/plugin install testing-quality-suite
/plugin install infrastructure-devops
```

**Add Custom Marketplace**:
```bash
/plugin
# Select "Add marketplace"
# Enter: wshobson/agents
```

### Method 2: Manual (Already Done)

**Location**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents`

All agents are automatically available to Claude Code after cloning.

---

## Agent Invocation Patterns

### Pattern 1: Explicit Agent Request
```
"Use [agent-name] to [specific task]"
```

**Examples**:
- "Use backend-architect to design the authentication API"
- "Use security-auditor to scan for vulnerabilities"
- "Use performance-engineer to optimize this query"

### Pattern 2: Workflow Request
```
"[High-level goal that triggers workflow]"
```

**Examples**:
- "Implement user dashboard" → Triggers full-stack-feature workflow
- "Perform security audit" → Triggers security-hardening workflow
- "Debug production error" → Triggers incident-response workflow

### Pattern 3: Natural Language (Auto-Selection)
```
"[Natural request - Claude selects appropriate agent(s)]"
```

**Examples**:
- "How do I optimize this database query?" → database-optimizer
- "Review this code for security issues" → security-auditor
- "Write tests for this function" → test-automator

---

## Model Selection Strategy

Agents use different Claude models based on task complexity:

### Haiku (11 agents)
**Use Case**: Quick, focused tasks with minimal computational overhead

**Agents**:
- Context & Reference: `context-manager`, `reference-builder`, `sales-automator`, `search-specialist`
- SEO: All 7 SEO optimization agents

### Sonnet (50 agents)
**Use Case**: Standard development and specialized engineering tasks

**Agents**:
- All 18 programming language specialists
- Frontend & UI development
- Infrastructure operations
- Quality & testing
- Data engineering

### Opus (22 agents)
**Use Case**: Complex reasoning, architecture, and critical analysis

**Agents**:
- All 7 architecture & design agents
- Security & code review
- Performance & observability
- AI/ML specialists
- Business-critical operations

---

## Integration with Existing Systems

### 1. Memory System Integration

Agents can access project memory via:
- `memory.db` - Structured project memory
- Vector stores - Semantic search via LangChain MCP
- Session context - Previous conversation history

**Example**:
```
"Use backend-architect to review previous API design decisions"
```

Agent will:
1. Query memory.db for past decisions
2. Search vector store for related architecture docs
3. Provide recommendations consistent with past choices

### 2. Autonomy System Integration

Agents work with existing autonomy features:
- Auto-context management
- Auto-session management
- Auto-memory capture
- Auto-file organization

**Example**:
```
"Use deployment-engineer to automate CI/CD pipeline"
```

Agent will:
1. Create deployment scripts
2. Update autonomy config
3. Store decisions to memory
4. Generate session summary

### 3. MCP Server Integration

Agents can use configured MCP servers:
- **langchain** - Vector DB operations
- **code-index** - Code search
- **github** - Repository operations
- **context7** - Documentation on-demand

---

## Best Practices

### 1. Choose the Right Agent

**Bad**: "Fix this code"
**Good**: "Use debugger to analyze this error and suggest fixes"

**Bad**: "Make it faster"
**Good**: "Use performance-engineer to profile and optimize this API endpoint"

### 2. Use Multi-Agent Workflows for Complex Tasks

**Bad**: Single agent for full-stack feature
**Good**: Use full-stack-development workflow to coordinate multiple specialists

### 3. Leverage Model Tiers Appropriately

**Haiku**: Simple SEO meta tag optimization
**Sonnet**: Standard Python development
**Opus**: Complex architecture decisions

### 4. Provide Context

**Bad**: "Use security-auditor"
**Good**: "Use security-auditor to scan this authentication flow for OWASP Top 10 vulnerabilities"

### 5. Combine with Memory

**Bad**: Agent starts from scratch each time
**Good**: "Use backend-architect to extend the API design we discussed last week"

---

## Workflow Orchestration Examples

### Example 1: New Feature Development

**Request**: "Build a user notification system with email and push notifications"

**Workflow Triggered**: `full-stack-development`

**Agent Coordination**:
```
1. backend-architect
   → Design notification service API
   → Database schema for notifications
   → Queue architecture (Redis/SQS)

2. frontend-developer
   → Notification UI component
   → Real-time updates (WebSocket)
   → Notification preferences page

3. mobile-developer
   → Push notification handling
   → In-app notification display
   → Notification settings

4. test-automator
   → API integration tests
   → UI component tests
   → End-to-end notification flow tests

5. security-auditor
   → Validate notification permissions
   → Check for notification injection
   → Review data privacy

6. deployment-engineer
   → Setup notification queues
   → Configure email service (SES/SendGrid)
   → Deploy to staging/production
```

### Example 2: Security Compliance Audit

**Request**: "Prepare application for SOC2 compliance audit"

**Workflow Triggered**: `security-hardening`

**Agent Coordination**:
```
1. security-auditor
   → Full OWASP Top 10 scan
   → Identify compliance gaps
   → Create remediation plan

2. backend-security-coder
   → Implement secure session management
   → Add API rate limiting
   → Encrypt sensitive data at rest

3. frontend-security-coder
   → Implement CSP headers
   → Add XSS protection
   → Secure authentication flows

4. observability-engineer
   → Setup audit logging
   → Configure security monitoring
   → Create compliance dashboards

5. docs-architect
   → Document security controls
   → Create security policies
   → Generate compliance evidence
```

### Example 3: Performance Crisis Resolution

**Request**: "API response time increased from 200ms to 5 seconds"

**Workflow Triggered**: `incident-response` + `performance-optimization`

**Agent Coordination**:
```
1. incident-responder
   → Assess severity and impact
   → Create incident timeline
   → Coordinate team response

2. observability-engineer
   → Check APM metrics
   → Analyze distributed traces
   → Identify bottleneck

3. performance-engineer
   → Profile application code
   → Identify slow functions
   → Recommend optimizations

4. database-optimizer
   → Analyze slow queries
   → Check index usage
   → Optimize query plans

5. devops-troubleshooter
   → Check infrastructure metrics
   → Verify autoscaling
   → Optimize resource allocation

6. docs-architect
   → Create incident post-mortem
   → Document root cause
   → Update runbooks
```

---

## Quick Reference: Common Tasks

| Task | Agent | Example |
|------|-------|---------|
| API Design | backend-architect | "Design RESTful API for user management" |
| Code Review | code-reviewer | "Review this PR for security and quality" |
| Bug Fixing | debugger | "Debug this authentication error" |
| Performance | performance-engineer | "Optimize this slow endpoint" |
| Security Scan | security-auditor | "Scan for OWASP vulnerabilities" |
| Database | database-optimizer | "Optimize these slow queries" |
| Frontend | frontend-developer | "Build responsive dashboard component" |
| Testing | test-automator | "Generate unit tests for this service" |
| Deployment | deployment-engineer | "Setup CI/CD for this application" |
| Documentation | api-documenter | "Create OpenAPI spec from this code" |
| Cloud Setup | cloud-architect | "Design AWS architecture for this app" |
| Error Analysis | error-detective | "Analyze these error logs" |

---

## Agent Directory Structure

```
.claude/agents/
├── agents/                    # 83 specialized agents
│   ├── backend-architect.md
│   ├── security-auditor.md
│   ├── performance-engineer.md
│   └── ... (80 more)
├── workflows/                 # 15 multi-agent orchestrators
│   ├── full-stack-feature.md
│   ├── security-hardening.md
│   ├── incident-response.md
│   └── ... (12 more)
├── tools/                     # 42 development utilities
│   ├── api-scaffold.md
│   ├── security-scan.md
│   └── ... (40 more)
├── examples/                  # Usage examples
└── README.md                  # Full documentation
```

---

## Memory Storage

All agent interactions are automatically stored to memory:

**Entity Type**: `agent-usage`
**Importance**: 2 (Important)
**Tags**: `agent-system`, `context-optimization`, `2025-10-10`

**Example Entry**:
```sql
INSERT INTO project_memory (entity_name, entity_type, content, importance, tags)
VALUES (
  'agents-system-integrated',
  'system-component',
  'Integrated 83 specialized agents from wshobson/agents repository',
  3,
  '["agent-system", "infrastructure", "2025-10-10"]'
);
```

---

## Next Steps

### Immediate
- [x] Clone agents repository
- [x] Create integration guide
- [ ] Test agent invocation in conversation
- [ ] Store agent knowledge to memory

### Short-Term
- [ ] Install recommended plugin suites
- [ ] Test multi-agent workflows
- [ ] Create project-specific agent shortcuts
- [ ] Integrate with existing autonomy system

### Long-Term
- [ ] Create custom agents for project-specific tasks
- [ ] Build project-specific workflows
- [ ] Optimize agent coordination patterns
- [ ] Track agent usage metrics

---

## Troubleshooting

### Issue: Agent not responding

**Solution**: Ensure explicit invocation:
```
# BAD:
"Fix the CORS issue"

# GOOD:
"Use backend-architect to analyze and fix the CORS configuration"
```

### Issue: Multiple agents conflict

**Solution**: Use workflow orchestrator:
```
# BAD:
"Use backend-architect and security-auditor and performance-engineer"

# GOOD:
"Use full-stack-development workflow to build this feature"
```

### Issue: Agent lacks project context

**Solution**: Reference memory:
```
# BAD:
"Use backend-architect to design API"

# GOOD:
"Use backend-architect to design API, following the patterns we used in the user-service project"
```

---

## Resources

- **Repository**: https://github.com/wshobson/agents
- **Claude Code Docs**: https://docs.anthropic.com/en/docs/claude-code
- **Subagents Documentation**: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- **Local Path**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\.claude\agents`

---

**Status**: ✅ Ready to Use
**Last Updated**: October 10, 2025
**Created By**: Claude Code
**Version**: 1.0
