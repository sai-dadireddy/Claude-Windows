#!/usr/bin/env python3
"""
Claude Agent Dashboard - Real-time monitoring of the agentic environment.

Run in a split terminal: python3 ~/.claude/scripts/dashboard.py
Press Ctrl+C to exit.
"""

import time
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Paths
HINTS_FILE = Path.home() / ".claude" / "hints" / "current.txt"
TOOLS_LOG = Path.home() / ".claude" / "logs" / "tools.jsonl"
HOOKS_LOG = Path.home() / ".claude" / "logs" / "hooks.log"
MEMORY_DB = Path.home() / ".claude" / "memory" / "semantic.db"
ERROR_COUNTER = Path.home() / ".claude" / "logs" / "error_counter.json"

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80


def hr(char="─"):
    return char * get_terminal_width()


def read_last_lines(filepath: Path, n: int = 5) -> list:
    """Read last N lines from a file (cross-platform)."""
    try:
        if not filepath.exists():
            return []
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
            return [ln.strip() for ln in all_lines[-n:]]
    except Exception:
        return []
def get_hints():
    """Get current hints/context."""
    try:
        if HINTS_FILE.exists():
            content = HINTS_FILE.read_text().strip()
            # Get last 3 lines
            lines = content.split('\n')[-3:]
            return '\n'.join(lines)
    except:
        pass
    return "(empty)"


def get_last_tool():
    """Get last tool execution."""
    lines = read_last_lines(TOOLS_LOG, 1)
    if lines and lines[0]:
        try:
            data = json.loads(lines[0])
            tool = data.get("tool", "?")
            err = data.get("err", "")
            if err:
                return f"{RED}{tool}: {err[:40]}{RESET}"
            cmd = data.get("cmd", "")
            file = data.get("file", "")
            detail = cmd or file or ""
            return f"{GREEN}{tool}{RESET} {DIM}{detail[:30]}{RESET}"
        except:
            pass
    return "(none)"


def get_error_count():
    """Get current error count from all sessions."""
    try:
        if ERROR_COUNTER.exists():
            data = json.loads(ERROR_COUNTER.read_text())
            total = sum(s.get("count", 0) for s in data.values())
            return total
    except:
        pass
    return 0


def get_beads_status():
    """Get beads task queue status."""
    try:
        result = subprocess.run(
            ['bd', 'ready', '--limit', '3'],
            capture_output=True, text=True, timeout=5,
            env={**os.environ, "PATH": f"{Path.home()}/.local/bin:{os.environ.get('PATH', '')}"}
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split('\n')[:3]
            return '\n'.join(f"  {CYAN}{line}{RESET}" for line in lines)
        return f"  {DIM}(no ready tasks){RESET}"
    except:
        return f"  {DIM}(beads unavailable){RESET}"


def get_memory_count():
    """Get memory count from semantic DB."""
    try:
        if MEMORY_DB.exists():
            import sqlite3
            conn = sqlite3.connect(str(MEMORY_DB))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            count = cursor.fetchone()[0]
            conn.close()
            return count
    except:
        pass
    return "?"


def get_recent_hooks():
    """Get recent hook activity."""
    lines = read_last_lines(HOOKS_LOG, 3)
    if lines:
        formatted = []
        for line in lines:
            if line:
                # Truncate long lines
                formatted.append(f"  {DIM}{line[:60]}{RESET}")
        return '\n'.join(formatted)
    return f"  {DIM}(no recent activity){RESET}"


def get_active_agents():
    """Check for active workmux/tmux agents."""
    try:
        result = subprocess.run(
            ['tmux', 'list-sessions', '-F', '#{session_name}'],
            capture_output=True, text=True, timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            sessions = result.stdout.strip().split('\n')
            agent_sessions = [s for s in sessions if s.startswith('wm-') or 'agent' in s.lower()]
            if agent_sessions:
                return f"{GREEN}{len(agent_sessions)} active{RESET}: " + ", ".join(agent_sessions[:3])
    except:
        pass
    return f"{DIM}none{RESET}"


def main():
    print(f"{BOLD}Starting Claude Agent Dashboard...{RESET}")
    print("Press Ctrl+C to exit.\n")
    time.sleep(1)

    iteration = 0
    while True:
        try:
            clear()
            now = datetime.now().strftime("%H:%M:%S")
            width = get_terminal_width()

            # Header
            print(f"{BOLD}{BLUE}╔{'═' * (width - 2)}╗{RESET}")
            title = f"  CLAUDE AGENT DASHBOARD  │  {now}  │  Refresh: {iteration}"
            print(f"{BOLD}{BLUE}║{RESET} {title}{' ' * (width - len(title) - 4)}{BOLD}{BLUE}║{RESET}")
            print(f"{BOLD}{BLUE}╚{'═' * (width - 2)}╝{RESET}")

            # Active Context (Hints)
            print(f"\n{BOLD}{MAGENTA}🧠 ACTIVE CONTEXT{RESET}")
            print(hr())
            hints = get_hints()
            for line in hints.split('\n')[:3]:
                print(f"  {line[:width-4]}")

            # Last Tool Action
            print(f"\n{BOLD}{GREEN}🛠️  LAST ACTION{RESET}")
            print(hr())
            print(f"  {get_last_tool()}")

            # Error Status
            error_count = get_error_count()
            error_color = RED if error_count >= 3 else YELLOW if error_count > 0 else GREEN
            print(f"\n{BOLD}{error_color}⚠️  ERROR STATUS{RESET}")
            print(hr())
            if error_count >= 3:
                print(f"  {RED}META-COGNITION TRIGGERED: {error_count} consecutive errors{RESET}")
            else:
                print(f"  {error_color}Consecutive errors: {error_count}/3{RESET}")

            # Task Queue (Beads)
            print(f"\n{BOLD}{CYAN}📋 TASK QUEUE{RESET}")
            print(hr())
            print(get_beads_status())

            # Memory Status
            memory_count = get_memory_count()
            print(f"\n{BOLD}{YELLOW}💾 MEMORY{RESET}")
            print(hr())
            print(f"  Semantic memories: {memory_count}")

            # Active Agents
            print(f"\n{BOLD}{BLUE}🤖 AGENTS{RESET}")
            print(hr())
            print(f"  {get_active_agents()}")

            # Recent Hook Activity
            print(f"\n{BOLD}{DIM}📡 RECENT HOOKS{RESET}")
            print(hr())
            print(get_recent_hooks())

            # Footer
            print(f"\n{DIM}{'─' * width}{RESET}")
            print(f"{DIM}Ctrl+C to exit │ Logs: ~/.claude/logs/ │ Doctor: claude-doctor{RESET}")

            iteration += 1
            time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n{YELLOW}Dashboard stopped.{RESET}")
            break
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            time.sleep(2)


if __name__ == "__main__":
    main()
