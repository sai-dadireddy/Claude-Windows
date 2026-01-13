const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Create screenshots directory
const screenshotsDir = path.join(__dirname, 'screenshots-test-accelerator-v4');
if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir, { recursive: true });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let screenshotCounter = 0;
async function takeScreenshot(page, name) {
  screenshotCounter++;
  const filename = path.join(screenshotsDir, `${String(screenshotCounter).padStart(2, '0')}-${name}.png`);
  await page.screenshot({ path: filename, fullPage: true });
  console.log(`  [Screenshot] ${name}`);
  return filename;
}

async function main() {
  console.log('='.repeat(70));
  console.log('  Test Accelerator - AI Feature Deep Dive');
  console.log('='.repeat(70));

  const browser = await chromium.launch({
    headless: false,
    slowMo: 200
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  try {
    // Login
    console.log('\n[STEP 1] LOGGING IN...');
    await page.goto('http://54.173.231.4/dashboard', { waitUntil: 'networkidle', timeout: 60000 });

    if (page.url().includes('login')) {
      await page.fill('input[type="email"], input[placeholder*="Email"]', 'sainath.dadireddy@erpa.com');
      await page.fill('input[type="password"], input[placeholder*="Password"]', 'Wel#$come@321');
      await page.click('button:has-text("Sign In")');
      await delay(3000);
    }
    console.log(`  Logged in. URL: ${page.url()}`);
    await takeScreenshot(page, 'dashboard');

    // ===========================================
    // EXPLORE MICROPHONE/VOICE FEATURE
    // ===========================================
    console.log('\n[STEP 2] EXPLORING MICROPHONE/VOICE FEATURE...');

    // Look for the microphone button in header - I can see it in screenshots
    // Try clicking on elements in the top-right area
    const headerRight = await page.$('.layout-topbar, header, nav');

    // Try to find any SVG icons or buttons that might be the microphone
    const allSvgs = await page.$$('svg');
    console.log(`  Found ${allSvgs.length} SVG elements`);

    // Look for clickable elements in the user area
    const userArea = await page.$$('[class*="user"], [class*="profile"], [class*="topbar"] button, [class*="topbar"] svg');
    console.log(`  Found ${userArea.length} user area elements`);

    // Get all clickable elements in the header area
    const topbarElements = await page.evaluate(() => {
      const elements = [];
      document.querySelectorAll('header *, nav *, [class*="topbar"] *, [class*="header"] *').forEach(el => {
        if (el.tagName === 'BUTTON' || el.tagName === 'SVG' || el.onclick || el.style.cursor === 'pointer') {
          elements.push({
            tag: el.tagName,
            class: el.className?.toString()?.substring(0, 50) || '',
            id: el.id || '',
            ariaLabel: el.getAttribute('aria-label') || ''
          });
        }
      });
      return elements;
    });
    console.log('  Clickable header elements:');
    topbarElements.forEach(el => console.log(`    - <${el.tag}> class="${el.class}" id="${el.id}"`));

    // Try to click on SVGs in the header that might be the mic icon
    try {
      // The mic icon appears to be after the username
      const micButton = await page.$('button:has(svg), [class*="mic"], svg[class*="mic"]');
      if (micButton) {
        console.log('  Found potential microphone button, clicking...');
        await micButton.click();
        await delay(2000);
        await takeScreenshot(page, 'mic-clicked');
      }
    } catch (e) {
      console.log(`  Could not find mic button: ${e.message}`);
    }

    // ===========================================
    // CLICK ON A TEST SUITE TO VIEW SCENARIOS
    // ===========================================
    console.log('\n[STEP 3] NAVIGATING TO TEST SUITES...');

    await page.click('text=Test Studio');
    await delay(500);
    await page.click('text=Test Suites');
    await delay(2000);
    await takeScreenshot(page, 'test-suites-list');

    // Click on HCM test suite to view its scenarios
    console.log('  Clicking on HCM Test Suite...');
    const hcmLink = await page.$('a:has-text("HCM"), text=HCM >> xpath=ancestor::tr//a');
    if (hcmLink) {
      await hcmLink.click();
      await delay(2000);
      await takeScreenshot(page, 'hcm-test-suite');
    }

    // Look for a view/eye icon to see scenarios for a suite
    const viewIcons = await page.$$('[class*="eye"], button[aria-label*="view"], button:has(svg)');
    console.log(`  Found ${viewIcons.length} potential view icons`);

    // Click the first view icon (eye icon) for HCM
    if (viewIcons.length > 0) {
      console.log('  Clicking view icon for first test suite...');
      await viewIcons[0].click();
      await delay(2000);
      await takeScreenshot(page, 'test-suite-detail');
    }

    // ===========================================
    // GO TO TEST SCENARIOS AND SELECT A SUITE
    // ===========================================
    console.log('\n[STEP 4] EXPLORING TEST SCENARIOS WITH SUITE SELECTED...');

    await page.click('text=Test Studio');
    await delay(500);
    await page.click('text=Test Scenarios');
    await delay(2000);

    // Select a Test Suite from dropdown
    console.log('  Selecting Test Suite from dropdown...');
    const suiteDropdown = await page.$('text=Select Test Suite');
    if (suiteDropdown) {
      await suiteDropdown.click();
      await delay(1000);
      await takeScreenshot(page, 'suite-dropdown-open');

      // Select HCM
      const hcmOption = await page.$('text=HCM >> visible=true');
      if (hcmOption) {
        await hcmOption.click();
        await delay(2000);
        await takeScreenshot(page, 'hcm-suite-selected');
      }
    }

    // Now try to add a scenario
    console.log('  Clicking Add button...');
    const addButton = await page.$('button:has-text("Add")');
    if (addButton) {
      await addButton.click();
      await delay(2000);
      await takeScreenshot(page, 'add-scenario-dialog');

      // Look for what's in the dialog
      const dialogContent = await page.evaluate(() => {
        const dialog = document.querySelector('[role="dialog"], .modal, .p-dialog, [class*="dialog"]');
        if (dialog) {
          return {
            text: dialog.innerText,
            inputs: Array.from(dialog.querySelectorAll('input, textarea, select')).map(el => ({
              type: el.type || el.tagName,
              placeholder: el.placeholder || '',
              name: el.name || '',
              label: el.labels?.[0]?.innerText || ''
            })),
            buttons: Array.from(dialog.querySelectorAll('button')).map(b => b.innerText)
          };
        }
        return null;
      });

      if (dialogContent) {
        console.log('\n  Dialog Content:');
        console.log('    Text:', dialogContent.text?.substring(0, 500));
        console.log('    Inputs:', JSON.stringify(dialogContent.inputs, null, 2));
        console.log('    Buttons:', dialogContent.buttons);
      }

      // Look for AI generation options
      const aiOptions = await page.$$('button:has-text("Generate"), button:has-text("AI"), [class*="ai"], input[placeholder*="AI"]');
      console.log(`  AI-related elements in dialog: ${aiOptions.length}`);

      // Close dialog
      await page.keyboard.press('Escape');
      await delay(1000);
    }

    // ===========================================
    // CHECK EXECUTION STUDIO FOR AI FEATURES
    // ===========================================
    console.log('\n[STEP 5] CHECKING EXECUTION STUDIO...');

    await page.click('text=Execution Studio');
    await delay(500);
    await page.click('text=Test Execution');
    await delay(2000);
    await takeScreenshot(page, 'test-execution');

    // Look for any AI/automation features
    const executionButtons = await page.$$('button');
    console.log('  Buttons on Test Execution page:');
    for (const btn of executionButtons) {
      const text = await btn.textContent();
      if (text?.trim()) console.log(`    - ${text.trim()}`);
    }

    // ===========================================
    // ANALYZE FULL PAGE STRUCTURE
    // ===========================================
    console.log('\n[STEP 6] FULL PAGE STRUCTURE ANALYSIS...');

    const fullAnalysis = await page.evaluate(() => {
      // Get all links
      const links = Array.from(document.querySelectorAll('a')).map(a => ({
        text: a.innerText.trim(),
        href: a.href
      })).filter(l => l.text);

      // Get all buttons
      const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(t => t);

      // Look for any AI-related text anywhere
      const aiPatterns = /\b(AI|artificial intelligence|generate|generative|GPT|copilot|assistant|auto-generate|smart|intelligent)\b/gi;
      const bodyText = document.body.innerText;
      const aiMatches = bodyText.match(aiPatterns) || [];

      return { links, buttons, aiMatches: [...new Set(aiMatches)] };
    });

    console.log('  Links found:', fullAnalysis.links.length);
    fullAnalysis.links.slice(0, 10).forEach(l => console.log(`    - ${l.text}: ${l.href}`));

    console.log('  Buttons:', fullAnalysis.buttons);
    console.log('  AI-related text:', fullAnalysis.aiMatches);

    // ===========================================
    // TRY DIRECT API EXPLORATION
    // ===========================================
    console.log('\n[STEP 7] CHECKING FOR API/NETWORK CALLS...');

    // Monitor network requests
    const apiEndpoints = [];
    page.on('request', request => {
      if (request.url().includes('api') || request.url().includes('AI') || request.url().includes('generate')) {
        apiEndpoints.push(request.url());
      }
    });

    // Navigate around to trigger API calls
    await page.click('text=Analytics');
    await delay(500);
    await page.click('text=Report');
    await delay(2000);
    await takeScreenshot(page, 'analytics-report');

    console.log('  API endpoints detected:', apiEndpoints);

    // ===========================================
    // CHECK USER MENU
    // ===========================================
    console.log('\n[STEP 8] CHECKING USER MENU...');

    const userMenu = await page.$('text=Sainathreddy');
    if (userMenu) {
      await userMenu.click();
      await delay(1000);
      await takeScreenshot(page, 'user-menu');
    }

    // ===========================================
    // FINAL SCREENSHOT
    // ===========================================
    await page.click('text=Test Accelerator');
    await delay(1000);
    await takeScreenshot(page, 'final-dashboard');

    // ===========================================
    // REPORT
    // ===========================================
    console.log('\n' + '='.repeat(70));
    console.log('  FINAL REPORT: TEST ACCELERATOR AI FEATURES');
    console.log('='.repeat(70));

    console.log('\n[APPLICATION STRUCTURE]');
    console.log('  Brand: ActiveGenie (Test Accelerator)');
    console.log('  Main Modules:');
    console.log('    1. Test Studio');
    console.log('       - Test Suites (HCM, Human Resource, Payroll, Student Application)');
    console.log('       - Test Scenarios');
    console.log('    2. Execution Studio');
    console.log('       - Test Execution');
    console.log('       - Execution Result');
    console.log('    3. Analytics');
    console.log('       - Report');

    console.log('\n[AI FEATURES IDENTIFIED]');
    console.log('  1. Microphone icon in header - possible voice input feature');
    console.log('  2. "ActiveGenie" branding suggests AI/automation capabilities');
    console.log('  3. Test Scenario creation may have AI generation (needs package first)');

    console.log('\n[RECOMMENDATIONS FOR FURTHER TESTING]');
    console.log('  1. Create a new test scenario to explore AI script generation');
    console.log('  2. Click on microphone icon to test voice features');
    console.log('  3. Check browser network tab for AI API endpoints');

    console.log(`\n[SCREENSHOTS]`);
    console.log(`  Location: ${screenshotsDir}`);
    console.log(`  Count: ${screenshotCounter}`);

  } catch (error) {
    console.error('\n[ERROR]', error);
    await takeScreenshot(page, 'error');
  } finally {
    console.log('\n' + '='.repeat(70));
    console.log('  Browser open for 45 seconds for manual exploration...');
    console.log('='.repeat(70));
    await delay(45000);
    await browser.close();
  }
}

main().catch(console.error);
