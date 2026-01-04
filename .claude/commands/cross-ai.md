# Cross-AI Workflow

Use other AI tools (Gemini, ChatGPT, etc.) from Claude Code.

## Concept

Since Claude-in-Chrome uses your authenticated browser sessions,
you can interact with other AI web apps without API keys.

## Supported Services

| Service | URL | Use Case |
|---------|-----|----------|
| Gemini | gemini.google.com | Image generation, Google integration |
| ChatGPT | chat.openai.com | Alternative perspective |
| Perplexity | perplexity.ai | Web search with citations |
| Midjourney | midjourney.com | Image generation |

## Workflow

### 1. Navigate to AI Service
```
Use mcp__claude-in-chrome__navigate with:
- url: "gemini.google.com" (or other)
- tabId: [tab]
```

### 2. Find Input Box
```
Use mcp__claude-in-chrome__find with:
- query: "prompt input box" or "chat input"
- tabId: [tab]
```

### 3. Enter Prompt
```
Use mcp__claude-in-chrome__form_input with:
- ref: [from find]
- value: "your prompt"
- tabId: [tab]
```

### 4. Submit and Wait
```
Use mcp__claude-in-chrome__computer with:
- action: "key"
- text: "Enter"
- tabId: [tab]

Then wait for response
```

### 5. Extract Result
```
Use mcp__claude-in-chrome__get_page_text or
Use mcp__claude-in-chrome__computer action: "screenshot"
```

## Example: Generate Image with Gemini
```
/cross-ai gemini "generate an image of a sunset over mountains"
```

## Security Note
- Only use on trusted AI services
- Don't send sensitive data through third-party AIs
- Review outputs before using

## Usage
```
/cross-ai [service] [prompt]
/cross-ai gemini "create an image of..."
/cross-ai perplexity "search for..."
```
