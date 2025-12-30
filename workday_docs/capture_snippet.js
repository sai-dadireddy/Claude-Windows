// DevTools Snippet: WorkdayCapture (Enhanced)
// Chrome DevTools > Sources > Snippets > New > Paste > Ctrl+S
// Run: Ctrl+Enter (or right-click > Run)

(function() {
    // --- CONFIGURATION ---
    const contentSelectors = ['article', '#main-content', '.main-content', 'main', 'div[role="main"]'];
    const junkSelectors = ['nav', 'header', 'footer', '.sidebar', 'button', '.toolbar', 'script', 'style', '.cookie-banner'];

    // --- MAIN LOGIC ---
    try {
        // 1. Find the content
        let contentNode = null;
        for (let sel of contentSelectors) {
            const el = document.querySelector(sel);
            if (el) { contentNode = el; break; }
        }
        if (!contentNode) contentNode = document.body;

        // 2. Clone and Clean
        const clone = contentNode.cloneNode(true);
        junkSelectors.forEach(sel => {
            clone.querySelectorAll(sel).forEach(el => el.remove());
        });

        // 3. Extract Meta Data
        const title = document.title.replace(/[^a-z0-9]/gi, '_').substring(0, 100);
        const url = window.location.href;
        const filename = `${title}.md`;
        const timestamp = new Date().toISOString();

        // 4. Build Markdown
        let markdown = `# Source: ${title}\n`;
        markdown += `# URL: ${url}\n`;
        markdown += `# Date: ${timestamp}\n`;
        markdown += `---------------------------------------------\n\n`;
        markdown += clone.innerText.replace(/\n\s*\n/g, '\n\n');

        // 5. TRIGGER DOWNLOAD
        const blob = new Blob([markdown], { type: 'text/markdown' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // 6. COPY CSV ROW
        const csvRow = `"${filename}","${url}","${document.title}","${timestamp}"`;
        navigator.clipboard.writeText(csvRow + "\n").then(() => {
            console.log(`✅ CAPTURED: ${filename}`);
            console.log(`📋 CSV Row copied to clipboard!`);
        });

    } catch (e) {
        console.error("Capture failed:", e);
        alert("Capture failed. Check console.");
    }
})();
