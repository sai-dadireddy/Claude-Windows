# Claude Canvas

Windows-native TUI & Electron toolkit for Claude Code - spawn interactive terminal interfaces for emails, calendars, tables, and more.

## Features

- **TUI Mode**: Terminal-based UI using ink/React (requires split pane)
- **Electron Mode**: Always-on-top popup windows (WIP - path issues with OneDrive)
- **Two-way communication**: WebSocket sync between Claude and canvas
- **Multiple canvas types**: email, calendar, table, todo, json

## Quick Start

```bash
cd "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/claude-canvas"
npm install

# List available canvas types
npm run canvas -- list

# Spawn a todo canvas (in split terminal pane)
npm run canvas -- spawn todo --data '{"items":[{"text":"Task 1","done":false}]}'

# Spawn an email canvas
npm run canvas -- spawn email --data '{"to":"user@example.com","subject":"Hello"}'
```

## Canvas Types

| Type | Description | Use Case |
|------|-------------|----------|
| `email` | Email composer | Drafting emails |
| `calendar` | Interactive calendar | Scheduling |
| `table` | Data table with sorting | Data display |
| `todo` | Interactive checklist | Task tracking |
| `json` | JSON explorer | Data inspection |

## Keyboard Controls

- **Esc**: Close canvas
- **Arrow keys**: Navigate
- **Space/Enter**: Select/toggle
- **Tab**: Next field (forms)
- **a**: Add item (todo)
- **d**: Delete item (todo)
- **1/2/3**: Set priority (todo)

## Architecture

```
claude-canvas/
├── src/
│   ├── cli.ts              # CLI entry point
│   ├── index.ts            # Canvas spawner
│   ├── server/index.ts     # WebSocket server (port 3847)
│   └── canvases/
│       ├── email.tsx       # Email composer
│       ├── calendar.tsx    # Calendar view
│       ├── table.tsx       # Data table
│       ├── todo.tsx        # Todo list
│       └── json.tsx        # JSON explorer
├── electron/               # Electron popup mode (WIP)
│   ├── main/index.ts
│   ├── preload/index.ts
│   └── spawn.ts
├── package.json
└── tsconfig.json
```

## Integration with Claude Code

Claude Code can spawn canvases via the `/canvas` skill:

```bash
# From Claude Code
npm run canvas -- spawn table --data '{"rows":[...]}'
```

The canvas communicates back via WebSocket, allowing Claude to receive user interactions.

## Known Issues

- **Electron mode**: Path with spaces (OneDrive - ERPA) causes issues. Workaround: move project to path without spaces.
- **TUI mode**: Requires interactive terminal (won't work in Claude Code's bash directly - use split pane)

## Requirements

- Node.js 18+
- npm
- Windows Terminal (for split pane support)
