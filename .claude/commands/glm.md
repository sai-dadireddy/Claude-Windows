Query **GLM 4.7** for coding tasks, multilingual code, or large context analysis.

## When to Use This Command

- Multilingual codebase work
- Large file/context analysis (>100K tokens)
- Cost-effective bulk operations
- Complex multi-step coding with thinking mode
- Tool calling / MCP integration tasks

## How It Works

1. Formats your query with optimal GLM prompting
2. Enables thinking mode for complex tasks
3. Calls GLM 4.7 via Z.AI Anthropic-compatible API
4. Returns response with reasoning (if enabled)

## Examples

```bash
# Code generation
/glm Implement a Redis cache wrapper in Python with TTL support

# Code review
/glm Review this file for security issues: @src/auth/login.ts

# Large context
/glm Analyze this codebase structure and suggest improvements

# Multilingual
/glm Fix the Unicode handling in this Go function
```

## Options

Add these keywords to modify behavior:

| Keyword | Effect |
|---------|--------|
| `fast` | Use GLM Air (faster, cheaper) |
| `no-think` | Disable thinking mode |
| `compare` | Also get Claude's answer |

## API Details

- **Endpoint:** `https://api.z.ai/api/anthropic`
- **Model:** glm-4.7 (default), glm-4.6, glm-air
- **Thinking:** Enabled by default for complex tasks

---

**Process the following with GLM 4.7:**

$ARGUMENTS
