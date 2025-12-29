Query multiple AI models and compare their responses for better decisions.

## Usage

```
/ask-models [question or task]
```

## What This Does

1. **Analyzes your question** to determine optimal models
2. **Routes to appropriate models** based on task type
3. **Returns comparison** of responses when beneficial

## Model Selection Logic

| Task Pattern | Models Used |
|--------------|-------------|
| Architecture/Design | opus, codex, glm-4.7 |
| Code Review | glm-4.7, gemini, sonnet |
| Security Analysis | opus, glm-4.7 (debate mode) |
| Large Codebase | glm-4.7, gemini (big context) |
| Quick Question | haiku, glm-air (fast) |
| Algorithm Design | codex, opus |
| General Coding | opus (your default) |

## Examples

```bash
# Architecture decision - gets consensus
/ask-models Should we use microservices or monolith for this project?

# Code review - multi-model analysis
/ask-models Review src/auth/ for security issues

# Quick question - fast model
/ask-models What's the syntax for async/await in Python?

# Compare approaches
/ask-models Compare Redux vs Zustand for state management
```

## MCP Tools Used

- `multi:chat` - Single model query
- `multi:compare` - Parallel multi-model comparison
- `multi:debate` - Models critique each other
- `multi:codereview` - Automated code review

## Configured Models

| Provider | Models | Status |
|----------|--------|--------|
| Claude | opus (default), sonnet, haiku | ✅ Ready (Max sub) |
| GLM/Z.AI | glm-4.7, glm-4.6 | ✅ Ready (Coding Plan) |
| Gemini | gemini-2.5-flash | ✅ Ready (free tier) |
| OpenAI | codex, gpt-5.x | ⏳ Need key |

---

**Analyze the following and route to appropriate model(s):**

$ARGUMENTS
