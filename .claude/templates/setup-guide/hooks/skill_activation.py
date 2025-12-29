#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Skill Activation Hook - Auto-loads relevant skills based on context

Triggers on SessionStart to inject skill awareness into Claude's context.
Maps task patterns to appropriate skills for automatic activation.
"""

import json
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".config" / "claude-code" / "skills"

# Skill mappings: pattern -> skill info
SKILL_MAP = {
    # Development workflows
    "debug": {"skill": "superpowers/skills/systematic-debugging", "trigger": ["debug", "error", "bug", "fix", "issue", "broken"]},
    "tdd": {"skill": "superpowers/skills/test-driven-development", "trigger": ["test", "tdd", "spec", "coverage"]},
    "plan": {"skill": "superpowers/skills/writing-plans", "trigger": ["plan", "implement", "feature", "build"]},
    "execute": {"skill": "superpowers/skills/executing-plans", "trigger": ["execute", "run plan", "implement plan"]},
    "brainstorm": {"skill": "superpowers/skills/brainstorming", "trigger": ["brainstorm", "idea", "design", "architect"]},
    "review": {"skill": "superpowers/skills/requesting-code-review", "trigger": ["review", "pr", "pull request"]},
    "git": {"skill": "superpowers/skills/using-git-worktrees", "trigger": ["worktree", "branch", "parallel"]},

    # Meta skills
    "create-skill": {"skill": "taches-cc-resources/skills/create-agent-skills", "trigger": ["create skill", "new skill", "make skill"]},
    "create-plan": {"skill": "taches-cc-resources/skills/create-plans", "trigger": ["create plan", "spec", "specification"]},
    "meta-prompt": {"skill": "taches-cc-resources/skills/create-meta-prompts", "trigger": ["meta prompt", "prompt chain"]},

    # Knowledge
    "docs-to-skill": {"skill": "Skill_Seekers", "trigger": ["convert docs", "documentation", "framework docs"]},
    "knowledge": {"skill": "tapestry/tapestry", "trigger": ["knowledge graph", "connect docs", "interlink"]},
    "youtube": {"skill": "tapestry/youtube-transcript", "trigger": ["youtube", "video transcript"]},
    "article": {"skill": "tapestry/article-extractor", "trigger": ["article", "extract", "web page"]},
}

def get_available_skills():
    """List available skills"""
    skills = []
    if SKILLS_DIR.exists():
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skills.append(item.name)
    return skills

def main():
    available = get_available_skills()

    if not available:
        sys.exit(0)

    # Build skill awareness message
    skill_info = []

    # Superpowers commands
    if "superpowers" in available:
        skill_info.append("SUPERPOWERS: /superpowers:brainstorm, /superpowers:write-plan, /superpowers:execute-plan")
        skill_info.append("  Skills: systematic-debugging, test-driven-development, root-cause-tracing, defense-in-depth")

    # Taches resources
    if "taches-cc-resources" in available:
        skill_info.append("TACHES: /create-plan, /create-meta-prompt, /create-agent-skill, /debug, /whats-next")

    # Skill Seekers
    if "Skill_Seekers" in available:
        skill_info.append("SKILL-SEEKERS: Convert any docs/codebase to Claude skills")

    # Tapestry
    if "tapestry" in available:
        skill_info.append("TAPESTRY: Knowledge graphs, article-extractor, youtube-transcript")

    if skill_info:
        context = "<skill-activation-hook>\n"
        context += "Available skills in ~/.config/claude-code/skills/:\n"
        context += "\n".join(f"  {s}" for s in skill_info)
        context += "\n\nALWAYS use relevant skills when task matches. Read skill SKILL.md before using."
        context += "\n</skill-activation-hook>"

        # Show user what skills are available
        output = {
            "systemMessage": f"🛠️ Skills loaded: {', '.join(available[:4])}",
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
