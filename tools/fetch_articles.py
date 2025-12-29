#!/usr/bin/env python3
"""
Fetch articles using Playwright for pages that block standard requests
"""
import asyncio
from playwright.async_api import async_playwright
import sys

async def fetch_article(url):
    """Fetch article content using Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to URL
            await page.goto(url, wait_until='networkidle')

            # Wait for content to load
            await page.wait_for_timeout(2000)

            # Get page content
            content = await page.content()

            # Get text content
            text_content = await page.evaluate('''() => {
                // Remove scripts, styles, etc
                const unwanted = document.querySelectorAll('script, style, noscript, iframe');
                unwanted.forEach(el => el.remove());
                return document.body.innerText;
            }''')

            await browser.close()
            return text_content

        except Exception as e:
            await browser.close()
            return f"Error: {e}"

async def main():
    urls = [
        "https://alirezarezvani.medium.com/5-tipps-to-automate-your-code-reviews-with-claude-code-5becd60bce5c",
        "https://claude.ai/public/artifacts/2b5f610d-a357-498a-b8f6-02a83d7ed1be"
    ]

    for url in urls:
        print(f"\n{'='*80}")
        print(f"Fetching: {url}")
        print('='*80)
        content = await fetch_article(url)
        print(content[:2000])  # First 2000 chars
        print(f"\n... (truncated)\n")

if __name__ == "__main__":
    asyncio.run(main())
