const { test, expect } = require('@playwright/test');

/**
 * Test: Review Role Based security group permissions
 * Scenario ID: PRA-1-0110
 * Confidence: 7.5/10
 *
 * Task: Go to: Data Catalog > Related Actions > Share
 * Expected: No expected result specified
 * Role: Prism Admn/Dataset Owner, etc
 */

test.describe('Review Role Based security group permissions', () => {
    test.beforeEach(async ({ page }) => {
        // Login as Prism Admn/Dataset Owner, etc
        await page.goto('https://wd5-impl.workday.com');
        // Add authentication steps
    });

    test('should complete: Go to: Data Catalog > Related Actions > Share', async ({ page }) => {

        // Verify expected result
        // Expected: No expected result specified
        await page.waitForLoadState("networkidle");
    });
});
