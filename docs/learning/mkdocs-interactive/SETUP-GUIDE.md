# AI Learning Syllabus - Interactive Dashboard Setup Guide

## Quick Start (5 Minutes)

```bash
# 1. Install MkDocs Material
pip install mkdocs-material

# 2. Navigate to project directory
cd "C:\Users\SainathreddyDadiredd\OneDrive - ERPA\Claude\docs\learning\mkdocs-interactive"

# 3. Serve locally
mkdocs serve

# 4. Open browser to http://127.0.0.1:8000
```

That's it! Your interactive syllabus is now running locally with full progress tracking.

---

## What You Get

### ✅ Full Features
- **52 Interactive Topics** with checkboxes
- **Progress Dashboard** with statistics
- **Personal Notes** per topic (auto-saved)
- **Study Mode Tags** (Learn/Practice/Deploy)
- **Provider Comparison** (Claude/GPT/Gemini)
- **Search** across all content
- **Dark/Light Mode** toggle
- **Mobile Responsive** design
- **Offline Capable** (after first load)

### 💾 Data Storage
- **localStorage**: All progress saved in browser
- **No Backend Required**: Pure client-side
- **Export/Import**: Download JSON backup anytime
- **Privacy**: Data never leaves your device

---

## Prerequisites

### Required
- **Python 3.7+**: Check with `python --version`
- **pip**: Package manager (comes with Python)

### Optional (for deployment)
- **Git**: For version control
- **GitHub Account**: For GitHub Pages deployment
- **Docker**: For containerized deployment

---

## Installation Steps

### Step 1: Install MkDocs Material

```bash
# Option 1: pip install (recommended)
pip install mkdocs-material

# Option 2: With all extensions
pip install mkdocs-material[imaging]

# Option 3: With specific version
pip install mkdocs-material==9.5.3
```

**Verify Installation**:
```bash
mkdocs --version
# Should output: mkdocs, version X.X.X
```

### Step 2: Install Optional Plugins

```bash
# For faster builds
pip install mkdocs-minify-plugin

# For better search
pip install mkdocs-search

# For PDF export (optional)
pip install mkdocs-with-pdf
```

### Step 3: Clone/Download Project

**If you have Git**:
```bash
git clone <your-repo-url>
cd ai-learning-syllabus-interactive
```

**If no Git**:
1. Download ZIP from GitHub
2. Extract to desired location
3. Navigate to extracted folder

### Step 4: Verify Project Structure

```
mkdocs-interactive/
├── mkdocs.yml                 # Configuration
├── docs/
│   ├── index.md              # Homepage
│   ├── dashboard.md          # Progress dashboard
│   ├── topics/               # All topic pages
│   │   └── transformer-architecture.md
│   ├── tracks/               # Study tracks
│   ├── reference/            # Quick references
│   ├── assessments/          # Checkpoints
│   ├── javascripts/
│   │   ├── progress-tracker.js    # Progress tracking
│   │   ├── notes-manager.js       # Notes functionality
│   │   └── localStorage-sync.js   # Data persistence
│   └── stylesheets/
│       ├── extra.css
│       └── progress-tracker.css
└── SETUP-GUIDE.md            # This file
```

---

## Local Development

### Start Development Server

```bash
mkdocs serve
```

**Output**:
```
INFO    -  Building documentation...
INFO    -  Cleaning site directory
INFO    -  Documentation built in 0.52 seconds
INFO    -  [15:23:45] Watching paths for changes: 'docs', 'mkdocs.yml'
INFO    -  [15:23:45] Serving on http://127.0.0.1:8000/
```

### Access Your Site
Open browser to: **http://127.0.0.1:8000**

### Live Reload
Changes to files automatically refresh the browser.

### Custom Port
```bash
mkdocs serve --dev-addr=127.0.0.1:8080
```

---

## Deployment Options

### Option 1: GitHub Pages (Free, Recommended)

**Step 1**: Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit: AI Learning Syllabus"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-syllabus.git
git push -u origin main
```

**Step 2**: Deploy
```bash
mkdocs gh-deploy
```

**What This Does**:
1. Builds static site
2. Pushes to `gh-pages` branch
3. Configures GitHub Pages automatically

**Access**: `https://YOUR-USERNAME.github.io/ai-syllabus/`

**Update Deployment**:
```bash
# Make changes to docs/
git add .
git commit -m "Updated content"
git push
mkdocs gh-deploy  # Deploy changes
```

---

### Option 2: Netlify (Free, Easy)

**Step 1**: Create `netlify.toml`
```toml
[build]
  command = "mkdocs build"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.9"
```

**Step 2**: Connect to Netlify
1. Go to [app.netlify.com](https://app.netlify.com)
2. "New site from Git"
3. Connect your GitHub repo
4. Deploy settings:
   - Build command: `mkdocs build`
   - Publish directory: `site`

**Access**: `https://YOUR-SITE-NAME.netlify.app`

**Automatic Deploys**: Pushes to `main` branch auto-deploy

---

### Option 3: Vercel (Free, Fast)

**Step 1**: Create `vercel.json`
```json
{
  "buildCommand": "mkdocs build",
  "outputDirectory": "site",
  "installCommand": "pip install mkdocs-material"
}
```

**Step 2**: Deploy
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

**Access**: `https://YOUR-PROJECT.vercel.app`

---

### Option 4: Docker (Self-Hosted)

**Step 1**: Create `Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /docs

# Install dependencies
RUN pip install --no-cache-dir mkdocs-material

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Serve
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
```

**Step 2**: Build and Run
```bash
# Build image
docker build -t ai-syllabus .

# Run container
docker run -p 8000:8000 ai-syllabus
```

**Access**: `http://localhost:8000`

---

### Option 5: Static Export (Any Host)

```bash
# Build static site
mkdocs build

# Output to site/ directory
ls site/
# index.html, assets/, topics/, etc.
```

**Upload `site/` folder to**:
- AWS S3 + CloudFront
- Firebase Hosting
- Cloudflare Pages
- Any web host (Apache, Nginx)

---

## Configuration

### Customize `mkdocs.yml`

**Change Site Name**:
```yaml
site_name: My AI Learning Journey
```

**Change Colors**:
```yaml
theme:
  palette:
    primary: teal      # Options: red, pink, purple, indigo, blue, teal, green
    accent: lime       # Options: same as above
```

**Add Google Analytics**:
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

**Add Social Links**:
```yaml
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourusername
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/yourusername
```

---

## Progress Tracking Technical Details

### How It Works

**1. localStorage**:
```javascript
// Data structure
{
  "topics": {
    "part1-transformer-architecture": {
      "completed": true,
      "completedDate": "2025-01-15T10:30:00Z"
    }
  },
  "notes": {
    "part1-transformer-architecture": {
      "content": "My notes...",
      "lastUpdated": "2025-01-15T11:00:00Z"
    }
  },
  "startDate": "2025-01-01T00:00:00Z",
  "lastUpdated": "2025-01-15T11:00:00Z"
}
```

**2. Events**:
- Checkbox change → save to localStorage → update dashboard
- Textarea blur → save notes → update timestamp
- Page load → load progress → render UI

**3. Dashboard**:
- Calculates overall progress
- Tracks completion dates
- Shows recent topics
- Calculates streaks

### Data Export

**Manual Export**:
```javascript
// Open browser console
const data = localStorage.getItem('ai-syllabus-progress');
console.log(JSON.parse(data));

// Or use Export button in dashboard
```

**Backup Script**:
```javascript
// Save to file
function exportProgress() {
    const data = localStorage.getItem('ai-syllabus-progress');
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `progress-backup-${new Date().toISOString()}.json`;
    a.click();
}
```

### Data Migration

**Between Browsers**:
1. Export from Browser A (JSON file)
2. Open Browser B
3. Open console:
```javascript
// Paste JSON content
const data = {...};  // Your exported data
localStorage.setItem('ai-syllabus-progress', JSON.stringify(data));
location.reload();
```

**Between Devices**:
- No automatic sync (localStorage is local)
- Options:
  - Manual export/import
  - Cloud sync (requires custom backend)
  - Browser profile sync (Chrome/Firefox)

---

## Customization

### Add New Topics

**Step 1**: Create topic file
```bash
# Create new file
touch docs/topics/new-topic.md
```

**Step 2**: Add content with tracking
```markdown
# New Topic Title

<div data-topic-id="part1-new-topic">

## Content here...

</div>
```

**Step 3**: Add to navigation
```yaml
# mkdocs.yml
nav:
  - Foundation Topics:
    - New Topic: topics/new-topic.md
```

### Modify Styles

**Edit `docs/stylesheets/progress-tracker.css`**:

```css
/* Change primary color */
:root {
  --custom-primary: #ff6b6b;
}

.progress-bar-fill {
  background: var(--custom-primary);
}
```

### Add Custom JavaScript

**Create `docs/javascripts/custom.js`**:
```javascript
// Your custom code
console.log("Custom JS loaded!");
```

**Add to `mkdocs.yml`**:
```yaml
extra_javascript:
  - javascripts/custom.js
```

---

## Troubleshooting

### Issue: "mkdocs: command not found"

**Solution**:
```bash
# Check Python installation
python --version

# Reinstall MkDocs
pip install --upgrade mkdocs-material

# Check PATH
which mkdocs  # Unix/Mac
where mkdocs  # Windows
```

### Issue: Progress not saving

**Debug**:
```javascript
// Open browser console
console.log(localStorage.getItem('ai-syllabus-progress'));

// If null, check:
// 1. Browser in private/incognito mode? (localStorage disabled)
// 2. Storage quota exceeded?
// 3. JavaScript errors? (check console)
```

**Solution**:
- Exit private/incognito mode
- Clear some browser data to free space
- Check browser console for errors

### Issue: Styles not loading

**Debug**:
```bash
# Check file exists
ls docs/stylesheets/progress-tracker.css

# Check mkdocs.yml
cat mkdocs.yml | grep progress-tracker.css
```

**Solution**:
```yaml
# Ensure in mkdocs.yml
extra_css:
  - stylesheets/progress-tracker.css
```

### Issue: Slow build times

**Optimize**:
```bash
# Install minify plugin
pip install mkdocs-minify-plugin

# Add to mkdocs.yml
plugins:
  - minify:
      minify_html: true
```

### Issue: 404 on GitHub Pages

**Check**:
1. Repository settings → Pages → Source = `gh-pages` branch
2. Wait 2-3 minutes after `mkdocs gh-deploy`
3. Check GitHub Actions tab for errors
4. Verify `index.html` exists in `gh-pages` branch

---

## Performance Optimization

### Build Speed
```yaml
# mkdocs.yml - Enable caching
plugins:
  - search:
      prebuild_index: true
```

### Page Load Speed
```yaml
# Enable compression
plugins:
  - minify:
      minify_html: true
      minify_js: true
      minify_css: true
```

### Search Optimization
```yaml
plugins:
  - search:
      separator: '[\s\-\.]+'
      lang:
        - en
```

---

## Monitoring & Analytics

### Add Google Analytics

```yaml
# mkdocs.yml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

### Add Plausible (Privacy-Friendly)

```html
<!-- docs/overrides/main.html -->
{% extends "base.html" %}

{% block scripts %}
  {{ super() }}
  <script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
{% endblock %}
```

### Custom Event Tracking

```javascript
// Track topic completions
function trackCompletion(topicId) {
    if (typeof gtag === 'function') {
        gtag('event', 'topic_completed', {
            'topic_id': topicId
        });
    }
}
```

---

## Backup & Recovery

### Automated Backup

**Create `backup.sh`**:
```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR
cp -r docs/ $BACKUP_DIR/
cp mkdocs.yml $BACKUP_DIR/

echo "Backup created: $BACKUP_DIR"
```

**Schedule with cron**:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

### Version Control

```bash
# Commit regularly
git add .
git commit -m "Progress checkpoint: $(date +%Y-%m-%d)"
git push
```

---

## FAQ

### Can multiple people use this?
Yes, but each user needs their own browser profile or separate progress exports.

### Does it work offline?
Yes! After first load, all content is cached. Progress tracking works offline too.

### Can I use custom domain?
Yes! All deployment options support custom domains:
- GitHub Pages: Settings → Pages → Custom domain
- Netlify: Domain settings
- Vercel: Project settings → Domains

### Can I password-protect it?
- GitHub Pages: Not natively (use Cloudflare Access)
- Netlify: Identity & Access control (paid)
- Self-hosted: Use HTTP basic auth

### How to reset all progress?
```javascript
// Browser console
localStorage.removeItem('ai-syllabus-progress');
location.reload();
```

Or use "Reset Progress" button in dashboard.

---

## Next Steps

1. **✅ Run Locally**: `mkdocs serve`
2. **🎨 Customize**: Edit colors, add logo
3. **📝 Start Learning**: Mark first topic complete
4. **🚀 Deploy**: Choose deployment option
5. **📤 Share**: Send link to friends/colleagues

---

## Support

**Issues?** Check:
1. [MkDocs Material Docs](https://squidfunk.github.io/mkdocs-material/)
2. [GitHub Issues](https://github.com/YOUR-REPO/issues)
3. [Stack Overflow](https://stackoverflow.com/questions/tagged/mkdocs)

**Want to contribute?**
- Fork the repo
- Make improvements
- Submit pull request

---

**Happy Learning!** 🚀
