#!/usr/bin/env python3
"""
Quick syntax validation for MCP servers
"""

import sys
import ast
import io

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "✅ Syntax valid"
    except SyntaxError as e:
        return False, f"❌ Syntax error: {e}"
    except Exception as e:
        return False, f"❌ Error: {e}"

if __name__ == "__main__":
    servers = [
        ("code-indexing", "projects/code-indexing/mcp-server/server.py"),
        ("testing-mcp", "projects/testing-mcp/server.py"),
    ]

    print("Testing MCP Server Syntax...\n")

    all_valid = True
    for name, path in servers:
        valid, msg = check_syntax(path)
        print(f"{name}: {msg}")
        if not valid:
            all_valid = False

    if all_valid:
        print("\n✅ All servers have valid syntax!")
        print("\nNext steps:")
        print("1. Install dependencies:")
        print("   pip install -r code-indexing/requirements.txt")
        print("   pip install -r testing-mcp/requirements.txt")
        print("\n2. Restart Claude Desktop to load new servers")
        print("\n3. Test in Claude Desktop by asking:")
        print("   - 'Index my codebase'")
        print("   - 'Search for authentication logic'")
        print("   - 'Run all tests'")
        sys.exit(0)
    else:
        print("\n❌ Some servers have syntax errors!")
        sys.exit(1)
