# Presentation Generation Best Practices

## Last Updated: 2025-10-17
## Purpose: Preserve lessons learned from creating professional presentations with Reveal.js

---

## 1. Full-Screen Layout Configuration

### Critical CSS Settings

```css
/* Root container - full viewport */
html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

/* Reveal.js container */
.reveal {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Individual slides - MUST be full screen with scrolling */
.reveal .slides section {
    padding: 2vh 3vw 80px 3vw;  /* Bottom padding for footer clearance */
    height: 100vh;
    overflow-y: auto;
}
```

### Why This Works
- **height: 100vh**: Ensures each slide takes full viewport height
- **overflow-y: auto**: Enables scrolling for content taller than viewport
- **padding bottom: 80px**: Prevents content from being hidden behind fixed footer

---

## 2. Global Footer (Outside Slides)

### Problem: Slide-Level Footers Don't Work
Individual slide footers get scrolled out of view when content overflows.

### Solution: Global Fixed Footer

```html
<!-- OUTSIDE .reveal container -->
<div class="global-footer">
    <div class="logo-text">ERPA | AWS Multi-Agent RAG Chatbot</div>
    <div class="slide-info">
        <span id="slide-number">Slide 1 of 17</span> | Oct 2025 | Confidential
    </div>
</div>
```

```css
.global-footer {
    position: fixed;
    bottom: 10px;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    font-size: 0.7em;
    color: var(--dark-blue);
    opacity: 0.6;
    z-index: 10000;  /* Above all slides */
    pointer-events: none;  /* Allows clicking through footer */
}

/* Hide individual slide footers */
.slide-footer {
    display: none !important;
}
```

---

## 3. Dynamic Slide Numbering

### JavaScript Implementation

```javascript
Reveal.initialize({
    width: '100%',
    height: '100%',
    margin: 0,
    minScale: 1,
    maxScale: 1,
    controls: true,
    progress: true,
    center: false,
    hash: true,
    transition: 'slide',
    transitionSpeed: 'default',
    backgroundTransition: 'fade'
});

// Update slide number in global footer
Reveal.on('slidechanged', event => {
    const currentSlide = event.indexh + 1;
    const totalSlides = Reveal.getTotalSlides();
    document.getElementById('slide-number').textContent = `Slide ${currentSlide} of ${totalSlides}`;
});

// Initialize slide number on load
Reveal.on('ready', event => {
    const currentSlide = event.indexh + 1;
    const totalSlides = Reveal.getTotalSlides();
    document.getElementById('slide-number').textContent = `Slide ${currentSlide} of ${totalSlides}`;
});
```

---

## 4. Custom Scrollbar Styling

### ERPA-Branded Scrollbar

```css
.reveal .slides section::-webkit-scrollbar {
    width: 8px;
}

.reveal .slides section::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.reveal .slides section::-webkit-scrollbar-thumb {
    background: var(--erpa-blue);
    border-radius: 4px;
}
```

---

## 5. ERPA Color Palette

### Standard Colors (Always Use These)

```css
:root {
    --erpa-blue: #0072BC;
    --erpa-green: #7EBA39;
    --dark-blue: #003366;
    --light-blue: #66B2FF;
    --success-green: #28A745;
    --warning-yellow: #FFC107;
    --danger-red: #DC3545;
    --light-gray: #F8F9FA;
}
```

### Usage Guidelines
- **Primary headings**: `var(--erpa-blue)`
- **Accent/borders**: `var(--erpa-green)`
- **Success states**: `var(--success-green)`
- **Warning states**: `var(--warning-yellow)`
- **Danger/blocked states**: `var(--danger-red)`

---

## 6. Reusable Component Styles

### Stats Grid

```css
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.stat-box {
    background: linear-gradient(135deg, var(--erpa-blue) 0%, var(--dark-blue) 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 2.5em;
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9em;
    opacity: 0.9;
}
```

### Feature Cards

```css
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.feature-card {
    background: white;
    border-left: 4px solid var(--erpa-green);
    padding: 15px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.feature-card h4 {
    color: var(--erpa-blue);
    margin-bottom: 8px;
    font-size: 1em;
}

.feature-card p {
    font-size: 0.85em;
    color: #666;
}
```

### Cost Tables

```css
.cost-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.85em;
}

.cost-table th {
    background: var(--erpa-blue);
    color: white;
    padding: 12px;
    text-align: left;
    font-weight: 600;
}

.cost-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #ddd;
}

.cost-table tr:nth-child(even) {
    background: var(--light-gray);
}

.cost-table .highlight {
    background: #d4edda !important;
    font-weight: 600;
}
```

### Scenario Boxes (Security Examples)

```css
.scenario-box {
    background: #fff3cd;
    border-left: 5px solid var(--warning-yellow);
    padding: 15px;
    margin: 15px 0;
    border-radius: 5px;
}

.scenario-box.blocked {
    background: #f8d7da;
    border-left-color: var(--danger-red);
}

.scenario-box.allowed {
    background: #d4edda;
    border-left-color: var(--success-green);
}

.scenario-title {
    font-weight: 600;
    color: var(--dark-blue);
    margin-bottom: 8px;
    font-size: 1em;
}

.scenario-query {
    font-family: 'Courier New', monospace;
    background: white;
    padding: 10px;
    border-radius: 3px;
    margin: 8px 0;
    font-size: 0.85em;
}

.scenario-response {
    font-style: italic;
    color: #666;
    font-size: 0.85em;
}
```

### Code Blocks

```css
.code-block {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 0.75em;
    overflow-x: auto;
    margin: 15px 0;
}
```

### Architecture Flow (ASCII Art)

```css
.arch-flow {
    background: var(--light-gray);
    padding: 20px;
    border-radius: 10px;
    margin: 20px 0;
    font-family: 'Courier New', monospace;
    font-size: 0.8em;
    line-height: 1.8;
}
```

### Timeline

```css
.timeline {
    position: relative;
    padding-left: 30px;
    margin: 20px 0;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--erpa-green);
}

.timeline-item {
    position: relative;
    margin-bottom: 20px;
    padding-left: 15px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -23px;
    top: 5px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--erpa-blue);
    border: 3px solid white;
    box-shadow: 0 0 0 3px var(--erpa-green);
}

.timeline-item h4 {
    color: var(--erpa-blue);
    font-size: 0.95em;
    margin-bottom: 5px;
}

.timeline-item p {
    font-size: 0.8em;
    color: #666;
}
```

### Highlight Boxes

```css
.highlight-box {
    background: linear-gradient(135deg, #fff9e6 0%, #ffe6cc 100%);
    border: 2px solid var(--warning-yellow);
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}

.highlight-box.success {
    background: linear-gradient(135deg, #e6f9e6 0%, #ccf2cc 100%);
    border-color: var(--success-green);
}

.highlight-box.danger {
    background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%);
    border-color: var(--danger-red);
}
```

---

## 7. Common Pitfalls & Solutions

### Pitfall 1: Footer Hidden by Scrolling Content
**Problem**: Individual `.slide-footer` divs scroll out of view.
**Solution**: Use global fixed footer outside `.reveal` container.

### Pitfall 2: Content Cut Off at Bottom
**Problem**: Last elements hidden behind footer.
**Solution**: Add `padding-bottom: 80px` to `.reveal .slides section`.

### Pitfall 3: Slide Not Full Height
**Problem**: Slides don't fill viewport, creating white space.
**Solution**: Set `height: 100vh` on `.reveal .slides section`.

### Pitfall 4: Inconsistent Slide Numbering
**Problem**: Slide numbers don't update or show wrong total.
**Solution**: Use `Reveal.getTotalSlides()` and update on `slidechanged` + `ready` events.

### Pitfall 5: Scrollbar Appears Suddenly
**Problem**: Scrollbar pops in abruptly when content overflows.
**Solution**: Always set `overflow-y: auto` even if current content fits (allows smooth overflow).

---

## 8. Presentation Delivery in Teams Chatbot

### Use Case
User asks chatbot: "Create a PowerPoint presentation about Q3 budget analysis"

### Workflow
1. **Complexity Analysis**: Score 9/10 (complex, multi-domain, visual)
2. **AI Selection**: Claude 3.5 Sonnet (best for structured content)
3. **RAG Query**: Finance KB + Q3 budget documents
4. **Content Generation**:
   - Outline (8-12 slides)
   - Title, bullet points, chart data per slide
5. **File Creation**: Lambda invokes python-pptx → Generate PPTX
6. **Upload**: S3 bucket → `presentations/{user_id}/q3-budget-analysis.pptx`
7. **Delivery**: Return to Teams (see options below)

### Delivery Options (Recommended Order)

#### Option 1: S3 Pre-Signed URL (MVP - Fastest)
```python
# Generate 15-minute pre-signed URL
url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'erpa-chatbot-generated', 'Key': file_key},
    ExpiresIn=900  # 15 minutes
)

# Return to Teams
return {
    "type": "message",
    "text": f"Your presentation is ready! [Download Q3 Budget Analysis.pptx]({url})\n\nLink expires in 15 minutes."
}
```

**Pros**: Simple, fast, works for all file types
**Cons**: External link, 15-minute expiry window
**Cost**: ~$0.0004 per GET request (essentially FREE)

#### Option 2: Teams File Attachment (Native Experience)
```python
# Upload to SharePoint/OneDrive via Microsoft Graph API
graph_client.me.drive.items.by_id(folder_id).children.post({
    "name": "q3-budget-analysis.pptx",
    "file": open('/tmp/q3-budget-analysis.pptx', 'rb')
})

# Send as Teams attachment
activity = {
    "type": "message",
    "attachments": [{
        "contentType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "contentUrl": sharepoint_url,
        "name": "Q3 Budget Analysis.pptx"
    }]
}
```

**Pros**: Native Teams experience, permanent link, opens in Office
**Cons**: Requires SharePoint API setup, OAuth token management
**Cost**: FREE (SharePoint storage already owned)

#### Option 3: Adaptive Card Preview (Best UX - Production)
```python
# Generate thumbnail (first slide preview)
from pptx import Presentation
from PIL import Image

prs = Presentation('/tmp/q3-budget-analysis.pptx')
slide = prs.slides[0]
# Convert to image, save thumbnail

# Upload thumbnail to S3
s3.upload_file(thumbnail_path, bucket, f'thumbnails/{file_key}.png')

# Create Adaptive Card
adaptive_card = {
    "type": "AdaptiveCard",
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.4",
    "body": [
        {
            "type": "TextBlock",
            "text": "Q3 Budget Analysis Presentation Ready",
            "weight": "bolder",
            "size": "large"
        },
        {
            "type": "Image",
            "url": thumbnail_url,
            "size": "large"
        },
        {
            "type": "TextBlock",
            "text": "10 slides • Generated in 3.2s • PPTX format",
            "isSubtle": True
        }
    ],
    "actions": [
        {
            "type": "Action.OpenUrl",
            "title": "Download PPTX",
            "url": presigned_url
        }
    ]
}
```

**Pros**: Beautiful UX, shows preview before download, professional appearance
**Cons**: Extra Lambda invocation for thumbnail (~200ms)
**Cost**: ~$0.001 per presentation (Lambda + S3)

#### Option 4: Email with Attachment (Compliance/Offline)
```python
import boto3
ses = boto3.client('ses')

# Send email via SES
ses.send_raw_email(
    Source='noreply@erpa.edu',
    Destinations=[user_email],
    RawMessage={
        'Data': email_with_attachment  # MIME-encoded with PPTX
    }
)
```

**Pros**: Works offline, compliance archival, permanent record
**Cons**: Slower delivery, requires email address in chat context
**Cost**: $0.0001 per email (SES)

### Recommended Strategy
- **MVP (Weeks 1-4)**: Option 1 (S3 Pre-Signed URL) - Fastest to implement
- **Production (Weeks 9+)**: Option 3 (Adaptive Card Preview) - Best UX
- **Compliance**: Option 4 (Email) - For regulated departments (Finance, Legal)

### python-pptx Lambda Layer Setup

```bash
# Create layer directory
mkdir -p python/lib/python3.11/site-packages
cd python/lib/python3.11/site-packages

# Install dependencies
pip install python-pptx Pillow -t .

# Create ZIP
cd ../../../../
zip -r pptx-layer.zip python

# Upload to Lambda Layer (via AWS Console or CLI)
aws lambda publish-layer-version \
    --layer-name pptx-generation \
    --zip-file fileb://pptx-layer.zip \
    --compatible-runtimes python3.11
```

**Layer Size**: ~25 MB (well within 50 MB Lambda layer limit)

### Performance Benchmarks
- **10-slide PPTX**: 2-4 seconds (including S3 upload)
- **20-slide PPTX**: 5-8 seconds
- **Cost per presentation**: ~$0.002 (Lambda compute + S3 storage)

---

## 9. File Organization

### Recommended Structure
```
projects/
└── aws-chatbot/
    ├── aws-chatbot-presentation.html           # Original (11 slides, 71% cost savings)
    ├── erpa-aws-multi-agent-chatbot-presentation.html  # Enhanced (17 slides, 89% savings)
    └── docs/
        ├── COMPLETE-COST-ANALYSIS-WITH-AGENTS.md
        ├── MULTI-AI-ORCHESTRATION-COST-OPTIMIZATION.md
        ├── SECURITY-JAILBREAK-DEFENSE.md
        └── ... (other documentation)
```

### When to Use Which Presentation
- **aws-chatbot-presentation.html**: Technical teams, architecture review, implementation planning
- **erpa-aws-multi-agent-chatbot-presentation.html**: Executive review, budget approval, comprehensive feature overview

---

## 10. Checklist for New Presentations

Before creating a new presentation, ensure:

- [ ] Full-screen layout (height: 100vh, overflow-y: auto)
- [ ] Global footer outside `.reveal` container
- [ ] Dynamic slide numbering JavaScript
- [ ] ERPA color palette CSS variables
- [ ] Custom scrollbar styling
- [ ] Responsive grid layouts (auto-fit, minmax)
- [ ] Code blocks with syntax highlighting
- [ ] Scenario boxes for examples
- [ ] Timeline for step-by-step flows
- [ ] Stats grids for key metrics
- [ ] Highlight boxes for important callouts
- [ ] Bottom padding (80px) for footer clearance

---

## 11. Memory Preservation

### Store in Global Memory
After creating presentations, always store:

1. **Architecture decisions**: Why certain features were included
2. **Cost analysis**: Tier comparisons, savings calculations
3. **Delivery options**: Teams bot file delivery methods
4. **Performance benchmarks**: Generation times, file sizes
5. **Lessons learned**: What worked, what didn't

### Example Memory Entry

```python
mcp__memory-auto__auto_store_memory({
    "content": """
    AWS Multi-Agent RAG Chatbot Presentation (2025-10-17)

    Key Decisions:
    - Two separate presentations: Original (11 slides) for technical, Enhanced (17 slides) for executive
    - Full-screen layout with overflow-y: auto per slide (prevents content cutoff)
    - Global fixed footer outside slides container (always visible)
    - Dynamic slide numbering via Reveal.js events

    Presentation Delivery in Teams:
    - Option 1: S3 Pre-Signed URL (MVP, 15-min expiry, FREE)
    - Option 2: SharePoint Attachment (native Teams, permanent link)
    - Option 3: Adaptive Card Preview (best UX, thumbnail preview)
    - Option 4: Email Attachment (compliance, offline)

    Recommended: Option 1 for MVP, Option 3 for production

    python-pptx Layer: 25 MB, generates 10-slide PPTX in 2-4s, cost $0.002/presentation
    """,
    "project_name": "aws-chatbot"
})
```

---

## 12. Future Enhancements

### Potential Improvements
1. **Interactive Charts**: Embed Chart.js/D3.js for dynamic visualizations
2. **Video Embeds**: Add YouTube/Vimeo iframe embeds
3. **Presenter Notes**: Use Reveal.js speaker notes feature
4. **PDF Export**: Add PDF generation from HTML (Puppeteer)
5. **Theme Switcher**: Dark mode toggle
6. **Analytics**: Track slide views, time spent per slide

### Advanced Features (Phase 3+)
- **Real-time Collaboration**: Multiple users editing same presentation
- **Version Control**: Track changes, rollback to previous versions
- **Template Library**: Pre-built templates for common use cases
- **AI Refinement**: "Make this slide more visual" → Auto-add charts/images

---

## End of Document

**Last Updated**: 2025-10-17
**Author**: Claude (with user collaboration)
**Project**: ERPA AWS Multi-Agent RAG Chatbot
**Next Review**: When creating next presentation (to validate/update best practices)
