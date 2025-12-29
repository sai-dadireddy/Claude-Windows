# Model Routing Brain - When/Where/How to Use Each Model

This skill defines EXACTLY when to route to which model. Claude Code should internalize this.

## The Golden Rule

```
DEFAULT: Claude Opus 4.5 (your subscription, best overall)
ROUTE ONLY WHEN: Specific advantage exists elsewhere
```

---

## Decision Matrix

### 1. CODING TASKS

| Scenario | Best Model | Why | Via Router |
|----------|------------|-----|------------|
| **General coding** | Claude Opus 4.5 | 77.2% SWE-bench, YOUR DEFAULT | Just do it |
| **Multilingual code** | GLM 4.7 | 66.7% SWE-bench multilingual | `router_execute(mcp_name="multi", tool_name="chat", arguments={"model": "glm-4.7"})` |
| **Code generation** | Codestral | Specialist for code | `router_execute(..., arguments={"model": "codestral"})` |
| **Large codebase** | Gemini 2.5 Flash | 1M context | `router_execute(..., arguments={"model": "gemini-2.5-flash"})` |
| **Budget coding** | DeepSeek V3.2 | FREE, 73%+ accuracy | `router_execute(..., arguments={"model": "deepseek-v3.2"})` |

### 2. REASONING TASKS

| Scenario | Best Model | Why | Via Router |
|----------|------------|-----|------------|
| **Complex reasoning** | Claude Opus 4.5 | Best overall | Just do it |
| **Math proofs** | DeepSeek R1 | FREE, built-in CoT | `router_execute(..., arguments={"model": "deepseek-r1"})` |
| **Scientific** | DeepSeek R1 | Strong on scientific | `router_execute(..., arguments={"model": "deepseek-r1"})` |
| **Step-by-step** | o1 | Dedicated reasoning | `router_execute(..., arguments={"model": "o1"})` |

### 3. CONTEXT SIZE

| Tokens Needed | Best Model | Context Limit | Via Router |
|---------------|------------|---------------|------------|
| < 100K | Claude Opus 4.5 | 200K | Default |
| 100K - 200K | GLM 4.7 | 200K | `router_execute(..., arguments={"model": "glm-4.7"})` |
| 200K - 1M | Gemini 2.5 Flash | 1M | `router_execute(..., arguments={"model": "gemini-2.5-flash"})` |
| > 1M | Gemini CLI | 2M+ | Use CLI directly |

### 4. MULTIMODAL

| Media Type | Best Model | Why | Via Router |
|------------|------------|-----|------------|
| **Images** | Gemini 2.5 | Native multimodal | `router_execute(..., arguments={"model": "gemini-2.5-flash"})` |
| **Vision+Text** | Pixtral Large | Mistral vision | `router_execute(..., arguments={"model": "pixtral-large"})` |
| **Video** | Gemini 3 | Video understanding | `router_execute(..., arguments={"model": "gemini-3-pro"})` |
| **Code screenshots** | Claude Opus 4.5 | Good vision | Default |

### 5. COST OPTIMIZATION

| Budget | Best Model | Cost | Via Router |
|--------|------------|------|------------|
| **FREE** | DeepSeek V3.2 | $0 (Ollama) | `router_execute(..., arguments={"model": "deepseek-v3.2"})` |
| **FREE** | Llama 405B | $0 (OpenRouter) | `router_execute(..., arguments={"model": "llama-405b"})` |
| **FREE** | DeepSeek R1 | $0 (OpenRouter) | `router_execute(..., arguments={"model": "deepseek-r1"})` |
| **Cheapest paid** | Gemini Flash-Lite | $0.10/$0.40 | `router_execute(..., arguments={"model": "gemini-flash-lite"})` |
| **Included** | Claude Opus 4.5 | Max subscription | Default |

### 6. TOOL CALLING / MCP

| Scenario | Best Model | Why | Via Router |
|----------|------------|-----|------------|
| **MCP integration** | Claude Opus 4.5 | Native MCP | Default |
| **Tool calling** | GLM 4.7 | 84.7 τ²-Bench | `router_execute(..., arguments={"model": "glm-4.7"})` |
| **Function calling** | GPT-4o | Reliable | `router_execute(..., arguments={"model": "gpt-4o"})` |

### 7. SPEED

| Need | Best Model | Latency | Via Router |
|------|------------|---------|------------|
| **Fastest** | Claude Haiku | ~0.5s | `router_execute(..., arguments={"model": "haiku"})` |
| **Fast + FREE** | GLM Air | ~1s | `router_execute(..., arguments={"model": "glm-air"})` |
| **Fast inference** | Cerebras* | Fastest | Need API key |

---

## Exact Routing Rules for Claude Code

### ALWAYS Stay with Claude Opus 4.5 When:
- Normal coding tasks (your default workflow)
- Writing/refactoring code
- Debugging
- Code review (unless comparing)
- Tool use / MCP operations
- Planning and architecture
- Documentation
- User doesn't specify otherwise

### ROUTE to GLM 4.7 When:
- User mentions "multilingual", "Chinese", "Japanese", "Korean", etc.
- Large context 100K-200K tokens
- Tool calling benchmarks/tests
- User says "use GLM" or "/glm"

### ROUTE to Gemini When:
- Context > 200K tokens
- User says "analyze entire codebase/repo"
- Multimodal (images, video)
- User says "use gemini"

### ROUTE to DeepSeek When:
- User says "cheap", "free", "budget"
- Need reasoning with chain-of-thought visible
- Scientific/math tasks
- User says "use deepseek" or "use r1"

### ROUTE to OpenAI When:
- User explicitly requests GPT
- Need specific OpenAI features
- o1/o3 for dedicated reasoning

### USE router_execute(mcp_name="multi", tool_name="compare") When:
- Architecture decisions
- "What's the best approach?"
- Need consensus from multiple models
- Security review (multiple perspectives)

### USE router_execute(mcp_name="multi", tool_name="debate") When:
- Critical decisions
- Want models to critique each other
- Need thorough analysis

---

## Prompting Templates by Model

### For Claude (Default)
```
[Just give the task directly - Claude understands context well]
```

### For GLM 4.7
```xml
<task>
[Clear imperative statement]
</task>

<context>
[Relevant code/info]
</context>

<constraints>
- Language: [specify]
- Must: [requirements]
- Must NOT: [restrictions]
</constraints>
```

### For Gemini
```
TASK: [One-line description]

CONTEXT:
[Large file/codebase - Gemini handles 1M tokens]

FOCUS ON:
- [Point 1]
- [Point 2]

OUTPUT FORMAT:
[Bullet points/JSON/etc]
```

### For DeepSeek
```
Think step by step.

[Your question/task]

Show your reasoning.
```

### For OpenAI
```markdown
# Task
[Description]

# Context
[Background]

# Requirements
1. [Req 1]
2. [Req 2]

# Output Format
[Specify exactly]
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    MODEL ROUTING CHEATSHEET                 │
├─────────────────────────────────────────────────────────────┤
│ DEFAULT → Claude Opus 4.5 (always, unless reason to route) │
├─────────────────────────────────────────────────────────────┤
│ Multilingual?     → router_execute(..., model="glm-4.7")    │
│ Context > 200K?   → router_execute(..., model="gemini")     │
│ FREE needed?      → router_execute(..., model="deepseek")   │
│ Reasoning/Math?   → router_execute(..., model="r1")         │
│ Images/Video?     → router_execute(..., model="pixtral")    │
│ Comparing options?→ router_execute(tool_name="compare")     │
│ Speed critical?   → router_execute(..., model="haiku")      │
│ Tool calling?     → Claude (default) or GLM 4.7             │
└─────────────────────────────────────────────────────────────┘
```

---

## API Test Results (Verified Working)

| Provider | Status | Model Tested |
|----------|--------|--------------|
| Claude | ✅ | Max subscription |
| GLM/Z.AI | ✅ | glm-4.7 |
| Gemini | ✅ | gemini-2.5-flash |
| OpenAI | ✅ | gpt-4o-mini |
| Ollama Cloud | ✅ | deepseek-v3.2 |
| OpenRouter | ✅ | deepseek-r1 |
| Mistral | ✅ | mistral-small |
| HuggingFace | ✅ | llama-3.3-70b |

---

## Sources

- [LLM Comparison 2025](https://mgx.dev/blog/2025-llm-review-gpt-5-2-gemini-3-pro-claude-4-5)
- [Model Benchmarks](https://rankllms.com/ai-model-benchmarks/)
- [Claude Code Router](https://lgallardo.com/2025/08/20/claude-code-router-openrouter-beyond-anthropic/)
- [DeepSeek vs Claude vs GPT](https://www.datastudios.org/post/chatgpt-vs-claude-vs-deepseek-full-report-and-comparison-on-features-capabilities-pricing-and-mo)
