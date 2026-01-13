const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SCREENSHOT_DIR = path.join(__dirname, 'screenshots');
const BASE_URL = 'http://54.173.231.4';
const LOGIN_EMAIL = 'sainath.dadireddy@erpa.com';
const LOGIN_PASSWORD = 'Wel#$come@321';

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function captureDashboard() {
    if (!fs.existsSync(SCREENSHOT_DIR)) {
        fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    }

    const browser = await chromium.launch({
        headless: false,
        slowMo: 200
    });
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    const page = await context.newPage();

    let screenshotIndex = 1;
    function nextIndex() {
        return String(screenshotIndex++).padStart(2, '0');
    }

    const results = {
        url: BASE_URL,
        timestamp: new Date().toISOString(),
        screenshots: [],
        navigation: { sidebar: [], topbar: [] },
        features: [],
        uiComponents: [],
        pageStructure: {},
        dataDisplayed: [],
        uxAnalysis: {}
    };

    try {
        // STEP 1: Navigate
        console.log('=== STEP 1: Navigate to dashboard ===');
        await page.goto(BASE_URL + '/dashboard', { waitUntil: 'networkidle', timeout: 30000 });
        await delay(2000);

        results.pageTitle = await page.title();
        console.log('Page title:', results.pageTitle);
        console.log('Current URL:', page.url());

        await page.screenshot({ path: path.join(SCREENSHOT_DIR, nextIndex() + '-initial-page.png'), fullPage: true });
        results.screenshots.push('01-initial-page.png');

        // STEP 2: Login
        console.log('\n=== STEP 2: Login ===');

        // Wait for form to be ready
        await page.waitForSelector('input[placeholder*="Email" i], input[placeholder*="email" i]', { timeout: 5000 }).catch(() => {});

        // Try multiple selectors for email input
        const emailInput = await page.$('input[placeholder*="Email" i]')
            || await page.$('input[type="email"]')
            || await page.$('input[name="email"]');
        const passwordInput = await page.$('input[placeholder*="Password" i]')
            || await page.$('input[type="password"]');

        if (emailInput && passwordInput) {
            console.log('Found email and password inputs');

            // Clear and fill email
            await emailInput.click();
            await delay(200);
            await emailInput.fill(LOGIN_EMAIL);
            console.log('Filled email');
            await delay(500);

            // Clear and fill password
            await passwordInput.click();
            await delay(200);
            await passwordInput.fill(LOGIN_PASSWORD);
            console.log('Filled password');
            await delay(500);

            await page.screenshot({ path: path.join(SCREENSHOT_DIR, nextIndex() + '-login-filled.png'), fullPage: true });
            results.screenshots.push('02-login-filled.png');

            // Find Sign In button - more specific selectors
            const loginBtn = await page.$('button:has-text("Sign In")')
                || await page.$('button:has-text("Login")')
                || await page.$('button[type="submit"]');

            if (loginBtn) {
                console.log('Clicking Sign In button...');
                await loginBtn.click();

                // Wait for navigation
                await Promise.race([
                    page.waitForURL('**/dashboard**', { timeout: 10000 }),
                    delay(5000)
                ]).catch(() => {});

                await page.waitForLoadState('networkidle').catch(() => {});
            } else {
                console.log('Login button not found!');
            }
            console.log('After login URL:', page.url());
        } else {
            console.log('Email input found:', !!emailInput);
            console.log('Password input found:', !!passwordInput);
        }

        // STEP 3: Dashboard Home
        console.log('\n=== STEP 3: Dashboard Home ===');
        await delay(2000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, nextIndex() + '-dashboard-home.png'), fullPage: true });
        results.screenshots.push('03-dashboard-home.png');

        // STEP 4: Analyze page structure
        console.log('\n=== STEP 4: Analyzing Page Structure ===');
        const pageAnalysis = await page.evaluate(() => {
            const analysis = {
                bodyClasses: document.body.className,
                hasNavbar: !!document.querySelector('nav, [class*="navbar"], [class*="header"], [class*="topbar"]'),
                hasSidebar: !!document.querySelector('[class*="sidebar"], [class*="sidenav"], aside, [class*="ant-layout-sider"]'),
                hasFooter: !!document.querySelector('footer'),
                framework: 'unknown'
            };
            if (document.querySelector('[class*="ant-"]')) analysis.framework = 'Ant Design';
            else if (document.querySelector('[class*="Mui"]')) analysis.framework = 'Material UI';
            else if (document.querySelector('[class*="chakra"]')) analysis.framework = 'Chakra UI';
            else if (document.querySelector('.btn')) analysis.framework = 'Bootstrap';
            return analysis;
        });
        results.pageStructure = pageAnalysis;
        console.log('Framework:', pageAnalysis.framework);
        console.log('Has Sidebar:', pageAnalysis.hasSidebar);

        // STEP 5: Get navigation items
        console.log('\n=== STEP 5: Navigation Items ===');
        const sidebarLinks = await page.evaluate(() => {
            const links = [];
            // Comprehensive selectors for navigation
            const selectors = [
                '.ant-menu-item',
                '.ant-menu-item-only-child',
                '.ant-menu-title-content',
                '[class*="sidebar"] a',
                '[class*="sidebar"] .ant-menu-item',
                '[class*="sider"] a',
                '[class*="sider"] .ant-menu-item',
                '.ant-layout-sider a',
                '.ant-layout-sider .ant-menu-item',
                'aside a',
                '[class*="nav-item"] a'
            ];
            for (const sel of selectors) {
                document.querySelectorAll(sel).forEach(el => {
                    const text = el.textContent ? el.textContent.trim() : '';
                    const href = el.getAttribute('href') || el.closest('a')?.getAttribute('href') || '#';
                    if (text && text.length > 0 && text.length < 50 && !links.some(l => l.text === text)) {
                        links.push({ text, href });
                    }
                });
            }
            return links;
        });
        results.navigation.sidebar = sidebarLinks;
        console.log('Sidebar items found:', sidebarLinks.length);
        console.log('Items:', sidebarLinks.map(l => l.text).join(' | '));

        // STEP 6: Navigate through pages
        console.log('\n=== STEP 6: Capturing All Pages ===');
        for (const navItem of sidebarLinks.slice(0, 15)) {
            try {
                console.log('Navigating to:', navItem.text);
                const menuItem = await page.$(`text="${navItem.text}"`);
                if (menuItem && await menuItem.isVisible()) {
                    await menuItem.click();
                    await delay(2000);
                    await page.waitForLoadState('networkidle').catch(() => {});

                    const safeName = navItem.text.toLowerCase().replace(/[^a-z0-9]/g, '-').substring(0, 30);
                    const filename = nextIndex() + '-page-' + safeName + '.png';
                    await page.screenshot({ path: path.join(SCREENSHOT_DIR, filename), fullPage: true });
                    results.screenshots.push(filename);
                    console.log('Captured:', filename);

                    // Check for tabs
                    const tabs = await page.$$('[role="tab"], .ant-tabs-tab');
                    for (let i = 0; i < Math.min(tabs.length, 4); i++) {
                        try {
                            await tabs[i].click();
                            await delay(1500);
                            const tabFilename = nextIndex() + '-' + safeName + '-tab' + (i+1) + '.png';
                            await page.screenshot({ path: path.join(SCREENSHOT_DIR, tabFilename), fullPage: true });
                            results.screenshots.push(tabFilename);
                        } catch (e) {}
                    }
                }
            } catch (e) {
                console.log('  Skip:', e.message);
            }
        }

        // STEP 7: Topbar interactions
        console.log('\n=== STEP 7: Topbar Interactions ===');
        const topbarBtns = await page.$$('header button, [class*="header"] button, .ant-layout-header button');
        for (let i = 0; i < Math.min(topbarBtns.length, 3); i++) {
            try {
                if (await topbarBtns[i].isVisible()) {
                    await topbarBtns[i].click();
                    await delay(1000);
                    const filename = nextIndex() + '-topbar-btn-' + (i+1) + '.png';
                    await page.screenshot({ path: path.join(SCREENSHOT_DIR, filename), fullPage: true });
                    results.screenshots.push(filename);
                    await page.keyboard.press('Escape');
                    await delay(500);
                }
            } catch (e) {}
        }

        // STEP 8: UI Components
        console.log('\n=== STEP 8: UI Components ===');
        const uiComponents = await page.evaluate(() => ({
            tables: document.querySelectorAll('table, .ant-table').length,
            cards: document.querySelectorAll('[class*="card"], .ant-card').length,
            charts: document.querySelectorAll('canvas, [class*="chart"]').length,
            forms: document.querySelectorAll('form').length,
            buttons: document.querySelectorAll('button').length,
            modals: document.querySelectorAll('[class*="modal"]').length,
            tabs: document.querySelectorAll('[role="tab"]').length,
            stats: document.querySelectorAll('.ant-statistic, [class*="stat"]').length
        }));
        results.uiComponents = uiComponents;
        console.log('Components:', JSON.stringify(uiComponents));

        // STEP 9: Responsive views
        console.log('\n=== STEP 9: Responsive Views ===');
        await page.setViewportSize({ width: 768, height: 1024 });
        await delay(1000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, nextIndex() + '-tablet-view.png'), fullPage: true });
        results.screenshots.push('tablet-view.png');

        await page.setViewportSize({ width: 375, height: 812 });
        await delay(1000);
        await page.screenshot({ path: path.join(SCREENSHOT_DIR, nextIndex() + '-mobile-view.png'), fullPage: true });
        results.screenshots.push('mobile-view.png');

        console.log('\n=== CAPTURE COMPLETE ===');
        console.log('Total screenshots:', results.screenshots.length);

    } catch (error) {
        console.error('Error:', error);
        results.error = error.message;
    } finally {
        await browser.close();
    }

    fs.writeFileSync(path.join(SCREENSHOT_DIR, 'analysis-results.json'), JSON.stringify(results, null, 2));
    return results;
}

captureDashboard().then(r => {
    console.log('\n========================================');
    console.log('Screenshots:', r.screenshots.length);
    console.log('Framework:', r.pageStructure ? r.pageStructure.framework : 'Unknown');
    console.log('Navigation items:', r.navigation.sidebar.length);
}).catch(e => {
    console.error('Fatal:', e);
    process.exit(1);
});
