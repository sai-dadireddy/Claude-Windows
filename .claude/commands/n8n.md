# Start n8n Automation Platform

Launch the n8n workflow automation platform and open it in your browser.

## Task

1. Execute the PowerShell script to start n8n:
   `C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\tools\start-n8n.ps1`

2. Wait for n8n to be ready (script will automatically open browser)

3. Display status information

## Output Format

```
🚀 Starting n8n...
================================================

✓ n8n installation checked
✓ n8n starting...
✓ Browser opening at http://localhost:5678

📊 n8n Status:
  • URL: http://localhost:5678
  • User Folder: C:\Users\SainathreddyDadiredd\.n8n
  • Status: Running ✅

💡 Quick Actions:
  • Import AI News workflow: Click '...' → 'Import from File'
  • Workflow location: claude/projects/n8n/ai-news-aggregator/workflows/
  • Stop n8n: docker stop n8n (if using Docker) or Ctrl+C

✅ n8n is ready!
```

## Additional Actions

After starting n8n, provide these helpful tips:

1. **Import the AI News Aggregator workflow**:
   - File: `claude/projects/n8n/ai-news-aggregator/workflows/ai-news-free-rag.json`
   - In n8n UI: Click "..." → "Import from File" → Select file

2. **Configure credentials** (if first time):
   - Reddit OAuth2 (for community news)
   - Ollama (auto-connects to localhost:11434)

3. **Activate workflow**:
   - Toggle the workflow switch to "Active"
   - Set schedule: Every 6 hours

4. **Test run**:
   - Click "Execute Workflow" to run immediately
   - Check `data/articles.json` gets populated

## Notes

- n8n runs on http://localhost:5678
- If port 5678 is in use, n8n will fail to start
- Check if n8n is already running: `docker ps` or `ps aux | grep n8n`
- Data persists in `~/.n8n` directory
- Workflows are stored in n8n's database

## Related Commands

- `/ai-news` - View aggregated AI news dashboard
- `/ai-briefing` - Get daily AI news summary
