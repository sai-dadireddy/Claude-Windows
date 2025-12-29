# n8n + Claude Code - Quick Start Guide

## ✅ Installation Complete!

All prerequisites have been installed and configured. You're ready to start using n8n with Claude Code integration.

## 🚀 Starting n8n

### Option 1: PowerShell Script (Recommended for Windows)
```powershell
.\tools\start-n8n.ps1
```

### Option 2: Bash Script
```bash
./tools/start-n8n.sh
```

### Option 3: Direct Command
```bash
n8n
```

## 📋 What Was Installed

### 1. n8n Workflow Automation
- **Version**: 1.114.4
- **Location**: Globally installed via npm
- **Access**: http://localhost:5678

### 2. Claude Code Community Node
- **Package**: @holtweb/n8n-nodes-claudecode
- **Location**: `~/.n8n/nodes/node_modules/@holtweb/n8n-nodes-claudecode`
- **Status**: ✅ Installed and ready

### 3. Configuration Files
- **Permissions**: `.claude/settings.json` - Configured for n8n automation
- **n8n Config**: `~/.n8n/` - User configuration directory
- **Startup Scripts**: `tools/start-n8n.ps1` and `tools/start-n8n.sh`

## 🎯 First Steps

### 1. Start n8n
```powershell
.\tools\start-n8n.ps1
```

### 2. Open n8n UI
Open your browser and navigate to:
```
http://localhost:5678
```

### 3. Create Your First Workflow

1. Click **"Create new workflow"**
2. Click **"+"** to add a node
3. Search for **"Claude Code"**
4. Configure the node:
   - **Operation**: Query
   - **Project Path**: `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude`
   - **Prompt**: Your AI task (e.g., "Review this code")
   - **Model**: Sonnet 4 (or Opus 3)

### 4. Test Your Workflow
1. Click **"Execute Workflow"**
2. See Claude Code in action!

## 📚 Example Workflows

### Workflow 1: Simple Code Review
```
Manual Trigger → Claude Code (review code) → Set (save results)
```

### Workflow 2: Automated Bug Fix
```
Schedule (daily) → HTTP (fetch logs) → Claude Code (analyze) → Claude Code Continue (fix) → Slack (notify)
```

### Workflow 3: SQL Generator
```
Webhook → Claude Code (convert to SQL) → Postgres (execute) → Webhook Response
```

## 🔧 Configuration Details

### Claude Code Settings (`.claude/settings.json`)

Configured permissions:
- ✅ File operations (read/write)
- ✅ Bash commands (whitelisted)
- ✅ Web access (allowed domains)
- ✅ All 12 MCP servers enabled
- ✅ Autonomous mode (5 minute max)
- ✅ Network requests enabled

### Whitelisted Bash Commands
- git, npm, node, python, pip, pytest
- docker, kubectl, aws, az, gcloud, terraform
- ls, cat, echo, mkdir, cd, pwd

### Allowed Web Domains
- github.com, gitlab.com, bitbucket.org
- stackoverflow.com, docs.python.org
- npmjs.com, pypi.org

## 🎨 Claude Code Node Configuration

### Required Parameters
- **Project Path**: Path to your project (for context)
- **Prompt**: Your instruction for Claude Code

### Optional Parameters
- **Operation**: Query (new request) or Continue (chain operations)
- **Model**: Sonnet 4 (fast) or Opus 3 (powerful)
- **Timeout**: Max execution time (default: 120s)

### Advanced Features
- **Chained Operations**: Use "Continue" to build multi-step workflows
- **MCP Integration**: Full access to all configured MCP servers
- **Slash Commands**: Can invoke `/create-presentation`, `/autonomous`, etc.
- **Context Awareness**: Uses your project files and configuration

## 💡 Pro Tips

### 1. Always Set Project Path
```javascript
{
  "projectPath": "C:\\Users\\SainathreddyDadiredd\\OneDrive - ERPA\\Claude"
}
```

### 2. Use Specific Prompts
❌ Bad: "check code"
✅ Good: "Review authentication.js for security vulnerabilities: SQL injection, XSS, CSRF, password handling"

### 3. Chain Complex Tasks
```
Claude Code (Analyze)
  → Claude Code Continue (Plan)
  → Claude Code Continue (Implement)
  → Claude Code Continue (Test)
```

### 4. Handle Errors
```javascript
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3
}
```

### 5. Use Different Models
- **Sonnet**: Quick code reviews, simple generation
- **Opus**: Complex architecture, deep analysis

## 🔍 Troubleshooting

### Issue: "Claude Code CLI not found"
**Solution**:
```bash
# Check installation
claude --version

# If not found, it should already be installed with Claude Max
```

### Issue: "Authentication failed"
**Solution**:
```bash
# Re-authenticate
claude auth login
```

### Issue: "Permission denied"
**Solution**: Check `.claude/settings.json` permissions

### Issue: "Node not found in n8n"
**Solution**:
1. Restart n8n
2. Clear browser cache
3. Reinstall community node in n8n UI

### Issue: "Timeout on long operations"
**Solution**: Increase timeout in node settings (up to 300s)

## 📖 Documentation

### Installed Documentation
- **Full Guide**: `docs/n8n-workflow-integration.md`
- **Global Instructions**: `global-instructions/n8n-workflow-automation.md`

### External Resources
- **n8n Documentation**: https://docs.n8n.io/
- **Claude Code Docs**: https://docs.claude.com/claude-code/
- **Repository**: https://github.com/holt-web-ai/n8n-nodes-claudecode

## 🎯 Example: Complete Workflow

Here's a complete automated code review workflow:

```json
{
  "name": "Automated Code Review",
  "nodes": [
    {
      "name": "Git Push",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "git-push"
      }
    },
    {
      "name": "Get Changed Files",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "git diff --name-only HEAD~1"
      }
    },
    {
      "name": "Claude Code Review",
      "type": "@holtweb/n8n-nodes-claudecode",
      "parameters": {
        "operation": "query",
        "projectPath": "C:\\Users\\SainathreddyDadiredd\\OneDrive - ERPA\\Claude",
        "prompt": "Review the following changed files for quality, security, and best practices: {{$json.files}}",
        "model": "sonnet"
      }
    },
    {
      "name": "Send to Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel": "#code-reviews",
        "text": "Code Review: {{$node['Claude Code Review'].json.output}}"
      }
    }
  ]
}
```

## 🚀 Next Steps

1. ✅ Start n8n: `.\tools\start-n8n.ps1`
2. ✅ Open UI: http://localhost:5678
3. ✅ Create your first workflow
4. ✅ Explore example workflows in `docs/n8n-workflow-integration.md`
5. ✅ Build custom automation for your needs

## 📊 System Information

**Installation Date**: October 11, 2025
**n8n Version**: 1.114.4
**Node.js Version**: 24.4.1
**npm Version**: 11.4.2
**Claude Subscription**: Claude Code Max ✅

**Installed Components**:
- ✅ n8n (workflow automation)
- ✅ @holtweb/n8n-nodes-claudecode (Claude Code integration)
- ✅ Configuration files
- ✅ Startup scripts
- ✅ Documentation

**Status**: 🟢 Ready to use!

---

## Quick Commands

```bash
# Start n8n
.\tools\start-n8n.ps1

# Check n8n version
n8n --version

# Check Claude Code status
claude auth status

# Open n8n UI
# Browser: http://localhost:5678
```

**Ready to automate your development workflow with AI! 🎉**
