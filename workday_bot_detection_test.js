/**
 * Workday Bot Detection Analysis Script
 * Tests for various security measures on the Workday login page
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TARGET_URL = 'https://impl-identity.wd12.myworkday.com/wday/authgwy/erpa_amu1/upc/login';
const SCREENSHOT_DIR = './workday_bot_detection_screenshots';

// Test credentials
const TEST_USERNAME = 'stud_isu';
const TEST_PASSWORD = 'Erpa@1234';

async function ensureScreenshotDir() {
    if (!fs.existsSync(SCREENSHOT_DIR)) {
        fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
    }
}

async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function checkForBotDetection(page) {
    const findings = {
        captcha: false,
        cloudflare: false,
        jsChallenge: false,
        accessDenied: false,
        rateLimiting: false,
        cookieConsent: false,
        fingerprinting: false,
        customBotDetection: false,
        details: []
    };

    const pageContent = await page.content();
    const pageText = await page.evaluate(() => document.body?.innerText || '');

    // Check for CAPTCHA
    const captchaSelectors = [
        'iframe[src*="recaptcha"]',
        'iframe[src*="hcaptcha"]',
        '.g-recaptcha',
        '.h-captcha',
        '[data-sitekey]',
        'img[src*="captcha"]',
        '#captcha',
        '.captcha'
    ];

    for (const selector of captchaSelectors) {
        if (await page.$(selector)) {
            findings.captcha = true;
            findings.details.push(`CAPTCHA detected: ${selector}`);
        }
    }

    // Check for Cloudflare
    if (pageContent.includes('cloudflare') ||
        pageContent.includes('cf-browser-verification') ||
        pageContent.includes('cf_clearance') ||
        pageText.includes('Checking your browser') ||
        pageText.includes('DDoS protection by Cloudflare')) {
        findings.cloudflare = true;
        findings.details.push('Cloudflare protection detected');
    }

    // Check for JavaScript challenges
    if (pageContent.includes('challenge-platform') ||
        pageContent.includes('__cf_chl') ||
        pageContent.includes('browser-check')) {
        findings.jsChallenge = true;
        findings.details.push('JavaScript challenge detected');
    }

    // Check for Access Denied messages
    const accessDeniedPhrases = [
        'access denied',
        'bot detected',
        'automated access',
        'suspicious activity',
        'blocked',
        'forbidden',
        '403',
        'rate limit exceeded'
    ];

    for (const phrase of accessDeniedPhrases) {
        if (pageText.toLowerCase().includes(phrase)) {
            findings.accessDenied = true;
            findings.details.push(`Access restriction detected: "${phrase}"`);
        }
    }

    // Check for cookie consent
    const cookieSelectors = [
        '[class*="cookie"]',
        '[id*="cookie"]',
        '[class*="consent"]',
        '[id*="consent"]',
        '[class*="gdpr"]'
    ];

    for (const selector of cookieSelectors) {
        const element = await page.$(selector);
        if (element && await element.isVisible()) {
            findings.cookieConsent = true;
            findings.details.push(`Cookie consent popup: ${selector}`);
            break;
        }
    }

    // Check for fingerprinting scripts
    const fingerprintIndicators = [
        'fingerprintjs',
        'fp2',
        'canvas fingerprint',
        'webgl fingerprint',
        'audio fingerprint'
    ];

    for (const indicator of fingerprintIndicators) {
        if (pageContent.toLowerCase().includes(indicator)) {
            findings.fingerprinting = true;
            findings.details.push(`Fingerprinting detected: ${indicator}`);
        }
    }

    // Check for Workday-specific bot detection
    if (pageContent.includes('deviceprint') ||
        pageContent.includes('botDetect') ||
        pageContent.includes('antibot')) {
        findings.customBotDetection = true;
        findings.details.push('Custom bot detection mechanism found');
    }

    return findings;
}

async function analyzeNetworkRequests(page) {
    const securityRelatedRequests = [];

    page.on('request', request => {
        const url = request.url();
        if (url.includes('captcha') ||
            url.includes('challenge') ||
            url.includes('fingerprint') ||
            url.includes('bot') ||
            url.includes('security')) {
            securityRelatedRequests.push({
                url: url,
                method: request.method(),
                type: request.resourceType()
            });
        }
    });

    return securityRelatedRequests;
}

async function main() {
    await ensureScreenshotDir();

    console.log('='.repeat(60));
    console.log('WORKDAY BOT DETECTION ANALYSIS');
    console.log('='.repeat(60));
    console.log(`Target URL: ${TARGET_URL}`);
    console.log(`Timestamp: ${new Date().toISOString()}`);
    console.log('='.repeat(60));

    const browser = await chromium.launch({
        headless: false, // Run headed to see the page
        args: [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 },
        locale: 'en-US',
        timezoneId: 'America/New_York'
    });

    const page = await context.newPage();

    // Track security-related network requests
    const securityRequests = [];
    page.on('request', request => {
        const url = request.url().toLowerCase();
        if (url.includes('captcha') ||
            url.includes('challenge') ||
            url.includes('fingerprint') ||
            url.includes('bot') ||
            url.includes('security') ||
            url.includes('verify')) {
            securityRequests.push({
                url: request.url(),
                method: request.method()
            });
        }
    });

    try {
        // Step 1: Navigate to login page
        console.log('\n[STEP 1] Navigating to login page...');
        const response = await page.goto(TARGET_URL, {
            waitUntil: 'networkidle',
            timeout: 30000
        });

        const statusCode = response?.status();
        console.log(`HTTP Status: ${statusCode}`);

        // Take initial screenshot
        await page.screenshot({
            path: path.join(SCREENSHOT_DIR, '01_initial_page.png'),
            fullPage: true
        });
        console.log('Screenshot saved: 01_initial_page.png');

        // Wait for page to fully load
        await delay(3000);

        // Step 2: Check for bot detection mechanisms
        console.log('\n[STEP 2] Analyzing bot detection mechanisms...');
        const findings = await checkForBotDetection(page);

        // Take screenshot after analysis
        await page.screenshot({
            path: path.join(SCREENSHOT_DIR, '02_after_analysis.png'),
            fullPage: true
        });
        console.log('Screenshot saved: 02_after_analysis.png');

        // Step 3: Analyze page structure
        console.log('\n[STEP 3] Analyzing page structure...');
        const pageTitle = await page.title();
        console.log(`Page Title: ${pageTitle}`);

        const currentUrl = page.url();
        console.log(`Current URL: ${currentUrl}`);

        // Check if we were redirected
        if (currentUrl !== TARGET_URL) {
            console.log(`NOTE: Page redirected from target URL`);
        }

        // Step 4: Look for login form elements
        console.log('\n[STEP 4] Looking for login form elements...');

        const usernameSelectors = [
            'input[name="username"]',
            'input[id="username"]',
            'input[type="text"]',
            'input[name="user"]',
            'input[id="user"]',
            'input[placeholder*="user"]',
            'input[placeholder*="User"]',
            'input[name="email"]'
        ];

        const passwordSelectors = [
            'input[name="password"]',
            'input[id="password"]',
            'input[type="password"]'
        ];

        let usernameField = null;
        let passwordField = null;

        for (const selector of usernameSelectors) {
            const field = await page.$(selector);
            if (field) {
                usernameField = { selector, element: field };
                console.log(`Username field found: ${selector}`);
                break;
            }
        }

        for (const selector of passwordSelectors) {
            const field = await page.$(selector);
            if (field) {
                passwordField = { selector, element: field };
                console.log(`Password field found: ${selector}`);
                break;
            }
        }

        // Step 5: Attempt to enter credentials
        console.log('\n[STEP 5] Attempting to enter credentials...');

        if (usernameField) {
            await delay(1000); // Human-like delay
            await usernameField.element.click();
            await delay(500);

            // Type slowly like a human
            for (const char of TEST_USERNAME) {
                await page.keyboard.type(char, { delay: 100 + Math.random() * 100 });
            }
            console.log('Username entered');

            await page.screenshot({
                path: path.join(SCREENSHOT_DIR, '03_username_entered.png'),
                fullPage: true
            });
            console.log('Screenshot saved: 03_username_entered.png');
        } else {
            console.log('WARNING: Username field not found');
        }

        if (passwordField) {
            await delay(1000);
            await passwordField.element.click();
            await delay(500);

            // Type password slowly
            for (const char of TEST_PASSWORD) {
                await page.keyboard.type(char, { delay: 100 + Math.random() * 100 });
            }
            console.log('Password entered');

            await page.screenshot({
                path: path.join(SCREENSHOT_DIR, '04_password_entered.png'),
                fullPage: true
            });
            console.log('Screenshot saved: 04_password_entered.png');
        } else {
            console.log('WARNING: Password field not found');
        }

        // Step 6: Look for and click submit button
        console.log('\n[STEP 6] Looking for submit button...');

        const submitSelectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            'button:has-text("Sign In")',
            'button:has-text("Login")',
            'button:has-text("Log In")',
            '[data-automation-id="signInSubmit"]',
            '.signin-button',
            '#submit'
        ];

        let submitButton = null;
        for (const selector of submitSelectors) {
            try {
                const button = await page.$(selector);
                if (button && await button.isVisible()) {
                    submitButton = { selector, element: button };
                    console.log(`Submit button found: ${selector}`);
                    break;
                }
            } catch (e) {
                // Some selectors may not be valid, continue
            }
        }

        if (submitButton) {
            await delay(1000);
            console.log('Clicking submit button...');
            await submitButton.element.click();

            // Wait for response
            await delay(5000);

            await page.screenshot({
                path: path.join(SCREENSHOT_DIR, '05_after_submit.png'),
                fullPage: true
            });
            console.log('Screenshot saved: 05_after_submit.png');

            // Check for any post-login bot detection
            const postLoginFindings = await checkForBotDetection(page);
            if (postLoginFindings.details.length > 0) {
                console.log('\nPost-submit security findings:');
                postLoginFindings.details.forEach(d => console.log(`  - ${d}`));
            }
        } else {
            console.log('WARNING: Submit button not found');
        }

        // Step 7: Generate report
        console.log('\n' + '='.repeat(60));
        console.log('SECURITY ANALYSIS REPORT');
        console.log('='.repeat(60));

        console.log('\n[BOT DETECTION MECHANISMS]');
        console.log(`  CAPTCHA Present: ${findings.captcha ? 'YES' : 'NO'}`);
        console.log(`  Cloudflare Protection: ${findings.cloudflare ? 'YES' : 'NO'}`);
        console.log(`  JavaScript Challenge: ${findings.jsChallenge ? 'YES' : 'NO'}`);
        console.log(`  Access Denied/Blocked: ${findings.accessDenied ? 'YES' : 'NO'}`);
        console.log(`  Cookie Consent: ${findings.cookieConsent ? 'YES' : 'NO'}`);
        console.log(`  Browser Fingerprinting: ${findings.fingerprinting ? 'YES' : 'NO'}`);
        console.log(`  Custom Bot Detection: ${findings.customBotDetection ? 'YES' : 'NO'}`);

        if (findings.details.length > 0) {
            console.log('\n[DETAILED FINDINGS]');
            findings.details.forEach(d => console.log(`  - ${d}`));
        }

        if (securityRequests.length > 0) {
            console.log('\n[SECURITY-RELATED NETWORK REQUESTS]');
            securityRequests.forEach(r => console.log(`  - ${r.method} ${r.url}`));
        }

        console.log('\n[PAGE INFORMATION]');
        console.log(`  Final URL: ${page.url()}`);
        console.log(`  Page Title: ${await page.title()}`);

        // Get all cookies
        const cookies = await context.cookies();
        console.log('\n[COOKIES SET]');
        cookies.forEach(c => console.log(`  - ${c.name}: ${c.value.substring(0, 30)}...`));

        // Take final screenshot
        await page.screenshot({
            path: path.join(SCREENSHOT_DIR, '06_final_state.png'),
            fullPage: true
        });
        console.log('\nScreenshot saved: 06_final_state.png');

        console.log('\n' + '='.repeat(60));
        console.log('ANALYSIS COMPLETE');
        console.log(`Screenshots saved to: ${path.resolve(SCREENSHOT_DIR)}`);
        console.log('='.repeat(60));

    } catch (error) {
        console.error('\n[ERROR]', error.message);

        // Take error screenshot
        try {
            await page.screenshot({
                path: path.join(SCREENSHOT_DIR, 'error_state.png'),
                fullPage: true
            });
            console.log('Error screenshot saved: error_state.png');
        } catch (e) {
            console.log('Could not capture error screenshot');
        }
    } finally {
        // Keep browser open for manual inspection
        console.log('\nBrowser will close in 10 seconds...');
        await delay(10000);
        await browser.close();
    }
}

main().catch(console.error);
