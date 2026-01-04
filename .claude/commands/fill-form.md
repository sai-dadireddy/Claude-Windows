# Fill Form

Intelligent form filling using Claude-in-Chrome.

## Workflow

1. Read page to understand form structure
2. Identify form fields
3. Fill fields with appropriate values
4. Optionally submit

## Steps

### 1. Read Page Structure
```
Use mcp__claude-in-chrome__read_page with:
- tabId: [tab]
- filter: "interactive"  # Focus on form elements
```

### 2. Find Specific Fields
```
Use mcp__claude-in-chrome__find with:
- query: "email input" or "name field"
- tabId: [tab]
```

### 3. Fill Fields
```
Use mcp__claude-in-chrome__form_input with:
- ref: [field ref]
- value: [value to enter]
- tabId: [tab]
```

### 4. For Dropdowns/Selects
```
Use mcp__claude-in-chrome__form_input with:
- ref: [select ref]
- value: "option text or value"
- tabId: [tab]
```

### 5. For Checkboxes
```
Use mcp__claude-in-chrome__form_input with:
- ref: [checkbox ref]
- value: true/false
- tabId: [tab]
```

## Smart Fill

When given context (like user profile), Claude can:
- Match field labels to appropriate data
- Handle various input types
- Skip already-filled fields

## Usage
```
/fill-form
/fill-form [context: "name=John, email=john@example.com"]
```

## Security Note
- Never auto-fill passwords
- Review before submitting
- Don't fill sensitive financial data
