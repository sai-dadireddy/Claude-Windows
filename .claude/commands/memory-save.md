# Memory Save

Save information to long-term memory.

## Usage
`/memory-save <type> <content>`

## Memory Types

- **decision** - Architecture or design decisions (why we chose X over Y)
- **learning** - Lessons learned, what worked or didn't
- **context** - Project-specific context and background
- **preference** - User preferences and coding style
- **architecture** - System architecture and patterns
- **bug** - Bugs encountered and how they were fixed
- **todo** - Things to remember for later

## Instructions

Parse the arguments: $ARGUMENTS

The format should be: `<type> <content>`

Example: `decision Chose SQLite over PostgreSQL for simplicity and zero-config`

Run:
```bash
~/.claude/scripts/memory_manager.py save-memory "$(basename $PWD)" "<type>" "<content>"
```

For global memories (not project-specific), use "global" as the project name.

Confirm to the user what was saved and where.
