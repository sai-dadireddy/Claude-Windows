# GLM Prompting Guide

## Best Practices

### DO:
1. **Frame as task completion** - "Implement X" not "Show me how to X"
2. **Be specific about requirements** - Include constraints, edge cases
3. **Use structured formats** - XML tags, markdown sections
4. **Enable thinking for complex tasks** - Worth the extra tokens
5. **Provide context upfront** - File contents, error messages, expected behavior

### DON'T:
1. Don't use for simple questions - Use Claude instead
2. Don't disable thinking for complex coding - Quality drops
3. Don't expect identical behavior to Claude - Different model, different strengths

## Prompt Templates

### Code Generation
```xml
<task>
Implement [feature] with the following requirements:
</task>

<requirements>
- [Requirement 1]
- [Requirement 2]
</requirements>

<constraints>
- Language: [Python/TypeScript/etc]
- Must handle: [edge cases]
- Do not: [restrictions]
</constraints>

<context>
[Relevant code or file contents]
</context>
```

### Code Review
```xml
<task>Review this code for security, performance, and best practices</task>

<code language="python">
[code here]
</code>

<focus>
- Security vulnerabilities (OWASP Top 10)
- Performance bottlenecks
- Error handling
</focus>
```

### Debugging
```xml
<task>Debug this error</task>

<error>
[Error message]
</error>

<code>
[Relevant code]
</code>

<context>
- What was expected: [expected behavior]
- What happened: [actual behavior]
- Already tried: [attempted fixes]
</context>
```

### Architecture Design
```xml
<task>Design [system/feature]</task>

<requirements>
[What it needs to do]
</requirements>

<constraints>
- Scale: [expected load]
- Stack: [technologies available]
- Budget: [if relevant]
</constraints>

<output>
Provide:
1. High-level architecture
2. Component breakdown
3. Data flow diagram (ASCII)
4. Key implementation decisions
</output>
```
