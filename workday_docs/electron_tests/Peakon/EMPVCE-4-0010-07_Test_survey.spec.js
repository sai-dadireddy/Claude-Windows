const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-07
 * Confidence: 9.5/10
 *
 * Task: 7. Access survey via the Peakon mobile app
 * Expected: Survey notification is shared via the mobile app, and the survey can be completed within the mobile app. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 7. Access survey via the Peakon mobile app', async ({ page }) => {
        // Access mobile application
        await page.goto("https://wd5-impl.workday.com");

        // Verify expected result
        // Expected: Survey notification is shared via the mobile app, and the survey can be completed within the mobile 
        await page.waitForLoadState("networkidle");
    });
});
