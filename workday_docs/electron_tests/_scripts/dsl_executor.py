#!/usr/bin/env python3
"""
DSL Executor - Runs Test Accelerator DSL scripts using Playwright
Usage: python dsl_executor.py <test_file.txt>
"""

import sys
import re
import time
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page, TimeoutError as PlaywrightTimeout


class DSLExecutor:
    def __init__(self, headless: bool = False, debug: bool = False):
        self.headless = headless
        self.debug = debug
        self.page: Page = None
        self.results = []
        self.screenshot_dir = Path(__file__).parent / 'screenshots'
        if self.debug:
            self.screenshot_dir.mkdir(exist_ok=True)

    async def execute_file(self, filepath: str) -> dict:
        """Execute a DSL test file and return results"""
        content = Path(filepath).read_text(encoding='utf-8')

        # Extract ELECTRON STEPS section
        steps = self._parse_steps(content)

        print(f"\n{'='*60}")
        print(f"Executing: {Path(filepath).name}")
        print(f"Total steps: {len(steps)}")
        print(f"{'='*60}\n")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            self.page = await context.new_page()

            passed = 0
            failed = 0

            for i, step in enumerate(steps, 1):
                result = await self._execute_step(step, i)
                if result['status'] == 'passed':
                    passed += 1
                    print(f"  [{i}] PASS: {step[:50]}...")
                elif result['status'] == 'skipped':
                    print(f"  [{i}] SKIP: {step[:50]}...")
                else:
                    failed += 1
                    print(f"  [{i}] FAIL: {step[:50]}...")
                    print(f"       Error: {result.get('error', 'Unknown')}")
                self.results.append(result)

            await browser.close()

        summary = {
            'file': filepath,
            'total': len(steps),
            'passed': passed,
            'failed': failed,
            'results': self.results
        }

        print(f"\n{'='*60}")
        print(f"SUMMARY: {passed} passed, {failed} failed, {len(steps)} total")
        print(f"{'='*60}\n")

        return summary

    def _parse_steps(self, content: str) -> list:
        """Extract executable steps from DSL file"""
        steps = []
        in_steps = False

        for line in content.split('\n'):
            line = line.strip()

            # Start capturing after ELECTRON STEPS header
            if 'ELECTRON STEPS' in line:
                in_steps = True
                continue

            # Stop at VERIFICATION or STATUS sections
            if in_steps and (line.startswith('VERIFICATION:') or line.startswith('STATUS:')):
                break

            # Skip comments and empty lines
            if not line or line.startswith('#') or line.startswith('//'):
                continue

            # Skip template placeholders
            if '{{' in line and '}}' in line:
                continue

            if in_steps:
                steps.append(line)

        return steps

    async def _execute_step(self, step: str, step_num: int) -> dict:
        """Execute a single DSL step"""
        step_lower = step.lower()

        try:
            # Navigate to URL
            if step_lower.startswith('navigate to'):
                url = step.split('Navigate to', 1)[1].strip()
                await self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
                return {'step': step, 'status': 'passed'}

            # Wait for N seconds
            if 'wait for' in step_lower and 'second' in step_lower:
                match = re.search(r'(\d+)\s*second', step_lower)
                if match:
                    seconds = int(match.group(1))
                    await asyncio.sleep(seconds)
                    return {'step': step, 'status': 'passed'}

            # Enter username/password
            if 'enter the username as' in step_lower:
                username = step.split(' as ', 1)[1].strip()
                await self.page.fill('input[name="userName"], input[type="text"]', username)
                return {'step': step, 'status': 'passed'}

            if 'enter the password as' in step_lower:
                password = step.split(' as ', 1)[1].strip()
                await self.page.fill('input[name="password"], input[type="password"]', password)
                return {'step': step, 'status': 'passed'}

            # Click on button
            if "click on the 'sign in' button" in step_lower or 'click sign in' in step_lower:
                await self.page.click('button[type="submit"], button:has-text("Sign In")')
                return {'step': step, 'status': 'passed'}

            # Click on Search button (Workday-specific)
            if "click on the 'search' button" in step_lower:
                # Workday search bar - try multiple selectors
                selectors = [
                    '[data-automation-id="searchBox"]',
                    '[data-automation-id="globalSearchButton"]',
                    '[data-automation-id="SEARCH_CATEGORY_INPUT"]',
                    'input[placeholder*="Search"]',
                    '[aria-label*="Search"]',
                    '.search-box',
                    'button[title="Search"]',
                ]
                for sel in selectors:
                    try:
                        await self.page.click(sel, timeout=3000)
                        return {'step': step, 'status': 'passed'}
                    except:
                        continue
                # Last resort - find any search-related element
                await self.page.click('text="Search"')
                return {'step': step, 'status': 'passed'}

            # Enter in search field (Workday-specific)
            if 'enter' in step_lower and 'in the search field' in step_lower:
                search_text = step[step.lower().find('enter')+6:step.lower().find('in the search field')].strip()
                selectors = [
                    '[data-automation-id="searchBox"] input',
                    '[data-automation-id="globalSearchInput"]',
                    'input[placeholder*="Search"]',
                    '[data-automation-id="SEARCH_CATEGORY_INPUT"]',
                    'input[type="search"]',
                    'input[aria-label*="Search"]',
                ]
                for sel in selectors:
                    try:
                        await self.page.fill(sel, search_text, timeout=3000)
                        return {'step': step, 'status': 'passed'}
                    except:
                        continue
                # Last resort - type into active element
                await self.page.keyboard.type(search_text)
                return {'step': step, 'status': 'passed'}

            # Press Enter
            if step_lower == 'press enter':
                await self.page.keyboard.press('Enter')
                return {'step': step, 'status': 'passed'}

            # Click on link (Workday search results)
            if step_lower.startswith("click on '") and "' link" in step_lower:
                match = re.search(r"click on '(.+?)' link", step, re.IGNORECASE)
                if match:
                    link_text = match.group(1)
                    # Wait for search results to appear
                    await asyncio.sleep(1)
                    selectors = [
                        f'a:has-text("{link_text}")',
                        f'[data-automation-id="searchResultItem"] a:has-text("{link_text}")',
                        f'[role="link"]:has-text("{link_text}")',
                        f'[role="option"]:has-text("{link_text}")',
                    ]
                    clicked = False
                    for sel in selectors:
                        try:
                            # Click and wait for navigation
                            async with self.page.expect_navigation(timeout=15000, wait_until='domcontentloaded'):
                                await self.page.click(sel, timeout=5000)
                            clicked = True
                            break
                        except:
                            try:
                                # Try click without navigation wait
                                await self.page.click(sel, timeout=3000)
                                await asyncio.sleep(2)  # Wait for possible page change
                                clicked = True
                                break
                            except:
                                continue
                    if not clicked:
                        # Last resort - click text directly
                        await self.page.click(f'text="{link_text}"')
                        await asyncio.sleep(2)
                    return {'step': step, 'status': 'passed'}

            # Click OK button
            if 'click ok button' in step_lower:
                await self.page.click('button:has-text("OK"), [data-automation-id="ok"]')
                return {'step': step, 'status': 'passed'}

            # Select option
            if step_lower.startswith('select') and ' as ' in step_lower:
                # Skip template placeholders
                if '{{' in step:
                    return {'step': step, 'status': 'skipped', 'reason': 'Template placeholder'}
                field = step.split('Select ', 1)[1].split(' as ')[0].strip()
                value = step.split(' as ', 1)[1].strip()
                # Try to find and click the dropdown/combobox
                await self.page.click(f'[data-automation-id*="{field}"], label:has-text("{field}")')
                await asyncio.sleep(0.5)
                await self.page.click(f'[role="option"]:has-text("{value}")')
                return {'step': step, 'status': 'passed'}

            # Verify page contains
            if 'verify page contains' in step_lower:
                text = step.split('Verify page contains', 1)[1].strip()
                await self.page.wait_for_selector(f'text="{text}"', timeout=10000)
                return {'step': step, 'status': 'passed'}

            # Unknown step
            return {'step': step, 'status': 'skipped', 'reason': 'Unknown DSL command'}

        except PlaywrightTimeout as e:
            if self.debug:
                await self._capture_screenshot(f'fail_step{step_num}')
            return {'step': step, 'status': 'failed', 'error': f'Timeout: {str(e)[:100]}'}
        except Exception as e:
            if self.debug:
                await self._capture_screenshot(f'fail_step{step_num}')
            return {'step': step, 'status': 'failed', 'error': str(e)[:200]}

    async def _capture_screenshot(self, name: str):
        """Capture screenshot for debugging"""
        try:
            path = self.screenshot_dir / f'{name}_{int(time.time())}.png'
            await self.page.screenshot(path=str(path))
            print(f"       Screenshot: {path}")
        except:
            pass


async def main():
    if len(sys.argv) < 2:
        print("Usage: python dsl_executor.py <test_file.txt> [--headless] [--debug]")
        print("\nOptions:")
        print("  --headless  Run without visible browser")
        print("  --debug     Capture screenshots on failures")
        print("\nExample:")
        print("  python dsl_executor.py STU-1-0010_Student_Load_Status.txt")
        print("  python dsl_executor.py STU-1-0010_Student_Load_Status.txt --debug")
        sys.exit(1)

    filepath = sys.argv[1]
    headless = '--headless' in sys.argv
    debug = '--debug' in sys.argv

    if not Path(filepath).exists():
        # Try relative to electron_tests directory
        base = Path(__file__).parent.parent
        for area in base.iterdir():
            if area.is_dir() and not area.name.startswith('_'):
                candidate = area / filepath
                if candidate.exists():
                    filepath = str(candidate)
                    break

    executor = DSLExecutor(headless=headless, debug=debug)
    results = await executor.execute_file(filepath)

    # Return exit code based on failures
    sys.exit(1 if results['failed'] > 0 else 0)


if __name__ == '__main__':
    asyncio.run(main())
