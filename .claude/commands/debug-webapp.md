# Debug Web App

Debug a web application using Claude-in-Chrome.

## Workflow

1. Get current tab context
2. Read console messages (filter for errors)
3. Check network requests for failed calls
4. Take screenshot of current state
5. Report findings

## Steps

### 1. Get Tab Context
```
Use mcp__claude-in-chrome__tabs_context_mcp to get available tabs
```

### 2. Read Console Errors
```
Use mcp__claude-in-chrome__read_console_messages with:
- tabId: [from context]
- onlyErrors: true
- pattern: "error|exception|failed"
```

### 3. Check Network Failures
```
Use mcp__claude-in-chrome__read_network_requests with:
- tabId: [from context]
- urlPattern: optional filter
```

### 4. Take Screenshot
```
Use mcp__claude-in-chrome__computer with:
- action: "screenshot"
- tabId: [from context]
```

### 5. Report
Summarize:
- Console errors found
- Failed network requests (4xx, 5xx)
- Visual state from screenshot
- Suggested fixes

## Usage
```
/debug-webapp
/debug-webapp [url-pattern-filter]
```
