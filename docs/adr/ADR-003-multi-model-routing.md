# ADR-003: Multi-Model Routing Strategy

## Status

**Accepted** - January 2025

## Context

Sherpa v4.0 used Claude Opus 4.5 for all tasks, which was:
- Expensive for simple operations
- Overkill for scaffolding and boilerplate
- Slower than necessary for parallel workloads
- Limited to single-model perspective

Different tasks have different requirements:

| Task Type | Requirements | Optimal Model |
|-----------|--------------|---------------|
| Architecture decisions | Deep reasoning, nuance | High-capability |
| Code generation | Speed, volume | Fast, capable |
| Boilerplate/scaffolding | Speed, low cost | Fast, cheap |
| Documentation | Accuracy, clarity | Balanced |
| Multi-perspective review | Diversity | Multiple models |

## Decision

Implement a three-tier model routing strategy with role-based assignments:

### Tier 1: Brain (Claude Opus 4.5)
**Role**: Chief Architect, critical decisions

**Used for**:
- Architecture decisions
- Security reviews
- Complex debugging
- User-facing responses
- Final approval/oversight

**Characteristics**: Highest capability, highest cost, slower

### Tier 2: Muscle (DeepSeek V3, Gemini 2.5 Flash)
**Role**: Heavy lifting, parallel execution

**Used for**:
- Code generation
- Refactoring
- Test writing
- Documentation generation
- Parallel agent tasks

**Characteristics**: Fast, capable, cost-effective, high throughput

### Tier 3: Intern (Amazon Nova, Haiku)
**Role**: Simple tasks, scaffolding

**Used for**:
- Boilerplate generation
- File scaffolding
- Simple transformations
- Bulk operations
- Background indexing

**Characteristics**: Very fast, very cheap, limited reasoning

## Routing Logic

```
User Request
     |
     v
+--------------------+
| Intent Analysis    |
| (by Opus)          |
+--------------------+
     |
     v
+--------------------+
| Complexity Score   |
| - Reasoning depth  |
| - Security impact  |
| - Novelty          |
+--------------------+
     |
     +---> High (>7): Opus (Brain)
     |
     +---> Medium (4-7): DeepSeek/Gemini (Muscle)
     |
     +---> Low (<4): Nova/Haiku (Intern)
```

### Explicit Routing

Users can override automatic routing:

```bash
# Force specific model via router
router_execute(mcp_name="multi", tool_name="chat",
  arguments={"model": "deepseek-v3.2", "content": "..."})

# Compare multiple models
router_execute(mcp_name="multi", tool_name="compare",
  arguments={"models": ["gpt-4o", "gemini-flash"], "content": "..."})

# Code review with specific model
router_execute(mcp_name="multi", tool_name="codereview",
  arguments={"content": "...", "base_path": "/path"})
```

### Agent-Model Mapping

| Agent | Default Model | Rationale |
|-------|---------------|-----------|
| @lead-architect | Opus | Critical decisions |
| @fullstack-dev | DeepSeek | Volume coding |
| @frontend-ux | Gemini Flash | Fast iteration |
| @product-lead | Opus | User-facing specs |
| @qa-engineer | DeepSeek | Test generation |
| @scribe | Gemini Flash | Documentation |

## Model Inventory

Access to 58 models via the multi-model router:

### Primary Models
| Model | Tier | Context | Cost | Speed |
|-------|------|---------|------|-------|
| Claude Opus 4.5 | Brain | 200K | $$$ | Slow |
| DeepSeek V3.2 | Muscle | 128K | FREE | Fast |
| Gemini 2.5 Flash | Muscle | 1M | $ | Fast |
| Amazon Nova | Intern | 128K | $ | Fast |
| Claude Haiku | Intern | 200K | $ | Fast |

### Specialty Models
| Model | Use Case |
|-------|----------|
| GLM 4.7 | Chinese/multilingual |
| Kimi K2 | Long context (FREE) |
| GPT-4o | Alternative perspective |
| Gemini 2.5 Pro | Complex reasoning |

## Consequences

### Positive

- **70% cost reduction**: Most tasks use cheaper models
- **3x throughput**: Parallel execution with fast models
- **Quality where needed**: Opus for critical decisions
- **Diverse perspectives**: Multi-model comparison available
- **Flexibility**: Override routing when needed

### Negative

- **Routing overhead**: Intent analysis adds latency
- **Quality variance**: Cheaper models may miss nuance
- **Complexity**: Multiple model APIs to maintain
- **Consistency**: Different models have different styles

### Mitigations

- Cache routing decisions for similar requests
- Opus reviews Muscle/Intern output for critical paths
- Standardized prompts reduce style variance
- Fallback to Opus on uncertainty

## Implementation Notes

### Router Configuration

```python
MODEL_TIERS = {
    "brain": ["claude-opus-4-5-20251101"],
    "muscle": ["deepseek-v3.2", "gemini-2.5-flash", "gpt-4o"],
    "intern": ["amazon-nova-lite", "claude-3-5-haiku"]
}

TASK_ROUTING = {
    "architecture": "brain",
    "security": "brain",
    "code_generation": "muscle",
    "refactoring": "muscle",
    "scaffolding": "intern",
    "documentation": "muscle"
}
```

### Cost Comparison (1M tokens)

| Model | Input Cost | Output Cost |
|-------|------------|-------------|
| Opus 4.5 | $15.00 | $75.00 |
| DeepSeek V3 | FREE | FREE |
| Gemini Flash | $0.075 | $0.30 |
| Nova Lite | $0.06 | $0.24 |

## References

- CLAUDE.md Section: "MODEL ROUTING (58 models via router)"
- Multi-model MCP: `router_execute(mcp_name="multi", ...)`
- Agent definitions: Sherpa 6 configuration
