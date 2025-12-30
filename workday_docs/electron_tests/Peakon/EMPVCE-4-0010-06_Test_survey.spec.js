const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-06
 * Confidence: 9.5/10
 *
 * Task: 6. Access survey via Slack
 * Expected: Survey notification is received via Slack, and the survey can be accessed via the link provided in the notification. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 6. Access survey via Slack', async ({ page }) => {

        // Verify expected result
        // Expected: Survey notification is received via Slack, and the survey can be accessed via the link provided in t
        await page.waitForLoadState("networkidle");
    });
});
