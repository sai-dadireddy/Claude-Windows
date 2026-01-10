---
name: model-routing
description: Route tasks to the optimal AI model based on requirements
user-invocable: true
triggers:
  - "route to"
  - "which model"
  - "use gemini"
  - "use deepseek"
  - "compare models"
---

# Model Routing Brain

Route tasks to the optimal model. **Default: Claude Opus 4.5** (your subscription).

## Quick Decision Tree

```
Is it multilingual code?     → GLM 4.7
Is context > 200K tokens?    → Gemini 2.5 Flash
Need it FREE?                → DeepSeek V3.2 or R1
Need model comparison?       → multi:compare
Otherwise?                   → Claude Opus (default)
```

## Routing Cheatsheet

| Scenario | Model | Command |
|----------|-------|---------|
| **Default** | Claude Opus 4.5 | Just ask |
| **Multilingual** | GLM 4.7 | `router_execute(..., model="glm-4.7")` |
| **Large context** | Gemini 2.5 Flash | `router_execute(..., model="gemini-2.5-flash")` |
| **FREE/Budget** | DeepSeek V3.2 | `router_execute(..., model="deepseek-v3.2")` |
| **Reasoning** | DeepSeek R1 | `router_execute(..., model="deepseek-r1")` |
| **Compare** | Multiple | `router_execute(tool_name="compare", ...)` |

## Learn More

- **Full Decision Matrix**: See `docs/decision-matrix.md`
- **Prompt Templates by Model**: See `docs/prompt-templates.md`
- **Cost Comparison**: See `docs/pricing.md`
