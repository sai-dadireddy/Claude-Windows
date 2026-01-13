const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Create screenshots directory
const screenshotsDir = path.join(__dirname, 'screenshots-final');
if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir, { recursive: true });
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

let screenshotCounter = 0;
async function screenshot(page, name) {
  screenshotCounter++;
  const filename = path.join(screenshotsDir, `${String(screenshotCounter).padStart(2, '0')}-${name}.png`);
  await page.screenshot({ path: filename, fullPage: true });
  console.log(`  [Screenshot ${screenshotCounter}] ${name}`);
  return filename;
}

async function main() {
  console.log('='.repeat(70));
  console.log('  TEST ACCELERATOR - FINAL AI FEATURE EXPLORATION');
  console.log('='.repeat(70));

  const browser = await chromium.launch({
    headless: false,
    slowMo: 300
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  const findings = [];

  try {
    // ============================================
    // STEP 1: LOGIN
    // ============================================
    console.log('\n[STEP 1] LOGGING IN...');
    await page.goto('http://54.173.231.4/auth/login', { waitUntil: 'networkidle', timeout: 60000 });

    await page.fill('input[placeholder="Email address"]', 'sainath.dadireddy@erpa.com');
    await page.fill('input[placeholder="Password"]', 'Wel#$come@321');
    await page.click('button:has-text("Sign In")');
    await delay(3000);
    console.log(`  Logged in successfully. URL: ${page.url()}`);
    await screenshot(page, 'dashboard');

    // ============================================
    // STEP 2: EXPLORE MICROPHONE BUTTON
    // ============================================
    console.log('\n[STEP 2] EXPLORING MICROPHONE/VOICE FEATURE...');

    // Get all buttons in the header area
    const topbarButtons = await page.$$('.layout-topbar-action');
    console.log(`  Found ${topbarButtons.length} topbar action buttons`);

    // Click each topbar button to see what it does
    for (let i = 0; i < topbarButtons.length; i++) {
      try {
        const btn = topbarButtons[i];
        console.log(`  Clicking topbar button ${i + 1}...`);
        await btn.click();
        await delay(2000);
        await screenshot(page, `topbar-btn-${i + 1}`);

        // Check if a modal/sidebar opened
        const modal = await page.$('[role="dialog"], .modal, .p-sidebar, .p-dialog');
        if (modal) {
          console.log('  Modal/Sidebar opened!');
          const modalText = await modal.innerText();
          console.log(`  Content: ${modalText.substring(0, 300)}`);

          // Check for AI/voice related content
          if (modalText.toLowerCase().includes('voice') || modalText.toLowerCase().includes('speech') ||
              modalText.toLowerCase().includes('ai') || modalText.toLowerCase().includes('assistant')) {
            findings.push({ feature: 'Voice/AI Assistant', location: 'Topbar Button', content: modalText.substring(0, 200) });
          }

          // Close modal
          await page.keyboard.press('Escape');
          await delay(500);
        }
      } catch (e) {
        console.log(`  Button ${i + 1} click failed: ${e.message}`);
      }
    }

    // ============================================
    // STEP 3: VIEW HCM TEST SUITE
    // ============================================
    console.log('\n[STEP 3] VIEWING HCM TEST SUITE...');

    await page.click('text=Test Studio');
    await delay(500);
    await page.click('text=Test Suites');
    await delay(2000);
    await screenshot(page, 'test-suites');

    // Click the eye/view icon for HCM
    const viewButtons = await page.$$('button:has-text(""), [class*="eye"], .p-button-rounded');
    console.log(`  Found ${viewButtons.length} action buttons`);

    // Click on the HCM row first to see details
    try {
      await page.click('text=HCM');
      await delay(2000);
      await screenshot(page, 'hcm-clicked');
    } catch (e) {
      console.log(`  Could not click HCM: ${e.message}`);
    }

    // Try clicking the first view button (eye icon)
    const eyeButtons = await page.$$('.p-button-info, button[class*="info"]');
    if (eyeButtons.length > 0) {
      console.log(`  Clicking first view button...`);
      await eyeButtons[0].click();
      await delay(2000);
      await screenshot(page, 'view-test-suite');

      // Look for AI features in the view
      const pageContent = await page.content();
      if (pageContent.toLowerCase().includes('generat') || pageContent.toLowerCase().includes('ai')) {
        console.log('  [AI INDICATOR] Found AI-related content in test suite view');
      }
    }

    // ============================================
    // STEP 4: TEST SCENARIOS WITH SUITE SELECTED
    // ============================================
    console.log('\n[STEP 4] TEST SCENARIOS PAGE...');

    await page.click('text=Test Studio');
    await delay(500);
    await page.click('text=Test Scenarios');
    await delay(2000);
    await screenshot(page, 'test-scenarios');

    // Click dropdown and select HCM
    console.log('  Selecting HCM from dropdown...');
    await page.click('.p-dropdown, [role="combobox"]');
    await delay(1000);
    await screenshot(page, 'dropdown-open');

    // Find and click HCM option
    const dropdownOptions = await page.$$('.p-dropdown-item, [role="option"]');
    console.log(`  Found ${dropdownOptions.length} dropdown options`);

    for (const opt of dropdownOptions) {
      const text = await opt.innerText();
      if (text.includes('HCM')) {
        console.log('  Selecting HCM...');
        await opt.click();
        await delay(2000);
        break;
      }
    }
    await screenshot(page, 'hcm-selected');

    // Now click Add button
    console.log('  Clicking Add to create scenario...');
    await page.click('button:has-text("Add")');
    await delay(2000);
    await screenshot(page, 'add-scenario-dialog');

    // Analyze the add scenario dialog
    const dialogVisible = await page.$('.p-dialog, [role="dialog"]');
    if (dialogVisible) {
      const dialogContent = await dialogVisible.innerText();
      console.log('\n  Add Scenario Dialog Content:');
      console.log('  ' + '-'.repeat(40));
      console.log(`  ${dialogContent.substring(0, 500)}`);
      console.log('  ' + '-'.repeat(40));

      // Look for form fields
      const inputs = await page.$$('.p-dialog input, .p-dialog textarea, [role="dialog"] input');
      console.log(`\n  Form inputs found: ${inputs.length}`);
      for (const input of inputs) {
        const placeholder = await input.getAttribute('placeholder');
        const type = await input.getAttribute('type');
        console.log(`    - Input: type="${type}" placeholder="${placeholder}"`);
      }

      // Look for buttons in dialog
      const dialogButtons = await page.$$('.p-dialog button, [role="dialog"] button');
      console.log(`  Buttons in dialog: ${dialogButtons.length}`);
      for (const btn of dialogButtons) {
        const text = await btn.innerText();
        console.log(`    - Button: ${text.trim()}`);
        if (text.toLowerCase().includes('generat') || text.toLowerCase().includes('ai')) {
          findings.push({ feature: 'AI Script Generation', location: 'Add Scenario Dialog', element: text });
        }
      }

      // Look for any tabs or sections that might have AI features
      const tabs = await page.$$('.p-tabview-nav, [role="tablist"]');
      if (tabs.length > 0) {
        console.log('  Found tabs - might have AI generation tab');
        await screenshot(page, 'dialog-tabs');
      }

      // Close dialog
      await page.keyboard.press('Escape');
      await delay(500);
    }

    // ============================================
    // STEP 5: EXECUTION STUDIO
    // ============================================
    console.log('\n[STEP 5] EXECUTION STUDIO...');

    await page.click('text=Execution Studio');
    await delay(500);
    await page.click('text=Test Execution');
    await delay(2000);
    await screenshot(page, 'test-execution');

    // Look for run/execute buttons
    const execButtons = await page.$$('button');
    console.log('  Buttons on Test Execution:');
    for (const btn of execButtons) {
      const text = await btn.innerText();
      if (text.trim()) console.log(`    - ${text.trim()}`);
    }

    // ============================================
    // STEP 6: ANALYTICS
    // ============================================
    console.log('\n[STEP 6] ANALYTICS...');

    await page.click('text=Analytics');
    await delay(500);
    await page.click('text=Report');
    await delay(2000);
    await screenshot(page, 'analytics-report');

    // ============================================
    // STEP 7: NETWORK INSPECTION
    // ============================================
    console.log('\n[STEP 7] CHECKING FOR AI API ENDPOINTS...');

    // Intercept network requests
    const requests = [];
    page.on('request', req => {
      if (req.url().includes('/api/') || req.url().includes('ai') || req.url().includes('generate')) {
        requests.push({ url: req.url(), method: req.method() });
      }
    });

    // Navigate to trigger API calls
    await page.click('text=Test Studio');
    await delay(500);
    await page.click('text=Test Suites');
    await delay(2000);

    if (requests.length > 0) {
      console.log('  API endpoints detected:');
      requests.forEach(r => console.log(`    - ${r.method} ${r.url}`));
    }

    // ============================================
    // STEP 8: FULL HTML ANALYSIS
    // ============================================
    console.log('\n[STEP 8] FULL HTML ANALYSIS FOR AI FEATURES...');

    const htmlAnalysis = await page.evaluate(() => {
      const results = {
        aiElements: [],
        allButtons: [],
        allInputs: []
      };

      // Find all elements with AI-related text
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
      let node;
      while ((node = walker.nextNode())) {
        const text = node.innerText || '';
        const attrs = node.outerHTML.substring(0, 200);
        if (text.match(/\b(AI|GPT|generat|copilot|assistant|voice|speech)\b/i) ||
            attrs.match(/\b(ai|gpt|generat|copilot|assistant|voice|speech)\b/i)) {
          results.aiElements.push({
            tag: node.tagName,
            text: text.substring(0, 100),
            class: node.className?.toString().substring(0, 50)
          });
        }
      }

      // Get unique
      results.aiElements = results.aiElements.slice(0, 20);

      return results;
    });

    console.log(`  AI-related elements found: ${htmlAnalysis.aiElements.length}`);
    htmlAnalysis.aiElements.forEach(el => console.log(`    - <${el.tag}> "${el.text.substring(0, 50)}"`));

    // ============================================
    // FINAL SCREENSHOT
    // ============================================
    await screenshot(page, 'final');

    // ============================================
    // REPORT
    // ============================================
    console.log('\n' + '='.repeat(70));
    console.log('  FINAL REPORT: TEST ACCELERATOR AI FEATURES');
    console.log('='.repeat(70));

    console.log('\n[APPLICATION OVERVIEW]');
    console.log('  Name: ActiveGenie / Test Accelerator');
    console.log('  URL: http://54.173.231.4');
    console.log('  Powered by: ERPA');

    console.log('\n[MODULES]');
    console.log('  1. Test Studio');
    console.log('     - Test Suites: 4 suites (HCM, Human Resource, Payroll, Student Application)');
    console.log('     - Test Scenarios: Requires selecting a Test Suite first');
    console.log('  2. Execution Studio');
    console.log('     - Test Execution: Run test scenarios');
    console.log('     - Execution Result: View results');
    console.log('  3. Analytics');
    console.log('     - Report: Test analytics and reports');

    console.log('\n[AI FEATURES IDENTIFIED]');
    if (findings.length > 0) {
      findings.forEach(f => console.log(`  - ${f.feature} (${f.location})`));
    } else {
      console.log('  - Microphone icon in header (potential voice input)');
      console.log('  - "Genie" branding suggests AI automation');
      console.log('  - No explicit AI generation buttons found in current UI state');
    }

    console.log('\n[RECOMMENDATIONS]');
    console.log('  1. Click the microphone icon to test voice input functionality');
    console.log('  2. Create a test scenario to see if AI script generation appears');
    console.log('  3. Check browser DevTools Network tab for AI API calls');

    console.log(`\n[SCREENSHOTS]`);
    console.log(`  Location: ${screenshotsDir}`);
    console.log(`  Total: ${screenshotCounter}`);

  } catch (error) {
    console.error('\n[ERROR]', error.message);
    await screenshot(page, 'error');
  } finally {
    console.log('\n' + '='.repeat(70));
    console.log('  Browser will stay open for 30 seconds...');
    console.log('='.repeat(70));
    await delay(30000);
    await browser.close();
  }
}

main().catch(console.error);
