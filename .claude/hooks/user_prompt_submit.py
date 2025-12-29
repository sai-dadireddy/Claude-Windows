#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-toon"]
# ///
"""
UserPromptSubmit Hook - Credential detection, MD warnings, TOON conversion

Features:
- Blocks prompts containing credentials
- Warns about MD file restrictions
- Converts JSON in prompts to TOON format (30-60% token savings)

TOON (Token-Oriented Object Notation) is a compact format for LLMs.
"""

import json
import sys
import re
from pathlib import Path

LOG_DIR = Path.home() / ".claude" / "logs"
HOOK_LOG = LOG_DIR / "hooks.log"
VERBOSE = False

def log(msg: str):
    if VERBOSE:
        print(f"[UserPromptSubmit] {msg}", file=sys.stderr)

def log_to_file(msg: str):
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [UPS] {msg}\n")
    except:
        pass

def block(reason: str):
    """Block prompt with user-visible message"""
    output = {
        "systemMessage": f"[STOP] {reason}",
        "decision": "block",
        "reason": reason
    }
    print(json.dumps(output))
    sys.exit(0)

def json_to_toon(data) -> str:
    """Convert JSON data to TOON format"""
    try:
        from toon import encode
        return encode(data)
    except ImportError:
        # Fallback: simple TOON-like format
        return fallback_toon(data)
    except Exception:
        return None

def fallback_toon(data, indent=0) -> str:
    """Fallback TOON-like encoding without library"""
    prefix = " " * indent

    if isinstance(data, dict):
        lines = []
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{prefix}{k}:")
                lines.append(fallback_toon(v, indent + 1))
            else:
                val = "null" if v is None else str(v)
                lines.append(f"{prefix}{k}: {val}")
        return "\n".join(lines)

    elif isinstance(data, list):
        if not data:
            return f"{prefix}[]"

        # Check if uniform array of objects
        if all(isinstance(x, dict) for x in data) and len(data) > 1:
            keys = list(data[0].keys())
            if all(set(x.keys()) == set(keys) for x in data):
                # Tabular format
                lines = [f"{prefix}[{len(data)}]{{{','.join(keys)}}}:"]
                for item in data:
                    vals = [str(item.get(k, "")) for k in keys]
                    lines.append(f"{prefix} {','.join(vals)}")
                return "\n".join(lines)

        # Regular array
        lines = []
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.append(fallback_toon(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
        return "\n".join(lines)

    else:
        return f"{prefix}{data}"

def convert_json_in_prompt(prompt: str) -> str:
    """Find and convert JSON blocks in prompt to TOON"""

    # Pattern for JSON code blocks
    json_block_pattern = r'```(?:json)?\s*\n([\s\S]*?)\n```'

    def replace_json_block(match):
        content = match.group(1).strip()
        try:
            data = json.loads(content)
            toon = json_to_toon(data)
            if toon and len(toon) < len(content) * 0.9:  # Only if saves >10%
                return f"```toon\n{toon}\n```"
        except:
            pass
        return match.group(0)

    # Replace JSON code blocks
    result = re.sub(json_block_pattern, replace_json_block, prompt)

    # Pattern for inline JSON objects (not in code blocks)
    # Only convert substantial JSON (> 100 chars)
    inline_pattern = r'(?<![`\w])(\{[^{}]{100,}\})(?![`\w])'

    def replace_inline_json(match):
        content = match.group(1)
        try:
            data = json.loads(content)
            toon = json_to_toon(data)
            if toon and len(toon) < len(content) * 0.85:
                return f"\n```toon\n{toon}\n```\n"
        except:
            pass
        return match.group(0)

    result = re.sub(inline_pattern, replace_inline_json, result)

    return result

def main():
    log_to_file("Hook invoked")
    try:
        data = json.load(sys.stdin)
    except:
        log_to_file("Failed to parse JSON")
        sys.exit(0)

    prompt = data.get("prompt", "")
    original_len = len(prompt)
    log_to_file(f"Prompt: {prompt[:50]}...")
    log(f"[RECV] Received prompt ({original_len} chars)")

    # Log prompt length
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Block credentials
    creds = [
        (r"(api[_-]?key|apikey)\s*[=:]\s*['\"]?[a-zA-Z0-9_-]{20,}", "API key"),
        (r"(password|passwd)\s*[=:]\s*['\"]?[^\s'\"]{8,}", "password"),
        (r"(secret|token)\s*[=:]\s*['\"]?[a-zA-Z0-9_-]{20,}", "secret"),
        (r"-----BEGIN.*PRIVATE KEY-----", "private key"),
    ]
    for pat, name in creds:
        if re.search(pat, prompt, re.I):
            block(f"Remove {name} from prompt")

    # Convert JSON to TOON
    converted_prompt = convert_json_in_prompt(prompt)

    # Log stats
    try:
        with open(LOG_DIR / "prompts.jsonl", "a") as f:
            savings = original_len - len(converted_prompt)
            f.write(json.dumps({
                "len": original_len,
                "toon_len": len(converted_prompt),
                "saved": savings if savings > 0 else 0
            }) + "\n")
    except:
        pass

    # Output converted prompt if different
    if converted_prompt != prompt and len(converted_prompt) < original_len:
        # Return modified prompt
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "modifiedPrompt": converted_prompt
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    # MD file warning with systemMessage
    if re.search(r"\b(create|make|write)\b.*\.(md|markdown)\b", prompt, re.I):
        output = {"systemMessage": "[NOTE] Note: Only CLAUDE.md, README.md, CHANGELOG.md allowed"}
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
