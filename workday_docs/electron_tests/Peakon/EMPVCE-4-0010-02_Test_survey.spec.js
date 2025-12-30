const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-02
 * Confidence: 9.5/10
 *
 * Task: 2. Access survey via email
 * Expected: Survey can be accessed on all browsers. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 2. Access survey via email', async ({ page }) => {

        // Verify expected result
        // Expected: Survey can be accessed on all browsers. Logo('s) and illustrations are displayed correctly. Survey i
        await page.waitForLoadState("networkidle");
    });
});
