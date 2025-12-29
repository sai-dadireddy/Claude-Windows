# Skills Guide - Detailed Documentation

## Development Skills (superpowers/)
Location: `~/.config/claude-code/skills/superpowers/`

### Slash Commands
- `/superpowers:brainstorm` - Socratic design refinement
- `/superpowers:write-plan` - Granular task breakdown (2-5 min tasks)
- `/superpowers:execute-plan` - Autonomous execution

### Key Skills

| Skill | When to Use | Key Points |
|-------|-------------|------------|
| `systematic-debugging` | Any bug, error, unexpected behavior | Reproduce -> Isolate -> Identify -> Fix -> Verify |
| `test-driven-development` | Writing new code, adding features | RED (fail) -> GREEN (pass) -> REFACTOR |
| `root-cause-tracing` | Complex bugs, cascading errors | Trace to origin, don't just fix symptoms |
| `defense-in-depth` | Security-sensitive code | Multiple validation layers |
| `using-git-worktrees` | Parallel branch work | Multiple branches simultaneously |
| `requesting-code-review` | Before PR/merge | Quality gates, plan alignment |

## Meta Skills (taches-cc-resources/)
Location: `~/.config/claude-code/skills/taches-cc-resources/`

| Command | When to Use | Output |
|---------|-------------|--------|
| `/create-plan` | Starting new feature | Spec-driven development plan |
| `/create-meta-prompt` | Complex multi-step task | Chain of prompts |
| `/create-agent-skill` | Need new capability | New skill definition |
| `/debug` | Expert debugging needed | Structured debug workflow |
| `/whats-next` | Stuck or unsure | Suggested next action |

## Document Skills (Plugins)
Enabled via `document-skills@anthropic-agent-skills`

Invoke with Skill tool: `skill: "docx"`, `skill: "pdf"`, etc.

| Skill | File Type | Key Operations |
|-------|-----------|----------------|
| `docx` | Word (.docx) | Create, edit, format documents |
| `pdf` | PDF (.pdf) | Create, merge, extract |
| `pptx` | PowerPoint (.pptx) | Create presentations, add slides |
| `xlsx` | Excel (.xlsx) | Create spreadsheets, formulas |

## Skill Seekers (Documentation -> Skills)
Location: `~/.config/claude-code/skills/Skill_Seekers/`

Converts documentation into Claude Skills.

**When to Use:**
- Working with unfamiliar framework -> Convert its docs to skill
- Internal/custom tools with docs -> Create company-specific skill
- API documentation integration -> Make API skill

## Tapestry (Knowledge Management)
Location: `~/.config/claude-code/skills/tapestry/`

| Skill | Purpose |
|-------|---------|
| `tapestry` | Create knowledge graphs from documents |
| `article-extractor` | Extract web article content |
| `youtube-transcript` | Get YouTube video transcripts |

## How Skills Work

1. **Auto-Detection**: `skill_reminder.py` hook detects task types
2. **Reminder Injection**: Adds `<skill-reminder>` context
3. **Manual Invocation**: Use Skill tool for document skills

## Critical Rules

1. **Debugging**: ALWAYS use systematic-debugging, don't guess fixes
2. **Tests**: ALWAYS use test-driven-development, don't skip tests
3. **Documents**: Use document skills, don't try to generate raw XML
4. **Planning**: For complex features, plan first with write-plan
5. **Code Review**: Use requesting-code-review before PRs
