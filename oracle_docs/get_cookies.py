#!/usr/bin/env python3
"""Extract Oracle cookies from Chrome browser locally"""

import os
import sys
import json
import sqlite3
import shutil
from pathlib import Path
from datetime import datetime

# Chrome cookie paths by OS
CHROME_PATHS = {
    'win32': Path(os.environ.get('LOCALAPPDATA', '')) / 'Google/Chrome/User Data/Default/Network/Cookies',
    'darwin': Path.home() / 'Library/Application Support/Google/Chrome/Default/Cookies',
    'linux': Path.home() / '.config/google-chrome/Default/Cookies'
}

def get_chrome_cookies(domain_filter='oracle.com'):
    """Extract cookies from Chrome's SQLite database"""

    cookie_path = CHROME_PATHS.get(sys.platform)
    if not cookie_path or not cookie_path.exists():
        print(f"Chrome cookies not found at: {cookie_path}")
        print("\nTry Method 2: DevTools export (see instructions below)")
        return None

    # Copy database (Chrome locks it while running)
    temp_path = Path.home() / '.chrome_cookies_temp.db'
    shutil.copy2(cookie_path, temp_path)

    try:
        conn = sqlite3.connect(str(temp_path))
        cursor = conn.cursor()

        # Query cookies for domain
        cursor.execute("""
            SELECT host_key, name, value, path, expires_utc, is_secure, is_httponly
            FROM cookies
            WHERE host_key LIKE ?
        """, (f'%{domain_filter}%',))

        cookies = []
        for row in cursor.fetchall():
            host, name, value, path, expires, secure, httponly = row
            cookies.append({
                'domain': host,
                'name': name,
                'value': value,
                'path': path,
                'expires': expires,
                'secure': bool(secure),
                'httpOnly': bool(httponly)
            })

        conn.close()
        return cookies

    finally:
        temp_path.unlink(missing_ok=True)

def save_cookies_json(cookies, output_file='oracle_cookies.json'):
    """Save cookies as JSON (for Playwright)"""
    with open(output_file, 'w') as f:
        json.dump(cookies, f, indent=2)
    print(f"Saved {len(cookies)} cookies to {output_file}")

def save_cookies_netscape(cookies, output_file='cookies.txt'):
    """Save cookies in Netscape format (for curl, wget)"""
    lines = ["# Netscape HTTP Cookie File"]

    for c in cookies:
        # Netscape format: domain, flag, path, secure, expiry, name, value
        domain = c['domain']
        flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = c.get('path', '/')
        secure = 'TRUE' if c.get('secure') else 'FALSE'
        expiry = str(c.get('expires', 0))
        name = c['name']
        value = c['value']

        lines.append(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}")

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Saved {len(cookies)} cookies to {output_file}")

def main():
    print("=" * 50)
    print("Oracle Cookie Extractor")
    print("=" * 50)
    print()

    # Check if Chrome is running
    print("Note: Close Chrome for best results (it locks the cookie database)")
    print()

    cookies = get_chrome_cookies('oracle.com')

    if cookies:
        print(f"Found {len(cookies)} Oracle cookies")
        print()

        # Save both formats
        output_dir = Path(__file__).parent
        save_cookies_json(cookies, output_dir / 'oracle_cookies.json')
        save_cookies_netscape(cookies, output_dir / 'cookies.txt')

        print()
        print("Files created:")
        print(f"  - oracle_cookies.json (for Playwright/AWS)")
        print(f"  - cookies.txt (Netscape format for curl)")

    else:
        print()
        print("=" * 50)
        print("METHOD 2: DevTools Export")
        print("=" * 50)
        print("""
1. Open Chrome and login to https://support.oracle.com
2. Press F12 to open DevTools
3. Go to Console tab
4. Paste this script and press Enter:

(function() {
    const cookies = document.cookie.split(';').map(c => {
        const [name, ...rest] = c.trim().split('=');
        return {
            name: name,
            value: rest.join('='),
            domain: '.oracle.com',
            path: '/'
        };
    });
    const json = JSON.stringify(cookies, null, 2);
    const blob = new Blob([json], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'oracle_cookies.json';
    a.click();
    console.log('Downloaded ' + cookies.length + ' cookies!');
})();

5. File will download automatically
""")

if __name__ == '__main__':
    main()
