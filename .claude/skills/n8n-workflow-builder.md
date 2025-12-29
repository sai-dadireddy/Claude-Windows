# n8n Workflow Builder Skill

Generate production-ready n8n workflows from natural language descriptions. Self-hosted = free unlimited workflows.

## Trigger Keywords
- "n8n workflow", "build workflow", "automate with n8n"
- "workflow automation", "create automation"

## Capabilities

1. **Generate Valid n8n JSON** - Ready to import
2. **Node Configuration** - Proper connections, error handling
3. **Multi-Service Integration** - 400+ available integrations
4. **AI-Enhanced Workflows** - Claude, OpenAI, Ollama nodes

## Workflow Generation Prompt Pattern

When user asks to build an n8n workflow:

```
Generate an n8n workflow JSON that:

WORKFLOW: [User's description]

REQUIREMENTS:
1. Use proper n8n node types from the official node library
2. Include error handling with Try/Catch or Error Trigger
3. Add Sticky Notes for documentation
4. Use placeholder credentials (user will configure)
5. Ensure all nodes are properly connected
6. Output valid JSON ready for n8n import

OUTPUT FORMAT:
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "settings": {...}
}
```

## Recommended Workflow Ideas (By Scenario)

### Developer Productivity

| Workflow | Trigger | Actions |
|----------|---------|---------|
| **GitHub → Slack Alerts** | GitHub webhook | Filter by label, post to Slack channel |
| **PR Review Reminder** | Schedule (daily) | Check stale PRs, notify reviewers |
| **Deploy Notification** | GitHub Actions webhook | Post to team channel with status |
| **Error Log Monitor** | CloudWatch/logs | Parse errors, create Jira ticket |
| **Documentation Sync** | Git push to docs/ | Build, deploy to Notion/Confluence |

### AI/LLM Workflows

| Workflow | Trigger | Actions |
|----------|---------|---------|
| **AI Code Review** | PR webhook | Send diff to Claude, post comments |
| **Document Summarizer** | File upload | Extract text, summarize with Ollama |
| **Meeting Notes** | Calendar event end | Transcribe, summarize, email attendees |
| **RAG Ingestion** | New file in folder | Chunk, embed, store in vector DB |
| **AI Slack Bot** | Slack mention | Query Claude/Ollama, respond |

### Data & Integration

| Workflow | Trigger | Actions |
|----------|---------|---------|
| **Lead Enrichment** | New CRM contact | Clearbit lookup, update record |
| **Invoice Processing** | Email attachment | OCR extract, create in accounting |
| **Report Generation** | Schedule (weekly) | Query DBs, generate PDF, email |
| **Data Backup** | Schedule (nightly) | Export data, upload to S3 |
| **Cross-Platform Sync** | Webhook | Sync data between services |

### DevOps & Monitoring

| Workflow | Trigger | Actions |
|----------|---------|---------|
| **Health Check** | Schedule (5min) | Ping endpoints, alert on failure |
| **Cost Alert** | AWS billing webhook | Threshold check, Slack alert |
| **SSL Expiry Check** | Schedule (daily) | Check certs, warn 30 days out |
| **Container Restart** | Error detection | Restart service, notify |
| **Deployment Pipeline** | Git tag push | Build, test, deploy, notify |

### Content & Marketing

| Workflow | Trigger | Actions |
|----------|---------|---------|
| **Social Media Publisher** | Notion update | Format, post to Twitter/LinkedIn |
| **Newsletter Curator** | Schedule (weekly) | Aggregate content, draft email |
| **SEO Monitor** | Schedule (daily) | Check rankings, alert on drops |
| **Content Repurposer** | New blog post | Generate social posts, schedule |

## Example: GitHub PR to Slack Notification

```json
{
  "name": "GitHub PR to Slack",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "github-pr"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [{
            "value1": "={{ $json.action }}",
            "value2": "opened"
          }]
        }
      },
      "name": "Filter New PRs",
      "type": "n8n-nodes-base.if",
      "position": [450, 300]
    },
    {
      "parameters": {
        "channel": "#dev-prs",
        "text": "🔀 New PR: {{ $json.pull_request.title }}\nBy: {{ $json.pull_request.user.login }}\n{{ $json.pull_request.html_url }}"
      },
      "name": "Post to Slack",
      "type": "n8n-nodes-base.slack",
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Filter New PRs", "type": "main", "index": 0 }]] },
    "Filter New PRs": { "main": [[{ "node": "Post to Slack", "type": "main", "index": 0 }]] }
  }
}
```

## Best Practices

1. **Error Handling**: Always add Error Trigger node for critical workflows
2. **Rate Limiting**: Use Wait nodes for APIs with quotas
3. **Credentials**: Use n8n's credential system, never hardcode
4. **Documentation**: Add Sticky Notes explaining complex logic
5. **Testing**: Use Manual Trigger during development
6. **Versioning**: Export workflows to Git regularly

## MCP Integration

Execute via Claude Code:
```javascript
// List workflows
router_execute({ category: "n8n", server: "n8n", tool: "list_workflows", args: {} })

// Execute workflow
router_execute({ category: "n8n", server: "n8n", tool: "execute_workflow", args: { workflow_id: "123", data: {...} } })

// Create workflow
router_execute({ category: "n8n", server: "n8n", tool: "create_workflow", args: { name: "...", nodes: [...] } })
```

## n8n Self-Hosted Setup

Already installed at: `C:\Users\SainathreddyDadiredd\AppData\Roaming\npm\n8n.ps1`

**Start**: `tools/n8n/Start-n8n.ps1` or `n8n start`
**Stop**: `tools/n8n/Stop-n8n.ps1`
**URL**: http://localhost:5678

## Sources
- [n8n Workflow Templates](https://n8n.io/workflows/) - 7,100+ community templates
- [n8n Claude Integration](https://n8n.io/integrations/claude/)
- [n8n-MCP for Claude](https://github.com/czlonkowski/n8n-mcp)
- [Self-hosted AI Starter Kit](https://github.com/n8n-io/self-hosted-ai-starter-kit)
