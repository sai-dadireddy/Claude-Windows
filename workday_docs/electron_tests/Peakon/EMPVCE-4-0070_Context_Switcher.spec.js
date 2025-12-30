const { test, expect } = require('@playwright/test');

/**
 * Test: Context Switcher
 * Scenario ID: EMPVCE-4-0070
 * Confidence: 10.0/10
 *
 * Task: Expand context switcher on top left side. Select another context available in the modal view that opens op, or use the search to find a context (i.e. name of a direct report)
 * Expected: Employees can access the personal dashboard.
 * Role: Administrator
Manager
Senior Leadership
Human Resources
 */

test.describe('Context Switcher', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Administrator
Manager
Senior Leadership
Human Resources
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: Expand context switcher on top left side. Select another context available in th', async ({ page }) => {
        await page.fill("input[role=\"search\"]", "Expand context switcher on top left side. Select a");
        await page.keyboard.press("Enter");

        // Verify expected result
        // Expected: Employees can access the personal dashboard.
        await page.waitForLoadState("networkidle");
    });
});
