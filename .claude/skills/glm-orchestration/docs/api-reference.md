# GLM API Reference

## Endpoints

### Anthropic-Compatible (For Claude Code Integration)
```bash
curl "https://api.z.ai/api/anthropic/v1/messages" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.7",
    "max_tokens": 4096,
    "thinking": {"type": "enabled", "budget_tokens": 5000},
    "messages": [{"role": "user", "content": "Your prompt here"}]
  }'
```

### Native OpenAI-Compatible
```bash
curl "https://api.z.ai/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.7",
    "max_tokens": 4096,
    "stream": true,
    "messages": [{"role": "user", "content": "Your prompt here"}]
  }'
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | `glm-4.7`, `glm-4.6`, `glm-4.5-air` |
| `max_tokens` | int | Up to 128K |
| `temperature` | float | 0.0-1.0 (default: 1.0 for thinking) |
| `stream` | bool | Enable streaming responses |
| `thinking` | object | `{"type": "enabled", "budget_tokens": N}` |
| `tools` | array | Function calling definitions |
| `tool_choice` | string | `auto`, `required`, or specific tool |

## Model Specifications

| Spec | GLM 4.7 |
|------|---------|
| **Context Length** | 200K tokens |
| **Max Output** | 128K tokens |
| **SWE-bench** | 73.8% (best open-source) |
| **SWE-bench Multilingual** | 66.7% (+12.9% vs 4.6) |
| **LiveCodeBench V6** | 84.9 SOTA |
| **Tool Calling (τ²-Bench)** | 84.7 |
| **Pricing** | ~1/7 of Claude |

## SDK Installation

```bash
# Python SDK
pip install zai-sdk

# Or use OpenAI-compatible client
pip install openai
```

```python
# Using zai-sdk
from zai import ZAI
client = ZAI(api_key="your-key")
response = client.chat.completions.create(
    model="glm-4.7",
    messages=[{"role": "user", "content": "Hello"}]
)

# Using OpenAI client
from openai import OpenAI
client = OpenAI(
    api_key="your-key",
    base_url="https://api.z.ai/api/paas/v4"
)
```

## Tool Calling Example

```json
{
  "model": "glm-4.7",
  "messages": [{"role": "user", "content": "What's the weather in Tokyo?"}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Get current weather for a location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "City name"},
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
        },
        "required": ["location"]
      }
    }
  }],
  "tool_choice": "auto"
}
```
