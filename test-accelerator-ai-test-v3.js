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

let screenshotCounter = 0;
async function takeScreenshot(page, name) {
  screenshotCounter++;
  const filename = path.join(screenshotsDir, `${String(screenshotCounter).padStart(2, '0')}-${name}.png`);
  await page.screenshot({ path: filename, fullPage: true });
  console.log(`  [Screenshot] ${filename}`);
  return filename;
}

async function main() {
  console.log('='.repeat(70));
  console.log('  Test Accelerator (ActiveGenie) - Comprehensive AI Feature Exploration');
  console.log('='.repeat(70));
  console.log('');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 200
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 }
  });

  const page = await context.newPage();

  const findings = {
    aiFeatures: [],
    menuItems: [],
    interactiveElements: []
  };

  try {
    // ===========================================
    // STEP 1: Login
    // ===========================================
    console.log('\n[STEP 1] LOGGING IN...');
    await page.goto('http://54.173.231.4/dashboard', { waitUntil: 'networkidle', timeout: 60000 });

    if (page.url().includes('login')) {
      await page.fill('input[placeholder="Email address"], input[type="email"]', 'sainath.dadireddy@erpa.com');
      await page.fill('input[placeholder="Password"], input[type="password"]', 'Wel#$come@321');
      await page.click('button:has-text("Sign In")');
      await delay(3000);
    }

    console.log(`  Logged in successfully. URL: ${page.url()}`);
    await takeScreenshot(page, 'dashboard-main');

    // ===========================================
    // STEP 2: Explore Test Studio Menu
    // ===========================================
    console.log('\n[STEP 2] EXPLORING TEST STUDIO MENU...');

    // Hover/click on Test Studio dropdown
    const testStudioMenu = await page.$('text=Test Studio');
    if (testStudioMenu) {
      await testStudioMenu.hover();
      await delay(1000);
      await takeScreenshot(page, 'test-studio-hover');

      // Click to open dropdown
      await testStudioMenu.click();
      await delay(1000);
      await takeScreenshot(page, 'test-studio-expanded');

      // Find submenu items
      const submenuItems = await page.$$('text=Test Suites, text=Test Scenarios');
      console.log('  Test Studio submenu items found');

      // Navigate to Test Suites
      try {
        await page.click('text=Test Suites');
        await delay(2000);
        await takeScreenshot(page, 'test-suites-page');
        console.log('  Navigated to Test Suites');

        // Look for any AI/Generate buttons
        const aiButtons = await page.$$('button:has-text("Generate"), button:has-text("AI"), button:has-text("Create")');
        console.log(`  Found ${aiButtons.length} potential AI buttons`);

        for (const btn of aiButtons) {
          const text = await btn.textContent();
          console.log(`    - Button: ${text?.trim()}`);
          findings.aiFeatures.push({ page: 'Test Suites', element: text?.trim() });
        }

        // Go back to dashboard
        await page.click('text=Test Accelerator');
        await delay(2000);
      } catch (e) {
        console.log(`  Error exploring Test Suites: ${e.message}`);
      }

      // Navigate to Test Scenarios
      try {
        await page.click('text=Test Studio');
        await delay(500);
        await page.click('text=Test Scenarios');
        await delay(2000);
        await takeScreenshot(page, 'test-scenarios-page');
        console.log('  Navigated to Test Scenarios');

        // Look for AI features
        const pageContent = await page.evaluate(() => document.body.innerText);
        if (pageContent.toLowerCase().includes('generat') || pageContent.toLowerCase().includes('ai')) {
          console.log('  [AI INDICATOR] Found AI-related text on Test Scenarios page');
        }

        // Look for any generation buttons
        const generateBtns = await page.$$('button');
        for (const btn of generateBtns) {
          const text = await btn.textContent();
          if (text) {
            console.log(`    - Button: ${text.trim()}`);
          }
        }

        await page.click('text=Test Accelerator');
        await delay(2000);
      } catch (e) {
        console.log(`  Error exploring Test Scenarios: ${e.message}`);
      }
    }

    // ===========================================
    // STEP 3: Explore Execution Studio Menu
    // ===========================================
    console.log('\n[STEP 3] EXPLORING EXECUTION STUDIO MENU...');

    try {
      await page.click('text=Execution Studio');
      await delay(1000);
      await takeScreenshot(page, 'execution-studio-expanded');

      // Test Execution
      await page.click('text=Test Execution');
      await delay(2000);
      await takeScreenshot(page, 'test-execution-page');
      console.log('  Navigated to Test Execution');

      await page.click('text=Test Accelerator');
      await delay(1000);

      // Execution Result
      await page.click('text=Execution Studio');
      await delay(500);
      await page.click('text=Execution Result');
      await delay(2000);
      await takeScreenshot(page, 'execution-result-page');
      console.log('  Navigated to Execution Result');

      await page.click('text=Test Accelerator');
      await delay(1000);
    } catch (e) {
      console.log(`  Error exploring Execution Studio: ${e.message}`);
    }

    // ===========================================
    // STEP 4: Explore Analytics Menu
    // ===========================================
    console.log('\n[STEP 4] EXPLORING ANALYTICS MENU...');

    try {
      await page.click('text=Analytics');
      await delay(1000);
      await takeScreenshot(page, 'analytics-expanded');

      await page.click('text=Report');
      await delay(2000);
      await takeScreenshot(page, 'analytics-report-page');
      console.log('  Navigated to Analytics Report');

      await page.click('text=Test Accelerator');
      await delay(1000);
    } catch (e) {
      console.log(`  Error exploring Analytics: ${e.message}`);
    }

    // ===========================================
    // STEP 5: Look for Microphone/Voice Feature
    // ===========================================
    console.log('\n[STEP 5] CHECKING FOR VOICE/MICROPHONE FEATURE...');

    // Look for microphone icon (I saw one in the header)
    const microphoneSelectors = [
      '[class*="mic"]',
      '[class*="voice"]',
      'button[aria-label*="voice"]',
      'button[aria-label*="mic"]',
      'svg[class*="mic"]',
      '[data-icon="microphone"]'
    ];

    for (const selector of microphoneSelectors) {
      const elements = await page.$$(selector);
      if (elements.length > 0) {
        console.log(`  Found microphone element with selector: ${selector}`);
        findings.aiFeatures.push({ page: 'Header', element: 'Microphone/Voice feature', selector });

        // Try to click it
        try {
          await elements[0].click();
          await delay(2000);
          await takeScreenshot(page, 'voice-feature-activated');
        } catch (e) {
          console.log(`  Could not click microphone: ${e.message}`);
        }
      }
    }

    // Also check for any icon buttons in the header
    const headerButtons = await page.$$('header button, nav button, [class*="header"] button');
    console.log(`  Found ${headerButtons.length} buttons in header area`);

    for (let i = 0; i < headerButtons.length; i++) {
      const btn = headerButtons[i];
      const ariaLabel = await btn.getAttribute('aria-label');
      const className = await btn.getAttribute('class');
      console.log(`    Button ${i + 1}: aria-label="${ariaLabel}", class="${className}"`);

      // Click if it looks like a voice/AI feature
      if (ariaLabel?.toLowerCase().includes('voice') || ariaLabel?.toLowerCase().includes('ai') ||
          className?.toLowerCase().includes('voice') || className?.toLowerCase().includes('ai')) {
        try {
          await btn.click();
          await delay(2000);
          await takeScreenshot(page, `header-btn-${i + 1}-clicked`);
        } catch (e) {
          // ignore
        }
      }
    }

    // ===========================================
    // STEP 6: Deep Dive into Test Scenarios (likely where AI script generation is)
    // ===========================================
    console.log('\n[STEP 6] DEEP DIVE INTO TEST SCENARIOS FOR AI SCRIPT GENERATION...');

    try {
      await page.click('text=Test Studio');
      await delay(500);
      await page.click('text=Test Scenarios');
      await delay(3000);

      // Get all buttons on the page
      const allButtons = await page.$$('button');
      console.log(`  Found ${allButtons.length} buttons on Test Scenarios page`);

      for (const btn of allButtons) {
        const text = await btn.textContent();
        const isVisible = await btn.isVisible();
        if (isVisible && text?.trim()) {
          console.log(`    - ${text.trim()}`);
        }
      }

      // Look for "Create" or "New" or "Add" buttons
      const createButtons = await page.$$('button:has-text("Create"), button:has-text("New"), button:has-text("Add"), button:has-text("+")');
      if (createButtons.length > 0) {
        console.log('\n  Found Create/Add buttons. Clicking first one...');
        await createButtons[0].click();
        await delay(3000);
        await takeScreenshot(page, 'create-scenario-modal');

        // Check for AI generation options in the modal
        const modalContent = await page.evaluate(() => document.body.innerText);
        console.log('\n  Modal/Form content preview:');
        const lines = modalContent.split('\n').filter(l => l.trim()).slice(0, 30);
        lines.forEach(line => {
          if (line.length < 100) console.log(`    ${line}`);
        });

        // Look for AI-related inputs or options
        const aiInputs = await page.$$('[placeholder*="AI"], [placeholder*="generate"], textarea, input[type="text"]');
        console.log(`  Found ${aiInputs.length} input fields`);

        // Check for any "Generate" or AI buttons in the form
        const formButtons = await page.$$('.modal button, [role="dialog"] button, form button');
        for (const btn of formButtons) {
          const text = await btn.textContent();
          if (text?.trim()) {
            console.log(`    Form button: ${text.trim()}`);
            if (text.toLowerCase().includes('generat') || text.toLowerCase().includes('ai')) {
              findings.aiFeatures.push({ page: 'Test Scenarios Form', element: text.trim() });
            }
          }
        }

        // Close modal if there's a close button or by pressing Escape
        await page.keyboard.press('Escape');
        await delay(1000);
      }

    } catch (e) {
      console.log(`  Error in Test Scenarios deep dive: ${e.message}`);
    }

    // ===========================================
    // STEP 7: Check for chat widget or floating AI assistant
    // ===========================================
    console.log('\n[STEP 7] CHECKING FOR CHAT WIDGET OR FLOATING AI ASSISTANT...');

    const chatWidgetSelectors = [
      '[class*="chat"]',
      '[class*="widget"]',
      '[class*="assistant"]',
      '[class*="floating"]',
      '[class*="fab"]',
      'button[class*="chat"]',
      '#chatWidget',
      '.intercom-launcher',
      '[data-testid="chat"]'
    ];

    for (const selector of chatWidgetSelectors) {
      const elements = await page.$$(selector);
      if (elements.length > 0) {
        console.log(`  Found potential chat element: ${selector}`);
        findings.aiFeatures.push({ page: 'Global', element: 'Chat Widget', selector });
      }
    }

    // ===========================================
    // STEP 8: Analyze page for AI-related features in DOM
    // ===========================================
    console.log('\n[STEP 8] ANALYZING DOM FOR AI-RELATED FEATURES...');

    const aiAnalysis = await page.evaluate(() => {
      const results = {
        aiClasses: [],
        aiIds: [],
        aiTextContent: []
      };

      // Search for AI-related class names
      document.querySelectorAll('*').forEach(el => {
        const className = el.className?.toString() || '';
        const id = el.id || '';

        if (className.match(/ai|gpt|chat|generat|copilot|assistant/i)) {
          results.aiClasses.push({ tag: el.tagName, class: className.substring(0, 100) });
        }
        if (id.match(/ai|gpt|chat|generat|copilot|assistant/i)) {
          results.aiIds.push({ tag: el.tagName, id });
        }
      });

      // Search for AI-related text
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const text = node.textContent?.trim();
        if (text && text.match(/\b(AI|artificial intelligence|generate|GPT|copilot)\b/i)) {
          results.aiTextContent.push(text.substring(0, 200));
        }
      }

      return results;
    });

    console.log('  AI-related classes found:', aiAnalysis.aiClasses.length);
    aiAnalysis.aiClasses.forEach(item => console.log(`    - <${item.tag}> class="${item.class}"`));

    console.log('  AI-related IDs found:', aiAnalysis.aiIds.length);
    aiAnalysis.aiIds.forEach(item => console.log(`    - <${item.tag}> id="${item.id}"`));

    console.log('  AI-related text content found:', aiAnalysis.aiTextContent.length);
    aiAnalysis.aiTextContent.slice(0, 10).forEach(text => console.log(`    - "${text}"`));

    // Final screenshot
    await takeScreenshot(page, 'final-state');

    // ===========================================
    // SUMMARY REPORT
    // ===========================================
    console.log('\n' + '='.repeat(70));
    console.log('  TEST ACCELERATOR - AI FUNCTIONALITY REPORT');
    console.log('='.repeat(70));

    console.log('\n[PAGES EXPLORED]');
    console.log('  - Dashboard');
    console.log('  - Test Studio > Test Suites');
    console.log('  - Test Studio > Test Scenarios');
    console.log('  - Execution Studio > Test Execution');
    console.log('  - Execution Studio > Execution Result');
    console.log('  - Analytics > Report');

    console.log('\n[AI FEATURES FOUND]');
    if (findings.aiFeatures.length > 0) {
      findings.aiFeatures.forEach(f => {
        console.log(`  - ${f.page}: ${f.element}`);
      });
    } else {
      console.log('  No explicit AI features found in UI');
    }

    console.log('\n[OBSERVATIONS]');
    console.log('  1. The app is called "ActiveGenie" - suggesting AI/genie capabilities');
    console.log('  2. Main sections: Test Studio, Execution Studio, Analytics');
    console.log('  3. Look for AI features in Test Scenarios creation flow');

    console.log(`\n[SCREENSHOTS SAVED]`);
    console.log(`  Location: ${screenshotsDir}`);
    console.log(`  Total screenshots: ${screenshotCounter}`);

  } catch (error) {
    console.error('\n[ERROR] Test failed:', error);
    await takeScreenshot(page, 'error-state');
  } finally {
    console.log('\n' + '='.repeat(70));
    console.log('Browser will remain open for 30 seconds for manual inspection...');
    console.log('='.repeat(70));
    await delay(30000);
    await browser.close();
  }
}

main().catch(console.error);
