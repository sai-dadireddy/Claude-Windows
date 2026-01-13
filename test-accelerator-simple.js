const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const screenshotsDir = path.join(__dirname, 'screenshots-simple');
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
  console.log(`  [${counter}] ${name}`);
}

async function main() {
  console.log('='.repeat(60));
  console.log('  TEST ACCELERATOR - AI FEATURE EXPLORATION');
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
    console.log('  Logged in successfully');

    // TEST SUITES
    console.log('\n[2] TEST SUITES');
    await page.hover('text=Test Studio');
    await delay(500);
    await page.click('text=Test Suites');
    await page.waitForSelector('text=HCM');
    await delay(1000);
    await snap(page, 'test-suites');

    // Click view button for HCM (first blue eye icon)
    console.log('  Viewing HCM Test Suite...');
    const viewBtn = page.locator('button').filter({ has: page.locator('svg') }).first();
    await viewBtn.click();
    await delay(2000);
    await snap(page, 'hcm-view');

    // Close any dialog and go to Test Scenarios
    await page.keyboard.press('Escape');
    await delay(500);

    // TEST SCENARIOS
    console.log('\n[3] TEST SCENARIOS');
    await page.hover('text=Test Studio');
    await delay(500);
    await page.click('text=Test Scenarios');
    await delay(2000);
    await snap(page, 'test-scenarios');

    // Select HCM from dropdown
    console.log('  Selecting HCM Test Suite...');
    await page.click('span:has-text("Select Test Suite")');
    await delay(1000);
    await snap(page, 'dropdown-open');

    // Click HCM option in dropdown
    await page.click('li:has-text("HCM")');
    await delay(2000);
    await snap(page, 'hcm-selected');

    // Click Add button
    console.log('  Opening Add Scenario dialog...');
    await page.click('button:has-text("Add")');
    await delay(2000);
    await snap(page, 'add-scenario-dialog');

    // Analyze dialog
    const dialogText = await page.evaluate(() => {
      const dialog = document.querySelector('.p-dialog, [role="dialog"], .modal');
      return dialog ? dialog.innerText : 'No dialog found';
    });
    console.log('\n  Dialog content:');
    console.log('  ' + dialogText.split('\n').slice(0, 20).join('\n  '));

    // Look for input fields
    const inputs = await page.$$('.p-dialog input, .p-dialog textarea');
    console.log(`\n  Input fields: ${inputs.length}`);
    for (const input of inputs) {
      const placeholder = await input.getAttribute('placeholder');
      const label = await input.evaluate(el => {
        const labelEl = el.closest('.field')?.querySelector('label');
        return labelEl?.innerText || '';
      });
      console.log(`    - ${label || placeholder || 'unnamed'}`);
    }

    // Look for buttons in dialog
    const dialogBtns = await page.$$('.p-dialog button');
    console.log(`\n  Buttons: ${dialogBtns.length}`);
    for (const btn of dialogBtns) {
      const text = await btn.innerText();
      if (text.trim()) console.log(`    - ${text.trim()}`);
    }

    // Close dialog
    await page.keyboard.press('Escape');
    await delay(500);

    // EXECUTION STUDIO
    console.log('\n[4] EXECUTION STUDIO');
    await page.hover('text=Execution Studio');
    await delay(500);
    await page.click('text=Test Execution');
    await delay(2000);
    await snap(page, 'test-execution');

    // Check for any execute/run buttons
    const execBtns = await page.$$('button');
    console.log('  Buttons on page:');
    for (const btn of execBtns) {
      const text = await btn.innerText();
      if (text.trim()) console.log(`    - ${text.trim()}`);
    }

    // ANALYTICS
    console.log('\n[5] ANALYTICS');
    await page.hover('text=Analytics');
    await delay(500);
    await page.click('text=Report');
    await delay(2000);
    await snap(page, 'analytics');

    // FINAL ANALYSIS
    console.log('\n[6] FINAL ANALYSIS');

    // Check all page text for AI keywords
    const bodyText = await page.evaluate(() => document.body.innerText);
    const aiKeywords = ['AI', 'Generate', 'GPT', 'Copilot', 'Assistant', 'Automation', 'Script Generation'];
    console.log('  Searching for AI keywords in page...');
    for (const kw of aiKeywords) {
      if (bodyText.toLowerCase().includes(kw.toLowerCase())) {
        console.log(`    Found: "${kw}"`);
      }
    }

    await snap(page, 'final');

    // REPORT
    console.log('\n' + '='.repeat(60));
    console.log('  SUMMARY REPORT');
    console.log('='.repeat(60));
    console.log(`
  APPLICATION: ActiveGenie / Test Accelerator
  URL: http://54.173.231.4
  POWERED BY: ERPA

  MODULES EXPLORED:
  1. Test Studio
     - Test Suites (4 suites: HCM, Human Resource, Payroll, Student Application)
     - Test Scenarios (requires selecting a Test Suite first)
  2. Execution Studio
     - Test Execution
     - Execution Result
  3. Analytics
     - Report

  AI FEATURES FOUND:
  - Microphone/Voice icon in header (may be logout or voice feature)
  - "ActiveGenie" branding with genie imagery
  - No explicit "Generate with AI" buttons found in current UI

  POTENTIAL AI FEATURES (need further investigation):
  - Test Scenario creation may have AI assistance
  - The "Genie" branding suggests AI-powered automation
  - Voice input feature (microphone icon in header)

  SCREENSHOTS: ${screenshotsDir}
  TOTAL: ${counter}
`);

  } catch (error) {
    console.error('\n[ERROR]', error.message);
    await snap(page, 'error');
  } finally {
    console.log('\nBrowser open for 30 seconds...');
    await delay(30000);
    await browser.close();
  }
}

main().catch(console.error);
