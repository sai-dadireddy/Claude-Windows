Intelligently route a task to the optimal AI model based on the request.

## How It Works

Analyze the task and automatically select the best model:

| Task Pattern | Routes To | Why |
|--------------|-----------|-----|
| Multilingual code | GLM 4.7 | 66.7% SWE-bench multilingual |
| Large context (>200K) | Gemini 2.5 Flash | 1M token context |
| FREE/cheap/budget | DeepSeek V3.2 | $0 via Ollama |
| Reasoning/math | DeepSeek R1 | FREE chain-of-thought |
| Compare approaches | multi:compare | Multiple model consensus |
| Images/video | Gemini or Pixtral | Multimodal |
| Default | Claude Opus 4.5 | Best overall (your sub) |

## Examples

```bash
# Auto-route based on task
/route Review this 500K token codebase
→ Routes to Gemini (large context)

/route Debug this Chinese error message
→ Routes to GLM 4.7 (multilingual)

/route What's the cheapest way to analyze this?
→ Routes to DeepSeek (FREE)

/route Compare architectures for this feature
→ Uses multi:compare with 3 models
```

## Force Specific Model

Add model name to force routing:
```
/route glm: [task]     → Forces GLM 4.7
/route gemini: [task]  → Forces Gemini
/route deepseek: [task] → Forces DeepSeek
/route gpt: [task]      → Forces GPT-4o
/route compare: [task]  → Forces multi:compare
```

---

**Analyze and route the following task:**

$ARGUMENTS
