# Memory System - Detailed Guide

## How It Works

### Automatic (No action needed)
- Observations captured from tool usage (files, commands)
- Memories loaded at session start (progressive disclosure)
- Memory search triggered on "what did we...", "how did we..."
- Bug fixes tracked (error -> fix sequences)

### Manual (When YOU must act)
- User makes a DECISION -> Save immediately!
- User states a PREFERENCE -> Save immediately!
- Session ending -> Save session state!
- Important learning discovered -> Save it!

## Memory Types

| Type | When to Use | Examples |
|------|-------------|----------|
| `decision` | Technology choices, architecture decisions | "Using Redis for caching", "Chose monorepo structure" |
| `preference` | User likes/dislikes, coding style | "Prefers functional style", "Wants detailed comments" |
| `learning` | Patterns discovered, things that worked | "This API needs retry logic", "Tests must run in order" |
| `bug` | Bugs fixed, error solutions | "CORS error: needed credentials:true", "Memory leak in useEffect" |
| `architecture` | System structure, component relationships | "Auth flow: JWT -> Redis -> DB" |
| `context` | Current work, file purposes | "Working on payment integration" |

## Commands

### Save Memory
```bash
~/.claude/scripts/memory_manager.py save-memory PROJECT TYPE "content"
```

### Load/Search Memories
```bash
~/.claude/scripts/memory_manager.py load-memories PROJECT "search query"
~/.claude/scripts/semantic_memory.py search PROJECT "search query"
```

### Session Management
```bash
# Save session
~/.claude/scripts/memory_manager.py save-session "SESSION_ID" "PROJECT" "content"

# Load previous session
~/.claude/scripts/memory_manager.py load-session "last" "PROJECT"

# List sessions
~/.claude/scripts/memory_manager.py list-sessions "PROJECT"
```

## Memory Locations

```
~/.claude/memory/
├── semantic.db          # SQLite with embeddings
├── short-term/          # Session files
└── long-term/           # Persistent memories
    ├── global/          # Cross-project
    └── projectname/     # Project-specific
```

## Example Saves

```bash
# User chose a framework
~/.claude/scripts/memory_manager.py save-memory myproject decision "Chose Next.js 14 with App Router for SSR and SEO"

# User preference
~/.claude/scripts/memory_manager.py save-memory global preference "User prefers explicit error handling"

# Bug fixed
~/.claude/scripts/memory_manager.py save-memory myproject bug "Fixed undefined error - was accessing user.profile before null check"

# Session ending
~/.claude/scripts/memory_manager.py save-session "abc123" "myproject" "Completed auth module. Next: password reset"
```

## Critical Rules

1. **ALWAYS save user decisions** - "let's use X" or "I prefer Y" -> SAVE IT
2. **ALWAYS save preferences** - like/dislike -> SAVE IT
3. **Search before answering** - "what did we..." -> search memories FIRST
4. **Session save on goodbye** - "done", "bye", "stopping" -> save session
5. **Bug fixes are gold** - tricky bug fixed -> SAVE the solution
