# AI Model Pricing & Optimization Reference

## Cost Ranking (Cheapest to Most Expensive)

Per 1M **output** tokens (the expensive part):

| Rank | Model | Output/1M | Input/1M | Best For |
|------|-------|-----------|----------|----------|
| **FREE** | DeepSeek-v3.2 (671B) | $0.00 | $0.00 | Reasoning, thinking mode |
| **FREE** | Kimi-K2 (1T) | $0.00 | $0.00 | Massive model, complex tasks |
| **FREE** | Qwen3-Coder (480B) | $0.00 | $0.00 | Coding tasks |
| **FREE** | Mistral-Large-3 (675B) | $0.00 | $0.00 | Reasoning |
| **FREE** | Devstral-2 (123B) | $0.00 | $0.00 | Coding-focused |
| 1 | Gemini 2.5 Flash-Lite | $0.40 | $0.10 | Bulk/simple tasks |
| 2 | Gemini 2.5 Flash | $0.60* | $0.15 | Fast coding, large context |
| 3 | GLM-4.5-Air | $1.10 | $0.20 | Fast cheap coding |
| 4 | GLM-4.7/4.6 | $2.20 | $0.60 | Multilingual, tool calling |
| 5 | GPT-4o-mini | $2.40 | $0.60 | Simple tasks |
| 6 | Claude Haiku 4.5 | $5.00 | $1.00 | Fast quality coding |
| 7 | Gemini 2.5 Pro | $10.00 | $1.25 | Complex analysis |
| 8 | Claude Sonnet 4.5 | $15.00 | $3.00 | Daily coding (rate limited) |
| 9 | Claude Opus 4.5 | $25.00 | $5.00 | Best quality (your default) |

*Gemini 2.5 Flash: $0.60 without reasoning, $2.50 with thinking enabled

### Ollama Cloud FREE Models (Rate Limited)

| Model | Size | Best For | Limits |
|-------|------|----------|--------|
| `deepseek-v3.2` | 671B | Reasoning, built-in thinking | Hourly/weekly |
| `kimi-k2:1t` | 1T | Complex tasks | Hourly/weekly |
| `kimi-k2-thinking` | 1T | Deep reasoning | Hourly/weekly |
| `qwen3-coder:480b` | 480B | Coding | Hourly/weekly |
| `mistral-large-3:675b` | 675B | Reasoning | Hourly/weekly |
| `devstral-2:123b` | 123B | Coding | Hourly/weekly |
| `cogito-2.1:671b` | 671B | Reasoning | Hourly/weekly |

---

## Exact Model IDs (For API Calls)

### Claude (Anthropic)
```
claude-opus-4-5-20251101     # Opus 4.5 (YOUR DEFAULT)
claude-sonnet-4-5-20250929   # Sonnet 4.5
claude-haiku-4-5-20251015    # Haiku 4.5

# Aliases (auto-update to latest):
claude-opus-4-5
claude-sonnet-4-5
claude-haiku-4-5
```

### OpenAI
```
gpt-4o              # GPT-4o multimodal
gpt-4o-mini         # Fast and cheap
o1                  # Reasoning model
o1-mini             # Fast reasoning
o3                  # Latest reasoning (expensive)
o3-mini             # Fast o3
```

### Google Gemini
```
gemini-2.5-flash       # Fast, 1M context, cheap
gemini-2.5-pro         # Best quality (quota limits free tier)
gemini-2.5-flash-lite  # Cheapest option
gemini-2.0-flash       # Previous gen
```

### GLM (Z.AI)
```
glm-4.7       # Best multilingual/coding (200K context)
glm-4.6       # Strong tool calling
glm-4.5-air   # Fast and cheap
```

---

## Cost Optimization Strategies

### 1. Match Task to Model

| Task Type | Optimal Model | Why |
|-----------|---------------|-----|
| Quick questions | `glm-4.5-air` / `gemini-2.5-flash-lite` | Cheapest |
| Simple coding | `gpt-4o-mini` / `glm-air` | Fast + cheap |
| Daily coding | `claude-opus-4.5` (subscription) | Included in Max |
| Large context (100K+) | `gemini-2.5-flash` / `glm-4.7` | 1M context, cheap |
| Multilingual code | `glm-4.7` | 66.7% SWE-bench multilingual |
| Tool calling | `glm-4.7` | 84.7 on τ²-Bench |
| Complex reasoning | `claude-opus-4.5` / `o1` | Best quality |
| Code review | `glm-4.7` / `gemini-2.5-flash` | Good + cheap |

### 2. Subscription Value

**Your Claude Code Max subscription saves money:**
- Opus 4.5 at $5/$25 per 1M tokens via API
- With Max subscription: Unlimited (within fair use)
- **Always prefer Claude for general work** - it's "free" for you

**Your GLM Coding Plan ($3/month):**
- Quota-based, resets every 5 hours
- Use for: Large context, multilingual, bulk operations
- Don't waste on simple tasks Claude handles fine

### 3. Context Optimization

| Context Size | Best Model | Notes |
|--------------|------------|-------|
| <50K tokens | Claude Opus 4.5 | Your default |
| 50K-200K | Claude Opus 4.5 or GLM-4.7 | GLM cheaper |
| 200K-1M | Gemini 2.5 Flash | 1M context, cheap |
| >1M tokens | Gemini CLI | Uses your Google account |

### 4. Batch Processing

| Provider | Batch Discount | How |
|----------|----------------|-----|
| Gemini | 50% off | Use batch API endpoint |
| OpenAI | 50% off | Batch API available |
| Claude | Caching | Extended caching reduces costs |

---

## When to Use Each Provider

### Claude (Your Default - Max Subscription)
```
✅ General coding tasks
✅ Planning and architecture
✅ Debugging complex issues
✅ Documentation
✅ Code refactoring
✅ When quality matters most
```

### GLM (Coding Plan - Quota Based)
```
✅ Multilingual codebases
✅ Large file analysis (>100K tokens)
✅ Tool calling / MCP tasks
✅ Bulk code review
✅ When Claude is rate-limited
❌ Don't waste quota on simple tasks
```

### Gemini (Free Tier - Rate Limited)
```
✅ Very large context (up to 1M tokens)
✅ Quick code analysis
✅ Simple questions
✅ When Claude is unavailable
❌ Heavy usage hits quota fast
```

### OpenAI (API Key - Pay Per Use)
```
✅ Specific reasoning tasks (o1, o3)
✅ When you need GPT specifically
✅ Some specialized tool integrations
❌ More expensive than alternatives
```

---

## Thinking Modes (Save Tokens)

### GLM Thinking
```json
// Enable for complex tasks (uses more tokens)
{"thinking": {"type": "enabled", "budget_tokens": 5000}}

// Disable for simple tasks (faster, cheaper)
{"thinking": false}
```

### Gemini Thinking
```
gemini-2.5-flash: $0.60/1M output (no thinking)
gemini-2.5-flash: $2.50/1M output (with thinking)

→ Disable thinking for simple tasks to save 4x on output!
```

---

## Quick Reference Commands

```bash
# Check your current model
claude config get model

# GLM via multi_mcp
"Use multi:chat with glm-4.7 to analyze this file"

# Gemini for large context
"Use multi:chat with gemini-2.5-flash to review this codebase"

# Compare models
"Run multi:compare with opus, glm, gemini on this question"

# Code review (cost-effective)
"Do multi:codereview on src/ with glm-4.7"
```

---

## Sources

- [Claude Pricing](https://platform.claude.com/docs/en/about-claude/models/overview)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [GLM Pricing](https://docs.z.ai/guides/overview/pricing)
- [LLM Pricing Comparison](https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025)
