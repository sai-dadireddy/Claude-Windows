const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureDashboard() {
    const screenshotDir = path.join(__dirname, 'screenshots');
    if (!fs.existsSync(screenshotDir)) {
        fs.mkdirSync(screenshotDir, { recursive: true });
    }

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    const results = {
        url: 'http://54.173.231.4/dashboard',
        timestamp: new Date().toISOString(),
        screenshots: [],
        navigation: [],
        features: [],
        uiComponents: [],
        loginRequired: false,
        pageTitle: '',
        pageStructure: {}
    };

    try {
        console.log('Navigating to dashboard...');
        await page.goto('http://54.173.231.4/dashboard', {
            waitUntil: 'networkidle',
            timeout: 30000
        });

        // Wait a bit for any dynamic content
        await page.waitForTimeout(2000);

        // Get page title
        results.pageTitle = await page.title();
        console.log('Page title:', results.pageTitle);

        // Check if redirected to login
        const currentUrl = page.url();
        console.log('Current URL:', currentUrl);

        if (currentUrl.includes('login') || currentUrl.includes('auth')) {
            results.loginRequired = true;
            console.log('Login page detected');
        }

        // Take full page screenshot
        await page.screenshot({
            path: path.join(screenshotDir, '01-full-page.png'),
            fullPage: true
        });
        results.screenshots.push('01-full-page.png');
        console.log('Captured: 01-full-page.png');

        // Take viewport screenshot
        await page.screenshot({
            path: path.join(screenshotDir, '02-viewport.png')
        });
        results.screenshots.push('02-viewport.png');
        console.log('Captured: 02-viewport.png');

        // Analyze page structure
        const pageAnalysis = await page.evaluate(() => {
            const analysis = {
                bodyClasses: document.body.className,
                hasNavbar: false,
                hasSidebar: false,
                hasFooter: false,
                mainSections: [],
                buttons: [],
                links: [],
                forms: [],
                tables: [],
                cards: [],
                modals: [],
                framework: 'unknown'
            };

            // Check for common frameworks
            if (document.querySelector('[class*="ant-"]')) analysis.framework = 'Ant Design';
            else if (document.querySelector('[class*="MuiBox"]') || document.querySelector('[class*="MuiButton"]')) analysis.framework = 'Material UI';
            else if (document.querySelector('[class*="chakra"]')) analysis.framework = 'Chakra UI';
            else if (document.querySelector('[class*="bootstrap"]') || document.querySelector('.btn')) analysis.framework = 'Bootstrap';
            else if (document.querySelector('[class*="tailwind"]') || document.querySelector('[class*="bg-"]')) analysis.framework = 'Tailwind CSS';

            // Check for navigation elements
            analysis.hasNavbar = !!document.querySelector('nav, [class*="navbar"], [class*="header"], [class*="topbar"]');
            analysis.hasSidebar = !!document.querySelector('[class*="sidebar"], [class*="sidenav"], aside');
            analysis.hasFooter = !!document.querySelector('footer, [class*="footer"]');

            // Get all main sections
            document.querySelectorAll('section, [class*="section"], main, [class*="content"]').forEach(el => {
                if (el.className) {
                    analysis.mainSections.push(el.className.split(' ').slice(0, 3).join(' '));
                }
            });

            // Get buttons
            document.querySelectorAll('button, [class*="btn"], [role="button"]').forEach(btn => {
                const text = btn.textContent?.trim().substring(0, 50);
                if (text && !analysis.buttons.includes(text)) {
                    analysis.buttons.push(text);
                }
            });

            // Get navigation links
            document.querySelectorAll('nav a, [class*="nav"] a, [class*="menu"] a').forEach(link => {
                const text = link.textContent?.trim();
                const href = link.getAttribute('href');
                if (text && href) {
                    analysis.links.push({ text: text.substring(0, 30), href });
                }
            });

            // Count forms, tables, cards
            analysis.forms = document.querySelectorAll('form').length;
            analysis.tables = document.querySelectorAll('table').length;
            analysis.cards = document.querySelectorAll('[class*="card"]').length;
            analysis.modals = document.querySelectorAll('[class*="modal"], [class*="dialog"], [role="dialog"]').length;

            return analysis;
        });

        results.pageStructure = pageAnalysis;
        console.log('Page analysis:', JSON.stringify(pageAnalysis, null, 2));

        // Try to find and capture sidebar if exists
        const sidebar = await page.$('[class*="sidebar"], [class*="sidenav"], aside');
        if (sidebar) {
            await sidebar.screenshot({
                path: path.join(screenshotDir, '03-sidebar.png')
            });
            results.screenshots.push('03-sidebar.png');
            console.log('Captured: 03-sidebar.png');
        }

        // Try to find and capture header/navbar
        const navbar = await page.$('nav, [class*="navbar"], [class*="header"], [class*="topbar"]');
        if (navbar) {
            await navbar.screenshot({
                path: path.join(screenshotDir, '04-navbar.png')
            });
            results.screenshots.push('04-navbar.png');
            console.log('Captured: 04-navbar.png');
        }

        // Get all visible text content for feature analysis
        const visibleText = await page.evaluate(() => {
            const walker = document.createTreeWalker(
                document.body,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );
            const texts = [];
            let node;
            while (node = walker.nextNode()) {
                const text = node.textContent?.trim();
                if (text && text.length > 2 && text.length < 100) {
                    texts.push(text);
                }
            }
            return [...new Set(texts)].slice(0, 100);
        });
        results.visibleText = visibleText;

        // Check for any interactive elements
        const interactiveElements = await page.evaluate(() => {
            const elements = [];
            document.querySelectorAll('button, a, input, select, [onclick], [class*="clickable"]').forEach(el => {
                const tag = el.tagName.toLowerCase();
                const text = el.textContent?.trim().substring(0, 30) || el.getAttribute('placeholder') || '';
                const type = el.getAttribute('type') || '';
                elements.push({ tag, text, type });
            });
            return elements.slice(0, 50);
        });
        results.interactiveElements = interactiveElements;

        // Mobile viewport screenshot
        await page.setViewportSize({ width: 375, height: 812 });
        await page.waitForTimeout(1000);
        await page.screenshot({
            path: path.join(screenshotDir, '05-mobile-view.png'),
            fullPage: true
        });
        results.screenshots.push('05-mobile-view.png');
        console.log('Captured: 05-mobile-view.png');

        // Tablet viewport screenshot
        await page.setViewportSize({ width: 768, height: 1024 });
        await page.waitForTimeout(1000);
        await page.screenshot({
            path: path.join(screenshotDir, '06-tablet-view.png'),
            fullPage: true
        });
        results.screenshots.push('06-tablet-view.png');
        console.log('Captured: 06-tablet-view.png');

    } catch (error) {
        console.error('Error:', error.message);
        results.error = error.message;
    } finally {
        await browser.close();
    }

    // Save results to JSON
    fs.writeFileSync(
        path.join(screenshotDir, 'analysis-results.json'),
        JSON.stringify(results, null, 2)
    );
    console.log('\nAnalysis saved to analysis-results.json');
    console.log('Screenshots saved to:', screenshotDir);

    return results;
}

captureDashboard().then(results => {
    console.log('\n=== DASHBOARD ANALYSIS COMPLETE ===\n');
    console.log(JSON.stringify(results, null, 2));
}).catch(err => {
    console.error('Fatal error:', err);
    process.exit(1);
});
