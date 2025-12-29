# Model-Specific Prompting Guide

Use this skill when routing tasks to external models (GLM, Gemini, OpenAI) to ensure optimal results.

## Quick Decision Tree

```
Is it your normal workflow?
  └─ YES → Stay with Claude Opus 4.5 (your default)
  └─ NO → Continue below

Is context > 200K tokens?
  └─ YES → Use gemini-2.5-flash (1M context, cheap)

Is it multilingual code?
  └─ YES → Use glm-4.7 (66.7% SWE-bench multilingual)

Is it tool calling / MCP integration?
  └─ YES → Use glm-4.7 (84.7 on τ²-Bench)

Is cost the priority?
  └─ YES → Use gemini-2.5-flash-lite (cheapest)

Need deep reasoning?
  └─ YES → Stay with Claude Opus 4.5
```

---

## GLM Prompting (4.7/4.6)

### When to Use
- Multilingual codebases
- Large context (100K-200K tokens)
- Tool calling tasks
- Cost optimization (1/7 price of Claude API)

### Prompt Template
```xml
<task>
[Clear imperative: "Implement X", "Review Y", "Debug Z"]
</task>

<requirements>
- [Specific requirement 1]
- [Specific requirement 2]
- [Edge cases to handle]
</requirements>

<context>
[Relevant code or file contents]
</context>

<constraints>
- Language: [Python/TypeScript/Go/etc]
- Must: [what to do]
- Must NOT: [what to avoid]
</constraints>
```

### GLM Thinking Modes

**Enable for complex tasks:**
```json
{"thinking": {"type": "enabled", "budget_tokens": 5000}}
```

**Disable for simple tasks (saves tokens):**
```json
{"thinking": false}
```

### GLM Best Practices
1. **Be imperative** - "Implement X" not "How do I X?"
2. **Provide context upfront** - Include file contents before asking
3. **Use XML tags** - GLM responds well to structured prompts
4. **Enable thinking for debugging** - Worth the extra tokens
5. **Specify language explicitly** - Helps with multilingual

### Example GLM Prompts

**Code Generation:**
```
<task>Implement a rate limiter middleware for Express</task>

<requirements>
- Token bucket algorithm
- Configurable requests per minute
- Redis-backed for distributed systems
- Return 429 with Retry-After header
</requirements>

<constraints>
- Language: TypeScript
- Must use ioredis client
- Must be unit testable
</constraints>
```

**Debugging:**
```
<task>Debug this authentication failure</task>

<error>
JWT verification failed: TokenExpiredError
</error>

<code>
[paste relevant code]
</code>

<context>
- Expected: Token should be valid for 24h
- Actual: Expires after ~1h
- Already tried: Checked token creation timestamp
</context>
```

---

## Gemini Prompting (2.5 Flash/Pro)

### When to Use
- Very large context (200K-1M tokens)
- Analyzing entire codebases
- Quick code review
- When free tier is acceptable

### Prompt Template
```
TASK: [Clear one-line description]

CONTEXT:
[Large file or codebase contents - Gemini handles up to 1M tokens]

FOCUS ON:
- [Specific aspect 1]
- [Specific aspect 2]

OUTPUT FORMAT:
[Specify: bullet points, code, JSON, etc]
```

### Gemini Best Practices
1. **Front-load context** - Put large files first
2. **Disable thinking for simple tasks** - Saves 4x on output tokens
3. **Use for bulk analysis** - Great for reviewing many files
4. **Specify output format** - Gemini follows formats well
5. **Batch requests** - 50% discount for non-urgent work

### Thinking Mode Cost
- **Without thinking:** $0.60/1M output
- **With thinking:** $2.50/1M output
- **Rule:** Disable thinking unless complex reasoning needed

### Example Gemini Prompts

**Large Codebase Analysis:**
```
TASK: Analyze this codebase for architectural patterns

CONTEXT:
[paste 200K+ tokens of code]

FOCUS ON:
- Design patterns used
- Dependency relationships
- Potential refactoring opportunities

OUTPUT FORMAT:
1. Executive summary (2-3 sentences)
2. Pattern inventory (bullet list)
3. Dependency graph (ASCII)
4. Top 5 refactoring suggestions
```

**Quick Code Review:**
```
TASK: Security review of authentication module

CODE:
[paste files]

CHECK FOR:
- OWASP Top 10 vulnerabilities
- Input validation gaps
- Session management issues

OUTPUT: Bullet list of findings with severity
```

---

## OpenAI Prompting (GPT-4o/o1/o3)

### When to Use
- When user explicitly requests GPT
- Specific integrations requiring OpenAI
- Deep reasoning tasks (o1/o3)
- Multimodal (image) tasks

### Model Selection
| Model | Best For | Cost |
|-------|----------|------|
| gpt-4o-mini | Simple tasks, cheapest | $0.15/$0.60 |
| gpt-4o | Multimodal, balanced | $2.50/$10 |
| o1-mini | Fast reasoning | $3/$12 |
| o3-mini | Latest reasoning | $1.10/$4.40 |
| o1 | Deep reasoning | $15/$60 |

### Prompt Template
```
# Task
[Clear description]

# Context
[Background information]

# Requirements
1. [Requirement]
2. [Requirement]

# Expected Output
[Format specification]
```

### OpenAI Best Practices
1. **Use markdown headers** - GPT models parse markdown well
2. **Be explicit about format** - Include examples if needed
3. **For o1/o3:** Let the model think, don't rush it
4. **For gpt-4o-mini:** Keep prompts simple, it's a small model
5. **For images:** Include image analysis explicitly

---

## Routing Patterns

### Pattern 1: Large Context
```
IF context > 200K tokens:
  USE gemini-2.5-flash
ELIF context > 100K tokens:
  USE glm-4.7
ELSE:
  USE claude-opus-4.5 (your default)
```

### Pattern 2: Cost Optimization
```
IF bulk processing:
  USE gemini-2.5-flash-lite (cheapest)
ELIF simple task:
  USE gpt-4o-mini
ELIF coding task:
  USE glm-4.7 (good + cheap)
ELSE:
  USE claude-opus-4.5
```

### Pattern 3: Quality Priority
```
IF critical decision:
  USE claude-opus-4.5 + multi:compare (consensus)
ELIF deep reasoning:
  USE o1 or claude-opus-4.5
ELIF coding:
  USE claude-opus-4.5 (your default, best overall)
```

### Pattern 4: Multilingual
```
IF non-English code/comments:
  USE glm-4.7 (66.7% SWE-bench multilingual)
ELSE:
  USE claude-opus-4.5
```

---

## Anti-Patterns (Don't Do This)

### 1. Routing Simple Tasks Away
```
❌ "Ask gemini to print hello world"
✅ Just do it with Claude (your default, already paid for)
```

### 2. Using Expensive Models for Bulk
```
❌ Using o1 for reviewing 50 files
✅ Use gemini-2.5-flash or glm-4.7 (much cheaper)
```

### 3. Ignoring Context Limits
```
❌ Sending 500K tokens to GLM (200K limit)
✅ Use gemini-2.5-flash (1M limit)
```

### 4. Always Enabling Thinking
```
❌ Enabling thinking for "what is 2+2?"
✅ Only enable thinking for complex tasks
```

---

## MCP Tool Invocations

### Single Model Query
```
"Use multi:chat with glm-4.7:
<task>Review this file for security issues</task>
<code>
[code here]
</code>"
```

### Multi-Model Compare
```
"Run multi:compare with opus, glm-4.7, gemini-2.5-flash:
What's the best approach for implementing caching here?"
```

### Model Debate
```
"Use multi:debate with opus and glm-4.7:
Review this architecture decision for potential issues"
```

### Code Review
```
"Do multi:codereview on src/auth/ with glm-4.7"
```

---

## Summary: Model Strengths

| Model | Strength | Weakness |
|-------|----------|----------|
| **Claude Opus 4.5** | Best overall, your default | Paid (but included in Max) |
| **GLM 4.7** | Multilingual, tool calling, cheap | Smaller context than Gemini |
| **Gemini 2.5 Flash** | 1M context, very cheap | Quota limits on free tier |
| **GPT-4o-mini** | Cheapest OpenAI | Less capable |
| **o1** | Deep reasoning | Expensive, slow |

**Default:** Claude Opus 4.5 (already paid via Max subscription)
**Route when:** Large context, multilingual, cost-sensitive bulk ops
