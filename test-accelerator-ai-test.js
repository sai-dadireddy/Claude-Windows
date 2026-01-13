const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Create screenshots directory
const screenshotsDir = path.join(__dirname, 'screenshots-test-accelerator');
if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir, { recursive: true });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function takeScreenshot(page, name) {
  const filename = path.join(screenshotsDir, `${name}.png`);
  await page.screenshot({ path: filename, fullPage: true });
  console.log(`Screenshot saved: ${filename}`);
  return filename;
}

async function main() {
  console.log('Starting Test Accelerator AI functionality test...\n');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 500 // Slow down for visibility
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    // Step 1: Navigate to the dashboard
    console.log('Step 1: Navigating to Test Accelerator dashboard...');
    await page.goto('http://54.173.231.4/dashboard', { waitUntil: 'networkidle', timeout: 60000 });
    await delay(2000);
    await takeScreenshot(page, '01-initial-page');

    // Check current URL to see if we're redirected to login
    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);

    // Step 2: Handle Microsoft SAML login if needed
    if (currentUrl.includes('login') || currentUrl.includes('microsoft') || currentUrl.includes('microsoftonline')) {
      console.log('\nStep 2: Handling Microsoft SAML login...');

      // Wait for email input field
      try {
        // Microsoft login typically has input[type="email"] or input[name="loginfmt"]
        const emailSelector = 'input[type="email"], input[name="loginfmt"], input#i0116';
        await page.waitForSelector(emailSelector, { timeout: 30000 });
        await takeScreenshot(page, '02-microsoft-login-email');

        // Enter email
        console.log('Entering email...');
        await page.fill(emailSelector, 'sainath.dadireddy@erpa.com');
        await delay(1000);

        // Click Next button
        const nextButton = 'input[type="submit"], button[type="submit"], #idSIButton9';
        await page.click(nextButton);
        await delay(3000);
        await takeScreenshot(page, '03-after-email-submit');

      } catch (e) {
        console.log('Email field not found in expected location, checking for other login forms...');
        await takeScreenshot(page, '02-login-page-check');
      }

      // Wait for password field (might be on different page after email)
      try {
        const passwordSelector = 'input[type="password"], input[name="passwd"], input#i0118';
        await page.waitForSelector(passwordSelector, { timeout: 30000 });
        await takeScreenshot(page, '04-password-page');

        // Enter password
        console.log('Entering password...');
        await page.fill(passwordSelector, 'Wel#$come@321');
        await delay(1000);

        // Click Sign in button
        const signInButton = 'input[type="submit"], button[type="submit"], #idSIButton9';
        await page.click(signInButton);
        await delay(5000);
        await takeScreenshot(page, '05-after-password-submit');

      } catch (e) {
        console.log('Password field handling:', e.message);
      }

      // Handle "Stay signed in?" prompt if it appears
      try {
        const staySignedInButton = '#idSIButton9, button:has-text("Yes"), button:has-text("No")';
        const staySignedIn = await page.$(staySignedInButton);
        if (staySignedIn) {
          console.log('Handling "Stay signed in?" prompt...');
          await takeScreenshot(page, '06-stay-signed-in');
          await page.click('#idSIButton9'); // Click Yes or No
          await delay(3000);
        }
      } catch (e) {
        // No stay signed in prompt
      }
    }

    // Wait for dashboard to load after login
    console.log('\nStep 3: Waiting for dashboard to load...');
    await delay(5000);
    await takeScreenshot(page, '07-dashboard-loaded');

    const dashboardUrl = page.url();
    console.log(`Dashboard URL: ${dashboardUrl}`);

    // Step 4: Explore the dashboard for AI features
    console.log('\nStep 4: Exploring dashboard for AI features...');

    // Get page content to understand structure
    const pageContent = await page.content();
    console.log('\nAnalyzing page structure...');

    // Look for common AI-related elements
    const aiKeywords = ['AI', 'Chat', 'Generate', 'Script', 'Assistant', 'Copilot', 'GPT', 'Intelligence'];

    for (const keyword of aiKeywords) {
      const elements = await page.$$(`text=${keyword}`);
      if (elements.length > 0) {
        console.log(`Found ${elements.length} elements with "${keyword}"`);
      }
    }

    // Look for navigation menu items
    console.log('\nLooking for navigation elements...');
    const navItems = await page.$$('nav a, .sidebar a, .menu a, [role="navigation"] a');
    console.log(`Found ${navItems.length} navigation items`);

    for (let i = 0; i < Math.min(navItems.length, 20); i++) {
      const text = await navItems[i].textContent();
      if (text && text.trim()) {
        console.log(`  Nav item: ${text.trim()}`);
      }
    }

    // Look for buttons that might be AI-related
    const buttons = await page.$$('button, [role="button"]');
    console.log(`\nFound ${buttons.length} buttons`);

    for (let i = 0; i < buttons.length; i++) {
      const text = await buttons[i].textContent();
      const ariaLabel = await buttons[i].getAttribute('aria-label');
      const label = text?.trim() || ariaLabel || '';
      if (label && aiKeywords.some(kw => label.toLowerCase().includes(kw.toLowerCase()))) {
        console.log(`  AI-related button found: ${label}`);
      }
    }

    // Step 5: Look for specific AI features
    console.log('\nStep 5: Searching for specific AI features...');

    // Check for chat interface
    const chatElements = await page.$$('[class*="chat"], [id*="chat"], [data-testid*="chat"]');
    console.log(`Chat elements found: ${chatElements.length}`);

    // Check for script generation features
    const scriptElements = await page.$$('[class*="script"], [id*="script"], button:has-text("Generate")');
    console.log(`Script-related elements found: ${scriptElements.length}`);

    // Take screenshots of different sections
    await takeScreenshot(page, '08-dashboard-full');

    // Try to find and click on AI-related menu items
    const aiMenuItems = await page.$$('a:has-text("AI"), a:has-text("Chat"), a:has-text("Generate"), a:has-text("Assistant")');

    for (let i = 0; i < aiMenuItems.length; i++) {
      const text = await aiMenuItems[i].textContent();
      console.log(`\nExploring AI menu item: ${text?.trim()}`);

      try {
        await aiMenuItems[i].click();
        await delay(3000);
        await takeScreenshot(page, `09-ai-feature-${i + 1}`);

        // Go back to explore more
        await page.goBack();
        await delay(2000);
      } catch (e) {
        console.log(`Could not click: ${e.message}`);
      }
    }

    // Print all visible text to understand the page structure
    console.log('\n--- Page Text Content Summary ---');
    const bodyText = await page.evaluate(() => document.body.innerText);
    const lines = bodyText.split('\n').filter(line => line.trim()).slice(0, 100);
    for (const line of lines) {
      if (line.length < 200) {
        console.log(line);
      }
    }

    console.log('\n--- Test Complete ---');
    console.log(`Screenshots saved to: ${screenshotsDir}`);

  } catch (error) {
    console.error('Error during test:', error);
    await takeScreenshot(page, 'error-state');
  } finally {
    // Keep browser open for manual inspection
    console.log('\nBrowser will remain open for 60 seconds for manual inspection...');
    await delay(60000);
    await browser.close();
  }
}

main().catch(console.error);
