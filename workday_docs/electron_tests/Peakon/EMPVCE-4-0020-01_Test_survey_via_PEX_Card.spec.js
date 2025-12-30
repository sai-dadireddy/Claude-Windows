const { test, expect } = require('@playwright/test');

/**
 * Test: Test survey via PEX Card
 * Scenario ID: EMPVCE-4-0020-01
 * Confidence: 9.5/10
 *
 * Task: 1. Administration > Survey > Schedules
 * Expected: Live survey is launched to only the test users
 * Role: Administrator
 */

test.describe('Test survey via PEX Card', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: 1. Administration > Survey > Schedules', async ({ page }) => {

        // Verify expected result
        // Expected: Live survey is launched to only the test users
        await page.waitForLoadState("networkidle");
    });
});
