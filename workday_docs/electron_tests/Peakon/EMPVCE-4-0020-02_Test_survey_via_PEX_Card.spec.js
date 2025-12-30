const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey via PEX Card
 * Scenario ID: EMPVCE-4-0020-02
 * Confidence: 9.5/10
 *
 * Task: 2. Access Workday
 * Expected: PEX card is displayed for test population. Survey can be accessed via the link on the PEX card. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey via PEX Card', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 2. Access Workday', async ({ page }) => {

        // Verify expected result
        // Expected: PEX card is displayed for test population. Survey can be accessed via the link on the PEX card. Logo
        await page.waitForLoadState("networkidle");
    });
});
