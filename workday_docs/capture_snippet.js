// DevTools Snippet: WorkdayCapture
// Save in Chrome DevTools > Sources > Snippets
// Run with Ctrl+Enter after navigating to a page

(function() {
    const content = document.querySelector('article') ||
                    document.querySelector('.main-content') ||
                    document.querySelector('[role="main"]') ||
                    document.querySelector('main') ||
                    document.querySelector('#content') ||
                    document.querySelector('.content') ||
                    document.body;

    if (!content) {
        console.error("❌ Could not find content!");
        return;
    }

    // Clone and remove junk
    const clone = content.cloneNode(true);
    ['nav', 'header', 'footer', '.sidebar', '.navigation', '.breadcrumb',
     'button', 'script', 'style', '.ads', '.cookie-banner', '.modal',
     '[role="navigation"]', '[role="banner"]', '[aria-hidden="true"]']
        .forEach(sel => clone.querySelectorAll(sel).forEach(el => el.remove()));

    // Clean text
    const text = clone.innerText
        .replace(/\n\s*\n\s*\n/g, '\n\n')
        .replace(/^\s+/gm, '')
        .trim();

    const title = document.title.replace(/\s*\|.*$/, '').trim();
    const url = window.location.href;
    const timestamp = new Date().toISOString();
    const filename = title.replace(/[^a-z0-9]+/gi, '_').substring(0, 60) + '.md';

    // Format as Markdown
    const markdown = `# ${title}

**Source:** ${url}
**Captured:** ${timestamp}

---

${text}
`;

    // Create download
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();

    // Copy CSV row to clipboard for index_map
    const csvRow = `"${url}","${filename}","${title}","${timestamp}"`;
    navigator.clipboard.writeText(csvRow);

    console.log(`✅ CAPTURED: ${filename}`);
    console.log(`📋 CSV row copied to clipboard - paste into index_map.csv`);
    console.log(`Preview: ${text.substring(0, 200)}...`);
})();
