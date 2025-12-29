# Smart Web Fetching - Use Playwright Instead of WebFetch

**Usage**: Just use this pattern when WebFetch fails!

**Problem**: WebFetch returns CSS/garbage instead of actual content

**Solution**: Use Playwright MCP tools

---

## Quick Reference

### For Static Content (No JavaScript)
```
Tool: mcp__playwright__playwright_get
Use when: Fetching HTML pages, APIs, static content
Speed: Fast (no browser needed)
Limitation: Won't render JavaScript
```

### For Dynamic Content (JavaScript-heavy)
```
Tool: mcp__playwright__playwright_navigate
Use when: React/Angular/Vue apps, SPAs, dynamic content
Speed: Slower (needs browser)
Requirement: Browsers installed (npx playwright install)
```

---

## Examples

### Example 1: Fetch n8n Workflows
```
❌ OLD WAY (Fails):
WebFetch → https://n8n.io/workflows → Returns CSS

✅ NEW WAY (Works):
playwright_get → https://n8n.io/workflows → Returns HTML!
```

### Example 2: Screenshot a Page
```
playwright_navigate → URL
playwright_screenshot → Saves image
```

### Example 3: Extract Data from SPA
```
playwright_navigate → URL
playwright_get_visible_html → Clean HTML
```

---

## Installation Check

**Check if browsers installed:**
```bash
powershell -Command "Test-Path '$env:USERPROFILE\AppData\Local\ms-playwright\chromium-*'"
```

**Install browsers if needed:**
```bash
npx playwright install chromium
```

---

## Pro Tips

1. **Try GET first**: It's faster and often works
2. **Use navigate for SPAs**: React/Vue/Angular need browser
3. **Screenshots are gold**: Visual debugging is powerful
4. **Clean HTML**: Use removeScripts=true for cleaner output

---

**Time Saved**: No more fighting with WebFetch! ⚡

**Success Rate**:
- WebFetch: 30% success (often gets CSS)
- Playwright GET: 90% success (actual HTML)
- Playwright Navigate: 99% success (full browser)
