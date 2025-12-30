const { test, expect } = require('@playwright/test');

/**
 * Test: SSO
 * Scenario ID: EMPVCE-4-0080
 * Confidence: 7.5/10
 *
 * Task: No task specified
 * Expected: SSO authentication is started when email address is entered on login screen and you select continue.
 * Role: Administrator
 */

test.describe('SSO', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: No task specified', async ({ page }) => {

        // Verify expected result
        // Expected: SSO authentication is started when email address is entered on login screen and you select continue.
        await page.waitForLoadState("networkidle");
    });
});
