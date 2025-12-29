#!/usr/bin/env python3
"""
UserPromptSubmit Hook - AI Orchestration Reminder (ENHANCED)

Detects when to use:
- Parallel agents (multiple tasks)
- Specialized agents (lambda, frontend, etc.)
- Alternative AI models (GLM, Gemini, DeepSeek)
- Code-scout for file discovery

Injects guidance on HOW to prompt effectively.
"""

import json
import sys
import re

# Pre-compiled patterns for speed
PATTERNS = {
    # Parallel work
    "parallel": re.compile(r"\b(in parallel|simultaneously|at the same time|parallel agents?|multiple (features|tasks|things)|batch of|\b(3|4|5|6|7|8|9|10)\s*(features|tasks|things|lambdas|components))\b", re.I),

    # File discovery
    "scout": re.compile(r"\b(where is|find (the|all|any)?\s*(file|code|function|class)|locate|which file|where.*(implement|defin|handl)|explore.*(codebase|repo))\b", re.I),

    # Model routing triggers
    "multilingual": re.compile(r"\b(multilingual|chinese|japanese|korean|russian|arabic|hindi)\s*(code|project|comments?)\b", re.I),
    "large_context": re.compile(r"\b(500k|750k|1m|1\s*million)\s*(token|context)|analyze (entire|whole|full) (codebase|repo)|very large (file|codebase)\b", re.I),
    "cheap": re.compile(r"\b(cheap|cheapest|free|budget|frugal|low.?cost)\b", re.I),
    "reasoning": re.compile(r"\b(step.by.step|chain.of.thought|prove|mathematical proof|complex reasoning|think harder)\b", re.I),
    "compare": re.compile(r"\b(compare approaches|get consensus|multiple perspectives|what's the best|architecture decision)\b", re.I),

    # Additional model triggers
    "openai": re.compile(r"\b(gpt|openai|chatgpt|o1|o3)\b", re.I),
    "codegen": re.compile(r"\b(code generation|codestral|devstral|generate code)\b", re.I),
    "vision": re.compile(r"\b(image|vision|screenshot|picture|photo|pixtral)\b", re.I),
    "fast": re.compile(r"\b(fast|quick|speed|haiku|instant)\b", re.I),
    "llama": re.compile(r"\b(llama|meta|open.?source model)\b", re.I),
    "kimi": re.compile(r"\b(kimi|moonshot)\b", re.I),
    "qwen": re.compile(r"\b(qwen|alibaba)\b", re.I),
    "mistral": re.compile(r"\b(mistral|le chat)\b", re.I),

    # Specialized agents
    "lambda": re.compile(r"\b(lambda|serverless|api gateway|aws function)\b", re.I),
    "frontend": re.compile(r"\b(react|vue|next\.?js|frontend|component)\b", re.I),
    "ui": re.compile(r"\b(ui|ux|design system|styling|theme|accessibility)\b", re.I),
    "test": re.compile(r"\b(write tests|unit test|test coverage|tdd)\b", re.I),
    "refactor": re.compile(r"\b(refactor|clean up|restructure)\b", re.I),
}

# Minimal guidance templates
GUIDANCE = {
    "parallel": """<parallel-agent-guide>
**Parallel agents need SPECIFIC prompts:**

TASK: [one-line description]
DIRECTORY: [exact path - STAY HERE]
CREATE: [files to create]
DO NOT TOUCH: [files to avoid]
VERIFY: [test command]

Use `Task` tool with `subagent_type="autonomous-coder"` or workmux.
</parallel-agent-guide>""",

    "scout": "→ `code-scout` agent for fast file discovery",

    # Model routing - 8 providers, 44 models
    "multilingual": "→ `glm-4.7`: Best multilingual - `multi:chat glm`",
    "large_context": "→ `gemini-2.5-flash`: 1M context - `multi:chat gemini`",
    "cheap": "→ FREE: `deepseek` (Ollama), `llama-405b` (OpenRouter), `r1` - `multi:chat deepseek`",
    "reasoning": "→ `deepseek-r1`: FREE reasoning - `multi:chat r1` | or `o1`: $15/M",
    "compare": "→ `multi:compare` for 3-model consensus",
    "openai": "→ OpenAI: `gpt-4o` ($2.5/M), `o1` (reasoning), `o3-mini` - `multi:chat gpt`",
    "codegen": "→ `codestral`: Code specialist - `multi:chat codestral`",
    "vision": "→ Vision: `gemini` or `pixtral-large` - `multi:chat pixtral`",
    "fast": "→ Fast: `haiku`, `glm-air`, `gpt-mini` - `multi:chat haiku`",
    "llama": "→ `llama-405b`: FREE 405B open-source - `multi:chat llama`",
    "kimi": "→ `kimi-k2`: FREE 1T param model - `multi:chat kimi`",
    "qwen": "→ `qwen3-coder`: FREE coding model - `multi:chat qwen`",
    "mistral": "→ Mistral: `codestral`, `pixtral`, `mistral-large` - `multi:chat mistral`",

    # Agents
    "lambda": "→ `lambda-builder` agent for serverless",
    "frontend": "→ `frontend-builder` agent for React/Vue/Next",
    "ui": "→ `ui-ux-designer` agent for design systems",
    "test": "→ `test-writer` agent for test coverage",
    "refactor": "→ `refactorer` agent for code quality",
}

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    prompt = data.get("prompt", "")
    if len(prompt) < 10:
        sys.exit(0)

    matches = []

    # Check all patterns
    for key, pattern in PATTERNS.items():
        if pattern.search(prompt):
            matches.append(key)

    if not matches:
        sys.exit(0)

    # Build output
    parts = []

    # Parallel gets full guide
    if "parallel" in matches:
        parts.append(GUIDANCE["parallel"])
        matches.remove("parallel")

    # Others get one-line hints
    for key in matches:
        if key in GUIDANCE:
            parts.append(GUIDANCE[key])

    if parts:
        # Combine into minimal context
        context = "\n".join(parts)

        # Show user what hook detected
        user_hints = []
        for key in list(matches) + (["parallel"] if "parallel" in [p for p in parts if "parallel" in p.lower()] else []):
            if key in GUIDANCE and key != "parallel":
                user_hints.append(GUIDANCE[key].replace("→ ", ""))

        # Write to signal file (workaround for broken context injection)
        from pathlib import Path
        from datetime import datetime
        hint_file = Path.home() / ".claude" / "hints" / "current.txt"
        hint_file.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%H:%M:%S")

        # Build hint from matches
        hint_parts = []
        if "parallel" in matches:
            hint_parts.append("PARALLEL: Use Task tool with specific prompts per agent")
        for key in matches:
            if key != "parallel" and key in GUIDANCE:
                hint_parts.append(GUIDANCE[key].replace("→ ", ""))

        hint_text = " | ".join(hint_parts[:3])
        with open(hint_file, "a") as f:
            f.write(f"[{timestamp}] [orchestration] {hint_text}\n")

        print(f"🔔 Orchestration hint written to ~/.claude/hints/current.txt")
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
