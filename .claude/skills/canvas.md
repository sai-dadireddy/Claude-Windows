---
name: canvas
description: Spawn interactive TUI or Electron popup canvases for rich visual output
context: fork
allowed_tools:
  - Bash
---

# Canvas Skill

Spawn interactive interfaces for Claude Code - either terminal TUI or rich Electron popups. Faster than screenshot-based workflows.

## Two Modes

| Mode | Command | Best For |
|------|---------|----------|
| **TUI** | `npm run canvas --` | Terminal split panes, keyboard navigation |
| **Popup** | `npm run popup --` | Rich UI, mouse interaction, always-on-top |

## Available Canvas Types

| Type | Description | TUI | Popup |
|------|-------------|-----|-------|
| `email` | Email composer | ✓ | ✓ |
| `calendar` | Interactive calendar | ✓ | ✓ |
| `table` | Data table with sorting | ✓ | ✓ |
| `todo` | Interactive todo list | ✓ | ✓ |
| `json` | JSON viewer/explorer | ✓ | ✓ |

## Quick Start

```bash
cd "C:/Users/SainathreddyDadiredd/OneDrive - ERPA/Claude/claude-canvas"

# TUI mode (requires split terminal pane)
npm run canvas -- spawn email --data '{"to":"user@example.com"}'

# Electron popup mode (opens always-on-top window)
npm run popup -- --type email --data '{"to":"user@example.com"}'
```

## TUI Mode

Best for terminal-native workflows. Runs in a split pane.

```bash
# Split Windows Terminal first: Ctrl+Shift+D
npm run canvas -- spawn <type> --data '<json>'

# Examples
npm run canvas -- spawn email --data '{"to":"team@company.com","subject":"Update"}'
npm run canvas -- spawn todo --data '{"items":[{"text":"Review PR","done":false}]}'
npm run canvas -- spawn table --data '{"rows":[{"name":"Alice","age":30}]}'
```

**Keyboard Controls:**
- **Esc**: Close
- **Arrow keys**: Navigate
- **Tab**: Next field
- **Enter/Space**: Select

## Electron Popup Mode

Rich HTML/React UI in an always-on-top window. No terminal pane needed.

```bash
npm run popup -- --type <type> --data '<json>'

# Examples
npm run popup -- --type email --data '{"to":"team@company.com","subject":"Weekly Update"}'
npm run popup -- --type todo --data '{"items":[{"text":"Task 1","done":false}]}'
npm run popup -- --type table --data '{"rows":[{"name":"Alice","age":30}]}'
```

**Features:**
- Always-on-top window
- Dark theme UI
- Mouse interaction
- Drag titlebar to move
- Auto-positioned bottom-right

## Two-Way Communication

Both modes support WebSocket communication:
- **TUI**: Port 3847
- **Popup**: Port 3848

Canvas sends updates when user interacts. Claude can send updates to modify content.

## Examples

### Email Draft (Popup)
```bash
npm run popup -- --type email --data '{
  "to": "team@company.com",
  "cc": "manager@company.com",
  "subject": "Weekly Update",
  "body": "Here are the updates..."
}'
```

### Todo List (Popup)
```bash
npm run popup -- --type todo --data '{
  "items": [
    {"id": "1", "text": "Review PR", "done": false},
    {"id": "2", "text": "Update docs", "done": true}
  ]
}'
```

### Data Table (TUI)
```bash
npm run canvas -- spawn table --data '{
  "title": "API Endpoints",
  "columns": ["method", "path", "status"],
  "rows": [
    {"method": "GET", "path": "/users", "status": "200"},
    {"method": "POST", "path": "/users", "status": "201"}
  ]
}'
```
