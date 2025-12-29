#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Auto-Capture Memory Hook (PostToolUse) - Automatically extract observations

ENHANCED with Session Tracking (based on 2025 best practices):
- Monitors tool usage (file edits, bash commands, etc.)
- Extracts meaningful observations/learnings
- Stores them to semantic memory automatically
- SESSION TRACKING: Counts significant actions, reminds to save
- BIG SESSION DETECTION: Triggers reminder after threshold

Features:
- Privacy tags: Content in <private>...</private> is excluded
- Concept tagging: discovery, problem-solution, pattern, decision
- Bug fix detection: Tracks error → fix sequences
- Session activity tracking: Reminds on significant work

Captures:
- Architectural decisions (new files, patterns)
- Bug fixes (error → fix sequences)
- Session summaries (automatic after threshold)
"""

import json
import sys
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path

VERBOSE = False  # Reduce noise
LOG_DIR = Path.home() / ".claude" / "logs"
MEMORY_SCRIPT = Path.home() / ".claude" / "scripts" / "memory_manager.py"

# Track recent errors to detect bug fixes
ERROR_CACHE_FILE = LOG_DIR / "recent_errors.json"

# Session tracking
SESSION_FILE = LOG_DIR / "session_activity.json"
SIGNIFICANT_THRESHOLD = 15  # Remind after this many significant actions
REMINDER_COOLDOWN = 10  # Don't remind again for this many actions

def log(msg: str):
    if VERBOSE:
        print(f"[AutoCapture] {msg}", file=sys.stderr)

def strip_private_content(text: str) -> str:
    """Remove content wrapped in <private>...</private> tags."""
    if not text:
        return text
    # Remove all <private>...</private> blocks (including nested)
    pattern = r'<private>.*?</private>'
    return re.sub(pattern, '[REDACTED]', text, flags=re.DOTALL)

def contains_private_tag(text: str) -> bool:
    """Check if text contains private tags."""
    return '<private>' in text if text else False

def detect_concept_tag(observation: str, context: str = "") -> str:
    """Detect concept category for the observation (like claude-mem)."""
    obs_lower = observation.lower()
    ctx_lower = context.lower() if context else ""

    # Discovery: Learning something new about the codebase
    discovery_indicators = [
        "found", "discovered", "learned", "realized", "noticed",
        "turns out", "interesting", "pattern", "convention"
    ]
    if any(ind in obs_lower for ind in discovery_indicators):
        return "discovery"

    # Problem-Solution: Error encountered and fixed
    problem_indicators = [
        "fixed", "resolved", "solved", "error", "bug", "issue",
        "workaround", "solution"
    ]
    if any(ind in obs_lower for ind in problem_indicators):
        return "problem-solution"

    # Pattern: Recurring code pattern or architectural decision
    pattern_indicators = [
        "pattern", "always", "convention", "standard", "approach",
        "architecture", "structure", "design"
    ]
    if any(ind in obs_lower for ind in pattern_indicators):
        return "pattern"

    # Decision: Explicit choice made
    decision_indicators = [
        "chose", "decided", "selected", "installed", "using",
        "switched", "migrated", "prefer"
    ]
    if any(ind in obs_lower for ind in decision_indicators):
        return "decision"

    # Default to context
    return "context"

def save_memory(project: str, memory_type: str, content: str):
    """Save to semantic memory system."""
    if not MEMORY_SCRIPT.exists():
        return False

    try:
        result = subprocess.run(
            ["python3", str(MEMORY_SCRIPT), "save-memory", project, memory_type, content],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except:
        return False

def load_recent_errors() -> list:
    """Load recent errors from cache."""
    try:
        if ERROR_CACHE_FILE.exists():
            return json.loads(ERROR_CACHE_FILE.read_text())
    except:
        pass
    return []

def save_recent_error(error: str, file_path: str = ""):
    """Cache recent error for bug fix detection."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    errors = load_recent_errors()
    errors.append({
        "error": error[:500],
        "file": file_path,
        "time": datetime.now().isoformat()
    })
    # Keep only last 10 errors
    errors = errors[-10:]
    try:
        ERROR_CACHE_FILE.write_text(json.dumps(errors))
    except:
        pass

def clear_recent_errors():
    """Clear error cache after successful fix."""
    try:
        if ERROR_CACHE_FILE.exists():
            ERROR_CACHE_FILE.unlink()
    except:
        pass

# === SESSION TRACKING (NEW) ===

def load_session_activity() -> dict:
    """Load current session activity tracking."""
    try:
        if SESSION_FILE.exists():
            data = json.loads(SESSION_FILE.read_text())
            # Check if session is still valid (within 2 hours)
            last_ts = datetime.fromisoformat(data.get("last_activity", "2000-01-01"))
            if (datetime.now() - last_ts).total_seconds() > 7200:  # 2 hours
                return new_session_activity()
            return data
    except:
        pass
    return new_session_activity()

def new_session_activity() -> dict:
    """Create new session activity tracker."""
    return {
        "session_start": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat(),
        "significant_count": 0,
        "last_reminder_at": 0,
        "files_touched": [],
        "tools_used": {},
        "has_unsaved_work": False
    }

def save_session_activity(activity: dict):
    """Save session activity to file."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        activity["last_activity"] = datetime.now().isoformat()
        SESSION_FILE.write_text(json.dumps(activity, indent=2))
    except:
        pass

def is_significant_action(tool: str, tool_input: dict, tool_output: dict) -> bool:
    """Determine if this tool call represents significant work."""
    # Significant tools
    significant_tools = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
    if tool in significant_tools:
        return True

    # Bash with code execution (not just viewing)
    if tool == "Bash":
        cmd = tool_input.get("command", "")
        # Skip simple commands
        skip_prefixes = ("ls", "cat", "head", "tail", "pwd", "echo", "which", "git status", "git log", "git diff")
        if any(cmd.strip().startswith(p) for p in skip_prefixes):
            return False
        # Count as significant if it's installing, building, testing, etc.
        significant_prefixes = ("npm", "pip", "cargo", "pytest", "jest", "make", "docker", "git commit", "git push")
        if any(cmd.strip().startswith(p) for p in significant_prefixes):
            return True

    # Task tool is significant
    if tool == "Task":
        return True

    return False

def should_remind_to_save(activity: dict) -> bool:
    """Check if we should remind to save memories."""
    count = activity.get("significant_count", 0)
    last_reminder = activity.get("last_reminder_at", 0)

    # Remind at threshold and every REMINDER_COOLDOWN after
    if count >= SIGNIFICANT_THRESHOLD:
        if count - last_reminder >= REMINDER_COOLDOWN:
            return True
        if last_reminder == 0:  # First time reaching threshold
            return True
    return False

def get_session_summary(activity: dict) -> str:
    """Generate a brief session summary for reminder."""
    files = activity.get("files_touched", [])[:5]
    tools = activity.get("tools_used", {})
    count = activity.get("significant_count", 0)

    parts = [f"{count} significant actions"]
    if files:
        parts.append(f"files: {', '.join(files[:3])}")

    top_tools = sorted(tools.items(), key=lambda x: x[1], reverse=True)[:3]
    if top_tools:
        parts.append(f"tools: {', '.join(t[0] for t in top_tools)}")

    return " | ".join(parts)

def extract_observation(tool: str, tool_input: dict, tool_output: dict, cwd: str) -> dict:
    """Extract meaningful observation from tool usage."""

    observation = None
    memory_type = "context"

    # === FILE WRITES: Detect new files, patterns ===
    if tool == "Write":
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")
        filename = os.path.basename(file_path)

        # New file created
        if not os.path.exists(file_path) or tool_output.get("created"):
            # Detect file type and purpose
            if "test" in filename.lower() or "_test" in filename or "test_" in filename:
                observation = f"Created test file: {filename}"
                memory_type = "context"
            elif filename in ["Dockerfile", "docker-compose.yml", ".dockerignore"]:
                observation = f"Added Docker configuration: {filename}"
                memory_type = "architecture"
            elif filename.endswith((".yml", ".yaml")) and "ci" in file_path.lower():
                observation = f"Added CI/CD configuration: {filename}"
                memory_type = "architecture"
            elif filename == "package.json":
                observation = f"Initialized Node.js project"
                memory_type = "architecture"
            elif filename == "pyproject.toml" or filename == "setup.py":
                observation = f"Initialized Python project"
                memory_type = "architecture"
            else:
                # Extract purpose from content if possible
                first_lines = content[:200].replace("\n", " ")
                observation = f"Created {filename}: {first_lines[:100]}..."
                memory_type = "context"

    # === FILE EDITS: Detect bug fixes, refactors ===
    elif tool == "Edit":
        file_path = tool_input.get("file_path", "")
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        filename = os.path.basename(file_path)

        # Check if this fixes a recent error
        recent_errors = load_recent_errors()
        for error in recent_errors:
            if error.get("file") == file_path or filename in error.get("error", ""):
                observation = f"Fixed bug in {filename}: {error['error'][:100]}"
                memory_type = "bug"
                clear_recent_errors()
                break

        if not observation:
            # Detect type of change
            if "import" in old_string or "import" in new_string:
                observation = f"Modified imports in {filename}"
                memory_type = "context"
            elif "def " in new_string or "function " in new_string or "class " in new_string:
                # Extract function/class name
                match = re.search(r'(def|function|class)\s+(\w+)', new_string)
                if match:
                    name = match.group(2)
                    observation = f"Added/modified {match.group(1)} '{name}' in {filename}"
                    memory_type = "context"
            elif len(new_string) > len(old_string) * 2:
                observation = f"Significant expansion in {filename}"
                memory_type = "context"

    # === BASH COMMANDS: Detect decisions, errors ===
    elif tool == "Bash":
        command = tool_input.get("command", "")
        output = ""
        if isinstance(tool_output, dict):
            output = tool_output.get("stdout", "") + tool_output.get("stderr", "")
        elif isinstance(tool_output, str):
            output = tool_output

        # Detect errors
        error_indicators = ["error", "Error", "ERROR", "failed", "Failed", "FAILED",
                          "exception", "Exception", "traceback", "Traceback"]
        has_error = any(ind in output for ind in error_indicators)

        if has_error:
            # Save error for later bug fix detection
            error_summary = output[:300] if output else command
            save_recent_error(error_summary)
            observation = f"Error encountered: {error_summary[:100]}"
            memory_type = "bug"

        # Detect package installations (decisions)
        if re.match(r'^(npm|yarn|pnpm)\s+(install|add)\s+', command):
            packages = re.findall(r'(install|add)\s+(.+)', command)
            if packages:
                observation = f"Installed packages: {packages[0][1]}"
                memory_type = "decision"
        elif re.match(r'^(pip|uv pip)\s+install\s+', command):
            packages = re.findall(r'install\s+(.+)', command)
            if packages:
                observation = f"Installed Python packages: {packages[0]}"
                memory_type = "decision"
        elif re.match(r'^cargo\s+add\s+', command):
            packages = re.findall(r'add\s+(.+)', command)
            if packages:
                observation = f"Added Rust crates: {packages[0]}"
                memory_type = "decision"

        # Detect git operations
        if "git commit" in command:
            # Extract commit message
            match = re.search(r'-m\s+["\'](.+?)["\']', command)
            if match:
                observation = f"Committed: {match.group(1)[:80]}"
                memory_type = "context"
        elif "git checkout -b" in command or "git switch -c" in command:
            match = re.search(r'(-b|-c)\s+(\S+)', command)
            if match:
                observation = f"Created branch: {match.group(2)}"
                memory_type = "context"

    # === READ OPERATIONS: Track what's being explored ===
    elif tool == "Read":
        file_path = tool_input.get("file_path", "")
        filename = os.path.basename(file_path)

        # Only track significant reads (config files, main files)
        significant_files = ["package.json", "tsconfig.json", "pyproject.toml",
                           "Cargo.toml", "go.mod", "Makefile", "Dockerfile",
                           "README.md", "CLAUDE.md", ".env.example"]

        if filename in significant_files:
            observation = f"Reviewed {filename}"
            memory_type = "context"

    if observation:
        # Apply concept tagging
        concept = detect_concept_tag(observation)
        return {
            "observation": observation,
            "type": memory_type,
            "concept": concept
        }
    return None

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    tool_output = data.get("tool_response", {})
    cwd = data.get("cwd", os.getcwd())
    project = os.path.basename(cwd)

    # === SESSION TRACKING (runs for ALL tools) ===
    activity = load_session_activity()

    # Track significant actions
    if is_significant_action(tool, tool_input, tool_output):
        activity["significant_count"] = activity.get("significant_count", 0) + 1
        activity["has_unsaved_work"] = True

        # Track file touched
        file_path = tool_input.get("file_path", "")
        if file_path:
            filename = os.path.basename(file_path)
            if filename not in activity.get("files_touched", []):
                activity.setdefault("files_touched", []).append(filename)
                # Keep only last 10
                activity["files_touched"] = activity["files_touched"][-10:]

    # Track tool usage
    activity.setdefault("tools_used", {})
    activity["tools_used"][tool] = activity["tools_used"].get(tool, 0) + 1

    # Check if should remind to save
    reminder_output = None
    if should_remind_to_save(activity):
        summary = get_session_summary(activity)
        activity["last_reminder_at"] = activity["significant_count"]
        reminder_output = {
            "systemMessage": f"💾 Big session! {summary} - Consider saving important work with memory system."
        }

    save_session_activity(activity)

    # Skip observation extraction for non-actionable tools
    skip_tools = ["Glob", "Grep", "TodoWrite", "WebSearch", "WebFetch", "Task"]
    if tool in skip_tools:
        if reminder_output:
            print(json.dumps(reminder_output))
        sys.exit(0)

    # === PRIVACY CHECK ===
    input_str = json.dumps(tool_input) if tool_input else ""
    output_str = json.dumps(tool_output) if isinstance(tool_output, dict) else str(tool_output)

    if contains_private_tag(input_str) or contains_private_tag(output_str):
        if reminder_output:
            print(json.dumps(reminder_output))
        sys.exit(0)

    # Strip any partial private content
    tool_input_clean = json.loads(strip_private_content(input_str)) if input_str else {}
    if isinstance(tool_output, dict):
        tool_output_clean = json.loads(strip_private_content(output_str))
    else:
        tool_output_clean = strip_private_content(str(tool_output))

    # Extract observation
    result = extract_observation(tool, tool_input_clean, tool_output_clean, cwd)

    if result and result.get("observation"):
        observation = result["observation"]
        memory_type = result["type"]
        concept = result.get("concept", "context")

        # Save to memory
        if save_memory(project, memory_type, observation):
            # Log to file for debugging
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            try:
                with open(LOG_DIR / "observations.jsonl", "a") as f:
                    f.write(json.dumps({
                        "timestamp": datetime.now().isoformat(),
                        "project": project,
                        "tool": tool,
                        "type": memory_type,
                        "concept": concept,
                        "observation": observation
                    }) + "\n")
            except:
                pass

    # Output reminder if needed
    if reminder_output:
        print(json.dumps(reminder_output))

    sys.exit(0)

if __name__ == "__main__":
    main()
