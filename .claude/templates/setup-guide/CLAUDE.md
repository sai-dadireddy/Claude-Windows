# Claude Code Configuration

## Multi-Model Routing

**DEFAULT: Claude Opus 4.5** - Only route when specific advantage exists.

### Quick Routing Table

| Task Type | Model | Command |
|-----------|-------|---------|
| Normal coding | Claude Opus 4.5 | (default) |
| Multilingual/Chinese | GLM 4.7 | `/glm [task]` |
| Large context (>200K) | Gemini 2.5 Flash | `/route gemini [task]` |
| FREE/cheap tasks | DeepSeek | `/route deepseek [task]` |
| Reasoning/Math | DeepSeek R1 | `/route reasoning [task]` |
| Compare approaches | Multi-model | `/ask-models [question]` |
| Images/Video | Gemini or Pixtral | `/route vision [task]` |

### MCP Servers Available

| Server | Purpose | Trigger Keywords |
|--------|---------|------------------|
| `context7` | Library docs | "docs", "api", "react", "how to use" |
| `github` | GitHub ops | "pr", "issue", "commit", "repo" |
| `memory` | Entity graph | "remember", "recall", "entity" |
| `sequential-thinking` | Reasoning | "step by step", "analyze", "break down" |
| `playwright` | Browser | "screenshot", "scrape", "navigate" |

## Memory System

### Auto-Save Triggers
- **Decision**: "decided", "chose", "let's use", "going with"
- **Preference**: "I prefer", "I like", "always use"
- **Learning**: "realized", "discovered", "the trick is"

### Manual Save
```bash
~/.claude/scripts/memory_manager.py save-memory PROJECT TYPE "content"
```

## Complex Task Tracking (Beads)

Use Beads (`bd` CLI) for tasks with:
- Multiple steps
- Dependencies between tasks
- Multi-session work

```bash
bd init                           # Initialize in project
bd create "Task" -t feature -p 1  # Create issue
bd ready                          # Show ready tasks
bd close <id> --reason "Done"     # Complete task
```

## Hooks Active

- `intent_detector.py` - Auto-suggests MCP/model based on prompt
- `auto_capture_memory.py` - Saves observations from tool usage
- `skill_reminder.py` - Suggests relevant skills

## Rules

1. **RAG-First**: Query memory/docs before reading files
2. **Verify**: Always run tests after changes
3. **No Lies**: If unsure, say "I don't know"
4. **Save Decisions**: When user chooses something, save to memory
