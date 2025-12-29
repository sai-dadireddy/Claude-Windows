#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
SessionStart Hook - Progressive Memory Disclosure

Like Claude-Mem, this hook:
- Shows WHAT memories exist (index with token costs)
- Injects RELEVANT memories based on project
- Provides memory search instructions
- Shows git context and skills

Progressive Disclosure:
1. Index: Shows available memories with estimated tokens
2. Details: Claude fetches full content on-demand via search
3. Perfect Recall: Access original files if needed
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

LOG_DIR = Path.home() / ".claude" / "logs"
SKILLS_DIR = Path.home() / ".config" / "claude-code" / "skills"
PLUGINS_DIR = Path.home() / ".claude" / "plugins"
MEMORY_SCRIPT = Path.home() / ".claude" / "scripts" / "memory_manager.py"
SEMANTIC_SCRIPT = Path.home() / ".claude" / "scripts" / "semantic_memory.py"
MEMORY_DIR = Path.home() / ".claude" / "memory"
BD_PATH = Path.home() / ".local" / "bin" / "bd"

def cmd(c, cwd=None):
    """Run command, return output or empty string"""
    try:
        r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=5, cwd=cwd)
        return r.stdout.strip() if r.returncode == 0 else ""
    except:
        return ""

def estimate_tokens(text: str) -> int:
    """Rough token estimate (4 chars per token)"""
    return len(text) // 4

def get_memory_index(project: str) -> list:
    """Get index of available memories with token costs."""
    index = []

    # Check long-term memory files
    long_term = MEMORY_DIR / "long-term"

    # Global memories
    global_dir = long_term / "global"
    if global_dir.exists():
        for f in global_dir.glob("*.md"):
            content = f.read_text()
            entries = content.count("## [")  # Count entries
            tokens = estimate_tokens(content)
            index.append({
                "scope": "global",
                "type": f.stem,
                "entries": entries,
                "tokens": tokens,
                "priority": "high" if f.stem in ["decisions", "preferences", "bugs_and_fixes"] else "medium"
            })

    # Project memories
    if project:
        project_dir = long_term / project.lower().replace(" ", "_")[:50]
        if project_dir.exists():
            for f in project_dir.glob("*.md"):
                content = f.read_text()
                entries = content.count("## [")
                tokens = estimate_tokens(content)
                index.append({
                    "scope": project,
                    "type": f.stem,
                    "entries": entries,
                    "tokens": tokens,
                    "priority": "high"
                })

    return index

def get_recent_observations(project: str, limit: int = 5) -> list:
    """Get recent auto-captured observations."""
    obs_file = LOG_DIR / "observations.jsonl"
    if not obs_file.exists():
        return []

    observations = []
    try:
        lines = obs_file.read_text().strip().split("\n")
        for line in reversed(lines[-50:]):  # Check last 50
            try:
                obs = json.loads(line)
                if obs.get("project") == project or obs.get("project") == "global":
                    observations.append(obs)
                    if len(observations) >= limit:
                        break
            except:
                continue
    except:
        pass

    return observations

def get_semantic_stats(project: str) -> dict:
    """Get semantic memory statistics."""
    if not SEMANTIC_SCRIPT.exists():
        return {}

    try:
        result = subprocess.run(
            [sys.executable, str(SEMANTIC_SCRIPT), "stats", project],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return {}

def load_high_priority_memories(project: str) -> str:
    """Load high-priority memories (decisions, preferences, recent bugs)."""
    memories = []

    # Load global preferences and decisions
    global_dir = MEMORY_DIR / "long-term" / "global"

    for mem_type in ["preferences", "decisions"]:
        mem_file = global_dir / f"{mem_type}.md"
        if mem_file.exists():
            content = mem_file.read_text()
            # Get last 3 entries only (most recent)
            entries = content.split("## [")[-4:-1]  # Skip header, get last 3
            if entries:
                memories.append(f"### {mem_type.title()}\n" + "\n".join("## [" + e for e in entries))

    # Load project-specific memories
    if project:
        project_dir = MEMORY_DIR / "long-term" / project.lower().replace(" ", "_")[:50]
        if project_dir.exists():
            for mem_file in project_dir.glob("*.md"):
                content = mem_file.read_text()
                entries = content.split("## [")[-3:-1]  # Last 2 entries
                if entries:
                    memories.append(f"### {project}: {mem_file.stem}\n" + "\n".join("## [" + e for e in entries))

    return "\n\n".join(memories) if memories else ""

def get_skills_info() -> dict:
    """Get comprehensive skills information."""
    skills_info = {
        "superpowers": {"count": 0, "active": []},
        "taches": {"count": 0, "active": []},
        "documents": {"count": 0, "active": []},
        "other": {"count": 0, "active": []},
        "plugins": []
    }

    # Check skills directories
    if SKILLS_DIR.exists():
        # Superpowers
        superpowers_dir = SKILLS_DIR / "superpowers" / "skills"
        if superpowers_dir.exists():
            skill_dirs = [d for d in superpowers_dir.iterdir() if d.is_dir()]
            skills_info["superpowers"]["count"] = len(skill_dirs)
            # Get key skills
            key_skills = ["systematic-debugging", "test-driven-development", "requesting-code-review"]
            skills_info["superpowers"]["active"] = [s.name for s in skill_dirs if s.name in key_skills]

        # Taches
        taches_dir = SKILLS_DIR / "taches-cc-resources" / "skills"
        if taches_dir.exists():
            skill_dirs = [d for d in taches_dir.iterdir() if d.is_dir()]
            skills_info["taches"]["count"] = len(skill_dirs)
            key_skills = ["create-plan", "debug", "whats-next"]
            skills_info["taches"]["active"] = [s.name for s in skill_dirs if s.name in key_skills]

        # Skill Seekers
        seekers_dir = SKILLS_DIR / "Skill_Seekers"
        if seekers_dir.exists():
            skills_info["other"]["count"] += 1
            skills_info["other"]["active"].append("skill-seekers")

        # Tapestry
        tapestry_dir = SKILLS_DIR / "tapestry"
        if tapestry_dir.exists():
            skills_info["other"]["count"] += 1
            skills_info["other"]["active"].append("tapestry")

    # Check for document skills via plugins
    settings_file = Path.home() / ".claude" / "settings.json"
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text())
            enabled_plugins = settings.get("enabledPlugins", {})
            for plugin, enabled in enabled_plugins.items():
                if enabled:
                    if "document" in plugin.lower():
                        skills_info["documents"]["count"] += 4  # docx, pdf, pptx, xlsx
                        skills_info["documents"]["active"] = ["docx", "pdf", "pptx", "xlsx"]
                    skills_info["plugins"].append(plugin.split("@")[0])
        except:
            pass

    return skills_info

def get_beads_status(cwd: str) -> dict:
    """Get beads status for the current project."""
    beads_dir = Path(cwd) / ".beads"
    if not beads_dir.exists():
        return {"initialized": False}

    if not BD_PATH.exists():
        return {"initialized": True, "cli_missing": True}

    try:
        env = os.environ.copy()
        env["PATH"] = f"{Path.home()}/.local/bin:{env.get('PATH', '')}"

        # Get ready issues count
        result = subprocess.run(
            ["bd", "ready", "--json"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        ready_count = 0
        if result.returncode == 0 and result.stdout.strip():
            try:
                ready_issues = json.loads(result.stdout)
                ready_count = len(ready_issues) if isinstance(ready_issues, list) else 0
            except:
                pass

        # Get total issues
        result = subprocess.run(
            ["bd", "list", "--json"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        total_count = 0
        open_count = 0
        if result.returncode == 0 and result.stdout.strip():
            try:
                all_issues = json.loads(result.stdout)
                if isinstance(all_issues, list):
                    total_count = len(all_issues)
                    open_count = len([i for i in all_issues if i.get("status") in ["open", "in_progress"]])
            except:
                pass

        return {
            "initialized": True,
            "total": total_count,
            "open": open_count,
            "ready": ready_count
        }
    except:
        return {"initialized": True}

def build_memory_instructions() -> str:
    """Build COMPACT memory instructions (token-optimized)."""
    return """<memory-guide>
## 3 Memory Systems - When to Use Each

| System | Trigger | How |
|--------|---------|-----|
| **Auto-Capture** | File edits, installs, commits | Automatic (hook) |
| **Semantic** | Decisions, preferences, learnings | `memory_manager.py save-memory PROJECT TYPE "content"` |
| **MCP Memory** | Entity relationships | `mcp-router memory` category |

### MUST Save Manually:
- User decides tech/approach -> `save-memory PROJECT decision "..."`
- User states preference -> `save-memory global preference "..."`
- Session ending -> `save-session SESSION PROJECT "..."`

### Search: `memory_manager.py load-memories PROJECT "query"`
</memory-guide>"""

def main():
    # Clear old hints at session start
    hint_file = Path.home() / ".claude" / "hints" / "current.txt"
    try:
        if hint_file.exists():
            hint_file.unlink()
    except:
        pass

    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    source = data.get("source", "startup")  # startup, resume, clear, compact
    project = os.path.basename(cwd)

    # Log session start
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_DIR / "sessions.jsonl", "a") as f:
            f.write(json.dumps({
                "cwd": cwd,
                "source": source,
                "project": project,
                "timestamp": datetime.now().isoformat()
            }) + "\n")
    except:
        pass

    # Create visible session log file
    session_log_file = LOG_DIR / "session_start_output.log"

    # === BUILD USER-VISIBLE MESSAGE ===
    msg_parts = []

    # Git info
    branch = cmd("git branch --show-current 2>/dev/null", cwd)
    if branch:
        ctx = [f"branch:{branch}"]
        changes = cmd("git status --porcelain 2>/dev/null | wc -l", cwd)
        if changes and int(changes) > 0:
            ctx.append(f"changes:{changes}")
        msg_parts.append(f"[DIR] {' | '.join(ctx)}")

    # Memory index (progressive disclosure)
    memory_index = get_memory_index(project)
    if memory_index:
        total_memories = sum(m["entries"] for m in memory_index)
        total_tokens = sum(m["tokens"] for m in memory_index)
        high_priority = [m for m in memory_index if m["priority"] == "high"]

        mem_summary = f"[THINK] {total_memories} memories (~{total_tokens} tokens)"
        if high_priority:
            types = [m["type"] for m in high_priority[:3]]
            mem_summary += f" | Active: {', '.join(types)}"
        msg_parts.append(mem_summary)

    # Recent observations
    recent_obs = get_recent_observations(project, limit=3)
    if recent_obs:
        msg_parts.append(f"[NOTE] {len(recent_obs)} recent observations")

    # Skills (detailed)
    skills_info = get_skills_info()
    total_skills = sum([
        skills_info["superpowers"]["count"],
        skills_info["taches"]["count"],
        skills_info["documents"]["count"],
        skills_info["other"]["count"]
    ])
    if total_skills > 0:
        skill_parts = []
        if skills_info["superpowers"]["count"]:
            skill_parts.append(f"dev:{skills_info['superpowers']['count']}")
        if skills_info["taches"]["count"]:
            skill_parts.append(f"meta:{skills_info['taches']['count']}")
        if skills_info["documents"]["count"]:
            skill_parts.append(f"docs:{skills_info['documents']['count']}")
        msg_parts.append(f"[TOOL] Skills: {', '.join(skill_parts)}")

    # Beads status
    beads_status = get_beads_status(cwd)
    if beads_status.get("initialized"):
        ready = beads_status.get("ready", 0)
        total = beads_status.get("total", 0)
        open_count = beads_status.get("open", 0)
        if total > 0:
            msg_parts.append(f"[LIST] Beads: {open_count} open, {ready} ready")
        else:
            msg_parts.append("[LIST] Beads: initialized")

    # Session continuation available
    if source == "startup":
        last_session = cmd(f"{sys.executable} {MEMORY_SCRIPT} get-last-session '{project}'") if MEMORY_SCRIPT.exists() else ""
        if last_session:
            msg_parts.append("[SAVE] /session-continue available")

    # Build user message for terminal
    user_message = " | ".join(msg_parts) if msg_parts else ""

    # Log to visible file
    try:
        with open(session_log_file, "w") as f:
            f.write(f"=== SESSION START: {datetime.now().isoformat()} ===\n")
            f.write(f"Project: {project}\n")
            f.write(f"CWD: {cwd}\n")
            f.write(f"Source: {source}\n")
            f.write(f"\n--- USER MESSAGE ---\n{user_message}\n")
    except:
        pass

    # === BUILD CLAUDE CONTEXT (additionalContext) ===
    context_parts = []

    # Memory instructions (always include)
    context_parts.append(build_memory_instructions())

    # High-priority memories
    high_priority_memories = load_high_priority_memories(project)
    if high_priority_memories:
        context_parts.append(f"<loaded-memories>\n{high_priority_memories[:3000]}\n</loaded-memories>")

    # Recent observations summary
    if recent_obs:
        obs_summary = "\n".join([
            f"- [{o['type']}] {o['observation'][:80]}"
            for o in recent_obs
        ])
        context_parts.append(f"<recent-observations>\n{obs_summary}\n</recent-observations>")

    # Memory index for Claude's awareness
    if memory_index:
        index_text = "\n".join([
            f"- {m['scope']}/{m['type']}: {m['entries']} entries (~{m['tokens']} tokens) [{m['priority']}]"
            for m in memory_index
        ])
        context_parts.append(f"<memory-index>\n{index_text}\n</memory-index>")

    # Beads instructions (COMPACT)
    beads_context = """<beads-guide>
## Task Tracking: TodoWrite vs Beads

| Use | TodoWrite | Beads (bd) |
|-----|-----------|------------|
| Simple checklist | ✓ | - |
| Dependencies | - | ✓ |
| Multi-session | - | ✓ |
| Complex features | - | ✓ |

Beads: `PATH=$HOME/.local/bin:$PATH bd ready`
</beads-guide>"""

    if beads_status.get("initialized"):
        beads_context += f"\n<beads-status>Open: {beads_status.get('open', 0)} | Ready: {beads_status.get('ready', 0)}</beads-status>"

    context_parts.append(beads_context)

    # Skills context (COMPACT - just key mappings)
    skills_context = """<skills-quick>
| Task | Use |
|------|-----|
| Bug/Error | systematic-debugging |
| New feature | /plan-feature |
| Write tests | /tdd |
| Documents | docx/pdf/pptx/xlsx skills |
| Explore code | /explore |
| Model choice | /route or multi:chat |
</skills-quick>"""

    context_parts.append(skills_context)

    # Build additional context
    additional_context = "\n\n".join(context_parts) if context_parts else ""

    # === OUTPUT SINGLE JSON WITH BOTH CHANNELS ===
    output = {}

    if user_message:
        output["systemMessage"] = user_message

    if additional_context:
        output["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": additional_context
        }

    if output:
        print(json.dumps(output))

    # Append context to visible log file
    try:
        with open(session_log_file, "a") as f:
            f.write(f"\n--- CONTEXT INJECTED TO CLAUDE ---\n")
            f.write(additional_context)
            f.write(f"\n\n=== END SESSION START ===\n")
    except:
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
