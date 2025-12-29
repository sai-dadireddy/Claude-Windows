---
description: Intelligent agent analysis and creation (analyze|create|list|review)
argument-hint: <action> [options]
allowed-tools: Read, Write, Grep, Glob, Task
model: sonnet
---

# Intelligent Agent Management

**Purpose:** Organically grow your agent team based on actual workflow needs

Action: $ARGUMENTS

---

## Available Actions:

### analyze
**Analyze workflow and recommend specialized agents** (~800 tokens, 60 seconds)

**Purpose:** Let Claude study YOUR actual workflow and suggest agents you need

**Workflow:**

#### Step 1: Analyze Current Projects (20 seconds)
```bash
# Check what projects you have
Glob pattern:"projects/*/PROJECT-TRACKER.md"
Glob pattern:"projects/*/.claude/CLAUDE.md"

# Extract:
- Project names
- Tech stacks
- Common tasks
- Current phases
```

#### Step 2: Analyze Git Activity (15 seconds)
```bash
# For each project
Bash: cd projects/[project] && git log --oneline --since="1 month ago" | head -20

# Detect patterns:
- "fix:" commits → Need debugging agent?
- "test:" commits → Need test specialist?
- "refactor:" commits → Need refactoring agent?
- "security:" commits → Need security agent?
- "deploy:" commits → Need DevOps agent?
```

#### Step 3: Analyze File Types (10 seconds)
```bash
# Quick scan of each project
Glob pattern:"projects/**/src/**/*.ts"
Glob pattern:"projects/**/src/**/*.py"
Glob pattern:"projects/**/src/**/*.java"
Glob pattern:"projects/**/*.conf"
Glob pattern:"projects/**/*.yml"

# Tech stack detection:
- Lots of .ts/.tsx → frontend-specialist needed
- .py files → python-specialist needed
- .conf files → config-specialist needed
- .yml/.yaml → devops-specialist needed
```

#### Step 4: Check Existing Agents (5 seconds)
```bash
# What agents do you already have?
Glob pattern:".claude/agents/*.md"

# Compare with needs
```

#### Step 5: AI-Powered Recommendation (10 seconds)
```bash
Based on analysis, recommend agents with:

For each recommended agent:
  - Name: [descriptive-name]
  - Purpose: [specific use case from YOUR workflow]
  - Trigger patterns: [when it should activate]
  - Tools needed: [minimal set]
  - Priority: critical|high|medium|low
  - Estimated usage: [% of time you'd use it]
  - Token cost: [~200 tokens baseline]
  - ROI: [potential savings]
```

#### Output:
```
Agent Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Projects Analyzed: 8
  - strivacity (OIDC/Apache/Auth)
  - erpagpt (ChatGPT integration)
  - active-genie (Angular/Nginx)
  - PeopleSoft-RAG (RAG pipeline)
  - aarp (Research project)
  - aws-chatbot (AWS integration)
  - [...]

🔍 Workflow Patterns Detected:

Authentication/Security (40% of commits):
  - OIDC configuration debugging
  - Apache config reviews
  - Cognito integration
  → Recommend: oidc-auth-specialist

API Integration (25% of commits):
  - REST API endpoints
  - ChatGPT integration
  - Error handling
  → Recommend: api-integration-specialist

Infrastructure (20% of commits):
  - Nginx configuration
  - AWS ECS deployments
  - Docker/infrastructure
  → Recommend: devops-specialist

RAG/AI (15% of commits):
  - Vector database operations
  - Document indexing
  - Query optimization
  → Recommend: rag-specialist

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Recommended Agents (Priority Order):

1. oidc-auth-specialist ⭐⭐⭐ CRITICAL
   Purpose: Debug OIDC flows, Apache config, Cognito integration
   Usage: 40% of your work
   ROI: High (saves 5-10K tokens per auth issue)
   Tools: Read, Grep, Bash(systemctl, curl)

2. api-integration-specialist ⭐⭐⭐ HIGH
   Purpose: REST API design, ChatGPT integration, error handling
   Usage: 25% of your work
   ROI: High (saves 3-8K tokens per API task)
   Tools: Read, Write, Bash(curl, jq)

3. devops-specialist ⭐⭐ MEDIUM
   Purpose: Nginx config, ECS deployments, Docker
   Usage: 20% of your work
   ROI: Medium (saves 2-5K tokens per deploy)
   Tools: Read, Bash(docker, aws)

4. rag-specialist ⭐⭐ MEDIUM
   Purpose: Vector DB, document indexing, query optimization
   Usage: 15% of your work
   ROI: Medium (saves 2-4K tokens per RAG task)
   Tools: Read, Bash(python tools/)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Next Steps:
  1. Review recommendations
  2. Run: /agents create oidc-auth-specialist
  3. Or: /agents create all (creates top 4)

Would you like me to create these agents? (y/n)
```

---

### create [agent-name|all]
**Create specialized agent(s)** (~400 tokens per agent, 30 seconds each)

**Options:**
- `create oidc-auth-specialist` - Create single agent
- `create all` - Create all recommended agents

**Workflow:**

#### Step 1: Design Agent Prompt (15 seconds)
```bash
Based on analysis, create detailed agent with:

1. Role & Expertise
   "You are an OIDC authentication specialist focusing on..."

2. Specific Knowledge
   - Apache mod_auth_openidc configuration
   - Strivacity OIDC provider setup
   - PeopleSoft integration patterns
   - Debugging auth flows

3. Workflow Process
   - Step-by-step debugging approach
   - Common issues and solutions
   - Testing patterns

4. Constraints
   - Read before modifying
   - Test changes in dev first
   - Document all config changes

5. Success Criteria
   - OIDC flow works end-to-end
   - Logs show successful auth
   - No redirect errors
```

#### Step 2: Define Tool Permissions (5 seconds)
```bash
# Minimal tools only
allowed-tools: Read, Grep, Bash(systemctl:*, curl:*, tail:*)

# NOT: Write, Edit (read-only for safety)
# Exception: If agent needs to fix, grant Edit with approval
```

#### Step 3: Create Agent File (10 seconds)
```bash
Write .claude/agents/oidc-auth-specialist.md

Structure:
---
name: oidc-auth-specialist
description: [Trigger keywords for auto-activation]
allowed-tools: [minimal set]
model: sonnet
---

[Detailed instructions]
[Workflow steps]
[Common patterns]
[Troubleshooting]
```

#### Step 4: Update Skill Rules (5 seconds)
```bash
# Add to skill-rules.json for auto-activation
Edit .claude/hooks/skill-rules.json

Add trigger patterns:
  keywords: ["oidc", "apache", "cognito", "auth", "redirect"]
  intentPatterns: ["debug.*(auth|oidc)", "fix.*(redirect|401|403)"]
```

---

### list
**Show current agents and their usage** (50 tokens, 5 seconds)

```bash
Glob pattern:".claude/agents/*.md"

Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Agents (4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. oidc-auth-specialist
   Created: 2d ago
   Usage: High
   Tools: Read, Grep, Bash(systemctl, curl)

2. api-integration-specialist
   Created: 2d ago
   Usage: Medium
   Tools: Read, Write, Bash(curl, jq)

[...]

Run /agents analyze to find gaps
```

---

### review
**Review agent effectiveness and suggest improvements** (~600 tokens, 45 seconds)

**Workflow:**

#### Step 1: Check Agent Logs
```bash
# Review agent usage from logs
Read .claude/hooks/agent-usage.log (if exists)

Analyze:
- How often each agent was invoked
- Success rate
- Common failures
- Time saved
```

#### Step 2: Analyze Recent Conversations
```bash
# Check recent transcripts for agent usage
# Detect patterns:
- Agents that should have been used but weren't
- Agents used incorrectly
- Missing specialized agents
```

#### Step 3: Recommendations
```
Agent Review Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Working Well:
  - oidc-auth-specialist: 15 invocations, 93% success
  - api-integration-specialist: 8 invocations, 100% success

⚠️ Underutilized:
  - devops-specialist: Only 2 uses in 2 weeks
  → Consider: Merge with another agent or remove

❌ Missing:
  - Angular component specialist (detected 12 Angular tasks)
  - Database migration specialist (detected 5 DB migrations)

💡 Improvements:
  - oidc-auth-specialist: Add Nginx config knowledge
  - api-integration-specialist: Add rate limiting patterns

Recommended Actions:
  1. Create: angular-component-specialist
  2. Create: database-migration-specialist
  3. Update: oidc-auth-specialist (add Nginx)
  4. Consider removing: devops-specialist (low usage)
```

---

## 🎯 Complete Workflow Example

### **Step 1: Initial Analysis**
```bash
/agents analyze

# Claude analyzes your 8 projects
# Recommends 4 specialized agents
# Shows ROI and priority
```

### **Step 2: Create Agents**
```bash
/agents create all

# Creates:
✅ oidc-auth-specialist.md
✅ api-integration-specialist.md
✅ devops-specialist.md
✅ rag-specialist.md

# Updates skill-rules.json for auto-activation
```

### **Step 3: Use Organically**
```bash
# Your prompt: "Debug OIDC redirect issue"

# UserPromptSubmit hook detects "OIDC"
🎯 SKILL ACTIVATION CHECK:
   Agent available: oidc-auth-specialist

# Claude automatically uses the agent!
```

### **Step 4: Review After 2 Weeks**
```bash
/agents review

# Shows usage stats
# Suggests improvements
# Recommends new agents
# Identifies unused agents
```

---

## 💡 Advanced Features

### **Parallel Agent Orchestration**
```bash
# Claude detects complex task
# Automatically suggests:
"I recommend running these agents in parallel:
  - @api-integration-specialist (API endpoints)
  - @devops-specialist (infrastructure)
  - @rag-specialist (documentation)

  Use Task tool to run in parallel?"
```

### **Agent Chaining**
```bash
# For complex workflows
1. @rag-specialist → Research patterns
2. @api-integration-specialist → Design API
3. @code-reviewer → Review implementation
4. @devops-specialist → Deploy
```

### **Cost Optimization**
```bash
# Uses Haiku for simple agents (3x cheaper)
# Uses Sonnet for complex agents
# Configurable per agent in frontmatter
```

---

## 📊 Token Impact

**Agent Analysis:** 800 tokens (one-time)
**Agent Creation:** 400 tokens per agent
**Agent Usage:** Variable (depends on task)

**ROI:**
- Each specialized agent saves 2-10K tokens per invocation
- Analysis cost: 800 tokens
- 4 agents created: 1,600 tokens
- **Break-even: After using agents 1-2 times each**

---

## 🚀 Why This Command is Powerful

**Before:**
- Manually guess what agents you need
- Create generic agents
- Agents sit unused
- No data-driven decisions

**After:**
- ✅ Claude analyzes YOUR actual projects
- ✅ Recommends agents based on real usage patterns
- ✅ Creates project-specific agents
- ✅ Tracks effectiveness
- ✅ Suggests improvements
- ✅ Organic growth based on data

**The agents match YOUR workflow, not generic templates!**

---

## 🎯 Integration with Skills

**Skills** (general patterns):
- RAG queries, debugging, code review, TDD

**Agents** (project-specific):
- OIDC authentication for Strivacity
- ChatGPT integration for ERPAGPT
- Angular components for Active Genie
- RAG pipeline for PeopleSoft-RAG

**Together:** Complete coverage of general + specific needs!

---

**Run `/agents analyze` to get started!**
