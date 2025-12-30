// DevTools Snippet: ScrapeWorkday
// Usage: Chrome DevTools > Sources > Snippets > Run (Ctrl+Enter)
// Saves current page as Markdown file

(function() {
    const content = document.querySelector('article') ||
                    document.querySelector('.main-content') ||
                    document.querySelector('main') ||
                    document.querySelector('#content') ||
                    document.body;

    if (!content) {
        console.error("Could not find content!");
        return;
    }

    // Clone and clean
    const clone = content.cloneNode(true);
    ['nav', 'header', 'footer', '.sidebar', 'button', 'script', 'style', '.ads', '.cookie-banner']
        .forEach(sel => clone.querySelectorAll(sel).forEach(el => el.remove()));

    const text = clone.innerText.replace(/\n\s*\n/g, '\n\n');
    const title = document.title;
    const url = window.location.href;

    const output = `# ${title}\n\n**Source:** ${url}\n**Scraped:** ${new Date().toISOString()}\n\n---\n\n${text}\n`;

    // Auto-download as .md file
    const blob = new Blob([output], { type: 'text/markdown' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = title.replace(/[^a-z0-9]/gi, '_').substring(0, 50) + ".md";
    a.click();

    // Also copy to clipboard
    navigator.clipboard.writeText(output).then(() => {
        console.log("✅ Downloaded + Copied to clipboard!");
        console.log("Title:", title);
    });
})();
