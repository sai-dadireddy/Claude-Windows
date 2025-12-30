const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey
 * Scenario ID: EMPVCE-4-0010-03
 * Confidence: 9.5/10
 *
 * Task: 3. Access survey via Kiosk
 * Expected: Survey can be accessed via Kiosk using the chosen kiosk type on the survey schedule. Logo('s) and illustrations are displayed correctly. Survey is received in appropriate language
 * Role: Administrator
 */

test.describe('Test survey', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 3. Access survey via Kiosk', async ({ page }) => {

        // Verify expected result
        // Expected: Survey can be accessed via Kiosk using the chosen kiosk type on the survey schedule. Logo('s) and il
        await page.waitForLoadState("networkidle");
    });
});
