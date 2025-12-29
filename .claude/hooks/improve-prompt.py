#!/usr/bin/env python3
"""
Claude Code Prompt Improver Hook
Evaluates prompts for clarity and invokes the prompt-improver skill for vague cases.
"""
import json
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')

def sanitize_unicode(text):
    """Remove invalid Unicode surrogates that break JSON encoding."""
    if not text:
        return ""
    # Remove surrogates by encoding with 'surrogatepass' and replacing errors
    try:
        # First try to encode/decode normally
        return text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='replace')
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If that fails, remove all non-BMP characters and surrogates
        return ''.join(c for c in text if ord(c) < 0xD800 or (ord(c) > 0xDFFF and ord(c) < 0x10000))

def output_json(text):
    """Output text in UserPromptSubmit JSON format"""
    # Sanitize text before JSON encoding
    safe_text = sanitize_unicode(text)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": safe_text
        }
    }
    # Use ensure_ascii=True to avoid any Unicode issues in output
    print(json.dumps(output, ensure_ascii=True))

# Load input from stdin
try:
    raw_input = sys.stdin.read()
    # Sanitize input before JSON parsing
    safe_input = sanitize_unicode(raw_input)
    input_data = json.loads(safe_input)
except json.JSONDecodeError as e:
    # If JSON parsing fails, output empty and exit gracefully
    print(json.dumps({"hookSpecificOutput": {}}))
    sys.exit(0)
except Exception as e:
    print(json.dumps({"hookSpecificOutput": {}}))
    sys.exit(0)

prompt = input_data.get("prompt", "")

# Sanitize the prompt
prompt = sanitize_unicode(prompt)

# Escape quotes in prompt for safe embedding
escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')

# Check for bypass conditions
# 1. Explicit bypass with * prefix
# 2. Slash commands (built-in or custom)
# 3. Memorize feature (# prefix)
if prompt.startswith("*"):
    # User explicitly bypassed improvement - remove * prefix
    clean_prompt = prompt[1:].strip()
    output_json(clean_prompt)
    sys.exit(0)

if prompt.startswith("/"):
    # Slash command - pass through unchanged
    output_json(prompt)
    sys.exit(0)

if prompt.startswith("#"):
    # Memorize feature - pass through unchanged
    output_json(prompt)
    sys.exit(0)

# Build the evaluation wrapper
wrapped_prompt = f"""PROMPT EVALUATION

Original user request: "{escaped_prompt}"

EVALUATE: Is this prompt clear enough to execute, or does it need enrichment?

PROCEED IMMEDIATELY if:
- Detailed/specific OR you have sufficient context OR can infer intent

ONLY USE SKILL if genuinely vague (e.g., "fix the bug" with no context):
- If vague:
  1. First, preface with brief note: "Hey! The Prompt Improver Hook flagged your prompt as a bit vague because [specific reason: ambiguous scope/missing context/unclear target/etc]."
  2. Then use the prompt-improver skill to research and generate clarifying questions
- The skill will guide you through research, question generation, and execution
- Trust user intent by default. Check conversation history before using the skill.

If clear, proceed with the original request. If vague, invoke the skill."""

output_json(wrapped_prompt)
sys.exit(0)
