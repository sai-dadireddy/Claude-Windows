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
  console.log('='.repeat(60));
  console.log('Test Accelerator (ActiveGenie) - AI Functionality Test');
  console.log('='.repeat(60));
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 300
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    // Step 1: Navigate to the dashboard
    console.log('[Step 1] Navigating to Test Accelerator dashboard...');
    await page.goto('http://54.173.231.4/dashboard', { waitUntil: 'networkidle', timeout: 60000 });
    await delay(2000);

    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);

    // Step 2: Login to ActiveGenie
    if (currentUrl.includes('login')) {
      console.log('\n[Step 2] Logging in to ActiveGenie...');
      await takeScreenshot(page, '01-login-page');

      // Fill in email
      console.log('  - Entering email...');
      await page.fill('input[placeholder="Email address"], input[type="email"]', 'sainath.dadireddy@erpa.com');
      await delay(500);

      // Fill in password
      console.log('  - Entering password...');
      await page.fill('input[placeholder="Password"], input[type="password"]', 'Wel#$come@321');
      await delay(500);
      await takeScreenshot(page, '02-credentials-entered');

      // Click Sign In button
      console.log('  - Clicking Sign In...');
      await page.click('button:has-text("Sign In"), button[type="submit"]');

      // Wait for navigation after login
      await delay(5000);
      await takeScreenshot(page, '03-after-login');

      const afterLoginUrl = page.url();
      console.log(`After login URL: ${afterLoginUrl}`);

      if (afterLoginUrl.includes('login')) {
        console.log('  [WARNING] Still on login page - checking for error messages...');
        const errorMsg = await page.$('.error, .alert-danger, [class*="error"]');
        if (errorMsg) {
          const errorText = await errorMsg.textContent();
          console.log(`  Error: ${errorText}`);
        }
      }
    }

    // Step 3: Explore Dashboard
    console.log('\n[Step 3] Exploring Dashboard...');
    await delay(3000);
    await takeScreenshot(page, '04-dashboard');

    // Get all text content to understand the page
    const pageText = await page.evaluate(() => document.body.innerText);
    console.log('\n--- Page Content Summary ---');
    const textLines = pageText.split('\n').filter(l => l.trim()).slice(0, 50);
    textLines.forEach(line => {
      if (line.length < 150) console.log(`  ${line}`);
    });

    // Step 4: Find navigation/menu items
    console.log('\n[Step 4] Analyzing navigation structure...');

    // Look for sidebar/navigation
    const sidebarSelectors = [
      '.sidebar a',
      'nav a',
      '[class*="nav"] a',
      '[class*="menu"] a',
      '[class*="sidebar"] a',
      '.ant-menu-item',
      '.MuiDrawer-root a'
    ];

    let navItems = [];
    for (const selector of sidebarSelectors) {
      const items = await page.$$(selector);
      if (items.length > 0) {
        console.log(`Found ${items.length} items with selector: ${selector}`);
        navItems = navItems.concat(items);
      }
    }

    // Get unique nav item texts
    const navTexts = new Set();
    for (const item of navItems) {
      const text = await item.textContent();
      if (text && text.trim()) {
        navTexts.add(text.trim());
      }
    }
    console.log('\nNavigation items found:');
    navTexts.forEach(t => console.log(`  - ${t}`));

    // Step 5: Look for AI-related features
    console.log('\n[Step 5] Searching for AI-related features...');

    const aiKeywords = [
      'AI', 'Chat', 'Generate', 'Script', 'Assistant',
      'Copilot', 'GPT', 'Genie', 'Intelligence', 'Automation',
      'Test Generation', 'Script Generation', 'Natural Language'
    ];

    for (const keyword of aiKeywords) {
      const elements = await page.$$(`text=${keyword}`);
      if (elements.length > 0) {
        console.log(`  Found "${keyword}": ${elements.length} occurrence(s)`);
      }
    }

    // Step 6: Click on any AI-related menu items and explore
    console.log('\n[Step 6] Exploring AI features...');

    // Common AI feature selectors
    const aiFeatureSelectors = [
      'a:has-text("AI")',
      'a:has-text("Chat")',
      'a:has-text("Generate")',
      'a:has-text("Script")',
      'a:has-text("Genie")',
      'button:has-text("Generate")',
      '[class*="ai"]',
      '[class*="chat"]'
    ];

    let featureIndex = 0;
    for (const selector of aiFeatureSelectors) {
      try {
        const elements = await page.$$(selector);
        if (elements.length > 0) {
          console.log(`\n  Exploring: ${selector} (${elements.length} elements)`);

          for (let i = 0; i < Math.min(elements.length, 3); i++) {
            const element = elements[i];
            const isVisible = await element.isVisible();
            if (isVisible) {
              const text = await element.textContent();
              console.log(`    Clicking: ${text?.trim() || 'element'}`);

              try {
                await element.click();
                await delay(3000);
                featureIndex++;
                await takeScreenshot(page, `05-ai-feature-${featureIndex}-${text?.trim().replace(/\s+/g, '-').substring(0, 20) || 'unnamed'}`);

                // Analyze the new page
                const newPageText = await page.evaluate(() => document.body.innerText);
                const newLines = newPageText.split('\n').filter(l => l.trim()).slice(0, 20);
                console.log('    Page content:');
                newLines.forEach(line => {
                  if (line.length < 100) console.log(`      ${line}`);
                });

                // Look for input fields (chat interface indicators)
                const inputFields = await page.$$('input[type="text"], textarea');
                if (inputFields.length > 0) {
                  console.log(`    Found ${inputFields.length} input field(s) - possible chat/input interface`);
                }

                // Go back to explore more
                await page.goBack();
                await delay(2000);
              } catch (clickErr) {
                console.log(`    Could not interact: ${clickErr.message}`);
              }
            }
          }
        }
      } catch (err) {
        // Selector not found, continue
      }
    }

    // Step 7: Look for buttons and interactive elements
    console.log('\n[Step 7] Analyzing interactive elements...');

    const allButtons = await page.$$('button');
    console.log(`Total buttons on page: ${allButtons.length}`);

    for (const btn of allButtons) {
      const text = await btn.textContent();
      const isVisible = await btn.isVisible();
      if (isVisible && text && text.trim()) {
        console.log(`  Button: ${text.trim()}`);
      }
    }

    // Step 8: Check for any modals or popups that might be AI features
    console.log('\n[Step 8] Checking for modals/dialogs...');

    const modalSelectors = ['.modal', '[role="dialog"]', '.ant-modal', '.MuiDialog-root'];
    for (const selector of modalSelectors) {
      const modals = await page.$$(selector);
      if (modals.length > 0) {
        console.log(`Found modal with selector: ${selector}`);
        await takeScreenshot(page, '06-modal-found');
      }
    }

    // Final screenshot of explored state
    await takeScreenshot(page, '99-final-state');

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`Screenshots saved to: ${screenshotsDir}`);
    console.log('\nTo view screenshots, check the folder above.');
    console.log('');

  } catch (error) {
    console.error('\n[ERROR] Test failed:', error.message);
    await takeScreenshot(page, 'error-state');
  } finally {
    console.log('\nBrowser will remain open for 60 seconds for manual inspection...');
    console.log('You can manually explore the app during this time.');
    await delay(60000);
    await browser.close();
  }
}

main().catch(console.error);
