# Prompt Templates by Model

## Claude (Default)
```
[Just give the task directly - Claude understands context well]
```

## GLM 4.7
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

## Gemini
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

## DeepSeek
```
Think step by step.

[Your question/task]

Show your reasoning.
```

## OpenAI (GPT-4o, o1)
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

## Multi-Model Compare
```python
router_execute(
    mcp_name="multi",
    tool_name="compare",
    arguments={
        "models": ["claude-opus", "gpt-4o", "gemini-flash"],
        "content": "Your question here"
    }
)
```
