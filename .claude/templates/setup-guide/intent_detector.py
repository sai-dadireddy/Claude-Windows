#!/usr/bin/env python3
"""
Intent Detector Hook for Claude Code
Detects user intent and suggests appropriate MCP servers, models, or actions.
Hook Type: UserPromptSubmit
"""

import json
import sys
import re
import os

# =============================================================================
# MCP ROUTING PATTERNS
# =============================================================================
MCP_ROUTING = {
    "context7": {
        "keywords": ["docs", "documentation", "api", "library", "react", "vue",
                     "nextjs", "fastapi", "django", "node", "python", "typescript",
                     "how to use", "what is the syntax", "current version"],
        "description": "Library documentation lookup"
    },
    "github": {
        "keywords": ["pr", "pull request", "issue", "commit", "branch", "repo",
                     "repository", "merge", "github", "git history", "blame"],
        "description": "GitHub operations"
    },
    "memory": {
        "keywords": ["remember", "recall", "entity", "relationship", "knowledge graph",
                     "store entity", "what do you know about"],
        "description": "Entity memory and knowledge graph"
    },
    "sequential-thinking": {
        "keywords": ["step by step", "reason through", "analyze carefully",
                     "break down", "think through", "complex problem"],
        "description": "Multi-step reasoning"
    },
    "playwright": {
        "keywords": ["browser", "screenshot", "scrape", "web page", "click",
                     "navigate to", "fill form", "automate browser"],
        "description": "Browser automation"
    }
}

# =============================================================================
# MODEL ROUTING PATTERNS
# =============================================================================
MODEL_ROUTING = {
    "glm": {
        "keywords": ["chinese", "mandarin", "multilingual", "translate to chinese",
                     "asian language", "glm"],
        "model": "glm-4.7",
        "description": "Best for multilingual and Chinese content"
    },
    "gemini": {
        "keywords": ["large file", "long document", "huge context", "analyze entire",
                     "full codebase", ">100k", "million tokens"],
        "model": "gemini-2.5-flash",
        "description": "Best for large context (1M tokens)"
    },
    "deepseek": {
        "keywords": ["reasoning", "math", "logic", "proof", "algorithm",
                     "step by step calculation", "complex math"],
        "model": "deepseek-r1",
        "description": "Best for reasoning and math"
    },
    "openai": {
        "keywords": ["gpt", "openai", "o1", "chatgpt"],
        "model": "gpt-4o",
        "description": "OpenAI models"
    }
}

# =============================================================================
# MEMORY SAVE TRIGGERS
# =============================================================================
MEMORY_TRIGGERS = {
    "decision": ["decided", "decision", "chose", "choosing", "selected", "going with",
                 "let's use", "we'll use", "i prefer", "i want to use"],
    "preference": ["i prefer", "i like", "i don't like", "i hate", "always use",
                   "never use", "my preference", "i want"],
    "learning": ["learned", "realized", "discovered", "found out", "turns out",
                 "the trick is", "the key is", "important to note"]
}

# =============================================================================
# BEADS/COMPLEX TASK TRIGGERS
# =============================================================================
BEADS_TRIGGERS = [
    "complex", "multi-step", "dependencies", "multiple tasks", "epic",
    "feature with", "implement full", "build complete", "refactor entire",
    "migrate", "spanning multiple", "across files"
]

# =============================================================================
# SKILL TRIGGERS
# =============================================================================
SKILL_TRIGGERS = {
    "debugging": ["bug", "error", "crash", "broken", "not working", "fails",
                  "exception", "traceback", "debug"],
    "testing": ["test", "tdd", "coverage", "unit test", "integration test"],
    "planning": ["plan", "design", "architect", "strategy", "approach"],
    "code-review": ["review", "pr review", "check my code", "code quality"]
}


def detect_intent(prompt: str) -> dict:
    """Analyze prompt and return detected intents."""
    prompt_lower = prompt.lower()
    hints = []

    # Check MCP routing
    for mcp_name, config in MCP_ROUTING.items():
        for keyword in config["keywords"]:
            if keyword in prompt_lower:
                hints.append(f"[mcp] Consider using {mcp_name}: {config['description']}")
                break

    # Check model routing
    for model_key, config in MODEL_ROUTING.items():
        for keyword in config["keywords"]:
            if keyword in prompt_lower:
                hints.append(f"[model] Consider routing to {config['model']}: {config['description']}")
                break

    # Check memory triggers
    for mem_type, keywords in MEMORY_TRIGGERS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                hints.append(f"[memory] Detected {mem_type} - consider saving to memory")
                break

    # Check beads triggers
    for trigger in BEADS_TRIGGERS:
        if trigger in prompt_lower:
            hints.append("[beads] Complex task detected - consider using Beads for tracking")
            break

    # Check skill triggers
    for skill, keywords in SKILL_TRIGGERS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                hints.append(f"[skill] Consider using {skill} skill")
                break

    return {
        "hints": hints,
        "has_suggestions": len(hints) > 0
    }


def write_hints(hints: list, hint_file: str):
    """Write hints to the hint file for Claude to read."""
    os.makedirs(os.path.dirname(hint_file), exist_ok=True)

    if hints:
        content = "INTENT DETECTION HINTS:\n" + "\n".join(hints)
        with open(hint_file, 'w') as f:
            f.write(content)


def main():
    # Read hook input
    input_data = json.loads(sys.stdin.read())
    prompt = input_data.get("message", "")

    # Detect intent
    result = detect_intent(prompt)

    # Write hints to file
    hint_file = os.path.expanduser("~/.claude/hints/current.txt")
    write_hints(result["hints"], hint_file)

    # Return hook response
    output = {
        "continue": True
    }

    if result["has_suggestions"]:
        output["additionalContext"] = "\n".join(result["hints"])

    print(json.dumps(output))


if __name__ == "__main__":
    main()
