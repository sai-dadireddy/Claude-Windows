---
name: glm-orchestration
description: Use GLM 4.7 for multilingual code, large context, and tool calling tasks
context: fork
user-invocable: true
triggers:
  - "use glm"
  - "multilingual code"
  - "chinese"
  - "large context"
---

# GLM Orchestration

Use GLM 4.7 when you need:
- **Multilingual code** (66.7% SWE-bench multilingual - best in class)
- **Large context** (100K-200K tokens)
- **Tool calling** (84.7 τ²-Bench - beats Claude Sonnet)
- **Cost savings** (1/7 price of Claude)

## Quick Reference

| Scenario | Use GLM? | Why |
|----------|----------|-----|
| Multilingual/Chinese code | ✅ YES | Best multilingual performance |
| Context 100K-200K | ✅ YES | Handles large context well |
| Tool calling heavy | ✅ YES | 84.7 τ²-Bench score |
| Budget constraints | ✅ YES | 1/7 price, 3x quota |
| General coding | ❌ NO | Use Claude Opus (default) |

## How to Use

```python
router_execute(
  mcp_name="multi",
  tool_name="chat",
  arguments={"model": "glm-4.7", "content": "Your prompt"}
)
```

## Learn More

- **API Reference**: See `docs/api-reference.md`
- **Prompt Templates**: See `docs/prompting.md`
- **Thinking Modes**: See `docs/thinking-modes.md`
- **Scripts**: See `scripts/glm-query.py`
