#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Skill Reminder Hook (UserPromptSubmit) - OPTIMIZED VERSION

Detects task types and reminds Claude about relevant skills/commands.
Uses pre-compiled regex patterns and minimal output for efficiency.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime

HOOK_LOG = Path.home() / ".claude" / "logs" / "hooks.log"

def log_hook(msg: str):
    try:
        HOOK_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG, "a") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} [SkillReminder] {msg}\n")
    except:
        pass

# === PRE-COMPILED PATTERNS (for speed) ===
# Each tuple: (compiled_regex, category, skill/command, short_hint)

PATTERNS = [
    # Document tasks
    (re.compile(r"\b(create|make|generate|write|edit)\s+(a\s+)?(word|doc|docx)\b", re.I), "doc", "docx", "Use docx skill"),
    (re.compile(r"\b(create|make|generate|write|edit)\s+(a\s+)?(pdf)\b", re.I), "doc", "pdf", "Use pdf skill"),
    (re.compile(r"\b(create|make|generate|write|edit)\s+(a\s+)?(powerpoint|pptx|presentation|slides?)\b", re.I), "doc", "pptx", "Use pptx skill"),
    (re.compile(r"\b(create|make|generate|write|edit)\s+(a\s+)?(excel|xlsx|spreadsheet)\b", re.I), "doc", "xlsx", "Use xlsx skill"),

    # Debugging - combined patterns
    (re.compile(r"\b(debug|fix|troubleshoot|investigate|diagnose)\s+|\b(error|bug|issue|problem|broken|failing)\b", re.I), "debug", "systematic-debugging", "Root-cause analysis"),

    # Testing
    (re.compile(r"\b(write|add|create|implement)\s+(unit\s+)?tests?\b|\btdd\b|\btest-driven\b", re.I), "test", "/tdd", "RED-GREEN-REFACTOR"),
    (re.compile(r"\b(e2e|end-to-end|integration)\s+test|\bplaywright\b|\bpuppeteer\b", re.I), "test", "webapp-testing", "Browser automation"),

    # Planning
    (re.compile(r"\b(plan|design|architect)\s+(the\s+)?(implementation|feature|project)\b|\bprd\b", re.I), "plan", "/plan-feature", "Plan before code"),
    (re.compile(r"\b(brainstorm|ideate|explore\s+options|think\s+through)\b|\btrade-?offs?\b", re.I), "plan", "/brainstorm", "Multi-perspective"),

    # Code review
    (re.compile(r"\b(review|check|audit)\s+(the\s+)?(code|pr|pull\s+request)\b|\bcode\s+quality\b", re.I), "review", "/review-pr", "Quality gates"),

    # MCP building
    (re.compile(r"\b(create|build|make)\s+(an?\s+)?mcp\s+(server|tool)\b|\bmcp\s+(server|integration)\b", re.I), "mcp", "mcp-builder", "MCP best practices"),

    # Security
    (re.compile(r"\b(security|vulnerability|exploit|injection)\b|\baudit\s+(the\s+)?(code|security)\b", re.I), "sec", "/security-review", ">80% exploitability"),

    # Explore codebase
    (re.compile(r"\b(where|how)\s+(is|does|are)\s+\w+\s+(work|handle|located)\b|\bunderstand\s+(the\s+)?codebase\b", re.I), "explore", "/explore", "Read-only navigation"),

    # Bug fix workflow
    (re.compile(r"\b(fix|diagnose|troubleshoot)\s+(this\s+)?(bug|issue|error|problem)\b|\bproduction\s+(issue|bug)\b", re.I), "bug", "/lite-fix", "Severity-adaptive"),

    # Context/session
    (re.compile(r"\b(context|token)\s+(full|limit|running\s+out)\b|\bcompact\s+(the\s+)?context\b", re.I), "ctx", "/compact-context", "Save state first"),
    (re.compile(r"\b(create|write|update)\s+(a\s+)?handoff\b|\b(ending|stopping)\s+(the\s+)?session\b", re.I), "ctx", "/handoff", "Context transfer"),

    # GHA / CI
    (re.compile(r"\b(github\s+)?actions?\s+(fail|error|broken)\b|\bci\s+(fail|broken|error)\b|\bworkflow\s+fail\b", re.I), "ci", "/gha", "Investigate failure"),

    # Next steps
    (re.compile(r"\bwhat('s|\s+is)\s+next\b|\bnext\s+steps?\b|\b(stuck|unsure)\s+(what|where)\b", re.I), "nav", "/whats-next", "Analyze + suggest"),

    # Model routing
    (re.compile(r"\b(compare|get\s+consensus|multiple\s+perspectives?)\b|\bmulti(-|\s)?model\b|\b(debate|compare)\s+approaches\b", re.I), "model", "multi:compare", "Multi-model consensus"),
    (re.compile(r"\bmultilingual\s+(code|project)\b|\b(chinese|japanese|korean)\s+(code|project)\b", re.I), "model", "glm-4.7", "66.7% SWE-bench multilingual"),
    (re.compile(r"\b(500k|750k|1m|1\s*million)\s*(token|context)\b|\b(analyze|review)\s+(entire|whole)\s+(codebase|repo)\b", re.I), "model", "gemini-2.5-flash", "1M context window"),
    (re.compile(r"\b(cheap|cheapest|low\s*cost|budget|frugal|free)\b", re.I), "model", "deepseek (Ollama/OpenRouter)", "$0 FREE"),
]

# Minimal hints for each category
CATEGORY_HINTS = {
    "doc": "[DOC] Document skill available",
    "debug": "[SEARCH] Use systematic-debugging skill",
    "test": "🧪 TDD workflow available",
    "plan": "[LIST] Planning skill available",
    "review": "👀 Code review workflow",
    "mcp": "[FIX] MCP builder skill",
    "sec": "[LOCK] Security review command",
    "explore": "🗺️ Codebase exploration",
    "bug": "🐛 Bug fix workflow",
    "ctx": "[SAVE] Context management",
    "ci": "[GEAR] CI/CD debugging",
    "nav": "🧭 Next steps helper",
    "model": "[BOT] Model routing suggestion",
}


def main():
    log_hook("Hook invoked")
    try:
        data = json.load(sys.stdin)
    except:
        log_hook("Failed to parse JSON input")
        sys.exit(0)

    prompt = data.get("prompt", "")
    log_hook(f"Prompt: {prompt[:50]}...")

    # Skip short prompts
    if len(prompt) < 15:
        log_hook("Skipping - prompt too short")
        sys.exit(0)

    prompt_lower = prompt.lower()

    # Find matches (deduplicated by category)
    matches = {}
    for pattern, category, skill, hint in PATTERNS:
        if category not in matches and pattern.search(prompt_lower):
            matches[category] = (skill, hint)

    if not matches:
        log_hook("No matches found")
        sys.exit(0)

    log_hook(f"Found matches: {list(matches.keys())}")

    # Build minimal context (compact format saves tokens)
    lines = ["<skill-reminder>"]
    user_visible = []

    for category, (skill, hint) in matches.items():
        if category == "model":
            lines.append(f"-> Route to `{skill}`: {hint}")
            user_visible.append(f"{skill}")
        else:
            lines.append(f"-> `{skill}`: {hint}")
            user_visible.append(f"{skill}")

    lines.append("</skill-reminder>")

    # Build hint string
    hints = [f"{skill}: {hint}" for cat, (skill, hint) in matches.items()]
    hint_text = " | ".join(hints)

    log_hook(f"Writing hint: {hint_text}")

    # Write to signal file (workaround for broken context injection)
    hint_file = Path.home() / ".claude" / "hints" / "current.txt"
    hint_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(hint_file, "a") as f:
        f.write(f"[{timestamp}] [skill] {hint_text}\n")

    # Still output for transcript visibility
    print("[SKILL] Hints written to ~/.claude/hints/current.txt")
    sys.exit(0)


if __name__ == "__main__":
    main()
