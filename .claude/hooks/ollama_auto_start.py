#!/usr/bin/env python3
"""
Ollama Auto-Start Hook - Starts Ollama on-demand when AI category is used
For RAM-constrained systems (16GB), only starts when actually needed.

Triggers: PreToolUse for mcp__router__router_execute with category="ai"
"""

import sys
import json
import subprocess
import time
import urllib.request
import urllib.error

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')

OLLAMA_URL = "http://localhost:11434"

def sanitize_unicode(text):
    """Remove invalid Unicode surrogates that break JSON encoding."""
    if not text:
        return ""
    try:
        return text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return ''.join(c for c in text if ord(c) < 0xD800 or (ord(c) > 0xDFFF and ord(c) < 0x10000))

def is_ollama_running():
    """Check if Ollama API is responding."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except:
        return False

def start_ollama():
    """Start Ollama in background."""
    try:
        # Start ollama serve in background
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )

        # Wait for it to be ready (max 15 seconds)
        for _ in range(30):
            time.sleep(0.5)
            if is_ollama_running():
                return True
        return False
    except Exception as e:
        return False

def main():
    try:
        # Read input
        input_data = sanitize_unicode(sys.stdin.read())

        try:
            data = json.loads(input_data)
        except:
            # Not valid JSON, pass through
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        # Check if this is a router_execute call for AI category
        tool_name = data.get("toolName", "")
        tool_input = data.get("toolInput", {})

        # Only trigger for AI category calls
        if tool_name != "mcp__router__router_execute":
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        category = tool_input.get("category", "")
        server = tool_input.get("server", "")

        # Check if this is for Ollama
        if category != "ai" or server != "ollama":
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        # Check if Ollama is running
        if is_ollama_running():
            # Already running, proceed
            print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))
            return

        # Need to start Ollama
        context = "[AUTO-START] Starting Ollama for AI request... "

        if start_ollama():
            context += "Ollama started successfully."
        else:
            context += "WARNING: Failed to start Ollama. Request may fail."

        result = {
            "hookSpecificOutput": {
                "additionalContext": sanitize_unicode(context)
            }
        }
        print(json.dumps(result, ensure_ascii=True))

    except Exception as e:
        # Fail gracefully
        print(json.dumps({"hookSpecificOutput": {}}, ensure_ascii=True))

if __name__ == '__main__':
    main()
