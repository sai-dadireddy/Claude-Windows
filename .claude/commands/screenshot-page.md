# Screenshot Page

Take and save annotated screenshots using Claude-in-Chrome.

## Workflow

1. Get tab context
2. Take screenshot
3. Optionally save to file
4. Describe what's shown

## Steps

### 1. Get Tab
```
Use mcp__claude-in-chrome__tabs_context_mcp
```

### 2. Screenshot
```
Use mcp__claude-in-chrome__computer with:
- action: "screenshot"
- tabId: [from context]
```

### 3. For Zoom/Detail
```
Use mcp__claude-in-chrome__computer with:
- action: "zoom"
- region: [x0, y0, x1, y1]
- tabId: [from context]
```

## Output
- Screenshot displayed inline
- Description of page content
- Any notable UI elements or issues

## Usage
```
/screenshot-page
/screenshot-page [description of what to capture]
```
