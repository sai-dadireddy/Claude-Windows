# Claude Code Plugins & Marketplaces System

**Game-Changer**: Share slash commands, subagents, hooks, and MCP servers as reusable packages

**Release**: Claude Code 2.0+

---

## 🎯 What Are Plugins?

**Plugins** = Lightweight packages containing:
- ✅ Slash commands
- ✅ Subagents
- ✅ Hooks
- ✅ MCP servers

**Marketplaces** = Collections of plugins (like an app store)

---

## 🚀 Why This Matters

**Before plugins**:
- Share workflows via copy-paste
- No version control
- Manual setup for teams
- Hard to distribute to community

**With plugins**:
- ✅ One-command install
- ✅ Auto-updates
- ✅ Easy team sharing
- ✅ Open-source distribution
- ✅ Curated collections

---

## 📦 Installing Plugins

### Step 1: Add Marketplace

```bash
# In Claude Code
/plugin
> Add marketplace
> Enter URL: https://github.com/anthropics/claude-code-plugins
```

### Step 2: Browse & Install

```bash
/plugin
> Browse and install plugins
> Select plugins (space to select, enter to install)
> Restart Claude Code
```

### Step 3: Use New Tools

- Slash commands: Press `/` to see new commands
- Subagents: Use "Add agent" to see new agents
- MCP servers: Check `/mcp` for new servers
- Hooks: Automatically active

---

## 🏪 Official Anthropic Marketplace

**URL**: https://github.com/anthropics/claude-code-plugins

**Available Plugins**:

1. **Agent SDK**
   - Tools for building custom agents
   - Example workflows

2. **Commit Commands**
   - Git commit helpers
   - Conventional commit formats

3. **Feature Dev**
   - Feature development workflows
   - Planning & implementation

4. **PR Review Toolkit**
   - Advanced code review agents
   - Security scanning

5. **Security Guidance**
   - Security-focused subagents
   - Vulnerability detection

---

## 🛠️ Creating Your Own Plugin

### Project Structure

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest
└── plugins/
    └── my-plugin/
        ├── .claude-plugin/
        │   └── plugin.json   # Plugin manifest
        ├── commands/          # Slash commands
        │   └── my-command.md
        ├── agents/           # Subagents
        │   └── my-agent.md
        ├── hooks/            # Hooks
        │   └── hooks.json
        └── .mcp.json         # MCP servers
```

---

### Creating a Marketplace

**File**: `.claude-plugin/marketplace.json`

```json
{
  "name": "my-awesome-marketplace",
  "owner": {
    "name": "Your Name",
    "email": "your@email.com",
    "url": "https://github.com/yourname"
  },
  "metadata": {
    "description": "My collection of Claude Code tools",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "website-dev",
      "path": "plugins/website-dev",
      "description": "Commands, agents, hooks, and tools for building websites",
      "version": "1.0.0",
      "category": "development",
      "keywords": ["web", "html", "css"]
    }
  ]
}
```

**Important**:
- Marketplace name must be kebab-case (no spaces)
- Plugin name in manifest must match folder name

---

### Creating a Plugin

**File**: `plugins/my-plugin/.claude-plugin/plugin.json`

```json
{
  "name": "website-dev",
  "description": "Commands, agents, hooks, and tools for building websites",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  }
}
```

---

### Adding Slash Commands

**File**: `plugins/my-plugin/commands/website-starter.md`

```markdown
# Description
Create a basic HTML web page

# Prompt
Create a simple .html file based on the user's requirements.
Include proper HTML5 structure with:
- <!DOCTYPE html>
- <head> with meta tags
- <body> with semantic HTML
- Basic CSS in <style> tag
- Responsive design
```

**Auto-discovery**: Any `.md` file in `commands/` becomes a slash command!

---

### Adding Subagents

**File**: `plugins/my-plugin/agents/website-styler.md`

```markdown
# Name
website-styler

# Description
Use this agent to create beautiful styles for our website

# Model
sonnet

# Prompt
Your role is to improve the look and feel of a website by implementing proper styling.

Tasks:
1. Ensure a separate .css file exists
2. Implement beautiful gradients and color tokens
3. Use modern CSS features (grid, flexbox, custom properties)
4. Ensure mobile-responsive design
5. Follow accessibility best practices
```

---

### Adding MCP Servers

**File**: `plugins/my-plugin/.mcp.json`

```json
{
  "mcpServers": {
    "shadcn": {
      "command": "npx",
      "args": ["-y", "@executeautomation/shadcn-mcp"],
      "env": {}
    }
  }
}
```

**Windows users**: Use `"command": "cmd"` with `"args": ["/c", "npx", ...]`

---

### Adding Hooks

**File**: `plugins/my-plugin/hooks/hooks.json`

```json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint",
      "description": "Run linter before commits"
    },
    "post-success": {
      "command": "afplay /System/Library/Sounds/Glass.aiff",
      "description": "Play sound on success (Mac)"
    }
  }
}
```

---

## 🧪 Testing Locally

Before publishing to GitHub, test locally:

```bash
# In Claude Code
/plugin
> Add marketplace
> Enter: ./          # Current directory!
```

This loads the marketplace from your local folder.

---

## 🌍 Publishing to GitHub

### Step 1: Initialize Git Repo

```bash
git init
git add .
git commit -m "Initial marketplace"
```

### Step 2: Create GitHub Repo

- Create new public repo on GitHub
- Name it something like `claude-code-plugins`
- Push your code:

```bash
git remote add origin https://github.com/yourusername/claude-code-plugins
git push -u origin main
```

### Step 3: Share URL

Your marketplace URL:
```
https://github.com/yourusername/claude-code-plugins
```

Anyone can install with:
```bash
/plugin > Add marketplace > [paste URL]
```

---

## 🔄 Auto-Updates (KILLER FEATURE!)

**Changes automatically propagate!**

When you update your GitHub repo:
- Commands update automatically
- Agents update automatically
- Hooks update automatically
- MCP configs update automatically

**Users don't need to reinstall** - just restart Claude Code!

---

## 🎯 Use Cases

### 1. Team Workflows
Share curated MCP servers and agents with team members:
- Security review agents
- Code style enforcers
- Project-specific commands

### 2. Open Source Projects
Maintainers can provide:
- Project-specific commands
- Custom agents for contributing
- Pre-configured MCP servers
- Hooks for code quality

### 3. Domain Expertise
Experienced devs can share:
- Battle-tested workflows
- Industry best practices
- Optimized subagents

### 4. Learning & Onboarding
Junior devs get instant access to:
- Senior dev workflows
- Best practice agents
- Quality guardrails

---

## 📚 Real-World Examples

### Security Tools Plugin

```
plugins/security-tools/
├── .claude-plugin/plugin.json
├── commands/
│   ├── security-scan.md
│   ├── dependency-audit.md
│   └── code-review.md
├── agents/
│   ├── security-reviewer.md
│   └── vulnerability-scanner.md
└── hooks/
    └── hooks.json (pre-commit security checks)
```

### UI/UX Plugin

```
plugins/ui-tools/
├── .claude-plugin/plugin.json
├── commands/
│   ├── component-generator.md
│   └── style-system.md
├── agents/
│   ├── ui-designer.md
│   └── accessibility-checker.md
└── .mcp.json (shadcn, magic components)
```

---

## 🔧 Managing Plugins

### View Installed Plugins

```bash
/plugin > Manage and uninstall plugins
```

### Disable Plugin (Keep Installed)

```bash
/plugin > Manage and uninstall plugins
> Uncheck plugin > Apply changes
```

### Uninstall Plugin

```bash
/plugin > Manage and uninstall plugins
> Select plugin > Apply changes
```

### Remove Marketplace

```bash
/plugin > Manage marketplaces
> Select marketplace > Remove
> Confirm removal of all plugins
```

---

## 💡 Pro Tips

1. **Organize by domain** - Create plugins for specific domains (security, UI, backend, etc.)

2. **Version control** - Use semantic versioning in plugin.json

3. **Test locally first** - Always test with `./` before publishing

4. **Document well** - Add README.md to explain plugin usage

5. **Keep focused** - One plugin = one domain/purpose

6. **Use examples** - Include example commands/agents in repo

7. **Community feedback** - Open issues/PRs on your marketplace repo

---

## 🌟 Featured Marketplaces

**Official Anthropic**:
- https://github.com/anthropics/claude-code-plugins
- Agent SDK, security, PR reviews

**Community** (watch these spaces):
- UI/UX toolkits
- DevOps automation
- Data science workflows
- Game development tools

---

## 🚀 Future of Plugins

From Anthropic:
> "Plugins will be our standard way to bundle and share Claude Code customizations and will continue to evolve the format as we add more extension points."

**Expect**:
- More plugin types
- Enhanced marketplaces
- Plugin dependencies
- Version management
- Plugin testing frameworks

---

## 📖 Resources

**Official Docs**: https://docs.claude.com/plugins
**Example Marketplace**: https://github.com/anthropics/claude-code-plugins
**Video Tutorial**: [Link to tutorial video]

---

## Bottom Line

**Plugins = Game Changer**

- ✅ Share entire workflows in one command
- ✅ Auto-updates from GitHub
- ✅ Build once, share everywhere
- ✅ Perfect for teams & open source
- ✅ Future-proof your Claude Code setup

**Start building your plugin today!** 🚀
