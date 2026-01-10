# Model Pricing Reference

## Cost Tiers

| Tier | Models | Cost |
|------|--------|------|
| **FREE** | DeepSeek V3.2, DeepSeek R1, Llama 405B | $0 |
| **Cheapest** | Gemini Flash-Lite | $0.10/$0.40 per M tokens |
| **Included** | Claude Opus 4.5 | Max subscription |
| **Budget** | GLM 4.7 | ~1/7 of Claude |

## FREE Models via Router

```python
# DeepSeek V3.2 (via Ollama Cloud)
router_execute(mcp_name="multi", tool_name="chat",
    arguments={"model": "deepseek-v3.2", "content": "..."})

# DeepSeek R1 (via OpenRouter)
router_execute(mcp_name="multi", tool_name="chat",
    arguments={"model": "deepseek-r1", "content": "..."})

# Llama 405B (via OpenRouter)
router_execute(mcp_name="multi", tool_name="chat",
    arguments={"model": "llama-405b", "content": "..."})
```

## Verified Working APIs

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

## Cost Optimization Strategy

1. **Default to Claude** - It's included in your subscription
2. **Use FREE for bulk** - DeepSeek for repetitive tasks
3. **Use GLM for multilingual** - Better AND cheaper
4. **Use Gemini for large context** - 1M tokens at low cost
