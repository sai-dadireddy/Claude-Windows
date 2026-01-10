# Model Decision Matrix

## By Task Type

### Coding Tasks
| Scenario | Best Model | Why |
|----------|------------|-----|
| General coding | Claude Opus 4.5 | 77.2% SWE-bench, YOUR DEFAULT |
| Multilingual code | GLM 4.7 | 66.7% SWE-bench multilingual |
| Code generation | Codestral | Specialist for code |
| Large codebase | Gemini 2.5 Flash | 1M context |
| Budget coding | DeepSeek V3.2 | FREE, 73%+ accuracy |

### Reasoning Tasks
| Scenario | Best Model | Why |
|----------|------------|-----|
| Complex reasoning | Claude Opus 4.5 | Best overall |
| Math proofs | DeepSeek R1 | FREE, built-in CoT |
| Scientific | DeepSeek R1 | Strong on scientific |
| Step-by-step | o1 | Dedicated reasoning |

### Context Size
| Tokens Needed | Best Model | Context Limit |
|---------------|------------|---------------|
| < 100K | Claude Opus 4.5 | 200K |
| 100K - 200K | GLM 4.7 | 200K |
| 200K - 1M | Gemini 2.5 Flash | 1M |
| > 1M | Gemini CLI | 2M+ |

### Multimodal
| Media Type | Best Model | Why |
|------------|------------|-----|
| Images | Gemini 2.5 | Native multimodal |
| Vision+Text | Pixtral Large | Mistral vision |
| Video | Gemini 3 | Video understanding |
| Code screenshots | Claude Opus 4.5 | Good vision |

### Speed
| Need | Best Model | Latency |
|------|------------|---------|
| Fastest | Claude Haiku | ~0.5s |
| Fast + FREE | GLM Air | ~1s |

## Routing Rules

### STAY with Claude Opus 4.5 When:
- Normal coding tasks
- Writing/refactoring code
- Debugging
- Code review
- Tool use / MCP operations
- Planning and architecture
- Documentation
- User doesn't specify otherwise

### ROUTE to GLM 4.7 When:
- User mentions "multilingual", "Chinese", "Japanese", "Korean"
- Large context 100K-200K tokens
- Tool calling benchmarks/tests
- User says "use GLM" or "/glm"

### ROUTE to Gemini When:
- Context > 200K tokens
- User says "analyze entire codebase/repo"
- Multimodal (images, video)
- User says "use gemini"

### ROUTE to DeepSeek When:
- User says "cheap", "free", "budget"
- Need reasoning with chain-of-thought visible
- Scientific/math tasks
- User says "use deepseek" or "use r1"

### USE multi:compare When:
- Architecture decisions
- "What's the best approach?"
- Need consensus from multiple models
- Security review
