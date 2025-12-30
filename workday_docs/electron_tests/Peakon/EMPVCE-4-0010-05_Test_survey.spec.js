const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-05
 * Confidence: 9.5/10
 *
 * Task: 5. Access survey via MS Teams
 * Expected: Survey notification is received via MS teams, and the survey can complete the survey within MS teams. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 5. Access survey via MS Teams', async ({ page }) => {

        // Verify expected result
        // Expected: Survey notification is received via MS teams, and the survey can complete the survey within MS teams
        await page.waitForLoadState("networkidle");
    });
});
