# GLM 4.7 Thinking Modes

## 1. Interleaved Thinking (Default)

Model reasons before every response and tool call.

```json
{
  "thinking": true
}
```

**Best for:** Most tasks, good balance of speed and quality

## 2. Preserved Thinking (For Complex Tasks)

Retains reasoning blocks across multi-turn conversations.

```json
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```

**Use when:**
- Long-horizon coding
- Complex debugging
- Multi-file refactoring
- Architecture decisions

## 3. Turn-Level Thinking (Hybrid)

Enable/disable per turn to balance speed vs accuracy.

- **Disable** for simple lookups
- **Enable** for complex reasoning

## When to Use Each

| Task Type | Thinking Mode | Budget |
|-----------|---------------|--------|
| Simple question | Disabled | 0 |
| Code generation | Enabled | 5000 |
| Complex debugging | Preserved | 10000 |
| Architecture | Preserved | 15000 |
| Large refactor | Preserved | 20000 |

## Troubleshooting

### GLM Not Responding Well
1. Enable thinking mode for complex tasks
2. Provide more context
3. Use structured prompts (XML tags)
4. Break down into smaller steps

### GLM Making Mistakes
1. Check if thinking is enabled
2. Provide explicit constraints
3. Ask for step-by-step reasoning
4. Consider using Claude for that specific task

### Performance Issues
1. Disable thinking for simple tasks
2. Use GLM 4.6 or GLM Air for speed
3. Reduce max_tokens if not needed
