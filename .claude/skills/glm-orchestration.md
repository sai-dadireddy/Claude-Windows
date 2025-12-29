# GLM Orchestration Skill

Use this skill when working with GLM models (4.7, 4.6) for multi-model AI orchestration.

## Model Specifications

| Spec | GLM 4.7 |
|------|---------|
| **Context Length** | 200K tokens |
| **Max Output** | 128K tokens |
| **SWE-bench** | 73.8% (best open-source) |
| **SWE-bench Multilingual** | 66.7% (+12.9% vs 4.6) |
| **LiveCodeBench V6** | 84.9 SOTA (beats Claude Sonnet 4.5) |
| **Tool Calling (τ²-Bench)** | 84.7 (beats Claude Sonnet 4.5) |
| **Pricing** | ~1/7 of Claude, 3x quota |

## When to Use GLM

### ALWAYS Use GLM 4.7 For:
- **Multilingual code** - 66.7% SWE-bench multilingual (best in class)
- **Large context analysis** - Handles 100K+ tokens efficiently
- **Tool calling tasks** - 84.7 on τ²-Bench, surpasses Claude Sonnet
- **Complex multi-step coding** - 73.8% SWE-bench verified
- **Cost-sensitive tasks** - 1/7 price of Claude with 3x quota
- **Web browsing tasks** - 67 points on BrowseComp

### Use GLM 4.6 For:
- **MCP integration** - Strong tool calling support
- **Faster responses** - When GLM 4.7 thinking overhead not needed
- **Simpler coding tasks** - Good balance of speed and quality

### Stay with Claude Opus For:
- **General coding** - Still best overall
- **Creative writing** - Better natural language
- **Your default workflow** - No need to route simple tasks

## GLM 4.7 Thinking Modes

### 1. Interleaved Thinking (Default)
Model reasons before every response and tool call.
```json
{
  "thinking": true
}
```

### 2. Preserved Thinking (For Complex Tasks)
Retains reasoning blocks across multi-turn conversations.
```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```
**Use when:** Long-horizon coding, complex debugging, multi-file refactoring

### 3. Turn-Level Thinking (Hybrid)
Enable/disable per turn to balance speed vs accuracy.
- Disable for simple lookups
- Enable for complex reasoning

## API Endpoints

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

## API Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | `glm-4.7`, `glm-4.6`, `glm-4.5-air` |
| `max_tokens` | int | Up to 128K |
| `temperature` | float | 0.0-1.0 (default: 1.0 for thinking) |
| `stream` | bool | Enable streaming responses |
| `thinking` | object | `{"type": "enabled", "budget_tokens": N}` |
| `tools` | array | Function calling definitions |
| `tool_choice` | string | `auto`, `required`, or specific tool |

## Prompting Best Practices

### DO:
1. **Frame as task completion** - "Implement X" not "Show me how to X"
2. **Be specific about requirements** - Include constraints, edge cases
3. **Use structured formats** - XML tags, markdown sections
4. **Enable thinking for complex tasks** - Worth the extra tokens
5. **Provide context upfront** - File contents, error messages, expected behavior

### DON'T:
1. **Don't use for simple questions** - Use Claude instead
2. **Don't disable thinking for complex coding** - Quality drops
3. **Don't expect identical behavior to Claude** - Different model, different strengths

## Effective Prompt Templates

### For Code Generation:
```xml
<task>
Implement [feature] with the following requirements:
</task>

<requirements>
- [Requirement 1]
- [Requirement 2]
</requirements>

<constraints>
- Language: [Python/TypeScript/etc]
- Must handle: [edge cases]
- Do not: [restrictions]
</constraints>

<context>
[Relevant code or file contents]
</context>
```

### For Code Review:
```xml
<task>Review this code for security, performance, and best practices</task>

<code language="python">
[code here]
</code>

<focus>
- Security vulnerabilities (OWASP Top 10)
- Performance bottlenecks
- Error handling
</focus>
```

### For Debugging:
```xml
<task>Debug this error</task>

<error>
[Error message]
</error>

<code>
[Relevant code]
</code>

<context>
- What was expected: [expected behavior]
- What happened: [actual behavior]
- Already tried: [attempted fixes]
</context>
```

### For Architecture:
```xml
<task>Design [system/feature]</task>

<requirements>
[What it needs to do]
</requirements>

<constraints>
- Scale: [expected load]
- Stack: [technologies available]
- Budget: [if relevant]
</constraints>

<output>
Provide:
1. High-level architecture
2. Component breakdown
3. Data flow diagram (ASCII)
4. Key implementation decisions
</output>
```

## Multi-Model Workflow

### Compare Approaches:
```
1. Ask Claude Opus for architecture design
2. Ask GLM 4.7 for implementation with thinking mode
3. Ask Claude to review GLM's implementation
4. Iterate based on feedback
```

### Parallel Analysis:
```
1. Use multi:compare to get both Claude and GLM perspectives
2. Synthesize insights from both
3. Make informed decision
```

### Cost Optimization:
```
1. Use GLM for bulk operations (cheaper)
2. Use Claude for critical decisions (better quality)
3. Use GLM Air for fast, simple tasks
```

## Token/Cost Comparison

| Task | Claude Opus | GLM 4.7 | Recommendation |
|------|-------------|---------|----------------|
| Simple question | $$$ | $ | GLM or Claude Haiku |
| Code generation | $$$ | $ | GLM 4.7 with thinking |
| Code review | $$$ | $ | GLM 4.7 |
| Architecture | $$$ | $ | Claude (quality) or GLM (budget) |
| Large file analysis | $$$ | $ | GLM (better context handling) |

## Integration Commands

### Via MCP:
```
"Use multi:chat with glm-4.7 to [task]"
"Ask GLM 4.7 with thinking mode: [question]"
```

### Via Slash Command:
```
/ask-models [question] - Routes to appropriate model
```

### Direct Invocation:
```
"Route this to GLM 4.7: [task]"
"Get GLM's perspective on [topic]"
```

## Troubleshooting

### GLM Not Responding Well:
1. Enable thinking mode for complex tasks
2. Provide more context
3. Use structured prompts (XML tags)
4. Break down into smaller steps

### GLM Making Mistakes:
1. Check if thinking is enabled
2. Provide explicit constraints
3. Ask for step-by-step reasoning
4. Consider using Claude for that specific task

### Performance Issues:
1. Disable thinking for simple tasks
2. Use GLM 4.6 or GLM Air for speed
3. Reduce max_tokens if not needed

## Tool Calling Example

GLM 4.7 excels at tool calling (84.7 on τ²-Bench). Example:

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

## When GLM Beats Claude

| Task | GLM 4.7 | Claude Sonnet 4.5 | Winner |
|------|---------|-------------------|--------|
| LiveCodeBench V6 | 84.9 | Lower | **GLM** |
| Tool Calling (τ²-Bench) | 84.7 | Lower | **GLM** |
| SWE-bench Multilingual | 66.7% | N/A | **GLM** |
| 200K Context | ✅ Native | ✅ Native | Tie |
| Cost | 1/7 price | Full price | **GLM** |

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

---

**Remember:** GLM is a tool in your toolkit, not a replacement for Claude. Use each model for what it does best.

**Quick Reference:**
- GLM for: Multilingual, large context, tool calling, cost savings
- Claude for: General coding, creative tasks, your default workflow
