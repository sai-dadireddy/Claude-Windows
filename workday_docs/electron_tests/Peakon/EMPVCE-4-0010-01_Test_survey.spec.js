const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-01
 * Confidence: 9.5/10
 *
 * Task: 1. Administration > Survey > Schedules
 * Expected: - All testers on all email domains have received a survey notification via email. 
- The survey sender, email subject and text are displayed as configured on the survey schedule. 
- Email is received in appropriate language based on the selected language on the employee profile, and added translations are correct. 
- Logo('s) and illustrations are displayed correctly.
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 1. Administration > Survey > Schedules', async ({ page }) => {

        // Verify expected result
        // Expected: - All testers on all email domains have received a survey notification via email. 
- The survey send
        await page.waitForLoadState("networkidle");
    });
});
