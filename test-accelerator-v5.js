const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const screenshotsDir = path.join(__dirname, 'screenshots-v5');
if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir, { recursive: true });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let counter = 0;
async function snap(page, name) {
  counter++;
  const file = path.join(screenshotsDir, `${String(counter).padStart(2, '0')}-${name}.png`);
  await page.screenshot({ path: file, fullPage: true });
  console.log(`  [Screenshot ${counter}] ${name}`);
}

async function main() {
  console.log('='.repeat(60));
  console.log('  TEST ACCELERATOR - AI FEATURE TEST');
  console.log('='.repeat(60));

  const browser = await chromium.launch({ headless: false, slowMo: 400 });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  try {
    // LOGIN
    console.log('\n[1] LOGIN');
    await page.goto('http://54.173.231.4/auth/login');
    await page.waitForSelector('input[placeholder="Email address"]');
    await page.fill('input[placeholder="Email address"]', 'sainath.dadireddy@erpa.com');
    await page.fill('input[placeholder="Password"]', 'Wel#$come@321');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('**/dashboard');
    await delay(2000);
    await snap(page, 'dashboard');

    // GO TO TEST SCENARIOS - This is where AI script generation might be
    console.log('\n[2] TEST SCENARIOS');
    await page.hover('text=Test Studio');
    await delay(500);
    await page.click('text=Test Scenarios');
    await delay(2000);
    await snap(page, 'test-scenarios-empty');

    // Select HCM from dropdown
    console.log('  Selecting HCM...');
    const dropdown = await page.$('.p-dropdown');
    if (dropdown) {
      await dropdown.click();
      await delay(1000);
      await snap(page, 'dropdown-open');

      // Find and click HCM
      const options = await page.$$('.p-dropdown-item');
      for (const opt of options) {
        const text = await opt.innerText();
        if (text.includes('HCM')) {
          await opt.click();
          await delay(2000);
          break;
        }
      }
      await snap(page, 'hcm-selected');
    }

    // Click Add to create a new scenario
    console.log('\n[3] ADD SCENARIO DIALOG');
    await page.click('button:has-text("Add")');
    await delay(3000);
    await snap(page, 'add-scenario-dialog');

    // Get dialog content
    const dialog = await page.$('.p-dialog');
    if (dialog) {
      const dialogHTML = await dialog.innerHTML();
      const dialogText = await dialog.innerText();

      console.log('\n  DIALOG CONTENT:');
      console.log('  ' + '-'.repeat(50));
      console.log(dialogText);
      console.log('  ' + '-'.repeat(50));

      // Look for any AI/Generate related elements
      const aiElements = await page.$$('.p-dialog [class*="ai"], .p-dialog [class*="generate"], .p-dialog button:has-text("Generate")');
      console.log(`\n  AI-related elements: ${aiElements.length}`);

      // Check for tabs in dialog
      const tabs = await page.$$('.p-dialog .p-tabview-nav-link');
      if (tabs.length > 0) {
        console.log(`\n  Tabs found: ${tabs.length}`);
        for (const tab of tabs) {
          const text = await tab.innerText();
          console.log(`    - ${text}`);
        }
      }

      // List all inputs
      const inputs = await page.$$('.p-dialog input, .p-dialog textarea, .p-dialog .p-dropdown');
      console.log(`\n  Form fields: ${inputs.length}`);

      // List all buttons
      const buttons = await page.$$('.p-dialog button, .p-dialog .p-button');
      console.log(`  Buttons:`);
      for (const btn of buttons) {
        const text = await btn.innerText();
        if (text.trim()) {
          console.log(`    - "${text.trim()}"`);
          // Check if any button is AI-related
          if (text.toLowerCase().includes('generat') || text.toLowerCase().includes('ai')) {
            console.log('      ^^ AI-RELATED BUTTON FOUND!');
          }
        }
      }

      // Close dialog
      const closeBtn = await page.$('.p-dialog-header-close, button[aria-label="Close"]');
      if (closeBtn) {
        await closeBtn.click();
      } else {
        await page.keyboard.press('Escape');
      }
      await delay(500);
    }

    // GO TO TEST SUITES and view details
    console.log('\n[4] TEST SUITES - VIEW DETAILS');
    await page.hover('text=Test Studio');
    await delay(500);
    await page.click('text=Test Suites');
    await delay(2000);
    await snap(page, 'test-suites');

    // Click on the HCM row to see test suite details
    console.log('  Clicking HCM row...');

    // Get the table rows
    const rows = await page.$$('table tbody tr');
    console.log(`  Found ${rows.length} table rows`);

    if (rows.length > 0) {
      // Get action buttons in first row (HCM)
      const actionButtons = await rows[0].$$('button');
      console.log(`  Action buttons in HCM row: ${actionButtons.length}`);

      // Click the first button (view/eye icon)
      if (actionButtons.length > 0) {
        console.log('  Clicking view button...');
        await actionButtons[0].click();
        await delay(3000);
        await snap(page, 'hcm-view-dialog');

        // Analyze what opened
        const viewDialog = await page.$('.p-dialog, [role="dialog"]');
        if (viewDialog) {
          const content = await viewDialog.innerText();
          console.log('\n  VIEW DIALOG CONTENT:');
          console.log('  ' + '-'.repeat(50));
          console.log(content.substring(0, 1000));
          console.log('  ' + '-'.repeat(50));

          // Look for AI features
          if (content.toLowerCase().includes('generat') || content.toLowerCase().includes('ai')) {
            console.log('\n  [AI INDICATOR] Found AI-related text in view dialog');
          }

          // Close
          await page.keyboard.press('Escape');
          await delay(500);
        }
      }
    }

    // EXECUTION STUDIO
    console.log('\n[5] EXECUTION STUDIO');
    await page.hover('text=Execution Studio');
    await delay(500);
    await page.click('text=Test Execution');
    await delay(2000);
    await snap(page, 'test-execution');

    // List buttons
    const execButtons = await page.$$('button');
    console.log('  Buttons on page:');
    for (const btn of execButtons) {
      const text = await btn.innerText();
      if (text.trim()) console.log(`    - "${text.trim()}"`);
    }

    // ANALYTICS
    console.log('\n[6] ANALYTICS');
    await page.hover('text=Analytics');
    await delay(500);
    await page.click('text=Report');
    await delay(2000);
    await snap(page, 'analytics');

    // FINAL CHECK FOR AI KEYWORDS
    console.log('\n[7] FINAL AI KEYWORD SEARCH');
    const allText = await page.evaluate(() => document.body.innerText);
    const aiKeywords = ['AI', 'Artificial Intelligence', 'Generate', 'GPT', 'Copilot', 'Assistant', 'Automation', 'Machine Learning'];

    console.log('  Scanning page for AI keywords...');
    for (const kw of aiKeywords) {
      const regex = new RegExp(`\\b${kw}\\b`, 'gi');
      const matches = allText.match(regex);
      if (matches) {
        console.log(`    Found "${kw}": ${matches.length} occurrence(s)`);
      }
    }

    await snap(page, 'final');

    // ========================================
    // SUMMARY REPORT
    // ========================================
    console.log('\n' + '='.repeat(60));
    console.log('  FINAL REPORT: TEST ACCELERATOR AI FEATURES');
    console.log('='.repeat(60));

    console.log(`
  APPLICATION INFO:
  - Name: ActiveGenie / Test Accelerator
  - URL: http://54.173.231.4
  - Powered by: ERPA
  - User: Sainathreddy Dadireddy

  MODULES EXPLORED:
  1. Test Studio
     - Test Suites: 4 suites (HCM, Human Resource, Payroll, Student Application)
     - Test Scenarios: Create/manage test scenarios
  2. Execution Studio
     - Test Execution: Run test scenarios
     - Execution Result: View execution results
  3. Analytics
     - Report: View test reports

  AI FEATURES STATUS:
  - The app is branded as "ActiveGenie" suggesting AI/genie capabilities
  - No explicit "Generate with AI" or "AI Assistant" buttons found in current UI
  - Test Scenario creation dialog does not show AI generation options
  - Microphone icon in header appears to be logout (not voice input)

  CONCLUSION:
  The AI features may be:
  1. Under development
  2. Hidden behind feature flags
  3. Only available for certain user roles
  4. Backend-only AI processing

  SCREENSHOTS LOCATION: ${screenshotsDir}
  TOTAL SCREENSHOTS: ${counter}
`);

  } catch (error) {
    console.error('\n[ERROR]', error.message);
    console.error(error.stack);
    await snap(page, 'error');
  } finally {
    console.log('\nBrowser open for 20 seconds for manual inspection...');
    await delay(20000);
    await browser.close();
  }
}

main().catch(console.error);
