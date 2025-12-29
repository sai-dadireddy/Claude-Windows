#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""SubagentStop Hook - Notify when subagent completes"""

import json, sys
from pathlib import Path

def main():
    try:
        data = json.load(sys.stdin)
    except:
        sys.exit(0)

    task = data.get("task_description", "")
    agent_type = data.get("subagent_type", "agent")

    LOG = Path.home() / ".claude" / "logs"
    LOG.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG / "events.jsonl", "a") as f:
            f.write(json.dumps({"e": "subagent", "type": agent_type, "task": task[:30]}) + "\n")
    except:
        pass

    # Show completion to user
    task_short = task[:50] + "..." if len(task) > 50 else task
    output = {"systemMessage": f"🤖 {agent_type} completed: {task_short}"}
    print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()
