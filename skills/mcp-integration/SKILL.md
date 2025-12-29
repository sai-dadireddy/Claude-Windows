---
name: mcp-integration
description: How to effectively use all 11 MCP servers (100+ tools) including Playwright, GitHub, AWS, Memory, Code Index, Codex, and LM Studio
tags: [mcp, tools, playwright, github, aws, memory, code-index, integration]
---

# MCP Integration Skill

## Overview

This skill provides guidance on effectively using our 11 MCP servers with 100+ tools. It includes best practices, tool selection, and patterns for optimal MCP usage.

## MCP Servers (9/11 Connected)

### Connected & Operational:

1. **codex** (GPT-5) - Deep code review
2. **playwright** - Browser automation (32 tools)
3. **code-index-mcp** - Fast code search (13 tools)
4. **sequential-thinking** - Complex reasoning
5. **github** - GitHub operations (26 tools)
6. **memory-auto** - Intelligent memory (6 tools)
7. **langchain** - Vector search (5 tools)
8. **code-indexing** - Additional indexing
9. **aws** - AWS operations (7 tools)

### Configured, Awaiting Installation:

10. **lm-studio** - Local AI (4 tools) - Needs user install

### Needs Attention:

11. **testing** - Test automation - Connection failed

## Tool Selection Matrix

| Task Type | Primary MCP | Support MCPs | Reason |
|-----------|-------------|--------------|---------|
| **File Operations** | Built-in (Read/Write/Edit) | code-index-mcp | Direct, fast |
| **Code Search** | code-index-mcp | - | Fastest with ugrep/ripgrep |
| **Browser Automation** | playwright | - | Full control, persistent sessions |
| **Security Review** | codex | - | Best security expertise |
| **Large Codebase** | - | code-index-mcp | Fast search |
| **Bulk Generation** | lm-studio | - | Free, unlimited |
| **GitHub Operations** | github | - | Full API access |
| **AWS Operations** | aws | - | Official SDK |
| **Memory Storage** | memory-auto | - | Auto-classification |
| **Complex Reasoning** | sequential-thinking | - | Chain-of-thought |
| **Vector Search** | langchain | - | Semantic similarity |

## Key MCP Patterns

### Playwright (32 Tools) - Browser Automation

**When to Use**:
- Testing web applications
- Web scraping
- Automated workflows
- Screenshots and PDFs
- JavaScript execution in browser

**Best Practices**:
```javascript
// Always use persistent browser profiles
// Location: browser-profiles/claude-automation
// Sessions persist across restarts

// Navigation
await playwright_navigate({url: "https://example.com", headless: false})

// Interaction
await playwright_click({selector: "button.submit"})
await playwright_fill({selector: "input[name='email']", value: "test@example.com"})

// Screenshots
await playwright_screenshot({name: "result", fullPage: true, savePng: true})

// JavaScript execution
await playwright_evaluate({script: "return document.title"})

// Clean up when done
await playwright_close()
```

### GitHub (26 Tools) - Full API Access

**When to Use**:
- Creating PRs, issues, branches
- Searching code/repos/users
- Managing repositories
- Review workflows

**Best Practices**:
```javascript
// Search code across GitHub
await search_code({q: "filename:*.py authentication"})

// Create PR with proper description
await create_pull_request({
  owner: "...",
  repo: "...",
  title: "...",
  head: "feature-branch",
  base: "main",
  body: "Detailed PR description with test plan"
})

// Get PR files to review
await get_pull_request_files({owner: "...", repo: "...", pull_number: 123})
```

### Code Index (13 Tools) - Fast Search

**When to Use**:
- Finding files by pattern
- Searching code with regex
- Getting file summaries
- Project exploration

**Best Practices**:
```javascript
// Search code with context
await search_code_advanced({
  pattern: "function.*Error",
  file_pattern: "*.js",
  context_lines: 3,
  case_sensitive: true
})

// Find files by glob
await find_files({pattern: "*.test.js"})

// Get file summary
await get_file_summary({file_path: "src/auth.ts"})

// Refresh after major changes
await refresh_index()
```

### Memory (6 Tools) - Intelligent Storage

**When to Use**:
- Storing important decisions
- Project-specific knowledge
- Cross-project search
- Context preservation

**Best Practices**:
```javascript
// Auto-store with classification
await auto_store_memory({
  content: "Important architectural decision...",
  project_name: "my-project"
})

// Search globally
await search_global_memory({
  query: "authentication pattern",
  importance_min: 2
})

// Store project-specific
await store_project_memory({
  project_name: "my-project",
  content: "...",
  importance: 3
})
```

### AWS (7 Tools) - Cloud Operations

**When to Use**:
- CodeBuild operations
- CloudWatch logs
- S3 operations
- Secrets Manager

**Best Practices**:
```javascript
// Start CodeBuild
await codebuild_start_build({
  project_name: "...",
  profile: "default",
  region: "us-east-1"
})

// Get CloudWatch logs
await cloudwatch_get_logs({
  log_group: "/aws/lambda/...",
  log_stream: "...",
  limit: 100
})

// List S3 objects
await s3_list_objects({
  bucket: "my-bucket",
  prefix: "path/"
})
```

## MCP + Skills Synergy

### Pattern: GitHub PR Excellence
```
Skill: github-pr-excellence (defines best practices)
MCP: github (provides API tools)
Result: Perfect PRs with proper descriptions
```

### Pattern: Security Code Review
```
Skill: security-review (defines checklist)
MCP: codex (provides deep analysis)
Result: Comprehensive security validation
```

### Pattern: Performance Optimization
```
Skill: performance-optimization (defines approach)
MCP: code-index-mcp (finds all relevant code)
Result: Systematic optimization
```

## Common Workflows

### Workflow 1: Code Search + Review
```
1. code-index-mcp: search_code_advanced("TODO")
2. Read all files with TODOs
3. codex: Review critical TODOs for security
4. memory-auto: Store important findings
```

### Workflow 2: Web Testing
```
1. playwright: navigate to app
2. playwright: click/fill forms
3. playwright: screenshot results
4. playwright: evaluate JavaScript
5. playwright: save_as_pdf for report
6. playwright: close browser
```

### Workflow 3: GitHub Workflow
```
1. github: search_code for patterns
2. Read relevant files
3. Implement changes
4. github: create_branch
5. github: push_files
6. github: create_pull_request
```

## When NOT to Use MCPs

### Use Built-in Tools When:
- Simple file reads → Read tool (faster)
- Simple edits → Edit tool (direct)
- Simple file creation → Write tool (immediate)
- Git operations → Bash (simple commands)

### Use Bash When:
- Terminal operations (git, npm, docker)
- System commands
- Package management
- Process management

**Never** use Bash for:
- File reading (use Read)
- File editing (use Edit)
- File creation (use Write)
- Code search (use Grep or code-index-mcp)

## Troubleshooting

### MCP Connection Failed
```bash
# Check status
claude mcp list

# Test specific MCP
claude mcp test playwright

# Restart Claude Code
exit
claude
```

### Performance Issues
```
- Use code-index-mcp instead of Grep for large searches
- Use Gemini CLI for reading 50+ files
- Use playwright with headless: true for faster testing
- Close playwright when done to free resources
```

### Token Optimization
```
- Use MCPs for specialized tasks (more efficient)
- Use Gemini for large context (2M tokens)
- Use LM Studio for bulk generation (unlimited)
- Use built-in tools for simple operations
```

## Related Skills

- **Multi-AI Orchestration**: When to route to Codex/Gemini/LM Studio
- **Code Review Excellence**: How to structure reviews
- **Security Best Practices**: Security-specific MCP usage
- **Performance Optimization**: Performance-focused workflows

---

**Status**: ✅ PRODUCTION READY
**Version**: 1.0.0
**Last Updated**: 2025-10-18
