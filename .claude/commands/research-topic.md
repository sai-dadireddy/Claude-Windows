# Research Topic

Multi-tab research workflow using Claude-in-Chrome.

## Workflow

1. Create new tab for research
2. Navigate to search or specific sites
3. Extract relevant content
4. Aggregate findings
5. Save summary

## Steps

### 1. Create Tab
```
Use mcp__claude-in-chrome__tabs_create_mcp
```

### 2. Navigate
```
Use mcp__claude-in-chrome__navigate with:
- url: search URL or specific site
- tabId: [new tab]
```

### 3. Extract Content
```
Use mcp__claude-in-chrome__get_page_text with:
- tabId: [current tab]
```

### 4. Find Specific Elements
```
Use mcp__claude-in-chrome__find with:
- query: "article content" or specific selector
- tabId: [current tab]
```

## Multi-Source Research

For comprehensive research:
1. Open multiple tabs (create multiple)
2. Navigate each to different sources
3. Extract from each
4. Synthesize findings

## Usage
```
/research-topic [topic to research]
/research-topic [topic] --sources [site1,site2]
```
