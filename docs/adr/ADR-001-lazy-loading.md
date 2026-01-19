# ADR-001: Lazy Loading for Agents and Skills

## Status

**Accepted** - January 2025

## Context

Sherpa v4.0 loaded all agent configurations and skill definitions at session start, consuming approximately 15,000-20,000 tokens before any user interaction. With 6 specialized agents (Sherpa 6) and 24+ skill configurations, the context window filled rapidly, leaving limited space for actual work.

Key problems observed:
- Session start consumed 15-20K tokens (context pollution)
- Users rarely needed all agents in a single session
- Skills loaded even when not relevant to the task
- Context compaction triggered prematurely
- Cost per session was unnecessarily high

Token breakdown (v4.0 eager loading):
- Agent definitions: ~8,000 tokens
- Skill configurations: ~6,000 tokens
- MCP tool schemas: ~60,000 tokens
- Total overhead: ~74,000 tokens

## Decision

Implement lazy loading for all agents, skills, and MCP tools:

1. **Agent Loading**: Load agent definitions only when explicitly invoked via `@agent-name` or when task delegation occurs.

2. **Skill Loading**: Skills are loaded on-demand when:
   - User invokes `/skill-name` command
   - Hint system detects `[skill]` tag in `~/.claude/hints/current.txt`
   - Task type matches skill trigger patterns

3. **MCP Router**: Replace direct MCP connections with a router proxy that exposes only 4 lightweight tools (~2,400 tokens):
   - `router_analyze_intent` - Find appropriate MCP
   - `router_list_categories` - Show available backends
   - `router_load_toolset` - Get tool schemas on demand
   - `router_execute` - Execute tool on backend

4. **Progressive Disclosure**: At session start, load only:
   - Core CLAUDE.md instructions (~300 tokens)
   - Memory system hooks
   - Router stub tools

## Consequences

### Positive

- **97% token savings**: From ~74K to ~2.4K at session start
- **Faster session initialization**: Sub-second startup
- **Extended working context**: More room for actual code and conversation
- **Reduced costs**: Fewer tokens per session
- **Selective loading**: Only pay for what you use

### Negative

- **First-use latency**: ~500ms delay when loading an agent/skill for the first time
- **Discovery friction**: Users must know agent/skill names or use list commands
- **Router overhead**: Extra hop for MCP calls (minimal impact)

### Mitigations

- Hint system pre-loads likely-needed skills based on project context
- Tab completion for agent/skill names
- `router_list_categories` provides discoverability
- Frequently-used tools cached in router

## Implementation Notes

```
Session Start (v4.1):
+-----------------------+
| CLAUDE.md (~300 tok)  |
| Router tools (2.4K)   |
| Memory hooks          |
+-----------------------+
Total: ~2,700 tokens

On-Demand Loading:
@fullstack-dev -> +1,200 tokens (agent def)
/workday       -> +800 tokens (skill)
router_execute -> +0 tokens (already loaded)
```

## References

- CLAUDE.md Section: "MCP ROUTER (Lazy Loading)"
- Memory system: `~/.claude/scripts/memory_manager.py`
- Router implementation: MCP router proxy
