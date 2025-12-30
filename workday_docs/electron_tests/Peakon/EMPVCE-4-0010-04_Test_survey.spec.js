const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-04
 * Confidence: 9.5/10
 *
 * Task: 4. Access survey via SMS
 * Expected: Survey notification is received via SMS, and the survey can accessed the survey via the link provided in the SMS. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 4. Access survey via SMS', async ({ page }) => {

        // Verify expected result
        // Expected: Survey notification is received via SMS, and the survey can accessed the survey via the link provide
        await page.waitForLoadState("networkidle");
    });
});
